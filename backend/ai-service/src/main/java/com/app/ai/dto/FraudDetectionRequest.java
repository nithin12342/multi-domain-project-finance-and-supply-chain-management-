package com.app.ai.dto;

import java.time.LocalDateTime;

public class FraudDetectionRequest {
    private String transactionId;
    private Double amount;
    private String supplierId;
    private String buyerId;
    private LocalDateTime transactionDate;
    
    // Constructors
    public FraudDetectionRequest() {}
    
    public FraudDetectionRequest(String transactionId, Double amount, String supplierId, 
                                String buyerId, LocalDateTime transactionDate) {
        this.transactionId = transactionId;
        this.amount = amount;
        this.supplierId = supplierId;
        this.buyerId = buyerId;
        this.transactionDate = transactionDate;
    }
    
    // Getters and Setters
    public String getTransactionId() {
        return transactionId;
    }
    
    public void setTransactionId(String transactionId) {
        this.transactionId = transactionId;
    }
    
    public Double getAmount() {
        return amount;
    }
    
    public void setAmount(Double amount) {
        this.amount = amount;
    }
    
    public String getSupplierId() {
        return supplierId;
    }
    
    public void setSupplierId(String supplierId) {
        this.supplierId = supplierId;
    }
    
    public String getBuyerId() {
        return buyerId;
    }
    
    public void setBuyerId(String buyerId) {
        this.buyerId = buyerId;
    }
    
    public LocalDateTime getTransactionDate() {
        return transactionDate;
    }
    
    public void setTransactionDate(LocalDateTime transactionDate) {
        this.transactionDate = transactionDate;
    }
}