package com.app.supplychain.controller;

import com.app.supplychain.model.*;
import com.app.supplychain.service.SupplyService;
import com.app.supplychain.service.AnalyticsService;
import com.app.supplychain.dto.ShipmentRequest;
import com.app.supplychain.dto.OrderRequest;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.math.BigDecimal;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/supply")
@Tag(name = "Supply Chain", description = "Supply Chain Management API")
public class SupplyController {

        @Autowired
        private SupplyService supplyService;

        @Autowired
        private AnalyticsService analyticsService;

        // Inventory CRUD Operations
        @GetMapping("/inventory")
        @Operation(summary = "Get inventory items", description = "Retrieve a list of inventory items with optional filtering by location")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Successfully retrieved inventory items", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid request parameters")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<List<Inventory>>> getInventory(
                        @Parameter(description = "Location to filter inventory items") @RequestParam(required = false) String location,
                        @Parameter(description = "Page number (0-based)") @RequestParam(defaultValue = "0") int page,
                        @Parameter(description = "Number of items per page") @RequestParam(defaultValue = "10") int size) {
                List<Inventory> inventory = supplyService.getInventory(location, page, size);
                return ResponseEntity
                                .ok(new com.app.supplychain.dto.ApiResponse<>(inventory,
                                                "Inventory retrieved successfully"));
        }

        @GetMapping("/inventory/{id}")
        @Operation(summary = "Get inventory item by ID", description = "Retrieve a specific inventory item by its ID")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Successfully retrieved inventory item", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "404", description = "Inventory item not found")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Inventory>> getInventoryById(
                        @Parameter(description = "Inventory item ID") @PathVariable Long id) {
                Inventory inventory = supplyService.getInventoryById(id);
                return ResponseEntity
                                .ok(new com.app.supplychain.dto.ApiResponse<>(inventory,
                                                "Inventory item retrieved successfully"));
        }

        @PostMapping("/inventory")
        @Operation(summary = "Create inventory item", description = "Create a new inventory item")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Inventory item created successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid inventory data provided")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Inventory>> createInventory(
                        @Parameter(description = "Inventory item to create") @RequestBody Inventory inventory) {
                // Validate inventory data
                if (inventory.getProductId() == null || inventory.getProductId().isEmpty()) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null,
                                                        "Product ID is required"));
                }

                if (inventory.getUnitPrice() == null
                                || inventory.getUnitPrice().compareTo(java.math.BigDecimal.ZERO) <= 0) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null,
                                                        "Valid price is required"));
                }

                Inventory createdInventory = supplyService.createInventory(inventory);
                return ResponseEntity
                                .ok(new com.app.supplychain.dto.ApiResponse<>(createdInventory,
                                                "Inventory item created successfully"));
        }

        @PutMapping("/inventory/{id}")
        @Operation(summary = "Update inventory item", description = "Update an existing inventory item by ID")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Inventory item updated successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid inventory data or ID mismatch"),
                        @ApiResponse(responseCode = "404", description = "Inventory item not found")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Inventory>> updateInventory(
                        @Parameter(description = "Inventory item ID") @PathVariable Long id,
                        @Parameter(description = "Updated inventory item data") @RequestBody Inventory inventory) {
                try {
                        Inventory updatedInventory = supplyService.updateInventory(id, inventory);
                        return ResponseEntity.ok(
                                        new com.app.supplychain.dto.ApiResponse<>(updatedInventory,
                                                        "Inventory item updated successfully"));
                } catch (RuntimeException e) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null, e.getMessage()));
                }
        }

        @DeleteMapping("/inventory/{id}")
        @Operation(summary = "Delete inventory item", description = "Delete an inventory item by ID")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Inventory item deleted successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid inventory item ID"),
                        @ApiResponse(responseCode = "404", description = "Inventory item not found")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Void>> deleteInventory(
                        @Parameter(description = "Inventory item ID") @PathVariable Long id) {
                try {
                        // SECURITY: Check if user has admin role
                        // TODO: String currentUserRole =
                        // SecurityContextHolder.getContext().getAuthentication().getAuthorities()...
                        // if (!"ROLE_ADMIN".equals(currentUserRole)) throw new
                        // AccessDeniedException("Only admins can delete inventory");

                        supplyService.deleteInventory(id);
                        return ResponseEntity
                                        .ok(new com.app.supplychain.dto.ApiResponse<>(null,
                                                        "Inventory item deleted successfully"));
                } catch (RuntimeException e) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null, e.getMessage()));
                }
        }

        // Shipment CRUD Operations
        @PostMapping("/shipments")
        @Operation(summary = "Create shipment", description = "Create a new shipment")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Shipment created successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid shipment data provided")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Shipment>> createShipment(
                        @Parameter(description = "Shipment request data") @RequestBody ShipmentRequest request) {
                // Validate shipment request
                if (request.getOrigin() == null || request.getOrigin().isEmpty()) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null, "Origin is required"));
                }

                if (request.getDestination() == null || request.getDestination().isEmpty()) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null,
                                                        "Destination is required"));
                }

                if (request.getItems() == null || request.getItems().isEmpty()) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null,
                                                        "Shipment items are required"));
                }

                Shipment shipment = supplyService.createShipment(request);
                return ResponseEntity.ok(
                                new com.app.supplychain.dto.ApiResponse<>(shipment, "Shipment created successfully"));
        }

        @GetMapping("/shipments")
        @Operation(summary = "Get shipments", description = "Retrieve a list of shipments with optional filtering by status")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Successfully retrieved shipments", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid request parameters")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<List<Shipment>>> getShipments(
                        @Parameter(description = "Status to filter shipments") @RequestParam(required = false) String status,
                        @Parameter(description = "Page number (0-based)") @RequestParam(defaultValue = "0") int page,
                        @Parameter(description = "Number of items per page") @RequestParam(defaultValue = "10") int size) {
                List<Shipment> shipments = supplyService.getShipments(status, page, size);
                return ResponseEntity
                                .ok(new com.app.supplychain.dto.ApiResponse<>(shipments,
                                                "Shipments retrieved successfully"));
        }

        @GetMapping("/shipments/{id}")
        @Operation(summary = "Get shipment by ID", description = "Retrieve a specific shipment by its ID")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Successfully retrieved shipment", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "404", description = "Shipment not found")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Shipment>> getShipmentById(
                        @Parameter(description = "Shipment ID") @PathVariable Long id) {
                Shipment shipment = supplyService.getShipmentById(id);

                // SECURITY: Check if user owns this shipment or is admin
                // TODO: Long currentUserId = SecurityUtils.getCurrentUserId();
                // if (!shipment.getOwnerId().equals(currentUserId) && !isAdmin) throw new
                // AccessDeniedException(...);

                return ResponseEntity
                                .ok(new com.app.supplychain.dto.ApiResponse<>(shipment,
                                                "Shipment retrieved successfully"));
        }

        @PutMapping("/shipments/{id}")
        @Operation(summary = "Update shipment", description = "Update an existing shipment by ID")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Shipment updated successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid shipment data or ID mismatch"),
                        @ApiResponse(responseCode = "404", description = "Shipment not found")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Shipment>> updateShipment(
                        @Parameter(description = "Shipment ID") @PathVariable Long id,
                        @Parameter(description = "Updated shipment data") @RequestBody Shipment shipment) {
                try {
                        Shipment updatedShipment = supplyService.updateShipment(id, shipment);
                        return ResponseEntity
                                        .ok(new com.app.supplychain.dto.ApiResponse<>(updatedShipment,
                                                        "Shipment updated successfully"));
                } catch (RuntimeException e) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null, e.getMessage()));
                }
        }

        @DeleteMapping("/shipments/{id}")
        @Operation(summary = "Delete shipment", description = "Delete a shipment by ID")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Shipment deleted successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid shipment ID"),
                        @ApiResponse(responseCode = "404", description = "Shipment not found")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Void>> deleteShipment(
                        @Parameter(description = "Shipment ID") @PathVariable Long id) {
                try {
                        supplyService.deleteShipment(id);
                        return ResponseEntity.ok(new com.app.supplychain.dto.ApiResponse<>(null,
                                        "Shipment deleted successfully"));
                } catch (RuntimeException e) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null, e.getMessage()));
                }
        }

        @GetMapping("/shipments/{id}/track")
        @Operation(summary = "Track shipment", description = "Get tracking information for a specific shipment")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Successfully retrieved tracking information", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "404", description = "Shipment not found")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<ShipmentTracking>> trackShipment(
                        @Parameter(description = "Shipment ID") @PathVariable Long id) {
                ShipmentTracking tracking = supplyService.getShipmentTracking(id);
                return ResponseEntity
                                .ok(new com.app.supplychain.dto.ApiResponse<>(tracking,
                                                "Tracking info retrieved successfully"));
        }

        // Supplier CRUD Operations
        @GetMapping("/suppliers")
        @Operation(summary = "Get suppliers", description = "Retrieve a list of all active suppliers")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Successfully retrieved suppliers", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class)))
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<List<Supplier>>> getSuppliers() {
                List<Supplier> suppliers = supplyService.getActiveSuppliers();
                return ResponseEntity
                                .ok(new com.app.supplychain.dto.ApiResponse<>(suppliers,
                                                "Suppliers retrieved successfully"));
        }

        @GetMapping("/suppliers/{id}")
        @Operation(summary = "Get supplier by ID", description = "Retrieve a specific supplier by its ID")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Successfully retrieved supplier", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "404", description = "Supplier not found")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Supplier>> getSupplierById(
                        @Parameter(description = "Supplier ID") @PathVariable Long id) {
                Supplier supplier = supplyService.getSupplierById(id);
                return ResponseEntity
                                .ok(new com.app.supplychain.dto.ApiResponse<>(supplier,
                                                "Supplier retrieved successfully"));
        }

        @PostMapping("/suppliers")
        @Operation(summary = "Create supplier", description = "Create a new supplier")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Supplier created successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid supplier data provided")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Supplier>> createSupplier(
                        @Parameter(description = "Supplier data to create") @RequestBody Supplier supplier) {
                // Validate supplier data
                if (supplier.getName() == null || supplier.getName().isEmpty()) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null,
                                                        "Supplier name is required"));
                }

                if (supplier.getEmail() == null || supplier.getEmail().isEmpty()) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null,
                                                        "Supplier email is required"));
                }

                Supplier createdSupplier = supplyService.createSupplier(supplier);
                return ResponseEntity
                                .ok(new com.app.supplychain.dto.ApiResponse<>(createdSupplier,
                                                "Supplier created successfully"));
        }

        @PutMapping("/suppliers/{id}")
        @Operation(summary = "Update supplier", description = "Update an existing supplier by ID")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Supplier updated successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid supplier data or ID mismatch"),
                        @ApiResponse(responseCode = "404", description = "Supplier not found")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Supplier>> updateSupplier(
                        @Parameter(description = "Supplier ID") @PathVariable Long id,
                        @Parameter(description = "Updated supplier data") @RequestBody Supplier supplier) {
                try {
                        Supplier updatedSupplier = supplyService.updateSupplier(id, supplier);
                        return ResponseEntity
                                        .ok(new com.app.supplychain.dto.ApiResponse<>(updatedSupplier,
                                                        "Supplier updated successfully"));
                } catch (RuntimeException e) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null, e.getMessage()));
                }
        }

        @DeleteMapping("/suppliers/{id}")
        @Operation(summary = "Delete supplier", description = "Delete a supplier by ID")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Supplier deleted successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid supplier ID"),
                        @ApiResponse(responseCode = "404", description = "Supplier not found")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Void>> deleteSupplier(
                        @Parameter(description = "Supplier ID") @PathVariable Long id) {
                try {
                        supplyService.deleteSupplier(id);
                        return ResponseEntity.ok(new com.app.supplychain.dto.ApiResponse<>(null,
                                        "Supplier deleted successfully"));
                } catch (RuntimeException e) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null, e.getMessage()));
                }
        }

        // Analytics
        @GetMapping("/analytics/inventory")
        @Operation(summary = "Get inventory analytics", description = "Retrieve inventory analytics data")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Successfully retrieved analytics", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class)))
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<InventoryAnalytics>> getInventoryAnalytics() {
                InventoryAnalytics analytics = supplyService.getInventoryAnalytics();
                return ResponseEntity
                                .ok(new com.app.supplychain.dto.ApiResponse<>(analytics,
                                                "Analytics retrieved successfully"));
        }

        // Enhanced Analytics Endpoints
        @GetMapping("/analytics/metrics")
        @Operation(summary = "Get supply chain metrics", description = "Retrieve comprehensive supply chain metrics including AI-enhanced analytics")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Successfully retrieved metrics", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "500", description = "Internal server error")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Map<String, Object>>> getSupplyChainMetrics() {
                try {
                        Map<String, Object> metrics = analyticsService.getSupplyChainMetrics();
                        return ResponseEntity.ok(
                                        new com.app.supplychain.dto.ApiResponse<>(metrics,
                                                        "Supply chain metrics retrieved successfully"));
                } catch (Exception e) {
                        return ResponseEntity.internalServerError()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null,
                                                        "Error retrieving supply chain metrics: " + e.getMessage()));
                }
        }

        @GetMapping("/analytics/financial")
        @Operation(summary = "Get financial metrics", description = "Retrieve financial metrics for the supply chain")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Successfully retrieved financial metrics", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "500", description = "Internal server error")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Map<String, BigDecimal>>> getFinancialMetrics() {
                try {
                        Map<String, BigDecimal> metrics = analyticsService.getFinancialMetrics();
                        return ResponseEntity
                                        .ok(new com.app.supplychain.dto.ApiResponse<>(metrics,
                                                        "Financial metrics retrieved successfully"));
                } catch (Exception e) {
                        return ResponseEntity.internalServerError()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null,
                                                        "Error retrieving financial metrics: " + e.getMessage()));
                }
        }

        @GetMapping("/analytics/demand-forecast/{productId}")
        @Operation(summary = "Get demand forecast", description = "Retrieve AI-generated demand forecast for a product")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Successfully retrieved demand forecast", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid product ID"),
                        @ApiResponse(responseCode = "500", description = "Internal server error")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<DemandForecast>> getDemandForecast(
                        @Parameter(description = "Product ID") @PathVariable String productId,
                        @Parameter(description = "Forecast period (DAILY, WEEKLY, MONTHLY)") @RequestParam(defaultValue = "WEEKLY") String period) {
                try {
                        DemandForecast forecast = analyticsService.getDemandForecast(productId, period);
                        return ResponseEntity
                                        .ok(new com.app.supplychain.dto.ApiResponse<>(forecast,
                                                        "Demand forecast retrieved successfully"));
                } catch (Exception e) {
                        return ResponseEntity.internalServerError()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null,
                                                        "Error retrieving demand forecast: " + e.getMessage()));
                }
        }

        @GetMapping("/analytics/risk-assessment/supplier/{supplierId}")
        @Operation(summary = "Get supplier risk assessment", description = "Retrieve AI-generated risk assessment for a supplier")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Successfully retrieved risk assessment", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid supplier ID"),
                        @ApiResponse(responseCode = "500", description = "Internal server error")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<RiskAssessment>> getSupplierRiskAssessment(
                        @Parameter(description = "Supplier ID") @PathVariable String supplierId) {
                try {
                        RiskAssessment riskAssessment = analyticsService.getSupplierRiskAssessment(supplierId);
                        return ResponseEntity.ok(new com.app.supplychain.dto.ApiResponse<>(riskAssessment,
                                        "Risk assessment retrieved successfully"));
                } catch (Exception e) {
                        return ResponseEntity.internalServerError()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null,
                                                        "Error retrieving risk assessment: " + e.getMessage()));
                }
        }

        // Orders
        @PostMapping("/orders")
        @Operation(summary = "Create order", description = "Create a new order")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Order created successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid order data provided")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Order>> createOrder(
                        @Parameter(description = "Order request data") @RequestBody OrderRequest request) {
                // Validate order request
                if (request.getSupplierId() == null || request.getSupplierId().isEmpty()) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null,
                                                        "Supplier ID is required"));
                }

                if (request.getItems() == null || request.getItems().isEmpty()) {
                        return ResponseEntity.badRequest()
                                        .body(new com.app.supplychain.dto.ApiResponse<>(null,
                                                        "Order items are required"));
                }

                // VALIDATION: Check for negative quantities or invalid prices
                for (com.app.supplychain.model.OrderItem item : request.getItems()) {
                        if (item.getQuantity() <= 0) {
                                return ResponseEntity.badRequest()
                                                .body(new com.app.supplychain.dto.ApiResponse<>(null,
                                                                "Item quantity must be positive"));
                        }
                        if (item.getUnitPrice() != null
                                        && item.getUnitPrice().compareTo(java.math.BigDecimal.ZERO) < 0) {
                                return ResponseEntity.badRequest()
                                                .body(new com.app.supplychain.dto.ApiResponse<>(null,
                                                                "Item price cannot be negative"));
                        }
                }

                Order order = supplyService.createOrder(request);
                return ResponseEntity
                                .ok(new com.app.supplychain.dto.ApiResponse<>(order, "Order created successfully"));
        }

        @GetMapping("/orders")
        @Operation(summary = "Get orders", description = "Retrieve a list of orders with optional filtering by status")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Successfully retrieved orders", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "400", description = "Invalid request parameters")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<List<Order>>> getOrders(
                        @Parameter(description = "Status to filter orders") @RequestParam(required = false) String status,
                        @Parameter(description = "Page number (0-based)") @RequestParam(defaultValue = "0") int page,
                        @Parameter(description = "Number of items per page") @RequestParam(defaultValue = "10") int size) {
                List<Order> orders = supplyService.getOrders(status, page, size);
                return ResponseEntity
                                .ok(new com.app.supplychain.dto.ApiResponse<>(orders, "Orders retrieved successfully"));
        }

        @GetMapping("/orders/{id}")
        @Operation(summary = "Get order by ID", description = "Retrieve a specific order by its ID")
        @ApiResponses(value = {
                        @ApiResponse(responseCode = "200", description = "Successfully retrieved order", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.supplychain.dto.ApiResponse.class))),
                        @ApiResponse(responseCode = "404", description = "Order not found")
        })
        public ResponseEntity<com.app.supplychain.dto.ApiResponse<Order>> getOrderById(
                        @Parameter(description = "Order ID") @PathVariable Long id) {
                Order order = supplyService.getOrderById(id);
                return ResponseEntity
                                .ok(new com.app.supplychain.dto.ApiResponse<>(order, "Order retrieved successfully"));
        }
}