package com.app.finance.dto;

import java.math.BigDecimal;

public class FinanceRequest {
    private BigDecimal amount;
    private String financier;

    // Constructors
    public FinanceRequest() {}

    public FinanceRequest(BigDecimal amount, String financier) {
        this.amount = amount;
        this.financier = financier;
    }

    // Getters and Setters
    public BigDecimal getAmount() {
        return amount;
    }

    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }

    public String getFinancier() {
        return financier;
    }

    public void setFinancier(String financier) {
        this.financier = financier;
    }
}