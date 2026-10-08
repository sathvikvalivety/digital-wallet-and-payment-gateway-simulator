package com.dwpg.simulator.controller;

import com.dwpg.simulator.dto.AuditLogResponse;
import com.dwpg.simulator.service.AuditService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/admin")
@PreAuthorize("hasRole('ADMIN')")
public class AdminController {

    private final AuditService auditService;

    public AdminController(AuditService auditService) {
        this.auditService = auditService;
    }

    @GetMapping("/audit-logs")
    public ResponseEntity<List<AuditLogResponse>> getAuditLogs(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "50") int size) {
        return ResponseEntity.ok(auditService.getAllAuditLogs(page, size));
    }

    @GetMapping("/alerts")
    public ResponseEntity<List<AuditLogResponse>> getSecurityAlerts() {
        return ResponseEntity.ok(auditService.getSecurityAlerts());
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> getSystemHealth() {
        Map<String, Object> health = new HashMap<>();
        health.put("status", "UP");
        health.put("service", "Digital Wallet and Payment Gateway Simulator");
        health.put("securityMode", "Strict RBAC + Pessimistic DB Locking + Idempotency Replay Trapping");
        return ResponseEntity.ok(health);
    }
}
