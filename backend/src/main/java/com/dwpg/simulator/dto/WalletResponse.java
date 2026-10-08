package com.dwpg.simulator.dto;

import java.math.BigDecimal;
import java.time.Instant;

public class WalletResponse {
    private Long walletId;
    private Long userId;
    private String username;
    private BigDecimal balance;
    private String currency;
    private Instant updatedAt;

    public WalletResponse() {}

    public WalletResponse(Long walletId, Long userId, String username, BigDecimal balance, String currency, Instant updatedAt) {
        this.walletId = walletId;
        this.userId = userId;
        this.username = username;
        this.balance = balance;
        this.currency = currency;
        this.updatedAt = updatedAt;
    }

    public Long getWalletId() { return walletId; }
    public Long getUserId() { return userId; }
    public String getUsername() { return username; }
    public BigDecimal getBalance() { return balance; }
    public String getCurrency() { return currency; }
    public Instant getUpdatedAt() { return updatedAt; }
}
