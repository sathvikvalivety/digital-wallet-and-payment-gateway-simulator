package com.dwpg.simulator.service;

import com.dwpg.simulator.dto.*;
import com.dwpg.simulator.entity.*;
import com.dwpg.simulator.exception.IdempotencyException;
import com.dwpg.simulator.exception.InvalidAmountException;
import com.dwpg.simulator.exception.ResourceNotFoundException;
import com.dwpg.simulator.repository.UpiTransactionRepository;
import com.dwpg.simulator.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.List;
import java.util.UUID;

@Service
public class UpiService {

    public static final String DEFAULT_PAYEE_VPA = "valivetysathvik@ibl";
    public static final String DEFAULT_PAYEE_NAME = "sathvikvalivety";

    private final UpiTransactionRepository upiTransactionRepository;
    private final UserRepository userRepository;
    private final WalletService walletService;
    private final AuditService auditService;

    public UpiService(UpiTransactionRepository upiTransactionRepository,
                      UserRepository userRepository,
                      WalletService walletService,
                      AuditService auditService) {
        this.upiTransactionRepository = upiTransactionRepository;
        this.userRepository = userRepository;
        this.walletService = walletService;
        this.auditService = auditService;
    }

    @Transactional
    public UpiInitiateResponse initiatePayment(UpiInitiateRequest request, String username, String clientIp) {
        if (request.getAmount() == null || request.getAmount().compareTo(BigDecimal.ZERO) <= 0) {
            throw new InvalidAmountException("UPI transaction amount must be strictly positive");
        }

        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found: " + username));

        String refId = "DWPG-UPI-" + System.currentTimeMillis() + "-" + UUID.randomUUID().toString().substring(0, 6).toUpperCase();
        String note = (request.getNote() != null && !request.getNote().isBlank())
                ? request.getNote()
                : "DWPG Wallet UPI Top-up for " + username;
        String formattedAmount = request.getAmount().setScale(2, RoundingMode.HALF_UP).toPlainString();

        // Construct standard NPCI UPI URI
        String upiUri = String.format(
                "upi://pay?pa=%s&pn=%s&am=%s&cu=INR&tn=%s&tr=%s",
                URLEncoder.encode(DEFAULT_PAYEE_VPA, StandardCharsets.UTF_8),
                URLEncoder.encode(DEFAULT_PAYEE_NAME, StandardCharsets.UTF_8),
                formattedAmount,
                URLEncoder.encode(note, StandardCharsets.UTF_8),
                URLEncoder.encode(refId, StandardCharsets.UTF_8)
        );

        UpiTransaction tx = new UpiTransaction(
                refId,
                user,
                DEFAULT_PAYEE_VPA,
                DEFAULT_PAYEE_NAME,
                request.getAmount(),
                "INR",
                request.getPurpose() != null ? request.getPurpose() : "TOPUP",
                note,
                upiUri
        );
        upiTransactionRepository.save(tx);

        auditService.logEvent(AuditEventType.UPI_PAYMENT_INITIATED, tx.getId(), username, "SUCCESS",
                "UPI transaction initiated: Ref " + refId + " Amount ₹" + formattedAmount + " to " + DEFAULT_PAYEE_VPA, clientIp);

        return new UpiInitiateResponse(
                refId,
                DEFAULT_PAYEE_VPA,
                DEFAULT_PAYEE_NAME,
                request.getAmount(),
                "INR",
                upiUri,
                note,
                "PENDING",
                tx.getCreatedAt()
        );
    }

    @Transactional
    public UpiVerifyResponse verifyPayment(UpiVerifyRequest request, String username, String clientIp) {
        UpiTransaction tx = upiTransactionRepository.findByReferenceId(request.getReferenceId())
                .orElseThrow(() -> new ResourceNotFoundException("UPI transaction not found for reference: " + request.getReferenceId()));

        if (!tx.getUser().getUsername().equals(username)) {
            auditService.logEvent(AuditEventType.AUTHORIZATION_FAILURE, tx.getId(), username, "FAILED",
                    "Unauthorized attempt to verify foreign UPI reference: " + request.getReferenceId(), clientIp);
            throw new IllegalArgumentException("You do not own this UPI payment reference");
        }

        if ("CONFIRMED".equals(tx.getStatus())) {
            WalletResponse wallet = walletService.getMyWallet(username);
            return new UpiVerifyResponse(true, tx.getReferenceId(), tx.getUtrNumber(), "CONFIRMED",
                    tx.getAmount(), wallet.getBalance(), "UPI payment was already verified successfully.");
        }

        // Anti-Replay: Check if UTR number was already used
        String cleanUtr = request.getUtrNumber().trim();
        if (upiTransactionRepository.existsByUtrNumber(cleanUtr)) {
            auditService.logEvent(AuditEventType.REPLAY_DETECTED, tx.getId(), username, "FAILED",
                    "Replay attack detected: UTR " + cleanUtr + " has already been registered.", clientIp);
            throw new IdempotencyException("UTR / Reference " + cleanUtr + " has already been claimed for another transaction. Duplicate UTR detected.");
        }

        tx.setUtrNumber(cleanUtr);
        tx.setStatus("CONFIRMED");
        tx.setCompletedAt(Instant.now());
        upiTransactionRepository.save(tx);

        // Credit wallet if TOPUP
        BigDecimal newBalance = BigDecimal.ZERO;
        if ("TOPUP".equalsIgnoreCase(tx.getPurpose())) {
            walletService.createWallet(username);
            WalletResponse walletResp = walletService.fundMyWallet(new FundRequest(tx.getAmount()), username, clientIp);
            newBalance = walletResp.getBalance();
        }

        auditService.logEvent(AuditEventType.UPI_PAYMENT_CONFIRMED, tx.getId(), username, "SUCCESS",
                "UPI payment verified and settled. UTR: " + cleanUtr + " Amount: ₹" + tx.getAmount(), clientIp);

        return new UpiVerifyResponse(
                true,
                tx.getReferenceId(),
                cleanUtr,
                "CONFIRMED",
                tx.getAmount(),
                newBalance,
                "UPI payment verified successfully! Credited ₹" + tx.getAmount() + " to wallet."
        );
    }

    @Transactional(readOnly = true)
    public UpiStatusResponse getStatus(String referenceId) {
        UpiTransaction tx = upiTransactionRepository.findByReferenceId(referenceId)
                .orElseThrow(() -> new ResourceNotFoundException("UPI transaction not found for reference: " + referenceId));

        BigDecimal currentBalance = null;
        if ("CONFIRMED".equals(tx.getStatus())) {
            try {
                WalletResponse wallet = walletService.getMyWallet(tx.getUser().getUsername());
                currentBalance = wallet.getBalance();
            } catch (Exception ignored) {}
        }

        return new UpiStatusResponse(
                tx.getReferenceId(),
                tx.getStatus(),
                tx.getAmount(),
                tx.getUtrNumber(),
                currentBalance,
                "CONFIRMED".equals(tx.getStatus()) ? "Payment has been confirmed." : "Waiting for payment confirmation.",
                tx.getCreatedAt(),
                tx.getCompletedAt()
        );
    }

    @Transactional
    public UpiStatusResponse processWebhook(UpiWebhookRequest request, String clientIp) {
        if (request.getReferenceId() == null || request.getReferenceId().isBlank()) {
            throw new IllegalArgumentException("Reference ID is required in webhook payload");
        }

        UpiTransaction tx = upiTransactionRepository.findByReferenceId(request.getReferenceId().trim())
                .orElseThrow(() -> new ResourceNotFoundException("UPI transaction not found for reference: " + request.getReferenceId()));

        if ("CONFIRMED".equals(tx.getStatus())) {
            BigDecimal bal = BigDecimal.ZERO;
            try {
                bal = walletService.getMyWallet(tx.getUser().getUsername()).getBalance();
            } catch (Exception ignored) {}
            return new UpiStatusResponse(
                    tx.getReferenceId(),
                    tx.getStatus(),
                    tx.getAmount(),
                    tx.getUtrNumber(),
                    bal,
                    "UPI payment was already confirmed previously.",
                    tx.getCreatedAt(),
                    tx.getCompletedAt()
            );
        }

        // Validate amount if sent by webhook
        if (request.getAmount() != null && request.getAmount().compareTo(BigDecimal.ZERO) > 0) {
            if (tx.getAmount().compareTo(request.getAmount()) != 0) {
                auditService.logEvent(AuditEventType.SUSPICIOUS_ACTIVITY, tx.getId(), tx.getUser().getUsername(), "FAILED",
                        "Webhook amount mismatch. Expected: " + tx.getAmount() + ", Received: " + request.getAmount(), clientIp);
                throw new IllegalArgumentException("Webhook payment amount mismatch");
            }
        }

        // If webhook status is FAILED
        if (request.getStatus() != null && ("FAILED".equalsIgnoreCase(request.getStatus()) || "FAILURE".equalsIgnoreCase(request.getStatus()))) {
            tx.setStatus("FAILED");
            tx.setCompletedAt(Instant.now());
            upiTransactionRepository.save(tx);
            auditService.logEvent(AuditEventType.UPI_PAYMENT_FAILED, tx.getId(), tx.getUser().getUsername(), "FAILED",
                    "UPI payment marked FAILED via webhook callback", clientIp);
            return new UpiStatusResponse(tx.getReferenceId(), "FAILED", tx.getAmount(), null, null, "Payment failed via gateway callback", tx.getCreatedAt(), tx.getCompletedAt());
        }

        // Determine UTR
        String utr = (request.getUtrNumber() != null && !request.getUtrNumber().isBlank())
                ? request.getUtrNumber().trim()
                : generateRealisticUtr();

        // Check duplicate UTR
        if (upiTransactionRepository.existsByUtrNumber(utr)) {
            auditService.logEvent(AuditEventType.REPLAY_DETECTED, tx.getId(), tx.getUser().getUsername(), "FAILED",
                    "Webhook duplicate UTR detected: " + utr, clientIp);
            throw new IdempotencyException("Duplicate UTR detected in webhook: " + utr);
        }

        tx.setUtrNumber(utr);
        tx.setStatus("CONFIRMED");
        tx.setCompletedAt(Instant.now());
        upiTransactionRepository.save(tx);

        BigDecimal newBalance = BigDecimal.ZERO;
        if ("TOPUP".equalsIgnoreCase(tx.getPurpose())) {
            walletService.createWallet(tx.getUser().getUsername());
            WalletResponse walletResp = walletService.fundMyWallet(new FundRequest(tx.getAmount()), tx.getUser().getUsername(), clientIp);
            newBalance = walletResp.getBalance();
        }

        auditService.logEvent(AuditEventType.UPI_PAYMENT_CONFIRMED, tx.getId(), tx.getUser().getUsername(), "SUCCESS",
                "UPI payment auto-verified via Webhook callback. UTR: " + utr + " Amount: ₹" + tx.getAmount(), clientIp);

        return new UpiStatusResponse(
                tx.getReferenceId(),
                "CONFIRMED",
                tx.getAmount(),
                utr,
                newBalance,
                "UPI payment auto-verified successfully via bank webhook! Credited ₹" + tx.getAmount() + " to wallet.",
                tx.getCreatedAt(),
                tx.getCompletedAt()
        );
    }

    @Transactional
    public UpiStatusResponse simulateBankCallback(String referenceId, String clientIp) {
        String mockUtr = generateRealisticUtr();
        UpiWebhookRequest req = new UpiWebhookRequest(referenceId, mockUtr, null, "SUCCESS");
        return processWebhook(req, clientIp);
    }

    private String generateRealisticUtr() {
        long prefix = 428000000000L;
        long randomPart = (long) (Math.random() * 9999999999L);
        return String.valueOf(prefix + randomPart);
    }

    @Transactional(readOnly = true)
    public List<UpiTransaction> getMyTransactions(String username) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found: " + username));
        return upiTransactionRepository.findByUserIdOrderByCreatedAtDesc(user.getId());
    }
}
