package com.dwpg.simulator.repository;

import com.dwpg.simulator.entity.Refund;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface RefundRepository extends JpaRepository<Refund, Long> {
    Optional<Refund> findByPaymentId(Long paymentId);
    boolean existsByPaymentId(Long paymentId);
    List<Refund> findByMerchantIdOrderByCreatedAtDesc(Long merchantId);
}
