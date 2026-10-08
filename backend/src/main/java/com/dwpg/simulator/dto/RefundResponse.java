package com.dwpg.simulator.dto;

import java.math.BigDecimal;
import java.time.Instant;

public class RefundResponse {
    private Long refundId;
    private Long paymentId;
    private Long merchantId;
    private BigDecimal amount;
    private String reason;
    private String status;
    private Instant createdAt;

    public RefundResponse() {}

    public RefundResponse(Long refundId, Long paymentId, Long merchantId, BigDecimal amount, String reason, String status, Instant createdAt) {
        this.refundId = refundId;
        this.paymentId = paymentId;
        this.merchantId = merchantId;
        this.amount = amount;
        this.reason = reason;
        this.status = status;
        this.createdAt = createdAt;
    }

    public Long getRefundId() { return refundId; }
    public Long getPaymentId() { return paymentId; }
    public Long getMerchantId() { return merchantId; }
    public BigDecimal getAmount() { return amount; }
    public String getReason() { return reason; }
    public String getStatus() { return status; }
    public Instant getCreatedAt() { return createdAt; }
}
