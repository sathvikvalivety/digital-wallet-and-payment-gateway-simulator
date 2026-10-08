package com.dwpg.simulator.repository;

import com.dwpg.simulator.entity.CheckoutSession;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CheckoutSessionRepository extends JpaRepository<CheckoutSession, Long> {
    Optional<CheckoutSession> findBySessionId(String sessionId);
    List<CheckoutSession> findByMerchantIdOrderByCreatedAtDesc(Long merchantId);
}
