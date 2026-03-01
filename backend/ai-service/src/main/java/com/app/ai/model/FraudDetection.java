package com.app.ai.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "fraud_detections")
public class FraudDetection {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "transaction_id")
    private String transactionId;
    
    @Column(name = "risk_score")
    private Double riskScore;
    
    @Column(name = "is_fraud")
    private Boolean isFraud;
    
    @Column(name = "detection_date")
    private LocalDateTime detectionDate;
    
    @Column(name = "model_version")
    private String modelVersion;
    
    @Column(name = "confidence_level")
    private Double confidenceLevel;
    
    @Column(name = "details", columnDefinition = "TEXT")
    private String details;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    // Constructors
    public FraudDetection() {}
    
    public FraudDetection(String transactionId, Double riskScore, Boolean isFraud, 
                         LocalDateTime detectionDate, String modelVersion, Double confidenceLevel) {
        this.transactionId = transactionId;
        this.riskScore = riskScore;
        this.isFraud = isFraud;
        this.detectionDate = detectionDate;
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
    
    public String getTransactionId() {
        return transactionId;
    }
    
    public void setTransactionId(String transactionId) {
        this.transactionId = transactionId;
    }
    
    public Double getRiskScore() {
        return riskScore;
    }
    
    public void setRiskScore(Double riskScore) {
        this.riskScore = riskScore;
    }
    
    public Boolean getIsFraud() {
        return isFraud;
    }
    
    public void setIsFraud(Boolean isFraud) {
        this.isFraud = isFraud;
    }
    
    public LocalDateTime getDetectionDate() {
        return detectionDate;
    }
    
    public void setDetectionDate(LocalDateTime detectionDate) {
        this.detectionDate = detectionDate;
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
    
    public String getDetails() {
        return details;
    }
    
    public void setDetails(String details) {
        this.details = details;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}