package com.dwpg.simulator.repository;

import com.dwpg.simulator.entity.Merchant;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface MerchantRepository extends JpaRepository<Merchant, Long> {
    Optional<Merchant> findByUserId(Long userId);
    Optional<Merchant> findByApiKeyHash(String apiKeyHash);
    boolean existsByUserId(Long userId);
}
