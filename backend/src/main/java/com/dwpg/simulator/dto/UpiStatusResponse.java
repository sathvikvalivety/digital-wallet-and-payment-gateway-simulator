package com.dwpg.simulator.dto;

import java.math.BigDecimal;
import java.time.Instant;

public class UpiStatusResponse {

    private String referenceId;
    private String status;
    private BigDecimal amount;
    private String utrNumber;
    private BigDecimal newWalletBalance;
    private String message;
    private Instant createdAt;
    private Instant completedAt;

    public UpiStatusResponse() {}

    public UpiStatusResponse(String referenceId, String status, BigDecimal amount,
                             String utrNumber, Instant createdAt, Instant completedAt) {
        this(referenceId, status, amount, utrNumber, null, null, createdAt, completedAt);
    }

    public UpiStatusResponse(String referenceId, String status, BigDecimal amount,
                             String utrNumber, BigDecimal newWalletBalance, String message,
                             Instant createdAt, Instant completedAt) {
        this.referenceId = referenceId;
        this.status = status;
        this.amount = amount;
        this.utrNumber = utrNumber;
        this.newWalletBalance = newWalletBalance;
        this.message = message;
        this.createdAt = createdAt;
        this.completedAt = completedAt;
    }

    public String getReferenceId() { return referenceId; }
    public void setReferenceId(String referenceId) { this.referenceId = referenceId; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }

    public String getUtrNumber() { return utrNumber; }
    public void setUtrNumber(String utrNumber) { this.utrNumber = utrNumber; }

    public BigDecimal getNewWalletBalance() { return newWalletBalance; }
    public void setNewWalletBalance(BigDecimal newWalletBalance) { this.newWalletBalance = newWalletBalance; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }

    public Instant getCompletedAt() { return completedAt; }
    public void setCompletedAt(Instant completedAt) { this.completedAt = completedAt; }
}
