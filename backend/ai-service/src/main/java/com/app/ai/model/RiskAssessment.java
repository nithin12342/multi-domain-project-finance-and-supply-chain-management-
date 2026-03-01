package com.app.ai.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "risk_assessments")
public class RiskAssessment {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "supplier_id")
    private String supplierId;
    
    @Column(name = "risk_score")
    private Double riskScore;
    
    @Column(name = "risk_level")
    private String riskLevel; // LOW, MEDIUM, HIGH, CRITICAL
    
    @Column(name = "assessment_date")
    private LocalDateTime assessmentDate;
    
    @Column(name = "model_version")
    private String modelVersion;
    
    @Column(name = "confidence_level")
    private Double confidenceLevel;
    
    @Column(name = "factors", columnDefinition = "TEXT")
    private String factors; // JSON string of risk factors
    
    @Column(name = "recommendations", columnDefinition = "TEXT")
    private String recommendations; // JSON string of recommendations
    
    @Column(name = "created_at")
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