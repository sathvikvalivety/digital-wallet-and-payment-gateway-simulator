package com.dwpg.simulator.controller;

import com.dwpg.simulator.dto.*;
import com.dwpg.simulator.service.CheckoutService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/checkout")
public class CheckoutController {

    private final CheckoutService checkoutService;

    public CheckoutController(CheckoutService checkoutService) {
        this.checkoutService = checkoutService;
    }

    /**
     * Called by External Projects / Websites using Merchant API Key
     * Header: X-Api-Key: <merchant_api_key>
     */
    @PostMapping("/session")
    public ResponseEntity<CheckoutSessionResponse> createSession(
            @RequestHeader(value = "X-Api-Key", required = false) String apiKey,
            @Valid @RequestBody CreateCheckoutSessionRequest request,
            HttpServletRequest httpRequest) {

        String clientIp = extractClientIp(httpRequest);
        CheckoutSessionResponse response = checkoutService.createSession(request, apiKey, clientIp);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    /**
     * Called by Hosted Checkout Page to fetch order details
     */
    @GetMapping("/session/{sessionId}")
    public ResponseEntity<CheckoutSessionResponse> getSession(@PathVariable String sessionId) {
        return ResponseEntity.ok(checkoutService.getSession(sessionId));
    }

    /**
     * Called by Hosted Checkout Page when the customer completes payment (UPI, Card, or Wallet)
     */
    @PostMapping("/session/{sessionId}/complete")
    public ResponseEntity<CheckoutPaymentResult> completeSession(
            @PathVariable String sessionId,
            @RequestBody(required = false) CompleteCheckoutSessionRequest request,
            HttpServletRequest httpRequest) {

        if (request == null) {
            request = new CompleteCheckoutSessionRequest("UPI", null);
        }
        String clientIp = extractClientIp(httpRequest);
        CheckoutPaymentResult result = checkoutService.completeSession(sessionId, request, clientIp);
        return ResponseEntity.ok(result);
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
