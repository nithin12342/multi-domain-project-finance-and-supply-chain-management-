package com.app.supplychain.service;

import com.app.supplychain.model.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;

@Service
public class NotificationService {

    private static final Logger logger = LoggerFactory.getLogger(NotificationService.class);

    @Autowired
    private JavaMailSender emailSender;

    public void sendLowStockAlert(Inventory inventory) {
        logger.info("Sending low stock alert for product: {}", inventory.getProductId());
        try {
            String subject = "Low Stock Alert: " + inventory.getProductId();
            String message = String.format(
                "Product %s at location %s has low stock. Current quantity: %d",
                inventory.getProductId(),
                inventory.getLocation(),
                inventory.getQuantity()
            );
            sendEmail("inventory.manager@company.com", subject, message);
            logger.info("Successfully sent low stock alert for product: {}", inventory.getProductId());
        } catch (Exception e) {
            logger.error("Failed to send low stock alert for product: {}", inventory.getProductId(), e);
            throw e;
        }
    }

    public void sendShipmentStatusUpdate(Shipment shipment) {
        logger.info("Sending shipment status update for shipment ID: {}", shipment.getId());
        try {
            String subject = "Shipment Status Update: " + shipment.getId();
            String message = String.format(
                "Shipment %s status has been updated to: %s",
                shipment.getId(),
                shipment.getStatus()
            );
            sendEmail("logistics.manager@company.com", subject, message);
            logger.info("Successfully sent shipment status update for shipment ID: {}", shipment.getId());
        } catch (Exception e) {
            logger.error("Failed to send shipment status update for shipment ID: {}", shipment.getId(), e);
            throw e;
        }
    }

    public void sendOrderConfirmation(Order order) {
        logger.info("Sending order confirmation for order ID: {}", order.getId());
        try {
            String subject = "Order Confirmation: " + order.getId();
            String message = String.format(
                "Order %s has been confirmed with supplier %s",
                order.getId(),
                order.getSupplier().getName()
            );
            sendEmail("orders.manager@company.com", subject, message);
            logger.info("Successfully sent order confirmation for order ID: {}", order.getId());
        } catch (Exception e) {
            logger.error("Failed to send order confirmation for order ID: {}", order.getId(), e);
            throw e;
        }
    }

    private void sendEmail(String to, String subject, String text) {
        logger.debug("Sending email to: {}, subject: {}", to, subject);
        try {
            SimpleMailMessage message = new SimpleMailMessage();
            message.setFrom("noreply@company.com");
            message.setTo(to);
            message.setSubject(subject);
            message.setText(text);
            emailSender.send(message);
            logger.debug("Successfully sent email to: {}", to);
        } catch (Exception e) {
            logger.error("Failed to send email to: {}", to, e);
            throw e;
        }
    }

    public void sendDeliveryConfirmation(Shipment shipment) {
        logger.info("Sending delivery confirmation for shipment ID: {}", shipment.getId());
        try {
            String subject = "Delivery Confirmation: " + shipment.getId();
            String message = String.format(
                "Shipment %s has been delivered to %s",
                shipment.getId(),
                shipment.getDestination()
            );
            sendEmail("logistics.manager@company.com", subject, message);
            logger.info("Successfully sent delivery confirmation for shipment ID: {}", shipment.getId());
        } catch (Exception e) {
            logger.error("Failed to send delivery confirmation for shipment ID: {}", shipment.getId(), e);
            throw e;
        }
    }

    public void sendInventoryUpdateNotification(Inventory inventory) {
        logger.info("Sending inventory update notification for product: {}", inventory.getProductId());
        try {
            String subject = "Inventory Update: " + inventory.getProductId();
            String message = String.format(
                "Inventory for product %s at location %s has been updated. New quantity: %d",
                inventory.getProductId(),
                inventory.getLocation(),
                inventory.getQuantity()
            );
            sendEmail("inventory.manager@company.com", subject, message);
            logger.info("Successfully sent inventory update notification for product: {}", inventory.getProductId());
        } catch (Exception e) {
            logger.error("Failed to send inventory update notification for product: {}", inventory.getProductId(), e);
            throw e;
        }
    }
}