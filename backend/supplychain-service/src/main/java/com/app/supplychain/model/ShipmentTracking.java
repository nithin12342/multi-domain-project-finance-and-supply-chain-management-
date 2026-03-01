package com.app.supplychain.model;

import java.time.LocalDateTime;
import java.util.List;

public class ShipmentTracking {
    private Long shipmentId;
    private ShipmentStatus status;
    private String origin;
    private String destination;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private List<TrackingEvent> events;

    // Getters and Setters
    public Long getShipmentId() {
        return shipmentId;
    }

    public void setShipmentId(Long shipmentId) {
        this.shipmentId = shipmentId;
    }

    public ShipmentStatus getStatus() {
        return status;
    }

    public void setStatus(ShipmentStatus status) {
        this.status = status;
    }

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

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }

    public List<TrackingEvent> getEvents() {
        return events;
    }

    public void setEvents(List<TrackingEvent> events) {
        this.events = events;
    }
}