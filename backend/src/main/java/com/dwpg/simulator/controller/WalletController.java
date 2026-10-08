package com.dwpg.simulator.controller;

import com.dwpg.simulator.dto.FundRequest;
import com.dwpg.simulator.dto.WalletResponse;
import com.dwpg.simulator.security.SecurityUtils;
import com.dwpg.simulator.service.WalletService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping({"/api/wallets", "/api/wallet"})
public class WalletController {

    private final WalletService walletService;

    public WalletController(WalletService walletService) {
        this.walletService = walletService;
    }

    @GetMapping({"", "/me"})
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<WalletResponse> getMyWallet() {
        String username = SecurityUtils.getCurrentUsername();
        return ResponseEntity.ok(walletService.getMyWallet(username));
    }

    @PostMapping({"", "/create"})
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<WalletResponse> createWallet() {
        String username = SecurityUtils.getCurrentUsername();
        return ResponseEntity.status(HttpStatus.CREATED).body(walletService.createWallet(username));
    }

    @PostMapping({"/topup", "/fund"})
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<WalletResponse> fundMyWallet(@Valid @RequestBody FundRequest request,
                                                       HttpServletRequest httpRequest) {
        String username = SecurityUtils.getCurrentUsername();
        String clientIp = extractClientIp(httpRequest);
        return ResponseEntity.ok(walletService.fundMyWallet(request, username, clientIp));
    }

    @GetMapping("/{id}")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<WalletResponse> getWalletById(@PathVariable("id") Long id) {
        String username = SecurityUtils.getCurrentUsername();
        return ResponseEntity.ok(walletService.getWalletById(id, username));
    }

    @PostMapping("/{id}/fund")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<WalletResponse> fundWallet(@PathVariable("id") Long id,
                                                     @Valid @RequestBody FundRequest request,
                                                     HttpServletRequest httpRequest) {
        String username = SecurityUtils.getCurrentUsername();
        String clientIp = extractClientIp(httpRequest);
        return ResponseEntity.ok(walletService.fundWallet(id, request, username, clientIp));
    }

    private String extractClientIp(HttpServletRequest request) {
        if (request == null) return "127.0.0.1";
        String xf = request.getHeader("X-Forwarded-For");
        if (xf != null && !xf.isBlank()) {
            return xf.split(",")[0].trim();
        }
        return request.getRemoteAddr() != null ? request.getRemoteAddr() : "127.0.0.1";
    }
}
