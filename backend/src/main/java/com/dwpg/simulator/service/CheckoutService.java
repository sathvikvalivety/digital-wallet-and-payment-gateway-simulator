package com.dwpg.simulator.service;

import com.dwpg.simulator.dto.*;
import com.dwpg.simulator.entity.*;
import com.dwpg.simulator.exception.InvalidAmountException;
import com.dwpg.simulator.exception.ResourceNotFoundException;
import com.dwpg.simulator.exception.UnauthorizedAccessException;
import com.dwpg.simulator.repository.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.security.SecureRandom;
import java.time.Instant;
import java.util.UUID;

@Service
public class CheckoutService {

    private static final String STATUS_COMPLETED = "COMPLETED";
    private final SecureRandom secureRandom = new SecureRandom();

    private final CheckoutSessionRepository checkoutSessionRepository;
    private final MerchantRepository merchantRepository;
    private final WalletRepository walletRepository;
    private final TransactionRepository transactionRepository;
    private final IdempotencyService idempotencyService;
    private final AuditService auditService;

    public CheckoutService(CheckoutSessionRepository checkoutSessionRepository,
                           MerchantRepository merchantRepository,
                           WalletRepository walletRepository,
                           TransactionRepository transactionRepository,
                           IdempotencyService idempotencyService,
                           AuditService auditService) {
        this.checkoutSessionRepository = checkoutSessionRepository;
        this.merchantRepository = merchantRepository;
        this.walletRepository = walletRepository;
        this.transactionRepository = transactionRepository;
        this.idempotencyService = idempotencyService;
        this.auditService = auditService;
    }

    @Transactional
    public CheckoutSessionResponse createSession(CreateCheckoutSessionRequest request, String apiKey, String clientIp) {
        if (apiKey == null || apiKey.isBlank()) {
            throw new UnauthorizedAccessException("Merchant API key is required in 'X-Api-Key' header");
        }

        if (request.getAmount() == null || request.getAmount().compareTo(BigDecimal.ZERO) <= 0) {
            throw new InvalidAmountException("Order amount must be strictly positive");
        }

        // Authenticate merchant by API key
        String cleanKey = apiKey.trim();
        String keyHash = idempotencyService.computeSha256(cleanKey);
        Merchant merchant = merchantRepository.findByApiKeyHash(keyHash)
                .orElseGet(() -> merchantRepository.findAll().stream()
                        .filter(m -> cleanKey.equals(m.getApiKey()))
                        .findFirst()
                        .orElseThrow(() -> new UnauthorizedAccessException("Invalid or revoked Merchant API key")));

        if (!"ACTIVE".equalsIgnoreCase(merchant.getStatus())) {
            throw new UnauthorizedAccessException("Merchant account is currently " + merchant.getStatus());
        }

        String sessionId = "cs_dwpg_" + System.currentTimeMillis() + "_" + UUID.randomUUID().toString().substring(0, 8);
        CheckoutSession session = new CheckoutSession(
                sessionId,
                merchant,
                request.getAmount(),
                request.getCurrency(),
                request.getOrderId(),
                request.getProductName(),
                request.getCustomerName(),
                request.getCustomerEmail(),
                request.getReturnUrl(),
                request.getCancelUrl()
        );

        session = checkoutSessionRepository.save(session);

        auditService.logEvent(AuditEventType.PAYMENT_INITIATED, session.getId(),
                merchant.getUser().getUsername(), "SUCCESS",
                "Checkout session created: " + sessionId + " for Order #" + request.getOrderId() + " (₹" + request.getAmount() + ")", clientIp);

        return toResponse(session);
    }

    @Transactional(readOnly = true)
    public CheckoutSessionResponse getSession(String sessionId) {
        CheckoutSession session = checkoutSessionRepository.findBySessionId(sessionId)
                .orElseThrow(() -> new ResourceNotFoundException("Checkout session not found: " + sessionId));
        return toResponse(session);
    }

    @Transactional
    public CheckoutPaymentResult completeSession(String sessionId, CompleteCheckoutSessionRequest request, String clientIp) {
        CheckoutSession session = checkoutSessionRepository.findBySessionId(sessionId)
                .orElseThrow(() -> new ResourceNotFoundException("Checkout session not found: " + sessionId));

        if (STATUS_COMPLETED.equalsIgnoreCase(session.getStatus())) {
            String redirectUrl = buildRedirectUrl(session, session.getPaymentReference());
            return new CheckoutPaymentResult(
                    true,
                    session.getSessionId(),
                    STATUS_COMPLETED,
                    session.getOrderId(),
                    session.getAmount(),
                    session.getCurrency(),
                    redirectUrl,
                    "Payment was already completed successfully.",
                    session.getPaymentReference()
            );
        }

        // Generate payment reference based on method
        String method = (request.getPaymentMethod() != null && !request.getPaymentMethod().isBlank())
                ? request.getPaymentMethod().toUpperCase()
                : "UPI";

        String paymentRef;
        if ("UPI".equalsIgnoreCase(method)) {
            paymentRef = (request.getUtrNumber() != null && !request.getUtrNumber().isBlank())
                    ? request.getUtrNumber().trim()
                    : generateRealisticUtr();
        } else if ("CARD".equalsIgnoreCase(method)) {
            paymentRef = "CARD_AUTH_" + System.currentTimeMillis() + "_" + UUID.randomUUID().toString().substring(0, 6).toUpperCase();
        } else {
            paymentRef = "WALLET_REF_" + System.currentTimeMillis();
        }

        // Credit Merchant Wallet
        Merchant merchant = session.getMerchant();
        Wallet merchantWallet = walletRepository.findByIdForUpdate(merchant.getWallet().getId())
                .orElseThrow(() -> new ResourceNotFoundException("Merchant settlement wallet not found"));

        merchantWallet.credit(session.getAmount());
        walletRepository.save(merchantWallet);

        // Record Transaction Ledger Entry
        Transaction creditTx = new Transaction(
                merchantWallet,
                null,
                TransactionType.CREDIT,
                session.getAmount(),
                merchantWallet.getBalance(),
                "Checkout payment received for Order #" + session.getOrderId() + " (" + method + " Ref: " + paymentRef + ")"
        );
        transactionRepository.save(creditTx);

        // Update Session Status
        session.setStatus(STATUS_COMPLETED);
        session.setPaymentMethod(method);
        session.setPaymentReference(paymentRef);
        session.setCompletedAt(Instant.now());
        checkoutSessionRepository.save(session);

        auditService.logEvent(AuditEventType.PAYMENT_CONFIRMED, session.getId(),
                merchant.getUser().getUsername(), "SUCCESS",
                "Checkout session completed: " + sessionId + " | Order #" + session.getOrderId() + " | Settled ₹" + session.getAmount() + " to merchant", clientIp);

        String redirectUrl = buildRedirectUrl(session, paymentRef);

        return new CheckoutPaymentResult(
                true,
                session.getSessionId(),
                STATUS_COMPLETED,
                session.getOrderId(),
                session.getAmount(),
                session.getCurrency(),
                redirectUrl,
                "Payment confirmed successfully! Settled ₹" + session.getAmount() + " to " + merchant.getBusinessName() + ".",
                paymentRef
        );
    }

    private String buildRedirectUrl(CheckoutSession session, String paymentRef) {
        String base = session.getReturnUrl();
        String separator = base.contains("?") ? "&" : "?";
        return base + separator +
                "orderId=" + urlEncode(session.getOrderId()) +
                "&status=SUCCESS" +
                "&sessionId=" + urlEncode(session.getSessionId()) +
                "&amount=" + session.getAmount() +
                "&ref=" + urlEncode(paymentRef != null ? paymentRef : "CONFIRMED");
    }

    private String urlEncode(String value) {
        if (value == null) return "";
        return URLEncoder.encode(value, StandardCharsets.UTF_8);
    }

    private String generateRealisticUtr() {
        long prefix = 428000000000L;
        long randomPart = Math.abs(secureRandom.nextLong() % 10000000000L);
        return String.valueOf(prefix + randomPart);
    }

    private CheckoutSessionResponse toResponse(CheckoutSession session) {
        // Construct hosted checkout URL
        String checkoutUrl = "/checkout?session=" + session.getSessionId();

        return new CheckoutSessionResponse(
                session.getSessionId(),
                checkoutUrl,
                session.getMerchant().getId(),
                session.getMerchant().getBusinessName(),
                session.getAmount(),
                session.getCurrency(),
                session.getOrderId(),
                session.getProductName(),
                session.getCustomerName(),
                session.getCustomerEmail(),
                session.getReturnUrl(),
                session.getCancelUrl(),
                session.getStatus(),
                session.getPaymentMethod(),
                session.getPaymentReference(),
                session.getCreatedAt(),
                session.getCompletedAt()
        );
    }
}
