package com.dwpg.simulator.service;

import com.dwpg.simulator.dto.FundRequest;
import com.dwpg.simulator.dto.WalletResponse;
import com.dwpg.simulator.entity.*;
import com.dwpg.simulator.exception.InvalidAmountException;
import com.dwpg.simulator.exception.ResourceNotFoundException;
import com.dwpg.simulator.exception.UnauthorizedAccessException;
import com.dwpg.simulator.repository.TransactionRepository;
import com.dwpg.simulator.repository.UserRepository;
import com.dwpg.simulator.repository.WalletRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

@Service
public class WalletService {

    private final WalletRepository walletRepository;
    private final UserRepository userRepository;
    private final TransactionRepository transactionRepository;
    private final AuditService auditService;

    public WalletService(WalletRepository walletRepository,
                         UserRepository userRepository,
                         TransactionRepository transactionRepository,
                         AuditService auditService) {
        this.walletRepository = walletRepository;
        this.userRepository = userRepository;
        this.transactionRepository = transactionRepository;
        this.auditService = auditService;
    }

    @Transactional(readOnly = true)
    public WalletResponse getMyWallet(String username) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found: " + username));
        Wallet wallet = walletRepository.findByUserId(user.getId())
                .orElseThrow(() -> new ResourceNotFoundException("Wallet not found for user: " + username));

        return toResponse(wallet);
    }

    @Transactional(readOnly = true)
    public WalletResponse getWalletById(Long walletId, String username) {
        Wallet wallet = walletRepository.findById(walletId)
                .orElseThrow(() -> new ResourceNotFoundException("Wallet not found with id: " + walletId));

        // Object-Level Authorization (BOLA/IDOR protection)
        if (!wallet.getUser().getUsername().equals(username)) {
            auditService.logEvent(AuditEventType.AUTHORIZATION_FAILURE, walletId, username, "FAILED",
                    "Attempted to access foreign wallet ID: " + walletId);
            throw new UnauthorizedAccessException("Access denied. You do not own wallet ID: " + walletId);
        }

        return toResponse(wallet);
    }

    @Transactional(isolation = Isolation.READ_COMMITTED)
    public WalletResponse fundWallet(Long walletId, FundRequest request, String username, String clientIp) {
        if (request.getAmount() == null || request.getAmount().compareTo(BigDecimal.ZERO) <= 0) {
            throw new InvalidAmountException("Fund amount must be strictly positive");
        }

        // Acquire exclusive pessimistic lock on the wallet row
        Wallet wallet = walletRepository.findByIdForUpdate(walletId)
                .orElseThrow(() -> new ResourceNotFoundException("Wallet not found with id: " + walletId));

        // Ownership verification (BOLA prevention)
        if (!wallet.getUser().getUsername().equals(username)) {
            auditService.logEvent(AuditEventType.AUTHORIZATION_FAILURE, walletId, username, "FAILED",
                    "Unauthorized attempt to add funds to foreign wallet ID: " + walletId, clientIp);
            throw new UnauthorizedAccessException("Access denied. You do not own wallet ID: " + walletId);
        }

        wallet.credit(request.getAmount());
        wallet = walletRepository.save(wallet);

        // Record transaction ledger entry
        Transaction tx = new Transaction(
                wallet,
                null,
                TransactionType.TOP_UP,
                request.getAmount(),
                wallet.getBalance(),
                "Simulated funds deposit of $" + request.getAmount()
        );
        transactionRepository.save(tx);

        auditService.logEvent(AuditEventType.FUNDS_ADDED, wallet.getId(), username, "SUCCESS",
                "Added simulated funds: $" + request.getAmount() + ". New balance: $" + wallet.getBalance(), clientIp);

        return toResponse(wallet);
    }

    public WalletResponse toResponse(Wallet wallet) {
        return new WalletResponse(
                wallet.getId(),
                wallet.getUser().getId(),
                wallet.getUser().getUsername(),
                wallet.getBalance(),
                wallet.getCurrency(),
                wallet.getUpdatedAt()
        );
    }
}
