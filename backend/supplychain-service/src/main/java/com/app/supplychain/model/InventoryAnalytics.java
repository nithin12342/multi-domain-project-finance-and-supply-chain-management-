package com.app.supplychain.model;

import java.math.BigDecimal;
import java.util.Map;

public class InventoryAnalytics {
    private BigDecimal totalInventoryValue;
    private double averageTurnoverRate;
    private int lowStockItemsCount;
    private Map<String, Integer> inventoryByCategory;

    // Getters and Setters
    public BigDecimal getTotalInventoryValue() {
        return totalInventoryValue;
    }

    public void setTotalInventoryValue(BigDecimal totalInventoryValue) {
        this.totalInventoryValue = totalInventoryValue;
    }

    public double getAverageTurnoverRate() {
        return averageTurnoverRate;
    }

    public void setAverageTurnoverRate(double averageTurnoverRate) {
        this.averageTurnoverRate = averageTurnoverRate;
    }

    public int getLowStockItemsCount() {
        return lowStockItemsCount;
    }

    public void setLowStockItemsCount(int lowStockItemsCount) {
        this.lowStockItemsCount = lowStockItemsCount;
    }

    public Map<String, Integer> getInventoryByCategory() {
        return inventoryByCategory;
    }

    public void setInventoryByCategory(Map<String, Integer> inventoryByCategory) {
        this.inventoryByCategory = inventoryByCategory;
    }
}