package com.dwpg.simulator.dto;

import jakarta.validation.constraints.Size;

public class RefundRequest {
    private Long paymentId;

    @Size(max = 255, message = "Reason cannot exceed 255 characters")
    private String reason;

    public RefundRequest() {}

    public RefundRequest(String reason) {
        this.reason = reason;
    }

    public RefundRequest(Long paymentId, String reason) {
        this.paymentId = paymentId;
        this.reason = reason;
    }

    public Long getPaymentId() { return paymentId; }
    public void setPaymentId(Long paymentId) { this.paymentId = paymentId; }

    public String getReason() { return reason; }
    public void setReason(String reason) { this.reason = reason; }

    @Override
    public String toString() {
        return "RefundRequest{paymentId=" + paymentId + ", reason='" + reason + "'}";
    }
}
