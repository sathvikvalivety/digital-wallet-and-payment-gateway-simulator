package com.dwpg.simulator.service;

import com.dwpg.simulator.dto.RefundRequest;
import com.dwpg.simulator.dto.RefundResponse;
import com.dwpg.simulator.entity.*;
import com.dwpg.simulator.exception.InsufficientFundsException;
import com.dwpg.simulator.exception.InvalidStateTransitionException;
import com.dwpg.simulator.exception.ResourceNotFoundException;
import com.dwpg.simulator.exception.UnauthorizedAccessException;
import com.dwpg.simulator.repository.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Transactional;

@Service
public class RefundService {

    private final RefundRepository refundRepository;
    private final PaymentRepository paymentRepository;
    private final WalletRepository walletRepository;
    private final MerchantRepository merchantRepository;
    private final UserRepository userRepository;
    private final TransactionRepository transactionRepository;
    private final AuditService auditService;

    public RefundService(RefundRepository refundRepository,
                         PaymentRepository paymentRepository,
                         WalletRepository walletRepository,
                         MerchantRepository merchantRepository,
                         UserRepository userRepository,
                         TransactionRepository transactionRepository,
                         AuditService auditService) {
        this.refundRepository = refundRepository;
        this.paymentRepository = paymentRepository;
        this.walletRepository = walletRepository;
        this.merchantRepository = merchantRepository;
        this.userRepository = userRepository;
        this.transactionRepository = transactionRepository;
        this.auditService = auditService;
    }

    @Transactional(isolation = Isolation.READ_COMMITTED, rollbackFor = Exception.class)
    public RefundResponse processRefund(Long paymentId, RefundRequest request, String username, String clientIp) {
        // 1. Acquire Lock on Payment Entity
        Payment payment = paymentRepository.findByIdForUpdate(paymentId)
                .orElseThrow(() -> new ResourceNotFoundException("Payment not found with id: " + paymentId));

        // 2. Strict State Machine Validation (Thwarts Duplicate Refunds)
        if (payment.getStatus() == PaymentStatus.REFUNDED || refundRepository.existsByPaymentId(paymentId)) {
            auditService.logEvent(AuditEventType.SUSPICIOUS_ACTIVITY, paymentId, username, "FAILED",
                    "Duplicate refund attempted on payment ID: " + paymentId, clientIp);
            throw new InvalidStateTransitionException("Payment ID " + paymentId + " has already been refunded. Duplicate refund rejected.");
        }

        if (payment.getStatus() != PaymentStatus.CONFIRMED) {
            throw new InvalidStateTransitionException("Only CONFIRMED payments can be refunded. Current status: " + payment.getStatus());
        }

        // 3. Authorization Check (Sender customer, Merchant recipient, or Admin)
        User currentUser = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found: " + username));

        boolean isSender = payment.getSenderWallet().getUser().getUsername().equals(username);
        boolean isMerchantOwner = merchantRepository.findByUserId(currentUser.getId())
                .map(m -> m.getWallet().getId().equals(payment.getMerchantWallet().getId()))
                .orElse(false);
        boolean isAdmin = currentUser.getRole() == Role.ROLE_ADMIN;

        if (!isSender && !isMerchantOwner && !isAdmin) {
            auditService.logEvent(AuditEventType.AUTHORIZATION_FAILURE, paymentId, username, "FAILED",
                    "Unauthorized principal attempted to refund foreign payment ID: " + paymentId, clientIp);
            throw new UnauthorizedAccessException("Access denied. You can only refund payments associated with your account.");
        }

        Merchant merchant = merchantRepository.findByWalletId(payment.getMerchantWallet().getId())
                .orElseThrow(() -> new ResourceNotFoundException("Associated merchant profile not found for settlement wallet"));

        // 4. Acquire Locks on Wallets for Atomic Balance Reversal
        Wallet merchantWallet = walletRepository.findByIdForUpdate(payment.getMerchantWallet().getId())
                .orElseThrow(() -> new ResourceNotFoundException("Merchant settlement wallet unavailable"));
        Wallet senderWallet = walletRepository.findByIdForUpdate(payment.getSenderWallet().getId())
                .orElseThrow(() -> new ResourceNotFoundException("Customer wallet unavailable"));

        if (merchantWallet.getBalance().compareTo(payment.getAmount()) < 0) {
            throw new InsufficientFundsException("Merchant wallet does not possess sufficient funds to cover the refund of ₹" + payment.getAmount());
        }

        // 5. Reversal Mutations
        merchantWallet.debit(payment.getAmount());
        senderWallet.credit(payment.getAmount());
        walletRepository.save(merchantWallet);
        walletRepository.save(senderWallet);

        // 6. Transition Payment Status to REFUNDED
        payment.setStatus(PaymentStatus.REFUNDED);
        paymentRepository.save(payment);

        // 7. Persist Refund Record
        String reasonStr = (request != null && request.getReason() != null) ? request.getReason() : "Customer simulated refund";
        Refund refund = new Refund(payment, merchant, payment.getAmount(), reasonStr);
        refund = refundRepository.save(refund);

        // 8. Record Ledger Reversals
        Transaction customerTx = new Transaction(
                senderWallet,
                payment,
                TransactionType.REFUND,
                payment.getAmount(),
                senderWallet.getBalance(),
                "Refund received for payment #" + payment.getId() + " from " + merchant.getBusinessName()
        );
        Transaction merchantTx = new Transaction(
                merchantWallet,
                payment,
                TransactionType.REFUND,
                payment.getAmount().negate(),
                merchantWallet.getBalance(),
                "Refund debited for payment #" + payment.getId() + " to " + senderWallet.getUser().getUsername()
        );
        transactionRepository.save(customerTx);
        transactionRepository.save(merchantTx);

        auditService.logEvent(AuditEventType.PAYMENT_REFUNDED, refund.getId(), username, "SUCCESS",
                "Refund executed: ₹" + payment.getAmount() + " reversed for payment #" + payment.getId(), clientIp);

        return new RefundResponse(
                refund.getId(),
                payment.getId(),
                merchant.getId(),
                refund.getAmount(),
                refund.getReason(),
                refund.getStatus(),
                refund.getCreatedAt()
        );
    }
}
