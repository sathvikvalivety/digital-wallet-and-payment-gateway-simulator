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

@SpringBootApplication
public class DwpgSimulatorApplication {

    public static void main(String[] args) {
        SpringApplication.run(DwpgSimulatorApplication.class, args);
    }

    @Bean
    public CommandLineRunner dataInitializer(UserRepository userRepository,
                                             WalletRepository walletRepository,
                                             PasswordEncoder passwordEncoder) {
        return args -> {
            // Seed Admin User if not present
            if (!userRepository.existsByUsername("admin")) {
                User admin = new User(
                        "admin",
                        "admin@dwpg.simulator",
                        passwordEncoder.encode("Admin@Secure123!"),
                        Role.ROLE_ADMIN
                );
                userRepository.save(admin);
                Wallet adminWallet = new Wallet(admin, BigDecimal.valueOf(10000.00), "USD");
                walletRepository.save(adminWallet);
            }
        };
    }
}
