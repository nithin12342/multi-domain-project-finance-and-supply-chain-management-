package com.app.ai.service;

import com.app.ai.model.DemandForecast;
import com.app.ai.model.FraudDetection;
import com.app.ai.model.RiskAssessment;
import com.app.ai.repository.DemandForecastRepository;
import com.app.ai.repository.FraudDetectionRepository;
import com.app.ai.repository.RiskAssessmentRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class AIService {

    private static final Logger logger = LoggerFactory.getLogger(AIService.class);

    @Autowired
    private DemandForecastRepository demandForecastRepository;

    @Autowired
    private FraudDetectionRepository fraudDetectionRepository;

    @Autowired
    private RiskAssessmentRepository riskAssessmentRepository;

    // Demand Forecast Methods
    public DemandForecast saveDemandForecast(DemandForecast forecast) {
        logger.info("Saving demand forecast for product: {}", forecast.getProductId());
        return demandForecastRepository.save(forecast);
    }

    public List<DemandForecast> getDemandForecastsByProductId(String productId) {
        logger.info("Fetching demand forecasts for product: {}", productId);
        return demandForecastRepository.findByProductId(productId);
    }

    public List<DemandForecast> getDemandForecastsByPeriod(String period) {
        logger.info("Fetching demand forecasts for period: {}", period);
        return demandForecastRepository.findByPeriodOrderByForecastDateDesc(period);
    }

    public Optional<DemandForecast> getDemandForecastById(Long id) {
        logger.info("Fetching demand forecast by ID: {}", id);
        return demandForecastRepository.findById(id);
    }

    // Fraud Detection Methods
    public FraudDetection saveFraudDetection(FraudDetection fraudDetection) {
        logger.info("Saving fraud detection for transaction: {}", fraudDetection.getTransactionId());
        return fraudDetectionRepository.save(fraudDetection);
    }

    public List<FraudDetection> getFraudDetectionsByTransactionId(String transactionId) {
        logger.info("Fetching fraud detections for transaction: {}", transactionId);
        return fraudDetectionRepository.findByTransactionId(transactionId);
    }

    public List<FraudDetection> getHighRiskFraudDetections() {
        logger.info("Fetching high risk fraud detections");
        return fraudDetectionRepository.findByIsFraudTrueOrderByRiskScoreDesc();
    }

    public Optional<FraudDetection> getFraudDetectionById(Long id) {
        logger.info("Fetching fraud detection by ID: {}", id);
        return fraudDetectionRepository.findById(id);
    }

    // Risk Assessment Methods
    public RiskAssessment saveRiskAssessment(RiskAssessment riskAssessment) {
        logger.info("Saving risk assessment for supplier: {}", riskAssessment.getSupplierId());
        return riskAssessmentRepository.save(riskAssessment);
    }

    public List<RiskAssessment> getRiskAssessmentsBySupplierId(String supplierId) {
        logger.info("Fetching risk assessments for supplier: {}", supplierId);
        return riskAssessmentRepository.findBySupplierId(supplierId);
    }

    public List<RiskAssessment> getRiskAssessmentsByRiskLevel(String riskLevel) {
        logger.info("Fetching risk assessments for risk level: {}", riskLevel);
        return riskAssessmentRepository.findByRiskLevelOrderByRiskScoreDesc(riskLevel);
    }

    public Optional<RiskAssessment> getRiskAssessmentById(Long id) {
        logger.info("Fetching risk assessment by ID: {}", id);
        return riskAssessmentRepository.findById(id);
    }

    // Analytics Methods
    public long getTotalDemandForecasts() {
        return demandForecastRepository.count();
    }

    public long getTotalFraudDetections() {
        return fraudDetectionRepository.count();
    }

    public long getTotalRiskAssessments() {
        return riskAssessmentRepository.count();
    }
}