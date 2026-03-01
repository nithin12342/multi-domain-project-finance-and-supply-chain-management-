package com.app.finance.model;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDate;

@Entity
@Table(name = "invoices")
public class Invoice {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String supplier;
    private String buyer;
    private BigDecimal amount;
    private LocalDate dueDate;

    @Enumerated(EnumType.STRING)
    private InvoiceStatus status;

    private BigDecimal financingAmount;
    private String financier;
    private boolean isFinanced;

    // Constructors
    public Invoice() {
    }

    public Invoice(String supplier, String buyer, BigDecimal amount, LocalDate dueDate) {
        this.supplier = supplier;
        this.buyer = buyer;
        this.amount = amount;
        this.dueDate = dueDate;
        this.status = InvoiceStatus.PENDING;
        this.isFinanced = false;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

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

    public InvoiceStatus getStatus() {
        return status;
    }

    public void setStatus(InvoiceStatus status) {
        this.status = status;
    }

    public BigDecimal getFinancingAmount() {
        return financingAmount;
    }

    public void setFinancingAmount(BigDecimal financingAmount) {
        this.financingAmount = financingAmount;
    }

    public String getFinancier() {
        return financier;
    }

    public void setFinancier(String financier) {
        this.financier = financier;
    }

    @Version
    private Long version;

    public boolean isFinanced() {
        return isFinanced;
    }

    public void setFinanced(boolean financed) {
        isFinanced = financed;
    }

    public Long getVersion() {
        return version;
    }
}