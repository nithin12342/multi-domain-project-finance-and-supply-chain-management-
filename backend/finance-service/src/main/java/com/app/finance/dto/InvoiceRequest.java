package com.app.finance.dto;

import java.math.BigDecimal;
import java.time.LocalDate;

public class InvoiceRequest {
    private String supplier;
    private String buyer;
    private BigDecimal amount;
    private LocalDate dueDate;

    // Constructors
    public InvoiceRequest() {}

    public InvoiceRequest(String supplier, String buyer, BigDecimal amount, LocalDate dueDate) {
        this.supplier = supplier;
        this.buyer = buyer;
        this.amount = amount;
        this.dueDate = dueDate;
    }

    // Getters and Setters
    public String getSupplier() {
        return supplier;
    }

    public void setSupplier(String supplier) {
        this.supplier = supplier;
    }

    public String getBuyer() {
        return buyer;
    }

    public void setBuyer(String buyer) {
        this.buyer = buyer;
    }

    public BigDecimal getAmount() {
        return amount;
    }

    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }

    public LocalDate getDueDate() {
        return dueDate;
    }

    public void setDueDate(LocalDate dueDate) {
        this.dueDate = dueDate;
    }
}