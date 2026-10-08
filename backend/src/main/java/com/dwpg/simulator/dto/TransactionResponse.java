package com.dwpg.simulator.dto;

import com.dwpg.simulator.entity.TransactionType;
import java.math.BigDecimal;
import java.time.Instant;

public class TransactionResponse {
    private Long id;
    private Long walletId;
    private Long paymentId;
    private TransactionType type;
    private BigDecimal amount;
    private BigDecimal balanceAfter;
    private String description;
    private Instant createdAt;

    public TransactionResponse() {}

    public TransactionResponse(Long id, Long walletId, Long paymentId, TransactionType type, BigDecimal amount, BigDecimal balanceAfter, String description, Instant createdAt) {
        this.id = id;
        this.walletId = walletId;
        this.paymentId = paymentId;
        this.type = type;
        this.amount = amount;
        this.balanceAfter = balanceAfter;
        this.description = description;
        this.createdAt = createdAt;
    }

    public Long getId() { return id; }
    public Long getWalletId() { return walletId; }
    public Long getPaymentId() { return paymentId; }
    public TransactionType getType() { return type; }
    public BigDecimal getAmount() { return amount; }
    public BigDecimal getBalanceAfter() { return balanceAfter; }
    public String getDescription() { return description; }
    public Instant getCreatedAt() { return createdAt; }
}
