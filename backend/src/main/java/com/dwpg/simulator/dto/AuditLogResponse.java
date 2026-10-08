package com.dwpg.simulator.dto;

import com.dwpg.simulator.entity.AuditEventType;
import java.time.Instant;

public class AuditLogResponse {
    private Long id;
    private AuditEventType eventType;
    private String actorUsername;
    private Long resourceId;
    private String outcome;
    private String ipAddress;
    private String details;
    private Instant createdAt;

    public AuditLogResponse() {}

    public AuditLogResponse(Long id, AuditEventType eventType, String actorUsername, Long resourceId, String outcome, String ipAddress, String details, Instant createdAt) {
        this.id = id;
        this.eventType = eventType;
        this.actorUsername = actorUsername;
        this.resourceId = resourceId;
        this.outcome = outcome;
        this.ipAddress = ipAddress;
        this.details = details;
        this.createdAt = createdAt;
    }

    public Long getId() { return id; }
    public AuditEventType getEventType() { return eventType; }
    public String getActorUsername() { return actorUsername; }
    public Long getResourceId() { return resourceId; }
    public String getOutcome() { return outcome; }
    public String getIpAddress() { return ipAddress; }
    public String getDetails() { return details; }
    public Instant getCreatedAt() { return createdAt; }
}
