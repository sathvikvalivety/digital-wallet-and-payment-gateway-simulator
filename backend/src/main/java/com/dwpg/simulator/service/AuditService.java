package com.dwpg.simulator.service;

import com.dwpg.simulator.dto.AuditLogResponse;
import com.dwpg.simulator.entity.AuditEventType;
import com.dwpg.simulator.entity.AuditLog;
import com.dwpg.simulator.repository.AuditLogRepository;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.regex.Pattern;

@Service
public class AuditService {

    private final AuditLogRepository auditLogRepository;

    private static final String DEFAULT_IP_ADDRESS = "127.0.0.1";
    private static final Pattern PASSWORD_PATTERN = Pattern.compile("(?i)(password|secret|token)\"\\s*:\\s*\"[^\"]+\"");
    private static final Pattern CARD_PATTERN = Pattern.compile("\\b(?:4\\d{12}(?:\\d{3})?|5[1-5]\\d{14})\\b");

    public AuditService(AuditLogRepository auditLogRepository) {
        this.auditLogRepository = auditLogRepository;
    }

    @Transactional
    public AuditLog logEvent(AuditEventType eventType, Long resourceId, String actorUsername, String outcome, String details, HttpServletRequest request) {
        String ipAddress = extractClientIp(request);
        String sanitizedDetails = scrubSensitiveData(details);
        AuditLog log = new AuditLog(eventType, actorUsername, resourceId, outcome, ipAddress, sanitizedDetails);
        return auditLogRepository.save(log);
    }

    @Transactional
    public AuditLog logEvent(AuditEventType eventType, Long resourceId, String actorUsername, String outcome, String details, String ipAddress) {
        String sanitizedDetails = scrubSensitiveData(details);
        AuditLog log = new AuditLog(eventType, actorUsername, resourceId, outcome, ipAddress, sanitizedDetails);
        return auditLogRepository.save(log);
    }

    @Transactional
    public AuditLog logEvent(AuditEventType eventType, Long resourceId, String actorUsername, String outcome, String details) {
        return logEvent(eventType, resourceId, actorUsername, outcome, details, DEFAULT_IP_ADDRESS);
    }

    @Transactional
    public AuditLog logEvent(AuditEventType eventType, Long resourceId, String actorUsername, String outcome) {
        return logEvent(eventType, resourceId, actorUsername, outcome, null, DEFAULT_IP_ADDRESS);
    }

    public List<AuditLogResponse> getAllAuditLogs(int page, int size) {
        Page<AuditLog> pageResult = auditLogRepository.findAllByOrderByCreatedAtDesc(PageRequest.of(page, size));
        return pageResult.map(this::mapToResponse).getContent();
    }

    public List<AuditLogResponse> getSecurityAlerts() {
        List<AuditLog> alerts = auditLogRepository.findByEventTypeOrderByCreatedAtDesc(AuditEventType.REPLAY_DETECTED);
        alerts.addAll(auditLogRepository.findByEventTypeOrderByCreatedAtDesc(AuditEventType.AUTHORIZATION_FAILURE));
        alerts.addAll(auditLogRepository.findByEventTypeOrderByCreatedAtDesc(AuditEventType.SUSPICIOUS_ACTIVITY));
        return alerts.stream().map(this::mapToResponse).toList();
    }

    private AuditLogResponse mapToResponse(AuditLog log) {
        return new AuditLogResponse(
                log.getId(),
                log.getEventType(),
                log.getActorUsername(),
                log.getResourceId(),
                log.getOutcome(),
                log.getIpAddress(),
                log.getDetails(),
                log.getCreatedAt()
        );
    }

    private String extractClientIp(HttpServletRequest request) {
        if (request == null) return DEFAULT_IP_ADDRESS;
        String xf = request.getHeader("X-Forwarded-For");
        if (xf != null && !xf.isBlank()) {
            return xf.split(",")[0].trim();
        }
        return request.getRemoteAddr() != null ? request.getRemoteAddr() : DEFAULT_IP_ADDRESS;
    }

    private String scrubSensitiveData(String input) {
        if (input == null) return null;
        String scrubbed = PASSWORD_PATTERN.matcher(input).replaceAll("\"$1\":\"***REDACTED***\"");
        return CARD_PATTERN.matcher(scrubbed).replaceAll("****-****-****-****");
    }
}
