package com.dwpg.simulator.service;

import com.dwpg.simulator.entity.AuditEventType;
import com.dwpg.simulator.entity.IdempotencyRecord;
import com.dwpg.simulator.exception.IdempotencyException;
import com.dwpg.simulator.repository.IdempotencyRecordRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import java.util.Optional;

@Service
public class IdempotencyService {

    private final IdempotencyRecordRepository idempotencyRecordRepository;
    private final AuditService auditService;

    public IdempotencyService(IdempotencyRecordRepository idempotencyRecordRepository, AuditService auditService) {
        this.idempotencyRecordRepository = idempotencyRecordRepository;
        this.auditService = auditService;
    }

    public String computeSha256(String data) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(data.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(hash);
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException("SHA-256 algorithm unavailable", e);
        }
    }

    @Transactional(readOnly = true)
    public Optional<IdempotencyRecord> checkIdempotency(String idempotencyKey, String payloadHash, String username, String clientIp) {
        if (idempotencyKey == null || idempotencyKey.isBlank()) {
            throw new IdempotencyException("Mandatory 'Idempotency-Key' header is missing from payment request.");
        }

        Optional<IdempotencyRecord> recordOpt = idempotencyRecordRepository.findByIdempotencyKey(idempotencyKey);
        if (recordOpt.isPresent()) {
            IdempotencyRecord existingRecord = recordOpt.get();
            if (!existingRecord.getRequestHash().equals(payloadHash)) {
                auditService.logEvent(AuditEventType.REPLAY_DETECTED, existingRecord.getResourceId(), username, "FAILED",
                        "Idempotency key '" + idempotencyKey + "' reused with modified request payload (Replay/Tampering attempt).", clientIp);
                throw new IdempotencyException("Idempotency key was previously used with different request parameters. Replay attempt rejected.");
            }
            auditService.logEvent(AuditEventType.DUPLICATE_PAYMENT, existingRecord.getResourceId(), username, "SUCCESS",
                    "Idempotent duplicate request handled; returning cached response.", clientIp);
            return Optional.of(existingRecord);
        }
        return Optional.empty();
    }

    @Transactional
    public IdempotencyRecord saveIdempotencyRecord(String idempotencyKey, String payloadHash, Long resourceId, String responseBody, int statusCode) {
        IdempotencyRecord newRecord = new IdempotencyRecord(idempotencyKey, payloadHash, resourceId, responseBody, statusCode);
        return idempotencyRecordRepository.save(newRecord);
    }
}
