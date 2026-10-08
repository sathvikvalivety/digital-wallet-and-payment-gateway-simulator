package com.dwpg.simulator.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;

public class CreateCheckoutSessionRequest {

    @NotNull(message = "Amount is required")
    @DecimalMin(value = "0.01", message = "Amount must be strictly positive")
    private BigDecimal amount;

    private String currency = "INR";

    @NotBlank(message = "Order ID is required")
    private String orderId;

    private String productName;
    private String customerName;
    private String customerEmail;

    @NotBlank(message = "Return URL is required")
    private String returnUrl;

    private String cancelUrl;

    public CreateCheckoutSessionRequest() {}

    public CreateCheckoutSessionRequest(BigDecimal amount, String currency, String orderId,
                                        String productName, String customerName, String customerEmail,
                                        String returnUrl, String cancelUrl) {
        this.amount = amount;
        this.currency = currency;
        this.orderId = orderId;
        this.productName = productName;
        this.customerName = customerName;
        this.customerEmail = customerEmail;
        this.returnUrl = returnUrl;
        this.cancelUrl = cancelUrl;
    }

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
}
