package com.dwpg.simulator.service;

import com.dwpg.simulator.dto.AuthRequest;
import com.dwpg.simulator.dto.AuthResponse;
import com.dwpg.simulator.dto.RegisterRequest;
import com.dwpg.simulator.entity.Role;
import com.dwpg.simulator.entity.User;
import com.dwpg.simulator.entity.Wallet;
import com.dwpg.simulator.exception.UnauthorizedAccessException;
import com.dwpg.simulator.repository.UserRepository;
import com.dwpg.simulator.repository.WalletRepository;
import com.dwpg.simulator.security.JwtTokenProvider;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.math.BigDecimal;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private WalletRepository walletRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private JwtTokenProvider jwtTokenProvider;

    @Mock
    private AuditService auditService;

    @InjectMocks
    private AuthService authService;

    private User sampleUser;
    private Wallet sampleWallet;

    @BeforeEach
    void setUp() {
        sampleUser = new User("alice", "alice@test.com", "hashed_pwd_123", Role.ROLE_USER);
        sampleUser.setId(1L);
        sampleWallet = new Wallet(sampleUser, BigDecimal.ZERO, "INR");
        sampleWallet.setId(10L);
    }

    @Test
    @DisplayName("Unit Test: Successful User Registration provisions User and Wallet")
    void testRegisterSuccess() {
        RegisterRequest req = new RegisterRequest("alice", "alice@test.com", "Password123!", "USER");

        when(userRepository.existsByUsername("alice")).thenReturn(false);
        when(userRepository.existsByEmail("alice@test.com")).thenReturn(false);
        when(passwordEncoder.encode("Password123!")).thenReturn("hashed_pwd_123");
        when(userRepository.save(any(User.class))).thenReturn(sampleUser);
        when(walletRepository.save(any(Wallet.class))).thenReturn(sampleWallet);
        when(jwtTokenProvider.generateToken("alice", "ROLE_USER")).thenReturn("mock.jwt.token");

        AuthResponse resp = authService.register(req, "127.0.0.1");

        assertNotNull(resp);
        assertEquals("alice", resp.getUsername());
        assertEquals("ROLE_USER", resp.getRole());
        assertEquals("mock.jwt.token", resp.getToken());
        verify(walletRepository, times(1)).save(any(Wallet.class));
    }

    @Test
    @DisplayName("Unit Test: Registration rejects duplicate username")
    void testRegisterDuplicateUsername() {
        RegisterRequest req = new RegisterRequest("alice", "alice@test.com", "Password123!", "USER");
        when(userRepository.existsByUsername("alice")).thenReturn(true);

        assertThrows(IllegalArgumentException.class, () -> authService.register(req, "127.0.0.1"));
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    @DisplayName("Unit Test: Login fails with invalid password and masks details")
    void testLoginInvalidPassword() {
        AuthRequest req = new AuthRequest("alice", "WrongPassword!");
        when(userRepository.findByUsername("alice")).thenReturn(Optional.of(sampleUser));
        when(passwordEncoder.matches("WrongPassword!", "hashed_pwd_123")).thenReturn(false);

        UnauthorizedAccessException ex = assertThrows(UnauthorizedAccessException.class,
                () -> authService.login(req, "127.0.0.1"));

        assertEquals("Invalid username or password", ex.getMessage());
        verify(jwtTokenProvider, never()).generateToken(anyString(), anyString());
    }
}
