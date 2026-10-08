package com.dwpg.simulator.service;

import com.dwpg.simulator.dto.FundRequest;
import com.dwpg.simulator.dto.WalletResponse;
import com.dwpg.simulator.entity.Role;
import com.dwpg.simulator.entity.User;
import com.dwpg.simulator.entity.Wallet;
import com.dwpg.simulator.exception.InsufficientFundsException;
import com.dwpg.simulator.exception.InvalidAmountException;
import com.dwpg.simulator.exception.UnauthorizedAccessException;
import com.dwpg.simulator.repository.TransactionRepository;
import com.dwpg.simulator.repository.UserRepository;
import com.dwpg.simulator.repository.WalletRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class WalletServiceTest {

    @Mock
    private WalletRepository walletRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private TransactionRepository transactionRepository;

    @Mock
    private AuditService auditService;

    @InjectMocks
    private WalletService walletService;

    private User alice;
    private Wallet aliceWallet;

    @BeforeEach
    void setUp() {
        alice = new User("alice", "alice@test.com", "hash", Role.ROLE_USER);
        alice.setId(1L);
        aliceWallet = new Wallet(alice, BigDecimal.valueOf(100.00), "USD");
        aliceWallet.setId(10L);
    }

    @Test
    @DisplayName("Unit Test: Domain Invariant - Debit reduces balance and rejects overdraft")
    void testWalletDomainDebit() {
        aliceWallet.debit(BigDecimal.valueOf(40.00));
        assertEquals(BigDecimal.valueOf(60.00), aliceWallet.getBalance());

        // Overdraft attempt must throw InsufficientFundsException
        assertThrows(InsufficientFundsException.class, () -> aliceWallet.debit(BigDecimal.valueOf(70.00)));
    }

    @Test
    @DisplayName("Unit Test: BOLA Check - Querying another user's wallet is rejected")
    void testGetWalletByIdForeignUserAccessDenied() {
        when(walletRepository.findById(10L)).thenReturn(Optional.of(aliceWallet));

        // 'mallory' tries to access Alice's wallet
        assertThrows(UnauthorizedAccessException.class, () -> walletService.getWalletById(10L, "mallory"));
    }

    @Test
    @DisplayName("Unit Test: Funding wallet requires strictly positive amount")
    void testFundWalletNegativeAmount() {
        FundRequest req = new FundRequest(BigDecimal.valueOf(-50.00));
        assertThrows(InvalidAmountException.class, () -> walletService.fundWallet(10L, req, "alice", "127.0.0.1"));
    }
}
