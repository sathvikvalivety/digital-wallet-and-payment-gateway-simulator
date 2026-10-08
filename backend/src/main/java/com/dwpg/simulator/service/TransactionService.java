package com.dwpg.simulator.service;

import com.dwpg.simulator.dto.TransactionResponse;
import com.dwpg.simulator.entity.Transaction;
import com.dwpg.simulator.entity.User;
import com.dwpg.simulator.entity.Wallet;
import com.dwpg.simulator.exception.ResourceNotFoundException;
import com.dwpg.simulator.exception.UnauthorizedAccessException;
import com.dwpg.simulator.repository.TransactionRepository;
import com.dwpg.simulator.repository.UserRepository;
import com.dwpg.simulator.repository.WalletRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class TransactionService {

    private final TransactionRepository transactionRepository;
    private final UserRepository userRepository;
    private final WalletRepository walletRepository;

    public TransactionService(TransactionRepository transactionRepository,
                              UserRepository userRepository,
                              WalletRepository walletRepository) {
        this.transactionRepository = transactionRepository;
        this.userRepository = userRepository;
        this.walletRepository = walletRepository;
    }

    @Transactional(readOnly = true)
    public List<TransactionResponse> getMyTransactions(String username, int page, int size) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found: " + username));
        Wallet wallet = walletRepository.findByUserId(user.getId())
                .orElseThrow(() -> new ResourceNotFoundException("Wallet not found for: " + username));

        Page<Transaction> pageResult = transactionRepository.findByWalletIdOrderByCreatedAtDesc(
                wallet.getId(), PageRequest.of(page, size));

        return pageResult.map(this::toResponse).getContent();
    }

    @Transactional(readOnly = true)
    public TransactionResponse getTransactionById(Long id, String username) {
        Transaction tx = transactionRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Transaction not found with id: " + id));

        // Object-Level Authorization (BOLA prevention)
        if (!tx.getWallet().getUser().getUsername().equals(username)) {
            throw new UnauthorizedAccessException("Access denied. You do not own transaction ID: " + id);
        }

        return toResponse(tx);
    }

    private TransactionResponse toResponse(Transaction tx) {
        return new TransactionResponse(
                tx.getId(),
                tx.getWallet().getId(),
                tx.getPayment() != null ? tx.getPayment().getId() : null,
                tx.getType(),
                tx.getAmount(),
                tx.getBalanceAfter(),
                tx.getDescription(),
                tx.getCreatedAt()
        );
    }
}
