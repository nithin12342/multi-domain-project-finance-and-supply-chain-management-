package com.app.ai.repository;

import com.app.ai.model.FraudDetection;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface FraudDetectionRepository extends JpaRepository<FraudDetection, Long> {
    List<FraudDetection> findByTransactionId(String transactionId);
    List<FraudDetection> findByDetectionDateBetween(LocalDateTime startDate, LocalDateTime endDate);
    List<FraudDetection> findByIsFraudTrueOrderByRiskScoreDesc();
    List<FraudDetection> findByRiskScoreGreaterThan(Double riskScore);
    List<FraudDetection> findByDetectionDateAfterOrderByDetectionDateDesc(LocalDateTime date);
}