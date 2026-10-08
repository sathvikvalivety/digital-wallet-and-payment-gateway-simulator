package com.dwpg.simulator.dto;

import jakarta.validation.constraints.NotBlank;
import java.math.BigDecimal;

public class UpiWebhookRequest {

    @NotBlank(message = "Reference ID is required")
    private String referenceId;

    private String utrNumber;

    private BigDecimal amount;

    private String status = "SUCCESS";

    private String webhookSecret;

    public UpiWebhookRequest() {}

    public UpiWebhookRequest(String referenceId, String utrNumber, BigDecimal amount, String status) {
        this.referenceId = referenceId;
        this.utrNumber = utrNumber;
        this.amount = amount;
        this.status = status;
    }

    public String getReferenceId() { return referenceId; }
    public void setReferenceId(String referenceId) { this.referenceId = referenceId; }

    public String getUtrNumber() { return utrNumber; }
    public void setUtrNumber(String utrNumber) { this.utrNumber = utrNumber; }

    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public String getWebhookSecret() { return webhookSecret; }
    public void setWebhookSecret(String webhookSecret) { this.webhookSecret = webhookSecret; }
}
