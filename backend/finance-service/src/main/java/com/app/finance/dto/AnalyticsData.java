package com.app.finance.dto;

import java.math.BigDecimal;
import java.util.Map;

public class AnalyticsData {
    private long totalInvoices;
    private long totalFinanced;
    private BigDecimal averageFinancingAmount;
    private Map<String, Object> monthlyVolume;

    // Constructors
    public AnalyticsData() {}

    // Getters and Setters
    public long getTotalInvoices() {
        return totalInvoices;
    }

    public void setTotalInvoices(long totalInvoices) {
        this.totalInvoices = totalInvoices;
    }

    public long getTotalFinanced() {
        return totalFinanced;
    }

    public void setTotalFinanced(long totalFinanced) {
        this.totalFinanced = totalFinanced;
    }

    public BigDecimal getAverageFinancingAmount() {
        return averageFinancingAmount;
    }

    public void setAverageFinancingAmount(BigDecimal averageFinancingAmount) {
        this.averageFinancingAmount = averageFinancingAmount;
    }

    public Map<String, Object> getMonthlyVolume() {
        return monthlyVolume;
    }

    public void setMonthlyVolume(Map<String, Object> monthlyVolume) {
        this.monthlyVolume = monthlyVolume;
    }
}