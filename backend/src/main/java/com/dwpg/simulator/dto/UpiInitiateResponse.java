package com.dwpg.simulator.dto;

import java.math.BigDecimal;
import java.time.Instant;

public class UpiInitiateResponse {

    private String referenceId;
    private String payeeVpa;
    private String payeeName;
    private BigDecimal amount;
    private String currency;
    private String upiUri;
    private String note;
    private String status;
    private Instant createdAt;

    public UpiInitiateResponse() {}

    public UpiInitiateResponse(String referenceId, String payeeVpa, String payeeName,
                               BigDecimal amount, String currency, String upiUri,
                               String note, String status, Instant createdAt) {
        this.referenceId = referenceId;
        this.payeeVpa = payeeVpa;
        this.payeeName = payeeName;
        this.amount = amount;
        this.currency = currency;
        this.upiUri = upiUri;
        this.note = note;
        this.status = status;
        this.createdAt = createdAt;
    }

    public String getReferenceId() { return referenceId; }
    public void setReferenceId(String referenceId) { this.referenceId = referenceId; }

    public String getPayeeVpa() { return payeeVpa; }
    public void setPayeeVpa(String payeeVpa) { this.payeeVpa = payeeVpa; }

    public String getPayeeName() { return payeeName; }
    public void setPayeeName(String payeeName) { this.payeeName = payeeName; }

    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }

    public String getCurrency() { return currency; }
    public void setCurrency(String currency) { this.currency = currency; }

    public String getUpiUri() { return upiUri; }
    public void setUpiUri(String upiUri) { this.upiUri = upiUri; }

    public String getNote() { return note; }
    public void setNote(String note) { this.note = note; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
}
