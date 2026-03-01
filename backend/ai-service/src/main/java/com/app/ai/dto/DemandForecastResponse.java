package com.app.ai.dto;

import java.time.LocalDateTime;

public class DemandForecastResponse {
    private Long id;
    private String productId;
    private Integer predictedDemand;
    private Double confidenceLevel;
    private LocalDateTime forecastDate;
    private String period;
    private LocalDateTime createdAt;
    
    // Constructors
    public DemandForecastResponse() {}
    
    public DemandForecastResponse(Long id, String productId, Integer predictedDemand, 
                                 Double confidenceLevel, LocalDateTime forecastDate, 
                                 String period, LocalDateTime createdAt) {
        this.id = id;
        this.productId = productId;
        this.predictedDemand = predictedDemand;
        this.confidenceLevel = confidenceLevel;
        this.forecastDate = forecastDate;
        this.period = period;
        this.createdAt = createdAt;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getProductId() {
        return productId;
    }
    
    public void setProductId(String productId) {
        this.productId = productId;
    }
    
    public Integer getPredictedDemand() {
        return predictedDemand;
    }
    
    public void setPredictedDemand(Integer predictedDemand) {
        this.predictedDemand = predictedDemand;
    }
    
    public Double getConfidenceLevel() {
        return confidenceLevel;
    }
    
    public void setConfidenceLevel(Double confidenceLevel) {
        this.confidenceLevel = confidenceLevel;
    }
    
    public LocalDateTime getForecastDate() {
        return forecastDate;
    }
    
    public void setForecastDate(LocalDateTime forecastDate) {
        this.forecastDate = forecastDate;
    }
    
    public String getPeriod() {
        return period;
    }
    
    public void setPeriod(String period) {
        this.period = period;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}