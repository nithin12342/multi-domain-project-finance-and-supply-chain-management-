package com.app.supplychain.model;

import java.time.LocalDateTime;

public class TrackingEvent {
    private String status;
    private LocalDateTime timestamp;
    private String description;

    public TrackingEvent() {
    }

    public TrackingEvent(String status, LocalDateTime timestamp, String description) {
        this.status = status;
        this.timestamp = timestamp;
        this.description = description;
    }

    // Getters and Setters
    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}