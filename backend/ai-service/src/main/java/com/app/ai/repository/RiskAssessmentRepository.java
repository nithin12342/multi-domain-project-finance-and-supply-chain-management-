package com.app.ai.repository;

import com.app.ai.model.RiskAssessment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface RiskAssessmentRepository extends JpaRepository<RiskAssessment, Long> {
    List<RiskAssessment> findBySupplierId(String supplierId);
    List<RiskAssessment> findBySupplierIdAndAssessmentDateBetween(String supplierId, LocalDateTime startDate, LocalDateTime endDate);
    List<RiskAssessment> findByRiskLevelOrderByRiskScoreDesc(String riskLevel);
    List<RiskAssessment> findByAssessmentDateAfter(LocalDateTime date);
    List<RiskAssessment> findByAssessmentDateAfterOrderByAssessmentDateDesc(LocalDateTime date);
}