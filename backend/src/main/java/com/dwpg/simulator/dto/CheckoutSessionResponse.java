package com.dwpg.simulator.dto;

import java.math.BigDecimal;
import java.time.Instant;

public class CheckoutSessionResponse {

    private String sessionId;
    private String checkoutUrl;
    private Long merchantId;
    private String merchantBusinessName;
    private BigDecimal amount;
    private String currency;
    private String orderId;
    private String productName;
    private String customerName;
    private String customerEmail;
    private String returnUrl;
    private String cancelUrl;
    private String status;
    private String paymentMethod;
    private String paymentReference;
    private Instant createdAt;
    private Instant completedAt;

    public CheckoutSessionResponse() {}

    public CheckoutSessionResponse(String sessionId, String checkoutUrl, Long merchantId,
                                   String merchantBusinessName, BigDecimal amount, String currency,
                                   String orderId, String productName, String customerName,
                                   String customerEmail, String returnUrl, String cancelUrl,
                                   String status, String paymentMethod, String paymentReference,
                                   Instant createdAt, Instant completedAt) {
        this.sessionId = sessionId;
        this.checkoutUrl = checkoutUrl;
        this.merchantId = merchantId;
        this.merchantBusinessName = merchantBusinessName;
        this.amount = amount;
        this.currency = currency;
        this.orderId = orderId;
        this.productName = productName;
        this.customerName = customerName;
        this.customerEmail = customerEmail;
        this.returnUrl = returnUrl;
        this.cancelUrl = cancelUrl;
        this.status = status;
        this.paymentMethod = paymentMethod;
        this.paymentReference = paymentReference;
        this.createdAt = createdAt;
        this.completedAt = completedAt;
    }

    public String getSessionId() { return sessionId; }
    public void setSessionId(String sessionId) { this.sessionId = sessionId; }

    public String getCheckoutUrl() { return checkoutUrl; }
    public void setCheckoutUrl(String checkoutUrl) { this.checkoutUrl = checkoutUrl; }

    public Long getMerchantId() { return merchantId; }
    public void setMerchantId(Long merchantId) { this.merchantId = merchantId; }

    public String getMerchantBusinessName() { return merchantBusinessName; }
    public void setMerchantBusinessName(String merchantBusinessName) { this.merchantBusinessName = merchantBusinessName; }

    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }

    public String getCurrency() { return currency; }
    public void setCurrency(String currency) { this.currency = currency; }

    public String getOrderId() { return orderId; }
    public void setOrderId(String orderId) { this.orderId = orderId; }

    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }

    public String getCustomerName() { return customerName; }
    public void setCustomerName(String customerName) { this.customerName = customerName; }

    public String getCustomerEmail() { return customerEmail; }
    public void setCustomerEmail(String customerEmail) { this.customerEmail = customerEmail; }

    public String getReturnUrl() { return returnUrl; }
    public void setReturnUrl(String returnUrl) { this.returnUrl = returnUrl; }

    public String getCancelUrl() { return cancelUrl; }
    public void setCancelUrl(String cancelUrl) { this.cancelUrl = cancelUrl; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public String getPaymentMethod() { return paymentMethod; }
    public void setPaymentMethod(String paymentMethod) { this.paymentMethod = paymentMethod; }

    public String getPaymentReference() { return paymentReference; }
    public void setPaymentReference(String paymentReference) { this.paymentReference = paymentReference; }

    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }

    public Instant getCompletedAt() { return completedAt; }
    public void setCompletedAt(Instant completedAt) { this.completedAt = completedAt; }
}
