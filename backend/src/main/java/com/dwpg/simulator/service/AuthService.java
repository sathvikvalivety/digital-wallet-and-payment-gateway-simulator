package com.dwpg.simulator.service;

import com.dwpg.simulator.dto.AuthRequest;
import com.dwpg.simulator.dto.AuthResponse;
import com.dwpg.simulator.dto.RegisterRequest;
import com.dwpg.simulator.entity.AuditEventType;
import com.dwpg.simulator.entity.Role;
import com.dwpg.simulator.entity.User;
import com.dwpg.simulator.entity.Wallet;
import com.dwpg.simulator.exception.UnauthorizedAccessException;
import com.dwpg.simulator.repository.UserRepository;
import com.dwpg.simulator.repository.WalletRepository;
import com.dwpg.simulator.security.JwtTokenProvider;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final WalletRepository walletRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;
    private final AuditService auditService;

    public AuthService(UserRepository userRepository,
                       WalletRepository walletRepository,
                       PasswordEncoder passwordEncoder,
                       JwtTokenProvider jwtTokenProvider,
                       AuditService auditService) {
        this.userRepository = userRepository;
        this.walletRepository = walletRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtTokenProvider = jwtTokenProvider;
        this.auditService = auditService;
    }

    @Transactional
    public AuthResponse register(RegisterRequest request, String clientIp) {
        if (userRepository.existsByUsername(request.getUsername())) {
            throw new IllegalArgumentException("Username is already taken");
        }
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new IllegalArgumentException("Email is already registered");
        }

        Role role = Role.ROLE_USER;
        if (request.getRole() != null) {
            String roleStr = request.getRole().trim().toUpperCase();
            if (roleStr.contains("MERCHANT")) {
                role = Role.ROLE_MERCHANT;
            } else if (roleStr.contains("ADMIN")) {
                role = Role.ROLE_ADMIN;
            }
        }

        String hashedPassword = passwordEncoder.encode(request.getPassword());
        User user = new User(request.getUsername(), request.getEmail(), hashedPassword, role);
        user = userRepository.save(user);

        // Automatically provision digital wallet with zero balance
        Wallet wallet = new Wallet(user, BigDecimal.ZERO, "USD");
        wallet = walletRepository.save(wallet);

        auditService.logEvent(AuditEventType.WALLET_CREATED, wallet.getId(), user.getUsername(), "SUCCESS",
                "User registered and digital wallet provisioned.", clientIp);

        String token = jwtTokenProvider.generateToken(user.getUsername(), user.getRole().name());
        return new AuthResponse(token, user.getUsername(), user.getRole().name(), user.getId(), wallet.getId());
    }

    @Transactional
    public AuthResponse login(AuthRequest request, String clientIp) {
        User user = userRepository.findByUsername(request.getUsername()).orElse(null);

        if (user == null || !passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
            auditService.logEvent(AuditEventType.LOGIN_FAILURE, null, request.getUsername(), "FAILED",
                    "Invalid login credentials provided.", clientIp);
            throw new UnauthorizedAccessException("Invalid username or password");
        }

        Wallet wallet = walletRepository.findByUserId(user.getId()).orElse(null);
        Long walletId = wallet != null ? wallet.getId() : null;

        auditService.logEvent(AuditEventType.LOGIN_SUCCESS, user.getId(), user.getUsername(), "SUCCESS",
                "User authenticated successfully.", clientIp);

        String token = jwtTokenProvider.generateToken(user.getUsername(), user.getRole().name());
        return new AuthResponse(token, user.getUsername(), user.getRole().name(), user.getId(), walletId);
    }
}
