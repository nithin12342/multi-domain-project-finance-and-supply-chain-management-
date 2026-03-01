package com.app.blockchain.controller;

import com.app.blockchain.service.BlockchainService;
import com.app.blockchain.service.InvoiceDetails;
import com.app.blockchain.service.ShipmentDetails;
import com.app.common.dto.ApiResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.math.BigInteger;

@RestController
@RequestMapping("/api/blockchain")
public class BlockchainController {

    @Autowired
    private BlockchainService blockchainService;

    @PostMapping("/invoice")
    public ApiResponse<String> createInvoice(
            @RequestParam String supplier,
            @RequestParam String buyer,
            @RequestParam BigInteger amount,
            @RequestParam BigInteger dueDate) {
        try {
            String transactionHash = blockchainService.createInvoice(supplier, buyer, amount, dueDate);
            return new ApiResponse<>(transactionHash, "Invoice created successfully");
        } catch (Exception e) {
            return new ApiResponse<>(null, "Failed to create invoice: " + e.getMessage());
        }
    }

    @PostMapping("/invoice/{id}/finance")
    public ApiResponse<String> financeInvoice(
            @PathVariable BigInteger id,
            @RequestParam BigInteger amount) {
        try {
            String transactionHash = blockchainService.financeInvoice(id, amount);
            return new ApiResponse<>(transactionHash, "Invoice financed successfully");
        } catch (Exception e) {
            return new ApiResponse<>(null, "Failed to finance invoice: " + e.getMessage());
        }
    }

    @PostMapping("/shipment")
    public ApiResponse<String> createShipment(
            @RequestParam String supplier,
            @RequestParam String buyer,
            @RequestParam String productId,
            @RequestParam BigInteger quantity) {
        try {
            String transactionHash = blockchainService.createShipment(supplier, buyer, productId, quantity);
            return new ApiResponse<>(transactionHash, "Shipment created successfully");
        } catch (Exception e) {
            return new ApiResponse<>(null, "Failed to create shipment: " + e.getMessage());
        }
    }

    @PutMapping("/shipment/{id}/status")
    public ApiResponse<String> updateShipmentStatus(
            @PathVariable BigInteger id,
            @RequestParam String status) {
        try {
            String transactionHash = blockchainService.updateShipmentStatus(id, status);
            return new ApiResponse<>(transactionHash, "Shipment status updated successfully");
        } catch (Exception e) {
            return new ApiResponse<>(null, "Failed to update shipment status: " + e.getMessage());
        }
    }

    @GetMapping("/invoice/{id}")
    public ApiResponse<InvoiceDetails> getInvoice(@PathVariable BigInteger id) {
        try {
            InvoiceDetails invoice = blockchainService.getInvoice(id);
            return new ApiResponse<>(invoice, "Invoice retrieved successfully");
        } catch (Exception e) {
            return new ApiResponse<>(null, "Failed to retrieve invoice: " + e.getMessage());
        }
    }

    @GetMapping("/shipment/{id}")
    public ApiResponse<ShipmentDetails> getShipment(@PathVariable BigInteger id) {
        try {
            ShipmentDetails shipment = blockchainService.getShipment(id);
            return new ApiResponse<>(shipment, "Shipment retrieved successfully");
        } catch (Exception e) {
            return new ApiResponse<>(null, "Failed to retrieve shipment: " + e.getMessage());
        }
    }
}