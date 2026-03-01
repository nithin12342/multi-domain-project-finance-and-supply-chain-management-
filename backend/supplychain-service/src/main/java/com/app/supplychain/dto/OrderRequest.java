package com.app.supplychain.dto;

import com.app.supplychain.model.OrderItem;
import java.util.List;

public class OrderRequest {
    private String supplierId;
    private List<OrderItem> items;

    // Getters and Setters
    public String getSupplierId() {
        return supplierId;
    }

    public void setSupplierId(String supplierId) {
        this.supplierId = supplierId;
    }

    public List<OrderItem> getItems() {
        return items;
    }

    public void setItems(List<OrderItem> items) {
        this.items = items;
    }
}