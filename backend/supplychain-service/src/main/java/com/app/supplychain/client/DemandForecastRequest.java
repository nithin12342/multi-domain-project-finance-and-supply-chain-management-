package com.app.supplychain.client;

import java.time.LocalDateTime;

public class DemandForecastRequest {
    private String productId;
    private LocalDateTime startDate;
    private LocalDateTime endDate;
    private String period; // DAILY, WEEKLY, MONTHLY
    
    // Constructors
    public DemandForecastRequest() {}
    
    public DemandForecastRequest(String productId, LocalDateTime startDate, LocalDateTime endDate, String period) {
        this.productId = productId;
        this.startDate = startDate;
        this.endDate = endDate;
        this.period = period;
    }
    
    // Getters and Setters
    public String getProductId() {
        return productId;
    }
    
    public void setProductId(String productId) {
        this.productId = productId;
    }
    
    public LocalDateTime getStartDate() {
        return startDate;
    }
    
    public void setStartDate(LocalDateTime startDate) {
        this.startDate = startDate;
    }
    
    public LocalDateTime getEndDate() {
        return endDate;
    }
    
    public void setEndDate(LocalDateTime endDate) {
        this.endDate = endDate;
    }
    
    public String getPeriod() {
        return period;
    }
    
    public void setPeriod(String period) {
        this.period = period;
    }
}