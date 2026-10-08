package com.dwpg.simulator.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.math.BigDecimal;

public class PaymentRequest {

    @NotNull(message = "Merchant ID is mandatory")
    private Long merchantId;

    @NotNull(message = "Payment amount is mandatory")
    @DecimalMin(value = "0.01", message = "Payment amount must be greater than zero")
    private BigDecimal amount;

    @Size(max = 100, message = "Order reference cannot exceed 100 characters")
    private String orderReference;

    private String currency = "USD";

    public PaymentRequest() {}

    public PaymentRequest(Long merchantId, BigDecimal amount, String orderReference, String currency) {
        this.merchantId = merchantId;
        this.amount = amount;
        this.orderReference = orderReference;
        this.currency = currency != null ? currency : "USD";
    }

    public Long getMerchantId() { return merchantId; }
    public void setMerchantId(Long merchantId) { this.merchantId = merchantId; }

    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }

    public String getOrderReference() { return orderReference; }
    public void setOrderReference(String orderReference) { this.orderReference = orderReference; }

    public String getCurrency() { return currency; }
    public void setCurrency(String currency) { this.currency = currency; }

    @Override
    public String toString() {
        return "PaymentRequest{" +
                "merchantId=" + merchantId +
                ", amount=" + amount +
                ", orderReference='" + orderReference + '\'' +
                ", currency='" + currency + '\'' +
                '}';
    }
}
