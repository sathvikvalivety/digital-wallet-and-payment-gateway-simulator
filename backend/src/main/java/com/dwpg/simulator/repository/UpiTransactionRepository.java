package com.dwpg.simulator.repository;

import com.dwpg.simulator.entity.UpiTransaction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface UpiTransactionRepository extends JpaRepository<UpiTransaction, Long> {

    Optional<UpiTransaction> findByReferenceId(String referenceId);

    boolean existsByUtrNumber(String utrNumber);

    List<UpiTransaction> findByUserIdOrderByCreatedAtDesc(Long userId);
}
