package com.app.supplychain.model;

import java.time.LocalDateTime;

public class RiskAssessment {
    private Long id;
    private String supplierId;
    private Double riskScore;
    private String riskLevel; // LOW, MEDIUM, HIGH, CRITICAL
    private LocalDateTime assessmentDate;
    private String modelVersion;
    private Double confidenceLevel;
    private String factors; // JSON string of risk factors
    private String recommendations; // JSON string of recommendations
    private LocalDateTime createdAt;
    
    // Constructors
    public RiskAssessment() {}
    
    public RiskAssessment(String supplierId, Double riskScore, String riskLevel, 
                         LocalDateTime assessmentDate, String modelVersion, Double confidenceLevel) {
        this.supplierId = supplierId;
        this.riskScore = riskScore;
        this.riskLevel = riskLevel;
        this.assessmentDate = assessmentDate;
        this.modelVersion = modelVersion;
        this.confidenceLevel = confidenceLevel;
        this.createdAt = LocalDateTime.now();
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getSupplierId() {
        return supplierId;
    }
    
    public void setSupplierId(String supplierId) {
        this.supplierId = supplierId;
    }
    
    public Double getRiskScore() {
        return riskScore;
    }
    
    public void setRiskScore(Double riskScore) {
        this.riskScore = riskScore;
    }
    
    public String getRiskLevel() {
        return riskLevel;
    }
    
    public void setRiskLevel(String riskLevel) {
        this.riskLevel = riskLevel;
    }
    
    public LocalDateTime getAssessmentDate() {
        return assessmentDate;
    }
    
    public void setAssessmentDate(LocalDateTime assessmentDate) {
        this.assessmentDate = assessmentDate;
    }
    
    public String getModelVersion() {
        return modelVersion;
    }
    
    public void setModelVersion(String modelVersion) {
        this.modelVersion = modelVersion;
    }
    
    public Double getConfidenceLevel() {
        return confidenceLevel;
    }
    
    public void setConfidenceLevel(Double confidenceLevel) {
        this.confidenceLevel = confidenceLevel;
    }
    
    public String getFactors() {
        return factors;
    }
    
    public void setFactors(String factors) {
        this.factors = factors;
    }
    
    public String getRecommendations() {
        return recommendations;
    }
    
    public void setRecommendations(String recommendations) {
        this.recommendations = recommendations;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}