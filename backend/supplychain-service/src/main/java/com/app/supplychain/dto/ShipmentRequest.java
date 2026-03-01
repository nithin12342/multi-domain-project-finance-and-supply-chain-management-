package com.app.supplychain.dto;

import com.app.supplychain.model.ShipmentItem;
import java.util.List;

public class ShipmentRequest {
    private String origin;
    private String destination;
    private List<ShipmentItem> items;

    // Getters and Setters
    public String getOrigin() {
        return origin;
    }

    public void setOrigin(String origin) {
        this.origin = origin;
    }

    public String getDestination() {
        return destination;
    }

    public void setDestination(String destination) {
        this.destination = destination;
    }

    public List<ShipmentItem> getItems() {
        return items;
    }

    public void setItems(List<ShipmentItem> items) {
        this.items = items;
    }
}