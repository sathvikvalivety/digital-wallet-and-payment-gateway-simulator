package com.dwpg.simulator.concurrency;

import com.dwpg.simulator.dto.PaymentRequest;
import com.dwpg.simulator.dto.PaymentResponse;
import com.dwpg.simulator.entity.*;
import com.dwpg.simulator.exception.InsufficientFundsException;
import com.dwpg.simulator.repository.*;
import com.dwpg.simulator.service.PaymentService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.util.UUID;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@ActiveProfiles("test")
class PaymentConcurrencyTest {

    @Autowired
    private PaymentService paymentService;

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

    private Long merchantId;
    private Long senderWalletId;

    @BeforeEach
    void setUp() {
        refundRepository.deleteAll();
        transactionRepository.deleteAll();
        paymentRepository.deleteAll();
        idempotencyRecordRepository.deleteAll();
        merchantRepository.deleteAll();
        walletRepository.deleteAll();
        userRepository.deleteAll();

        // Create sender user with exactly $100.00
        User bob = new User("bob", "bob@concurrency.test", "hash", Role.ROLE_USER);
        bob = userRepository.save(bob);
        Wallet bobWallet = new Wallet(bob, BigDecimal.valueOf(100.00), "INR");
        bobWallet = walletRepository.save(bobWallet);
        senderWalletId = bobWallet.getId();

        // Create merchant user with ₹0.00
        User merchantUser = new User("acme_corp", "acme@test.com", "hash", Role.ROLE_MERCHANT);
        merchantUser = userRepository.save(merchantUser);
        Wallet merchantWallet = new Wallet(merchantUser, BigDecimal.ZERO, "INR");
        merchantWallet = walletRepository.save(merchantWallet);

        Merchant merchant = new Merchant(merchantUser, merchantWallet, "Acme Store", "mock_key");
        merchant = merchantRepository.save(merchant);
        merchantId = merchant.getId();
    }

    @Test
    @DisplayName("Critical Security Test: 10 Concurrent Payment Requests cannot Double-Spend; Exactly 1 succeeds and Balance never becomes negative")
    void testConcurrentDoubleSpendingPrevention() throws InterruptedException {
        int threadCount = 10;
        ExecutorService executor = Executors.newFixedThreadPool(threadCount);
        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch finishLatch = new CountDownLatch(threadCount);

        AtomicInteger successCount = new AtomicInteger(0);
        AtomicInteger failureCount = new AtomicInteger(0);

        for (int i = 0; i < threadCount; i++) {
            final int index = i;
            executor.submit(() -> {
                try {
                    startLatch.await(); // Synchronize all threads to fire at the exact same instant
                    String idempotencyKey = "concurrent-key-" + UUID.randomUUID();
                    PaymentRequest req = new PaymentRequest(merchantId, BigDecimal.valueOf(100.00), "ORD-CONC-" + index, "INR");
                    PaymentResponse resp = paymentService.processPayment(idempotencyKey, req, "bob", "127.0.0.1");
                    if (resp.getStatus() == PaymentStatus.CONFIRMED) {
                        successCount.incrementAndGet();
                    }
                } catch (InsufficientFundsException | org.springframework.dao.DataAccessException e) {
                    failureCount.incrementAndGet();
                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    finishLatch.countDown();
                }
            });
        }

        startLatch.countDown(); // Fire all 10 threads
        boolean completed = finishLatch.await(15, TimeUnit.SECONDS);
        assertTrue(completed, "Concurrency stress test did not finish in allocated time window");

        executor.shutdown();

        // Assertions:
        // Because Bob only has $100.00, EXACTLY ONE payment of $100.00 must succeed!
        // The other 9 MUST fail with InsufficientFundsException.
        assertEquals(1, successCount.get(), "Double spending detected! More than 1 concurrent payment succeeded.");
        assertEquals(9, failureCount.get(), "Expected 9 concurrent attempts to fail due to insufficient funds.");

        // Verify database persistence guarantees:
        Wallet finalBobWallet = walletRepository.findById(senderWalletId).orElseThrow();
        assertEquals(0, finalBobWallet.getBalance().compareTo(BigDecimal.ZERO),
                "Sender balance was corrupted or went negative! Current balance: " + finalBobWallet.getBalance());

        Merchant merchant = merchantRepository.findById(merchantId).orElseThrow();
        Wallet finalMerchantWallet = walletRepository.findById(merchant.getWallet().getId()).orElseThrow();
        assertEquals(0, finalMerchantWallet.getBalance().compareTo(BigDecimal.valueOf(100.00)),
                "Merchant balance should have received exactly $100.00. Current balance: " + finalMerchantWallet.getBalance());
    }
}
