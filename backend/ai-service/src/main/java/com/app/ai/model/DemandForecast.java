package com.app.ai.model;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "demand_forecasts")
public class DemandForecast {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "product_id")
    private String productId;
    
    @Column(name = "predicted_demand")
    private Integer predictedDemand;
    
    @Column(name = "confidence_level")
    private Double confidenceLevel;
    
    @Column(name = "forecast_date")
    private LocalDateTime forecastDate;
    
    @Column(name = "period")
    private String period; // DAILY, WEEKLY, MONTHLY
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    // Constructors
    public DemandForecast() {}
    
    public DemandForecast(String productId, Integer predictedDemand, Double confidenceLevel, 
                         LocalDateTime forecastDate, String period) {
        this.productId = productId;
        this.predictedDemand = predictedDemand;
        this.confidenceLevel = confidenceLevel;
        this.forecastDate = forecastDate;
        this.period = period;
        this.createdAt = LocalDateTime.now();
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