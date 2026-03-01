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
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class ModelMonitoringService {
    
    private static final Logger logger = LoggerFactory.getLogger(ModelMonitoringService.class);
    
    @Autowired
    private DemandForecastRepository demandForecastRepository;
    
    @Autowired
    private FraudDetectionRepository fraudDetectionRepository;
    
    @Autowired
    private RiskAssessmentRepository riskAssessmentRepository;
    
    @Autowired
    private MLIntegrationService mlIntegrationService;
    
    // Thresholds for model performance monitoring
    private static final double DEMAND_FORECAST_ACCURACY_THRESHOLD = 0.8;
    private static final double FRAUD_DETECTION_ACCURACY_THRESHOLD = 0.9;
    private static final double RISK_ASSESSMENT_ACCURACY_THRESHOLD = 0.85;
    
    // Track model performance metrics
    private double demandForecastAccuracy = 1.0;
    private double fraudDetectionAccuracy = 1.0;
    private double riskAssessmentAccuracy = 1.0;
    
    /**
     * Scheduled task to monitor model performance daily
     */
    @Scheduled(cron = "0 0 2 * * ?") // Run daily at 2 AM
    public void monitorModelPerformance() {
        logger.info("Starting daily model performance monitoring");
        
        try {
            // Calculate accuracy metrics for each model type
            calculateDemandForecastAccuracy();
            calculateFraudDetectionAccuracy();
            calculateRiskAssessmentAccuracy();
            
            // Check if retraining is needed
            checkForRetraining();
            
            logger.info("Model performance monitoring completed");
        } catch (Exception e) {
            logger.error("Error during model performance monitoring", e);
        }
    }
    
    /**
     * Calculate accuracy of demand forecasting models
     */
    private void calculateDemandForecastAccuracy() {
        try {
            // Get recent forecasts (last 30 days)
            LocalDateTime thirtyDaysAgo = LocalDateTime.now().minusDays(30);
            List<DemandForecast> recentForecasts = demandForecastRepository.findByForecastDateAfterOrderByForecastDateDesc(thirtyDaysAgo);
            
            if (recentForecasts.isEmpty()) {
                logger.info("No recent demand forecasts found for accuracy calculation");
                return;
            }
            
            // In a real implementation, we would compare forecasts with actual demand
            // For now, we'll simulate the calculation
            int accurateForecasts = 0;
            int totalForecasts = recentForecasts.size();
            
            for (DemandForecast forecast : recentForecasts) {
                // Simulate accuracy check - in reality, we would compare with actual demand
                if (Math.random() > 0.2) { // 80% chance of being accurate
                    accurateForecasts++;
                }
            }
            
            demandForecastAccuracy = (double) accurateForecasts / totalForecasts;
            logger.info("Demand forecast accuracy: {}%", demandForecastAccuracy * 100);
            
        } catch (Exception e) {
            logger.error("Error calculating demand forecast accuracy", e);
        }
    }
    
    /**
     * Calculate accuracy of fraud detection models
     */
    private void calculateFraudDetectionAccuracy() {
        try {
            // Get recent fraud detections (last 30 days)
            LocalDateTime thirtyDaysAgo = LocalDateTime.now().minusDays(30);
            List<FraudDetection> recentDetections = fraudDetectionRepository.findByDetectionDateAfterOrderByDetectionDateDesc(thirtyDaysAgo);
            
            if (recentDetections.isEmpty()) {
                logger.info("No recent fraud detections found for accuracy calculation");
                return;
            }
            
            // In a real implementation, we would compare detections with actual fraud cases
            // For now, we'll simulate the calculation
            int accurateDetections = 0;
            int totalDetections = recentDetections.size();
            
            for (FraudDetection detection : recentDetections) {
                // Simulate accuracy check - in reality, we would verify if detected fraud was actual fraud
                if (Math.random() > 0.1) { // 90% chance of being accurate
                    accurateDetections++;
                }
            }
            
            fraudDetectionAccuracy = (double) accurateDetections / totalDetections;
            logger.info("Fraud detection accuracy: {}%", fraudDetectionAccuracy * 100);
            
        } catch (Exception e) {
            logger.error("Error calculating fraud detection accuracy", e);
        }
    }
    
    /**
     * Calculate accuracy of risk assessment models
     */
    private void calculateRiskAssessmentAccuracy() {
        try {
            // Get recent risk assessments (last 30 days)
            LocalDateTime thirtyDaysAgo = LocalDateTime.now().minusDays(30);
            List<RiskAssessment> recentAssessments = riskAssessmentRepository.findByAssessmentDateAfterOrderByAssessmentDateDesc(thirtyDaysAgo);
            
            if (recentAssessments.isEmpty()) {
                logger.info("No recent risk assessments found for accuracy calculation");
                return;
            }
            
            // In a real implementation, we would compare assessments with actual supplier performance
            // For now, we'll simulate the calculation
            int accurateAssessments = 0;
            int totalAssessments = recentAssessments.size();
            
            for (RiskAssessment assessment : recentAssessments) {
                // Simulate accuracy check - in reality, we would verify if risk assessments were accurate
                if (Math.random() > 0.15) { // 85% chance of being accurate
                    accurateAssessments++;
                }
            }
            
            riskAssessmentAccuracy = (double) accurateAssessments / totalAssessments;
            logger.info("Risk assessment accuracy: {}%", riskAssessmentAccuracy * 100);
            
        } catch (Exception e) {
            logger.error("Error calculating risk assessment accuracy", e);
        }
    }
    
    /**
     * Check if model retraining is needed based on performance metrics
     */
    private void checkForRetraining() {
        boolean retrainingNeeded = false;
        
        if (demandForecastAccuracy < DEMAND_FORECAST_ACCURACY_THRESHOLD) {
            logger.warn("Demand forecast accuracy below threshold: {}%", demandForecastAccuracy * 100);
            retrainingNeeded = true;
        }
        
        if (fraudDetectionAccuracy < FRAUD_DETECTION_ACCURACY_THRESHOLD) {
            logger.warn("Fraud detection accuracy below threshold: {}%", fraudDetectionAccuracy * 100);
            retrainingNeeded = true;
        }
        
        if (riskAssessmentAccuracy < RISK_ASSESSMENT_ACCURACY_THRESHOLD) {
            logger.warn("Risk assessment accuracy below threshold: {}%", riskAssessmentAccuracy * 100);
            retrainingNeeded = true;
        }
        
        if (retrainingNeeded) {
            logger.info("Model retraining triggered due to performance degradation");
            triggerModelRetraining();
        } else {
            logger.info("All models performing within acceptable thresholds");
        }
    }
    
    /**
     * Trigger model retraining process
     */
    private void triggerModelRetraining() {
        try {
            logger.info("Starting automated model retraining process");
            
            boolean success = mlIntegrationService.retrainModels();
            
            if (success) {
                logger.info("Automated model retraining completed successfully");
                // Reset accuracy metrics after successful retraining
                demandForecastAccuracy = 1.0;
                fraudDetectionAccuracy = 1.0;
                riskAssessmentAccuracy = 1.0;
            } else {
                logger.error("Automated model retraining failed");
            }
        } catch (Exception e) {
            logger.error("Error during automated model retraining", e);
        }
    }
    
    /**
     * Get current model performance metrics
     */
    public ModelPerformanceMetrics getModelPerformanceMetrics() {
        return new ModelPerformanceMetrics(
            demandForecastAccuracy,
            fraudDetectionAccuracy,
            riskAssessmentAccuracy,
            LocalDateTime.now()
        );
    }
    
    /**
     * Inner class to hold model performance metrics
     */
    public static class ModelPerformanceMetrics {
        private double demandForecastAccuracy;
        private double fraudDetectionAccuracy;
        private double riskAssessmentAccuracy;
        private LocalDateTime lastUpdated;
        
        public ModelPerformanceMetrics(double demandForecastAccuracy, double fraudDetectionAccuracy, 
                                     double riskAssessmentAccuracy, LocalDateTime lastUpdated) {
            this.demandForecastAccuracy = demandForecastAccuracy;
            this.fraudDetectionAccuracy = fraudDetectionAccuracy;
            this.riskAssessmentAccuracy = riskAssessmentAccuracy;
            this.lastUpdated = lastUpdated;
        }
        
        // Getters
        public double getDemandForecastAccuracy() { return demandForecastAccuracy; }
        public double getFraudDetectionAccuracy() { return fraudDetectionAccuracy; }
        public double getRiskAssessmentAccuracy() { return riskAssessmentAccuracy; }
        public LocalDateTime getLastUpdated() { return lastUpdated; }
    }
}