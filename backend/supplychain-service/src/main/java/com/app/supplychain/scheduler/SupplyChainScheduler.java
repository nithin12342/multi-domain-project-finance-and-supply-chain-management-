package com.app.supplychain.scheduler;

import com.app.supplychain.service.AnalyticsService;
import com.app.supplychain.service.SupplyService;
import com.app.supplychain.service.NotificationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class SupplyChainScheduler {

    @Autowired
    private AnalyticsService analyticsService;

    @Autowired
    private SupplyService supplyService;

    @Autowired
    private NotificationService notificationService;

    @Scheduled(cron = "0 0 * * * *") // Every hour
    public void checkLowStockItems() {
        supplyService.getLowStockItems().forEach(item -> notificationService.sendLowStockAlert(item));
    }

    @Scheduled(cron = "0 0 0 * * *") // Every day at midnight
    public void generateDailyAnalytics() {
        analyticsService.getSupplyChainMetrics();
    }

    @Scheduled(cron = "0 */15 * * * *") // Every 15 minutes
    public void updateShipmentStatus() {
        // Implementation to update shipment status
    }

    @Scheduled(cron = "0 0 1 * * *") // Every day at 1 AM
    public void generateFinancialMetrics() {
        analyticsService.getFinancialMetrics();
    }

    @Scheduled(cron = "0 0 2 * * *") // Every day at 2 AM
    public void cleanupOldRecords() {
        // Implementation to clean up old records
    }
}
