package com.dwpg.simulator.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

public class GoogleOAuthRequest {

    private String idToken;

    @NotBlank(message = "Email is required")
    @Email(message = "Valid email is required")
    private String email;

    private String name;

    private String googleId;

    private String picture;

    public GoogleOAuthRequest() {}

    public GoogleOAuthRequest(String idToken, String email, String name, String googleId, String picture) {
        this.idToken = idToken;
        this.email = email;
        this.name = name;
        this.googleId = googleId;
        this.picture = picture;
    }

    public String getIdToken() { return idToken; }
    public void setIdToken(String idToken) { this.idToken = idToken; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getGoogleId() { return googleId; }
    public void setGoogleId(String googleId) { this.googleId = googleId; }

    public String getPicture() { return picture; }
    public void setPicture(String picture) { this.picture = picture; }
}
