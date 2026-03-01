package com.app.blockchain.service;

import lombok.Data;
import java.math.BigInteger;

@Data
public class InvoiceDetails {
    private BigInteger id;
    private String supplier;
    private String buyer;
    private BigInteger amount;
    private BigInteger dueDate;
    private Boolean isPaid;
    private Boolean isFinanced;
    private String financier;
    
    public InvoiceDetails() {}
    
    public InvoiceDetails(BigInteger id, String supplier, String buyer, BigInteger amount, 
                         BigInteger dueDate, Boolean isPaid, Boolean isFinanced, String financier) {
        this.id = id;
        this.supplier = supplier;
        this.buyer = buyer;
        this.amount = amount;
        this.dueDate = dueDate;
        this.isPaid = isPaid;
        this.isFinanced = isFinanced;
        this.financier = financier;
    }
}