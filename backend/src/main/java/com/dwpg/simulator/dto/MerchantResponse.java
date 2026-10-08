package com.dwpg.simulator.dto;

import java.time.Instant;

public class MerchantResponse {
    private Long merchantId;
    private Long userId;
    private String businessName;
    private Long walletId;
    private String status;
    private String apiKey; // Generated only on registration
    private Instant createdAt;

    public MerchantResponse() {}

    public MerchantResponse(Long merchantId, Long userId, String businessName, Long walletId, String status, String apiKey, Instant createdAt) {
        this.merchantId = merchantId;
        this.userId = userId;
        this.businessName = businessName;
        this.walletId = walletId;
        this.status = status;
        this.apiKey = apiKey;
        this.createdAt = createdAt;
    }

    public Long getMerchantId() { return merchantId; }
    public Long getUserId() { return userId; }
    public String getBusinessName() { return businessName; }
    public Long getWalletId() { return walletId; }
    public String getStatus() { return status; }
    public String getApiKey() { return apiKey; }
    public Instant getCreatedAt() { return createdAt; }
}
