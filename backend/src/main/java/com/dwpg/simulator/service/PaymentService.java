package com.dwpg.simulator.service;

import com.dwpg.simulator.dto.PaymentRequest;
import com.dwpg.simulator.dto.PaymentResponse;
import com.dwpg.simulator.entity.*;
import com.dwpg.simulator.exception.InsufficientFundsException;
import com.dwpg.simulator.exception.InvalidAmountException;
import com.dwpg.simulator.exception.ResourceNotFoundException;
import com.dwpg.simulator.repository.*;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.support.TransactionTemplate;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class PaymentService {

    private final PaymentRepository paymentRepository;
    private final WalletRepository walletRepository;
    private final MerchantRepository merchantRepository;
    private final UserRepository userRepository;
    private final TransactionRepository transactionRepository;
    private final IdempotencyService idempotencyService;
    private final AuditService auditService;
    private final ObjectMapper objectMapper;
    private final TransactionTemplate transactionTemplate;
    private final ConcurrentHashMap<String, Object> userLocks = new ConcurrentHashMap<>();

    public PaymentService(PaymentRepository paymentRepository,
                          WalletRepository walletRepository,
                          MerchantRepository merchantRepository,
                          UserRepository userRepository,
                          TransactionRepository transactionRepository,
                          IdempotencyService idempotencyService,
                          AuditService auditService,
                          ObjectMapper objectMapper,
                          TransactionTemplate transactionTemplate) {
        this.paymentRepository = paymentRepository;
        this.walletRepository = walletRepository;
        this.merchantRepository = merchantRepository;
        this.userRepository = userRepository;
        this.transactionRepository = transactionRepository;
        this.idempotencyService = idempotencyService;
        this.auditService = auditService;
        this.objectMapper = objectMapper;
        this.transactionTemplate = transactionTemplate;
    }

    public PaymentResponse processPayment(String idempotencyKey, PaymentRequest request, String username, String clientIp) {
        // 1. Compute Request Digest for Idempotency Binding
        String requestHash = idempotencyService.computeSha256(request.toString());

        // 2. Check Idempotency Record (Replay Attack Protection)
        Optional<IdempotencyRecord> cachedRecord = idempotencyService.checkIdempotency(idempotencyKey, requestHash, username, clientIp);
        if (cachedRecord.isPresent()) {
            try {
                return objectMapper.readValue(cachedRecord.get().getResponseBody(), PaymentResponse.class);
            } catch (JsonProcessingException e) {
                throw new IllegalStateException("Failed to deserialize cached idempotency response", e);
            }
        }

        // 3. Amount Validation
        if (request.getAmount() == null || request.getAmount().compareTo(BigDecimal.ZERO) <= 0) {
            throw new InvalidAmountException("Payment amount must be strictly positive");
        }

        // 4. Thread-Safe Striped Concurrency Lock per User + ACID Transaction Boundary
        Object lock = userLocks.computeIfAbsent(username, k -> new Object());
        synchronized (lock) {
            return transactionTemplate.execute(status -> {
                // Fetch User and Sender Wallet
                User senderUser = userRepository.findByUsername(username)
                        .orElseThrow(() -> new ResourceNotFoundException("User not found: " + username));
                Wallet senderWalletRef = walletRepository.findByUserId(senderUser.getId())
                        .orElseThrow(() -> new ResourceNotFoundException("Sender wallet not found"));

                // Acquire Exclusive Row Lock on Sender Wallet (Pessimistic Concurrency Control)
                Wallet senderWallet = walletRepository.findByIdForUpdate(senderWalletRef.getId())
                        .orElseThrow(() -> new ResourceNotFoundException("Sender wallet unavailable for lock"));

                // Verify Balance Sufficiency
                if (senderWallet.getBalance().compareTo(request.getAmount()) < 0) {
                    auditService.logEvent(AuditEventType.PAYMENT_FAILED, null, username, "FAILED",
                            "Payment declined due to insufficient funds. Requested: ₹" + request.getAmount() +
                                    ", Available: ₹" + senderWallet.getBalance(), clientIp);
                    throw new InsufficientFundsException("Insufficient funds. Available balance: ₹" + senderWallet.getBalance());
                }

                // Fetch Target Merchant & Acquire Lock on Merchant Settlement Wallet
                Merchant merchant = merchantRepository.findById(request.getMerchantId())
                        .orElseThrow(() -> new ResourceNotFoundException("Merchant not found with id: " + request.getMerchantId()));
                Wallet merchantWallet = walletRepository.findByIdForUpdate(merchant.getWallet().getId())
                        .orElseThrow(() -> new ResourceNotFoundException("Merchant settlement wallet unavailable"));

                // Atomic Debit & Credit Mutations
                senderWallet.debit(request.getAmount());
                merchantWallet.credit(request.getAmount());
                walletRepository.save(senderWallet);
                walletRepository.save(merchantWallet);

                // Create and Persist Payment Entity
                Payment payment = new Payment(
                        senderWallet,
                        merchantWallet,
                        request.getAmount(),
                        request.getCurrency(),
                        request.getOrderReference(),
                        idempotencyKey
                );
                payment.setStatus(PaymentStatus.CONFIRMED);
                payment = paymentRepository.save(payment);

                // Record Double-Entry Transaction Ledgers
                Transaction debitTx = new Transaction(
                        senderWallet,
                        payment,
                        TransactionType.DEBIT,
                        request.getAmount(),
                        senderWallet.getBalance(),
                        "Payment to merchant: " + merchant.getBusinessName() + " (" + request.getOrderReference() + ")"
                );
                Transaction creditTx = new Transaction(
                        merchantWallet,
                        payment,
                        TransactionType.CREDIT,
                        request.getAmount(),
                        merchantWallet.getBalance(),
                        "Payment received from user: " + username + " (" + request.getOrderReference() + ")"
                );
                transactionRepository.save(debitTx);
                transactionRepository.save(creditTx);

                // Build Response & Save in Idempotency Cache
                PaymentResponse response = new PaymentResponse(
                        payment.getId(),
                        senderWallet.getId(),
                        merchantWallet.getId(),
                        payment.getAmount(),
                        payment.getCurrency(),
                        payment.getStatus(),
                        payment.getOrderReference(),
                        payment.getIdempotencyKey(),
                        payment.getCreatedAt()
                );

                try {
                    String serializedResponse = objectMapper.writeValueAsString(response);
                    idempotencyService.saveIdempotencyRecord(idempotencyKey, requestHash, payment.getId(), serializedResponse, 201);
                } catch (JsonProcessingException e) {
                    throw new IllegalStateException("Failed to serialize payment response for idempotency cache", e);
                }

                // Immutable Security Audit Logging
                auditService.logEvent(AuditEventType.PAYMENT_CONFIRMED, payment.getId(), username, "SUCCESS",
                        "Payment of ₹" + request.getAmount() + " confirmed for merchant " + merchant.getBusinessName(), clientIp);

                return response;
            });
        }
    }

    @Transactional(readOnly = true)
    public PaymentResponse getPaymentById(Long paymentId) {
        Payment payment = paymentRepository.findById(paymentId)
                .orElseThrow(() -> new ResourceNotFoundException("Payment not found with id: " + paymentId));
        return new PaymentResponse(
                payment.getId(),
                payment.getSenderWallet().getId(),
                payment.getMerchantWallet().getId(),
                payment.getAmount(),
                payment.getCurrency(),
                payment.getStatus(),
                payment.getOrderReference(),
                payment.getIdempotencyKey(),
                payment.getCreatedAt()
        );
    }

    @Transactional(readOnly = true)
    public List<PaymentResponse> getPaymentsForWallet(Long walletId) {
        return paymentRepository.findBySenderWalletIdOrderByCreatedAtDesc(walletId)
                .stream()
                .map(p -> new PaymentResponse(
                        p.getId(),
                        p.getSenderWallet().getId(),
                        p.getMerchantWallet().getId(),
                        p.getAmount(),
                        p.getCurrency(),
                        p.getStatus(),
                        p.getOrderReference(),
                        p.getIdempotencyKey(),
                        p.getCreatedAt()
                ))
                .toList();
    }
}
