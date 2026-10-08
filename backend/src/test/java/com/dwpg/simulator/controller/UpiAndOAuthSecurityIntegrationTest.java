package com.dwpg.simulator.controller;

import com.dwpg.simulator.dto.*;
import com.dwpg.simulator.entity.Role;
import com.dwpg.simulator.entity.User;
import com.dwpg.simulator.repository.UserRepository;
import com.dwpg.simulator.repository.WalletRepository;
import com.dwpg.simulator.security.JwtTokenProvider;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import java.math.BigDecimal;

import static org.hamcrest.Matchers.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
public class UpiAndOAuthSecurityIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private WalletRepository walletRepository;

    @Autowired
    private JwtTokenProvider jwtTokenProvider;

    private String userToken;
    private String secondUserToken;

    @BeforeEach
    void setUp() {
        if (!userRepository.existsByUsername("upi_test_user")) {
            User u = new User("upi_test_user", "upi_test@user.com", "hash", Role.ROLE_USER);
            u = userRepository.save(u);
            walletRepository.save(new com.dwpg.simulator.entity.Wallet(u, BigDecimal.valueOf(100.00), "INR"));
        }
        if (!userRepository.existsByUsername("upi_other_user")) {
            User u2 = new User("upi_other_user", "upi_other@user.com", "hash", Role.ROLE_USER);
            u2 = userRepository.save(u2);
            walletRepository.save(new com.dwpg.simulator.entity.Wallet(u2, BigDecimal.valueOf(100.00), "INR"));
        }
        userToken = "Bearer " + jwtTokenProvider.generateToken("upi_test_user", "ROLE_USER");
        secondUserToken = "Bearer " + jwtTokenProvider.generateToken("upi_other_user", "ROLE_USER");
    }

    @Test
    @DisplayName("OAuth-01: Google OAuth login registers new user and provisions digital wallet")
    void testGoogleOAuthLogin() throws Exception {
        GoogleOAuthRequest req = new GoogleOAuthRequest(
                "mock_id_token",
                "test_oauth_user@gmail.com",
                "OAuth User",
                "google_12345",
                null
        );

        mockMvc.perform(post("/api/auth/oauth/google")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.token").isNotEmpty())
                .andExpect(jsonPath("$.role").value("ROLE_USER"))
                .andExpect(jsonPath("$.walletId").isNotEmpty());
    }

    @Test
    @DisplayName("UPI-01: Initiate UPI transaction produces valid NPCI URI with valivetysathvik@ibl")
    void testUpiInitiate() throws Exception {
        UpiInitiateRequest req = new UpiInitiateRequest(BigDecimal.valueOf(250.00), "Recharge", "TOPUP");

        mockMvc.perform(post("/api/upi/initiate")
                        .header("Authorization", userToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.referenceId").value(startsWith("DWPG-UPI-")))
                .andExpect(jsonPath("$.payeeVpa").value("valivetysathvik@ibl"))
                .andExpect(jsonPath("$.payeeName").value("sathvikvalivety"))
                .andExpect(jsonPath("$.amount").value(250.00))
                .andExpect(jsonPath("$.upiUri").value(containsString("valivetysathvik%40ibl")));
    }

    @Test
    @DisplayName("UPI-02: Verify UPI payment with UTR credits wallet and enforces anti-replay")
    void testUpiVerifyAndReplayDefense() throws Exception {
        // 1. Initiate
        UpiInitiateRequest req = new UpiInitiateRequest(BigDecimal.valueOf(150.00), "Recharge Test", "TOPUP");
        MvcResult initResult = mockMvc.perform(post("/api/upi/initiate")
                        .header("Authorization", userToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andReturn();

        UpiInitiateResponse initResp = objectMapper.readValue(initResult.getResponse().getContentAsString(), UpiInitiateResponse.class);
        String refId = initResp.getReferenceId();
        String utr = "UTR" + System.currentTimeMillis();

        // 2. Verify with UTR
        UpiVerifyRequest verifyReq = new UpiVerifyRequest(refId, utr);
        mockMvc.perform(post("/api/upi/verify")
                        .header("Authorization", userToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(verifyReq)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.success").value(true))
                .andExpect(jsonPath("$.status").value("CONFIRMED"))
                .andExpect(jsonPath("$.utrNumber").value(utr));

        // 3. Initiate second transaction
        MvcResult init2Result = mockMvc.perform(post("/api/upi/initiate")
                        .header("Authorization", userToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andReturn();
        UpiInitiateResponse init2Resp = objectMapper.readValue(init2Result.getResponse().getContentAsString(), UpiInitiateResponse.class);

        // 4. Attempt Replay with duplicate UTR -> must fail with HTTP 400 Idempotency Conflict
        UpiVerifyRequest replayReq = new UpiVerifyRequest(init2Resp.getReferenceId(), utr);
        mockMvc.perform(post("/api/upi/verify")
                        .header("Authorization", userToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(replayReq)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").value("Idempotency Conflict"))
                .andExpect(jsonPath("$.message").value(containsString("Duplicate UTR detected")));
    }

    @Test
    @DisplayName("UPI-03: Foreign user cannot verify someone else's UPI reference (BOLA/IDOR protection)")
    void testForeignUpiVerificationForbidden() throws Exception {
        UpiInitiateRequest req = new UpiInitiateRequest(BigDecimal.valueOf(300.00), "BOLA test", "TOPUP");
        MvcResult initResult = mockMvc.perform(post("/api/upi/initiate")
                        .header("Authorization", userToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andReturn();

        UpiInitiateResponse initResp = objectMapper.readValue(initResult.getResponse().getContentAsString(), UpiInitiateResponse.class);

        // Attempt verify by secondUser
        UpiVerifyRequest verifyReq = new UpiVerifyRequest(initResp.getReferenceId(), "UTR9999888877");
        mockMvc.perform(post("/api/upi/verify")
                        .header("Authorization", secondUserToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(verifyReq)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("You do not own this UPI payment reference"));
    }

    @Test
    @DisplayName("UPI-04: Status endpoint returns pending then confirmed after webhook auto-verification")
    void testUpiStatusAndWebhookAutoVerification() throws Exception {
        // 1. Initiate
        UpiInitiateRequest req = new UpiInitiateRequest(BigDecimal.valueOf(450.00), "Webhook Auto Verify Test", "TOPUP");
        MvcResult initResult = mockMvc.perform(post("/api/upi/initiate")
                        .header("Authorization", userToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andReturn();

        UpiInitiateResponse initResp = objectMapper.readValue(initResult.getResponse().getContentAsString(), UpiInitiateResponse.class);
        String refId = initResp.getReferenceId();

        // 2. Query status initially -> PENDING
        mockMvc.perform(get("/api/upi/status/" + refId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.referenceId").value(refId))
                .andExpect(jsonPath("$.status").value("PENDING"));

        // 3. Post webhook callback simulating bank/aggregator
        String bankUtr = "BANK" + System.currentTimeMillis();
        UpiWebhookRequest webhookReq = new UpiWebhookRequest(refId, bankUtr, BigDecimal.valueOf(450.00), "SUCCESS");
        mockMvc.perform(post("/api/upi/webhook")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(webhookReq)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("CONFIRMED"))
                .andExpect(jsonPath("$.utrNumber").value(bankUtr));

        // 4. Query status again -> CONFIRMED
        mockMvc.perform(get("/api/upi/status/" + refId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.referenceId").value(refId))
                .andExpect(jsonPath("$.status").value("CONFIRMED"))
                .andExpect(jsonPath("$.utrNumber").value(bankUtr))
                .andExpect(jsonPath("$.newWalletBalance").isNotEmpty());
    }

    @Test
    @DisplayName("UPI-05: Simulate bank callback triggers zero-click auto-verification")
    void testSimulateBankCallback() throws Exception {
        UpiInitiateRequest req = new UpiInitiateRequest(BigDecimal.valueOf(100.00), "Simulate Test", "TOPUP");
        MvcResult initResult = mockMvc.perform(post("/api/upi/initiate")
                        .header("Authorization", userToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andReturn();

        UpiInitiateResponse initResp = objectMapper.readValue(initResult.getResponse().getContentAsString(), UpiInitiateResponse.class);
        String refId = initResp.getReferenceId();

        // Trigger simulation
        mockMvc.perform(post("/api/upi/simulate-callback/" + refId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("CONFIRMED"))
                .andExpect(jsonPath("$.utrNumber").isNotEmpty())
                .andExpect(jsonPath("$.referenceId").value(refId));
    }
}
