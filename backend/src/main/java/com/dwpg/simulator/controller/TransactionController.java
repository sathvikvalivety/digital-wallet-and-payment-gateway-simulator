package com.dwpg.simulator.controller;

import com.dwpg.simulator.dto.TransactionResponse;
import com.dwpg.simulator.security.SecurityUtils;
import com.dwpg.simulator.service.TransactionService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping({"/api/transactions", "/api/transaction"})
public class TransactionController {

    private final TransactionService transactionService;

    public TransactionController(TransactionService transactionService) {
        this.transactionService = transactionService;
    }

    @GetMapping({"", "/my"})
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<List<TransactionResponse>> getMyTransactions(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "50") int size) {
        String username = SecurityUtils.getCurrentUsername();
        return ResponseEntity.ok(transactionService.getMyTransactions(username, page, size));
    }

    @GetMapping("/{id}")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<TransactionResponse> getTransactionById(@PathVariable("id") Long id) {
        String username = SecurityUtils.getCurrentUsername();
        return ResponseEntity.ok(transactionService.getTransactionById(id, username));
    }
}
