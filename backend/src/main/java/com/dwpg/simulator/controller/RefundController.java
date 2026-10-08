package com.dwpg.simulator.controller;

import com.dwpg.simulator.dto.RefundRequest;
import com.dwpg.simulator.dto.RefundResponse;
import com.dwpg.simulator.exception.InvalidAmountException;
import com.dwpg.simulator.security.SecurityUtils;
import com.dwpg.simulator.service.RefundService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping({"/api/refunds", "/api/refund"})
public class RefundController {

    private final RefundService refundService;

    public RefundController(RefundService refundService) {
        this.refundService = refundService;
    }

    @PostMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<RefundResponse> requestRefund(
            @RequestBody RefundRequest request,
            HttpServletRequest httpRequest) {

        if (request == null || request.getPaymentId() == null) {
            throw new InvalidAmountException("Payment ID is required to process a refund");
        }

        String username = SecurityUtils.getCurrentUsername();
        String clientIp = extractClientIp(httpRequest);

        RefundResponse response = refundService.processRefund(request.getPaymentId(), request, username, clientIp);
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
