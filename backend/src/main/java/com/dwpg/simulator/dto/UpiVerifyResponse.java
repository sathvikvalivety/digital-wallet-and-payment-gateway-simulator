package com.dwpg.simulator.dto;

import java.math.BigDecimal;

public class UpiVerifyResponse {

    private boolean success;
    private String referenceId;
    private String utrNumber;
    private String status;
    private BigDecimal amount;
    private BigDecimal newWalletBalance;
    private String message;

    public UpiVerifyResponse() {}

    public UpiVerifyResponse(boolean success, String referenceId, String utrNumber,
                             String status, BigDecimal amount, BigDecimal newWalletBalance, String message) {
        this.success = success;
        this.referenceId = referenceId;
        this.utrNumber = utrNumber;
        this.status = status;
        this.amount = amount;
        this.newWalletBalance = newWalletBalance;
        this.message = message;
    }

    public boolean isSuccess() { return success; }
    public void setSuccess(boolean success) { this.success = success; }

    public String getReferenceId() { return referenceId; }
    public void setReferenceId(String referenceId) { this.referenceId = referenceId; }

    public String getUtrNumber() { return utrNumber; }
    public void setUtrNumber(String utrNumber) { this.utrNumber = utrNumber; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }

    public BigDecimal getNewWalletBalance() { return newWalletBalance; }
    public void setNewWalletBalance(BigDecimal newWalletBalance) { this.newWalletBalance = newWalletBalance; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
}
