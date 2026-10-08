package com.dwpg.simulator.controller;

import com.dwpg.simulator.dto.PaymentRequest;
import com.dwpg.simulator.dto.RefundRequest;
import com.dwpg.simulator.entity.*;
import com.dwpg.simulator.repository.*;
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

import java.math.BigDecimal;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class PaymentSecurityIntegrationTest {

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
    private PaymentRepository paymentRepository;

    @Autowired
    private RefundRepository refundRepository;

    @Autowired
    private TransactionRepository transactionRepository;

    @Autowired
    private IdempotencyRecordRepository idempotencyRecordRepository;

    @Autowired
    private com.dwpg.simulator.repository.CheckoutSessionRepository checkoutSessionRepository;

    @Autowired
    private com.dwpg.simulator.repository.UpiTransactionRepository upiTransactionRepository;

    @Autowired
    private JwtTokenProvider jwtTokenProvider;

    private String userToken;
    private String merchantToken;
    private String adminToken;
    private Long merchantId;
    private Long userWalletId;

    @BeforeEach
    void setUp() {
        refundRepository.deleteAll();
        transactionRepository.deleteAll();
        paymentRepository.deleteAll();
        idempotencyRecordRepository.deleteAll();
        checkoutSessionRepository.deleteAll();
        upiTransactionRepository.deleteAll();
        merchantRepository.deleteAll();
        walletRepository.deleteAll();
        userRepository.deleteAll();

        // 1. End User
        User user = new User("alice", "alice@sec.test", "hash", Role.ROLE_USER);
        user = userRepository.save(user);
        Wallet userWallet = new Wallet(user, BigDecimal.valueOf(500.00), "INR");
        userWallet = walletRepository.save(userWallet);
        userWalletId = userWallet.getId();
        userToken = "Bearer " + jwtTokenProvider.generateToken("alice", "ROLE_USER");

        // 2. Merchant User
        User merchantUser = new User("bob_merchant", "bob@sec.test", "hash", Role.ROLE_MERCHANT);
        merchantUser = userRepository.save(merchantUser);
        Wallet merchantWallet = new Wallet(merchantUser, BigDecimal.valueOf(50.00), "INR");
        merchantWallet = walletRepository.save(merchantWallet);
        Merchant merchant = new Merchant(merchantUser, merchantWallet, "Bob Electronics", "m_key");
        merchant = merchantRepository.save(merchant);
        merchantId = merchant.getId();
        merchantToken = "Bearer " + jwtTokenProvider.generateToken("bob_merchant", "ROLE_MERCHANT");

        // 3. Admin User
        User adminUser = new User("sec_admin", "admin@sec.test", "hash", Role.ROLE_ADMIN);
        userRepository.save(adminUser);
        adminToken = "Bearer " + jwtTokenProvider.generateToken("sec_admin", "ROLE_ADMIN");
    }

    @Test
    @DisplayName("Integration Test: Idempotent Payment - Same Idempotency-Key returns cached response without second debit")
    void testDuplicatePaymentWithSameIdempotencyKey() throws Exception {
        String idempotencyKey = "idem-" + UUID.randomUUID();
        PaymentRequest req = new PaymentRequest(merchantId, BigDecimal.valueOf(50.00), "ORD-001", "INR");

        // 1st request -> executes payment
        String firstResponse = mockMvc.perform(post("/api/payments")
                        .header("Authorization", userToken)
                        .header("Idempotency-Key", idempotencyKey)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andReturn().getResponse().getContentAsString();

        // Check user balance: 500 - 50 = 450
        Wallet w1 = walletRepository.findById(userWalletId).orElseThrow();
        assertEquals(0, w1.getBalance().compareTo(BigDecimal.valueOf(450.00)));

        // 2nd request with identical Idempotency-Key -> returns cached response
        String secondResponse = mockMvc.perform(post("/api/payments")
                        .header("Authorization", userToken)
                        .header("Idempotency-Key", idempotencyKey)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andReturn().getResponse().getContentAsString();

        // User balance must STILL be 450.00 (NOT 400.00!)
        Wallet w2 = walletRepository.findById(userWalletId).orElseThrow();
        assertEquals(0, w2.getBalance().compareTo(BigDecimal.valueOf(450.00)), "User was debited twice despite Idempotency-Key!");
    }

    @Test
    @DisplayName("Integration Test: Replay Attack - Reused Idempotency-Key with altered payload is rejected with 409 Conflict")
    void testReplayAttackWithModifiedPayloadAndReusedKey() throws Exception {
        String idempotencyKey = "replay-key-" + UUID.randomUUID();
        PaymentRequest reqOriginal = new PaymentRequest(merchantId, BigDecimal.valueOf(50.00), "ORD-ORIGINAL", "INR");

        // Valid initial request
        mockMvc.perform(post("/api/payments")
                        .header("Authorization", userToken)
                        .header("Idempotency-Key", idempotencyKey)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(reqOriginal)))
                .andExpect(status().isCreated());

        // Attacker attempts replay with modified amount ($999.00)
        PaymentRequest reqTampered = new PaymentRequest(merchantId, BigDecimal.valueOf(999.00), "ORD-TAMPERED", "INR");

        mockMvc.perform(post("/api/payments")
                        .header("Authorization", userToken)
                        .header("Idempotency-Key", idempotencyKey)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(reqTampered)))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.error").value("Idempotency Conflict"));
    }

    @Test
    @DisplayName("Integration Test: Duplicate Refund Prevention - Payment cannot be refunded twice")
    void testDuplicateRefundPrevention() throws Exception {
        String idempotencyKey = "refund-idem-" + UUID.randomUUID();
        PaymentRequest req = new PaymentRequest(merchantId, BigDecimal.valueOf(30.00), "ORD-REFUND", "INR");

        // Execute initial payment
        String respStr = mockMvc.perform(post("/api/payments")
                        .header("Authorization", userToken)
                        .header("Idempotency-Key", idempotencyKey)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isCreated())
                .andReturn().getResponse().getContentAsString();

        Long paymentId = objectMapper.readTree(respStr).get("paymentId").asLong();

        RefundRequest refundReq = new RefundRequest("Item returned");

        // 1st refund -> succeeds
        mockMvc.perform(post("/api/payments/" + paymentId + "/refund")
                        .header("Authorization", merchantToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(refundReq)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("COMPLETED"));

        // 2nd refund on same payment -> MUST fail with 400 Bad Request
        mockMvc.perform(post("/api/payments/" + paymentId + "/refund")
                        .header("Authorization", merchantToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(refundReq)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").value("Invalid State Transition"));
    }

    @Test
    @DisplayName("Integration Test: BOLA Protection - Accessing foreign wallet returns 403 Forbidden")
    void testUnauthorizedWalletAccessBOLA() throws Exception {
        // bob_merchant attempts to access Alice's wallet
        mockMvc.perform(get("/api/wallets/" + userWalletId)
                        .header("Authorization", merchantToken))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.error").value("Forbidden"));
    }

    @Test
    @DisplayName("Integration Test: RBAC - Standard user accessing Admin Audit Logs is rejected with 403 Forbidden")
    void testAdminAuditLogsForbiddenForStandardUser() throws Exception {
        mockMvc.perform(get("/api/admin/audit-logs")
                        .header("Authorization", userToken))
                .andExpect(status().isForbidden());
    }

    @Test
    @DisplayName("Integration Test: Admin Token can access Audit Logs successfully")
    void testAdminAuditLogsAccessSuccess() throws Exception {
        mockMvc.perform(get("/api/admin/audit-logs")
                        .header("Authorization", adminToken))
                .andExpect(status().isOk());
    }
}
