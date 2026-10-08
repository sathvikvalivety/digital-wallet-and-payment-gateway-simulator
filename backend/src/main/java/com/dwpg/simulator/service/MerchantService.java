package com.dwpg.simulator.service;

import com.dwpg.simulator.dto.MerchantRequest;
import com.dwpg.simulator.dto.MerchantResponse;
import com.dwpg.simulator.entity.Merchant;
import com.dwpg.simulator.entity.Role;
import com.dwpg.simulator.entity.User;
import com.dwpg.simulator.entity.Wallet;
import com.dwpg.simulator.exception.ResourceNotFoundException;
import com.dwpg.simulator.repository.MerchantRepository;
import com.dwpg.simulator.repository.UserRepository;
import com.dwpg.simulator.repository.WalletRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.UUID;

@Service
public class MerchantService {

    private final MerchantRepository merchantRepository;
    private final UserRepository userRepository;
    private final WalletRepository walletRepository;
    private final IdempotencyService idempotencyService;

    public MerchantService(MerchantRepository merchantRepository,
                           UserRepository userRepository,
                           WalletRepository walletRepository,
                           IdempotencyService idempotencyService) {
        this.merchantRepository = merchantRepository;
        this.userRepository = userRepository;
        this.walletRepository = walletRepository;
        this.idempotencyService = idempotencyService;
    }

    @Transactional
    public MerchantResponse registerMerchant(MerchantRequest request, String username) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found: " + username));

        if (merchantRepository.existsByUserId(user.getId())) {
            throw new IllegalArgumentException("User is already registered as a merchant");
        }

        // Elevate user role to MERCHANT if currently USER
        if (user.getRole() == Role.ROLE_USER) {
            user.setRole(Role.ROLE_MERCHANT);
            userRepository.save(user);
        }

        // Provision or associate merchant settlement wallet
        Wallet settlementWallet = walletRepository.findByUserId(user.getId())
                .orElseGet(() -> walletRepository.save(new Wallet(user, BigDecimal.ZERO, "USD")));

        // Generate high-entropy API key
        String plainApiKey = "mkey_" + UUID.randomUUID().toString().replace("-", "");
        String apiKeyHash = idempotencyService.computeSha256(plainApiKey);

        Merchant merchant = new Merchant(user, settlementWallet, request.getBusinessName(), apiKeyHash);
        merchant = merchantRepository.save(merchant);

        return new MerchantResponse(
                merchant.getId(),
                user.getId(),
                merchant.getBusinessName(),
                settlementWallet.getId(),
                merchant.getStatus(),
                plainApiKey,
                merchant.getCreatedAt()
        );
    }

    @Transactional(readOnly = true)
    public MerchantResponse getMerchantById(Long merchantId) {
        Merchant merchant = merchantRepository.findById(merchantId)
                .orElseThrow(() -> new ResourceNotFoundException("Merchant not found with id: " + merchantId));

        return new MerchantResponse(
                merchant.getId(),
                merchant.getUser().getId(),
                merchant.getBusinessName(),
                merchant.getWallet().getId(),
                merchant.getStatus(),
                null,
                merchant.getCreatedAt()
        );
    }

    @Transactional(readOnly = true)
    public MerchantResponse getMerchantByUsername(String username) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found: " + username));
        Merchant merchant = merchantRepository.findByUserId(user.getId())
                .orElseThrow(() -> new ResourceNotFoundException("Merchant profile not registered for: " + username));

        return new MerchantResponse(
                merchant.getId(),
                user.getId(),
                merchant.getBusinessName(),
                merchant.getWallet().getId(),
                merchant.getStatus(),
                null,
                merchant.getCreatedAt()
        );
    }
}
