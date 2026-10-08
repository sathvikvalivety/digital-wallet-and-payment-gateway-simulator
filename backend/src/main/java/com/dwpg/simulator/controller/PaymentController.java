package com.dwpg.simulator.controller;

import com.dwpg.simulator.dto.PaymentRequest;
import com.dwpg.simulator.dto.PaymentResponse;
import com.dwpg.simulator.dto.RefundRequest;
import com.dwpg.simulator.dto.RefundResponse;
import com.dwpg.simulator.exception.IdempotencyException;
import com.dwpg.simulator.security.SecurityUtils;
import com.dwpg.simulator.service.PaymentService;
import com.dwpg.simulator.service.RefundService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/payments")
public class PaymentController {

    private final PaymentService paymentService;
    private final RefundService refundService;

    public PaymentController(PaymentService paymentService, RefundService refundService) {
        this.paymentService = paymentService;
        this.refundService = refundService;
    }

    @PostMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<PaymentResponse> initiatePayment(
            @RequestHeader(value = "Idempotency-Key", required = false) String idempotencyKey,
            @Valid @RequestBody PaymentRequest request,
            HttpServletRequest httpRequest) {

        if (idempotencyKey == null || idempotencyKey.isBlank()) {
            throw new IdempotencyException("Header 'Idempotency-Key' is mandatory for initiating payment transactions");
        }

        String username = SecurityUtils.getCurrentUsername();
        String clientIp = extractClientIp(httpRequest);

        PaymentResponse response = paymentService.processPayment(idempotencyKey, request, username, clientIp);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/{id}")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<PaymentResponse> getPaymentById(@PathVariable("id") Long id) {
        return ResponseEntity.ok(paymentService.getPaymentById(id));
    }

    @PostMapping("/{id}/refund")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<RefundResponse> refundPayment(
            @PathVariable("id") Long id,
            @RequestBody(required = false) RefundRequest request,
            HttpServletRequest httpRequest) {

        String username = SecurityUtils.getCurrentUsername();
        String clientIp = extractClientIp(httpRequest);

        RefundResponse response = refundService.processRefund(id, request, username, clientIp);
        return ResponseEntity.ok(response);
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
