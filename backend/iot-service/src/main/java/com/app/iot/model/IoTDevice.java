package com.app.iot.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "iot_devices")
public class IoTDevice {
    @Id
    private String id;
    private String name;
    private String type;
    private String location;
    private String status;
    private long lastUpdated;
    private String firmware;
    private String config;

    // Getters and Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getType() { return type; }
    public void setType(String type) { this.type = type; }

    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public long getLastUpdated() { return lastUpdated; }
    public void setLastUpdated(long lastUpdated) { this.lastUpdated = lastUpdated; }

    public String getFirmware() { return firmware; }
    public void setFirmware(String firmware) { this.firmware = firmware; }

    public String getConfig() { return config; }
    public void setConfig(String config) { this.config = config; }
}
