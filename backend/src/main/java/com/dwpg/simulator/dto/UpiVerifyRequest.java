package com.dwpg.simulator.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;

public class UpiVerifyRequest {

    @NotBlank(message = "Reference ID is required")
    private String referenceId;

    @NotBlank(message = "12-digit UTR number is required")
    @Pattern(regexp = "^[0-9A-Za-z]{6,20}$", message = "UTR / Transaction Reference must be 6 to 20 alphanumeric characters (standard UPI UTR is 12 digits)")
    private String utrNumber;

    public UpiVerifyRequest() {}

    public UpiVerifyRequest(String referenceId, String utrNumber) {
        this.referenceId = referenceId;
        this.utrNumber = utrNumber;
    }

    public String getReferenceId() { return referenceId; }
    public void setReferenceId(String referenceId) { this.referenceId = referenceId; }

    public String getUtrNumber() { return utrNumber; }
    public void setUtrNumber(String utrNumber) { this.utrNumber = utrNumber; }
}
