package com.dwpg.simulator.dto;

import com.dwpg.simulator.entity.PaymentStatus;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.time.Instant;
import java.util.HexFormat;

public class PaymentResponse {
    private Long paymentId;
    private Long senderWalletId;
    private Long merchantWalletId;
    private BigDecimal amount;
    private String currency;
    private PaymentStatus status;
    private String orderReference;
    private String idempotencyKey;
    private Instant timestamp;

    public PaymentResponse() {}

    public PaymentResponse(Long paymentId, Long senderWalletId, Long merchantWalletId, BigDecimal amount, String currency, PaymentStatus status, String orderReference, String idempotencyKey, Instant timestamp) {
        this.paymentId = paymentId;
        this.senderWalletId = senderWalletId;
        this.merchantWalletId = merchantWalletId;
        this.amount = amount;
        this.currency = currency;
        this.status = status;
        this.orderReference = orderReference;
        this.idempotencyKey = idempotencyKey;
        this.timestamp = timestamp;
    }

    public Long getPaymentId() { return paymentId; }
    public Long getId() { return paymentId; }
    public Long getSenderWalletId() { return senderWalletId; }
    public Long getMerchantWalletId() { return merchantWalletId; }
    public Long getMerchantId() { return merchantWalletId; }
    public BigDecimal getAmount() { return amount; }
    public String getCurrency() { return currency; }
    public PaymentStatus getStatus() { return status; }
    public String getOrderReference() { return orderReference; }
    public String getIdempotencyKey() { return idempotencyKey; }
    public Instant getTimestamp() { return timestamp; }
    public String getCorrelationId() {
        return "CORR-" + (idempotencyKey != null ? idempotencyKey.substring(0, Math.min(8, idempotencyKey.length())) : "TX");
    }
    public String getTamperHash() {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            String raw = paymentId + ":" + amount + ":" + status + ":" + (idempotencyKey != null ? idempotencyKey : "");
            return HexFormat.of().formatHex(digest.digest(raw.getBytes(StandardCharsets.UTF_8)));
        } catch (Exception e) {
            return "HASH_COMPUTATION_ERROR";
        }
    }
}
