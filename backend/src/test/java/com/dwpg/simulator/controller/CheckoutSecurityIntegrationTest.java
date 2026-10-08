package com.dwpg.simulator.controller;

import com.dwpg.simulator.dto.CheckoutPaymentResult;
import com.dwpg.simulator.dto.CheckoutSessionResponse;
import com.dwpg.simulator.dto.CompleteCheckoutSessionRequest;
import com.dwpg.simulator.dto.CreateCheckoutSessionRequest;
import com.dwpg.simulator.entity.Merchant;
import com.dwpg.simulator.entity.Role;
import com.dwpg.simulator.entity.User;
import com.dwpg.simulator.entity.Wallet;
import com.dwpg.simulator.repository.MerchantRepository;
import com.dwpg.simulator.repository.UserRepository;
import com.dwpg.simulator.repository.WalletRepository;
import com.dwpg.simulator.service.IdempotencyService;
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
public class CheckoutSecurityIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private WalletRepository walletRepository;

    @Autowired
    private MerchantRepository merchantRepository;

    @Autowired
    private com.dwpg.simulator.repository.CheckoutSessionRepository checkoutSessionRepository;

    @Autowired
    private IdempotencyService idempotencyService;

    private String validApiKey = "dwpg_live_test_merchant_key_12345";
    private Merchant testMerchant;

    @BeforeEach
    void setUp() {
        checkoutSessionRepository.deleteAll();
        if (!userRepository.existsByUsername("checkout_merchant_user")) {
            User u = new User("checkout_merchant_user", "merchant@checkout.com", "hash", Role.ROLE_MERCHANT);
            u = userRepository.save(u);
            Wallet w = walletRepository.save(new Wallet(u, BigDecimal.valueOf(500.00), "INR"));

            String keyHash = idempotencyService.computeSha256(validApiKey);
            testMerchant = new Merchant(u, w, "Sathvik Tech Store", keyHash);
            testMerchant.setApiKey(validApiKey);
            testMerchant = merchantRepository.save(testMerchant);
        } else {
            testMerchant = merchantRepository.findAll().stream()
                    .filter(m -> "Sathvik Tech Store".equals(m.getBusinessName()))
                    .findFirst().orElse(null);
        }
    }

    @Test
    @DisplayName("CHECKOUT-01: External client creates session with valid X-Api-Key")
    void testCreateSessionWithValidApiKey() throws Exception {
        CreateCheckoutSessionRequest req = new CreateCheckoutSessionRequest(
                BigDecimal.valueOf(499.00),
                "INR",
                "ORD-TEST-101",
                "Pro Gaming Headset",
                "Alice Wonder",
                "alice@example.com",
                "https://external-store.com/success",
                "https://external-store.com/cart"
        );

        mockMvc.perform(post("/api/checkout/session")
                        .header("X-Api-Key", validApiKey)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.sessionId").value(startsWith("cs_dwpg_")))
                .andExpect(jsonPath("$.checkoutUrl").value(containsString("/checkout?session=")))
                .andExpect(jsonPath("$.amount").value(499.00))
                .andExpect(jsonPath("$.merchantBusinessName").value("Sathvik Tech Store"))
                .andExpect(jsonPath("$.status").value("PENDING"));
    }

    @Test
    @DisplayName("CHECKOUT-02: External client rejected with 401 if X-Api-Key is missing or invalid")
    void testCreateSessionWithInvalidApiKey() throws Exception {
        CreateCheckoutSessionRequest req = new CreateCheckoutSessionRequest(
                BigDecimal.valueOf(100.00),
                "INR",
                "ORD-FAIL",
                "Item",
                "Bob",
                "bob@example.com",
                "https://store.com/return",
                null
        );

        // Missing Key
        mockMvc.perform(post("/api/checkout/session")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isForbidden());

        // Invalid Key
        mockMvc.perform(post("/api/checkout/session")
                        .header("X-Api-Key", "invalid_fake_key_999")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isForbidden());
    }

    @Test
    @DisplayName("CHECKOUT-03: Hosted checkout page fetches session details without authentication")
    void testGetSessionDetailsPublic() throws Exception {
        CreateCheckoutSessionRequest req = new CreateCheckoutSessionRequest(
                BigDecimal.valueOf(250.00),
                "INR",
                "ORD-PUBLIC-1",
                "Wireless Mouse",
                "Carol",
                "carol@example.com",
                "https://store.com/ok",
                null
        );

        MvcResult result = mockMvc.perform(post("/api/checkout/session")
                        .header("X-Api-Key", validApiKey)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andReturn();

        CheckoutSessionResponse session = objectMapper.readValue(result.getResponse().getContentAsString(), CheckoutSessionResponse.class);

        // Fetch without any Auth token or API key (as a customer browser would)
        mockMvc.perform(get("/api/checkout/session/" + session.getSessionId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.sessionId").value(session.getSessionId()))
                .andExpect(jsonPath("$.amount").value(250.00))
                .andExpect(jsonPath("$.productName").value("Wireless Mouse"));
    }

    @Test
    @DisplayName("CHECKOUT-04: Complete payment via UPI credits merchant wallet and returns returnUrl")
    void testCompletePaymentUpiAndCreditMerchant() throws Exception {
        Long walletId = testMerchant.getWallet().getId();
        BigDecimal initialBal = walletRepository.findById(walletId).orElseThrow().getBalance();

        CreateCheckoutSessionRequest req = new CreateCheckoutSessionRequest(
                BigDecimal.valueOf(300.00),
                "INR",
                "ORD-UPI-TEST",
                "Mechanical Keyboard",
                "Dave",
                "dave@example.com",
                "https://external-store.com/order-success",
                null
        );

        MvcResult result = mockMvc.perform(post("/api/checkout/session")
                        .header("X-Api-Key", validApiKey)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andReturn();

        CheckoutSessionResponse session = objectMapper.readValue(result.getResponse().getContentAsString(), CheckoutSessionResponse.class);

        // Customer completes via UPI with 12-digit UTR
        CompleteCheckoutSessionRequest payReq = new CompleteCheckoutSessionRequest("UPI", "428192837461");
        mockMvc.perform(post("/api/checkout/session/" + session.getSessionId() + "/complete")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payReq)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.success").value(true))
                .andExpect(jsonPath("$.status").value("COMPLETED"))
                .andExpect(jsonPath("$.redirectUrl").value(containsString("orderId=ORD-UPI-TEST")))
                .andExpect(jsonPath("$.redirectUrl").value(containsString("status=SUCCESS")));

        // Verify merchant wallet credited
        Wallet refreshedWallet = walletRepository.findById(testMerchant.getWallet().getId()).orElseThrow();
        assertEquals(0, initialBal.add(BigDecimal.valueOf(300.00)).compareTo(refreshedWallet.getBalance()));
    }

    @Test
    @DisplayName("CHECKOUT-05: Complete payment via Card and verify redirectUrl format")
    void testCompletePaymentCard() throws Exception {
        CreateCheckoutSessionRequest req = new CreateCheckoutSessionRequest(
                BigDecimal.valueOf(150.00),
                "INR",
                "ORD-CARD-TEST",
                "USB-C Hub",
                "Eve",
                "eve@example.com",
                "https://merchant-store.com/checkout/callback",
                null
        );

        MvcResult result = mockMvc.perform(post("/api/checkout/session")
                        .header("X-Api-Key", validApiKey)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andReturn();

        CheckoutSessionResponse session = objectMapper.readValue(result.getResponse().getContentAsString(), CheckoutSessionResponse.class);

        CompleteCheckoutSessionRequest payReq = new CompleteCheckoutSessionRequest();
        payReq.setPaymentMethod("CARD");
        payReq.setCardNumber("4532892311849021");

        mockMvc.perform(post("/api/checkout/session/" + session.getSessionId() + "/complete")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payReq)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.success").value(true))
                .andExpect(jsonPath("$.status").value("COMPLETED"))
                .andExpect(jsonPath("$.redirectUrl").value(containsString("status=SUCCESS")))
                .andExpect(jsonPath("$.redirectUrl").value(containsString("orderId=ORD-CARD-TEST")));
    }
}
