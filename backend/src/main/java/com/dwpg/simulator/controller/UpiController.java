package com.dwpg.simulator.controller;

import com.dwpg.simulator.dto.*;
import com.dwpg.simulator.entity.UpiTransaction;
import com.dwpg.simulator.security.SecurityUtils;
import com.dwpg.simulator.service.UpiService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/upi")
public class UpiController {

    private final UpiService upiService;

    public UpiController(UpiService upiService) {
        this.upiService = upiService;
    }

    @PostMapping("/initiate")
    public ResponseEntity<UpiInitiateResponse> initiate(@Valid @RequestBody UpiInitiateRequest request, HttpServletRequest httpRequest) {
        String username = SecurityUtils.getCurrentUsername();
        if (username == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        String clientIp = extractClientIp(httpRequest);
        UpiInitiateResponse response = upiService.initiatePayment(request, username, clientIp);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PostMapping("/verify")
    public ResponseEntity<UpiVerifyResponse> verify(@Valid @RequestBody UpiVerifyRequest request, HttpServletRequest httpRequest) {
        String username = SecurityUtils.getCurrentUsername();
        if (username == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        String clientIp = extractClientIp(httpRequest);
        UpiVerifyResponse response = upiService.verifyPayment(request, username, clientIp);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/status/{referenceId}")
    public ResponseEntity<UpiStatusResponse> getStatus(@PathVariable String referenceId) {
        return ResponseEntity.ok(upiService.getStatus(referenceId));
    }

    @PostMapping("/webhook")
    public ResponseEntity<UpiStatusResponse> handleWebhook(@Valid @RequestBody UpiWebhookRequest request, HttpServletRequest httpRequest) {
        String clientIp = extractClientIp(httpRequest);
        UpiStatusResponse response = upiService.processWebhook(request, clientIp);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/simulate-callback/{referenceId}")
    public ResponseEntity<UpiStatusResponse> simulateBankCallback(@PathVariable String referenceId, HttpServletRequest httpRequest) {
        String clientIp = extractClientIp(httpRequest);
        UpiStatusResponse response = upiService.simulateBankCallback(referenceId, clientIp);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/my")
    public ResponseEntity<List<UpiTransaction>> getMyTransactions() {
        String username = SecurityUtils.getCurrentUsername();
        if (username == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        return ResponseEntity.ok(upiService.getMyTransactions(username));
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
