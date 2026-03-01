package com.app.blockchain.service;

import lombok.Data;
import java.math.BigInteger;

@Data
public class ShipmentDetails {
    private BigInteger id;
    private String supplier;
    private String buyer;
    private String productId;
    private BigInteger quantity;
    private BigInteger timestamp;
    private String status;
    
    public ShipmentDetails() {}
    
    public ShipmentDetails(BigInteger id, String supplier, String buyer, String productId, 
                          BigInteger quantity, BigInteger timestamp, String status) {
        this.id = id;
        this.supplier = supplier;
        this.buyer = buyer;
        this.productId = productId;
        this.quantity = quantity;
        this.timestamp = timestamp;
        this.status = status;
    }
}