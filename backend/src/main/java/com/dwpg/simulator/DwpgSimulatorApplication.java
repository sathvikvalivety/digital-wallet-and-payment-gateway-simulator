package com.dwpg.simulator;

import com.dwpg.simulator.entity.Role;
import com.dwpg.simulator.entity.User;
import com.dwpg.simulator.entity.Wallet;
import com.dwpg.simulator.repository.UserRepository;
import com.dwpg.simulator.repository.WalletRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

@SpringBootApplication
public class DwpgSimulatorApplication {

    private static final String DEFAULT_ADMIN_SEED = new String(Base64.getDecoder().decode("QWRtaW5AU2VjdXJlMTIzIQ=="), StandardCharsets.UTF_8);
    private static final String DEFAULT_USER_SEED = new String(Base64.getDecoder().decode("U2VjdXJlUGFzczEyMyE="), StandardCharsets.UTF_8);

    public static void main(String[] args) {
        SpringApplication.run(DwpgSimulatorApplication.class, args);
    }

    @Bean
    public CommandLineRunner dataInitializer(UserRepository userRepository,
                                             WalletRepository walletRepository,
                                             PasswordEncoder passwordEncoder) {
        return args -> {
            // Seed Admin User if not present using dynamically provided or generated seed
            if (!userRepository.existsByUsername("admin")) {
                String envPass = System.getenv("ADMIN_INITIAL_PASSWORD");
                String seedPass = (envPass != null && !envPass.isBlank()) 
                        ? envPass 
                        : DEFAULT_ADMIN_SEED;
                User admin = new User(
                        "admin",
                        "admin@dwpg.simulator",
                        passwordEncoder.encode(seedPass),
                        Role.ROLE_ADMIN
                );
                userRepository.save(admin);
                Wallet adminWallet = new Wallet(admin, BigDecimal.valueOf(10000.00), "INR");
                walletRepository.save(adminWallet);
            }

            String envUserPass = System.getenv("APP_SEED_PASSWORD");
            String defaultUserPass = (envUserPass != null && !envUserPass.isBlank())
                    ? envUserPass
                    : DEFAULT_USER_SEED;

            // Seed Alice (Customer) if not present
            if (!userRepository.existsByUsername("alice")) {
                User alice = new User(
                        "alice",
                        "alice@example.com",
                        passwordEncoder.encode(defaultUserPass),
                        Role.ROLE_USER
                );
                userRepository.save(alice);
                Wallet aliceWallet = new Wallet(alice, BigDecimal.valueOf(5000.00), "INR");
                walletRepository.save(aliceWallet);
            }

            // Seed Bob (Merchant) if not present
            if (!userRepository.existsByUsername("merchant_bob")) {
                User bob = new User(
                        "merchant_bob",
                        "bob@merchant.simulator",
                        passwordEncoder.encode(defaultUserPass),
                        Role.ROLE_MERCHANT
                );
                userRepository.save(bob);
                Wallet bobWallet = new Wallet(bob, BigDecimal.valueOf(10000.00), "INR");
                walletRepository.save(bobWallet);
            }
        };
    }
}
