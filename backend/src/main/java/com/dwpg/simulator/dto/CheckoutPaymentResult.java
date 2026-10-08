package com.dwpg.simulator.dto;

import java.math.BigDecimal;

public class CheckoutPaymentResult {

    private boolean success;
    private String sessionId;
    private String status;
    private String orderId;
    private BigDecimal amount;
    private String currency;
    private String redirectUrl;
    private String message;
    private String paymentReference;

    public CheckoutPaymentResult() {}

    public CheckoutPaymentResult(boolean success, String sessionId, String status,
                                 String orderId, BigDecimal amount, String currency,
                                 String redirectUrl, String message, String paymentReference) {
        this.success = success;
        this.sessionId = sessionId;
        this.status = status;
        this.orderId = orderId;
        this.amount = amount;
        this.currency = currency;
        this.redirectUrl = redirectUrl;
        this.message = message;
        this.paymentReference = paymentReference;
    }

    public boolean isSuccess() { return success; }
    public void setSuccess(boolean success) { this.success = success; }

    public String getSessionId() { return sessionId; }
    public void setSessionId(String sessionId) { this.sessionId = sessionId; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public String getOrderId() { return orderId; }
    public void setOrderId(String orderId) { this.orderId = orderId; }

    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }

    public String getCurrency() { return currency; }
    public void setCurrency(String currency) { this.currency = currency; }

    public String getRedirectUrl() { return redirectUrl; }
    public void setRedirectUrl(String redirectUrl) { this.redirectUrl = redirectUrl; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public String getPaymentReference() { return paymentReference; }
    public void setPaymentReference(String paymentReference) { this.paymentReference = paymentReference; }
}
