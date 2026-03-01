package com.app.supplychain.service;

import com.app.supplychain.dto.InventoryUpdateRequest;
import com.app.supplychain.dto.OrderRequest;
import com.app.supplychain.dto.ShipmentRequest;
import com.app.supplychain.exception.InsufficientInventoryException;
import com.app.supplychain.exception.ResourceNotFoundException;
import com.app.supplychain.exception.ValidationException;
import com.app.supplychain.model.*;
import com.app.supplychain.repository.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class SupplyService {

    private static final Logger logger = LoggerFactory.getLogger(SupplyService.class);

    @Autowired
    private InventoryRepository inventoryRepository;

    @Autowired
    private ShipmentRepository shipmentRepository;

    @Autowired
    private SupplierRepository supplierRepository;

    @Autowired
    private OrderRepository orderRepository;

    // Inventory CRUD Operations
    public List<Inventory> getInventory(String location, int page, int size) {
        logger.info("Fetching inventory with location: {}, page: {}, size: {}", location, page, size);
        if (location != null && !location.isEmpty()) {
            return inventoryRepository.findByLocation(location, PageRequest.of(page, size));
        }
        return inventoryRepository.findAll(PageRequest.of(page, size)).getContent();
    }

    public Inventory getInventoryById(Long id) {
        logger.info("Fetching inventory item by ID: {}", id);
        return inventoryRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Inventory item not found: " + id));
    }

    public Inventory createInventory(Inventory inventory) {
        logger.info("Creating new inventory item for product: {}", inventory.getProductId());
        if (inventory.getProductId() == null || inventory.getProductId().isEmpty()) {
            throw new ValidationException("Product ID is required");
        }

        Inventory saved = inventoryRepository.save(inventory);
        logger.info("Successfully created inventory item with ID: {}", saved.getId());
        return saved;
    }

    public Inventory updateInventory(Long id, Inventory inventory) {
        logger.info("Updating inventory item with ID: {}", id);
        Inventory existing = getInventoryById(id);
        existing.setProductId(inventory.getProductId());
        existing.setQuantity(inventory.getQuantity());
        existing.setLocation(inventory.getLocation());
        existing.setCategory(inventory.getCategory());
        existing.setUnitPrice(inventory.getUnitPrice());
        Inventory saved = inventoryRepository.save(existing);
        logger.info("Successfully updated inventory item with ID: {}", saved.getId());
        return saved;
    }

    public void deleteInventory(Long id) {
        logger.info("Deleting inventory item with ID: {}", id);
        if (!inventoryRepository.existsById(id)) {
            throw new ResourceNotFoundException("Inventory item not found: " + id);
        }
        inventoryRepository.deleteById(id);
        logger.info("Successfully deleted inventory item with ID: {}", id);
    }

    public List<Inventory> getLowStockItems() {
        logger.info("Fetching low stock inventory items");
        return inventoryRepository.findAll().stream()
                .filter(item -> item.getQuantity() < 10)
                .collect(Collectors.toList());
    }

    // Shipment CRUD Operations
    @Transactional
    public Shipment createShipment(ShipmentRequest request) {
        logger.info("Creating new shipment from {} to {}", request.getOrigin(), request.getDestination());

        // Create shipment record
        Shipment shipment = new Shipment();
        shipment.setOrigin(request.getOrigin());
        shipment.setDestination(request.getDestination());
        shipment.setItems(request.getItems());
        shipment.setStatus(ShipmentStatus.CREATED);

        // Atomically update inventory to prevent race conditions
        for (ShipmentItem item : request.getItems()) {
            int updatedRows = inventoryRepository.deductInventory(item.getId(), item.getQuantity());
            if (updatedRows == 0) {
                throw new InsufficientInventoryException("Insufficient inventory for item: " + item.getId());
            }
        }

        Shipment saved = shipmentRepository.save(shipment);
        logger.info("Successfully created shipment with ID: {}", saved.getId());
        return saved;
    }

    public List<Shipment> getShipments(String status, int page, int size) {
        logger.info("Fetching shipments with status: {}, page: {}, size: {}", status, page, size);
        if (status != null && !status.isEmpty()) {
            return shipmentRepository.findByStatus(ShipmentStatus.valueOf(status.toUpperCase()),
                    PageRequest.of(page, size));
        }
        return shipmentRepository.findAll(PageRequest.of(page, size)).getContent();
    }

    public Shipment getShipmentById(Long id) {
        logger.info("Fetching shipment by ID: {}", id);
        return shipmentRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Shipment not found: " + id));
    }

    public Shipment updateShipment(Long id, Shipment shipment) {
        logger.info("Updating shipment with ID: {}", id);
        Shipment existing = getShipmentById(id);
        existing.setOrigin(shipment.getOrigin());
        existing.setDestination(shipment.getDestination());
        existing.setStatus(shipment.getStatus());
        Shipment saved = shipmentRepository.save(existing);
        logger.info("Successfully updated shipment with ID: {}", saved.getId());
        return saved;
    }

    public void deleteShipment(Long id) {
        logger.info("Deleting shipment with ID: {}", id);
        if (!shipmentRepository.existsById(id)) {
            throw new ResourceNotFoundException("Shipment not found: " + id);
        }
        shipmentRepository.deleteById(id);
        logger.info("Successfully deleted shipment with ID: {}", id);
    }

    public ShipmentTracking getShipmentTracking(Long id) {
        logger.info("Fetching tracking info for shipment ID: {}", id);
        Shipment shipment = shipmentRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Shipment not found: " + id));
        return buildTrackingInfo(shipment);
    }

    // Supplier CRUD Operations
    public List<Supplier> getActiveSuppliers() {
        logger.info("Fetching active suppliers");
        return supplierRepository.findByStatus(SupplierStatus.ACTIVE);
    }

    public Supplier getSupplierById(Long id) {
        logger.info("Fetching supplier by ID: {}", id);
        return supplierRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Supplier not found: " + id));
    }

    public Supplier createSupplier(Supplier supplier) {
        logger.info("Creating new supplier: {}", supplier.getName());
        if (supplier.getName() == null || supplier.getName().isEmpty()) {
            throw new ValidationException("Supplier name is required");
        }

        Supplier saved = supplierRepository.save(supplier);
        logger.info("Successfully created supplier with ID: {}", saved.getId());
        return saved;
    }

    public Supplier updateSupplier(Long id, Supplier supplier) {
        logger.info("Updating supplier with ID: {}", id);
        Supplier existing = getSupplierById(id);
        existing.setName(supplier.getName());
        existing.setEmail(supplier.getEmail());
        existing.setPhone(supplier.getPhone());
        existing.setAddress(supplier.getAddress());
        existing.setStatus(supplier.getStatus());
        Supplier saved = supplierRepository.save(existing);
        logger.info("Successfully updated supplier with ID: {}", saved.getId());
        return saved;
    }

    public void deleteSupplier(Long id) {
        logger.info("Deleting supplier with ID: {}", id);
        if (!supplierRepository.existsById(id)) {
            throw new ResourceNotFoundException("Supplier not found: " + id);
        }
        supplierRepository.deleteById(id);
        logger.info("Successfully deleted supplier with ID: {}", id);
    }

    // Order CRUD Operations
    @Transactional
    public Order createOrder(OrderRequest request) {
        logger.info("Creating new order for supplier ID: {}", request.getSupplierId());

        // Validate supplier
        Supplier supplier = supplierRepository.findById(Long.valueOf(request.getSupplierId()))
                .orElseThrow(() -> new ResourceNotFoundException("Supplier not found: " + request.getSupplierId()));

        // Create order
        Order order = new Order();
        order.setSupplier(supplier);
        order.setItems(request.getItems());
        order.setStatus(OrderStatus.PENDING);
        order.setTotalAmount(calculateOrderAmount(request.getItems()));

        Order saved = orderRepository.save(order);
        logger.info("Successfully created order with ID: {}", saved.getId());
        return saved;
    }

    public List<Order> getOrders(String status, int page, int size) {
        logger.info("Fetching orders with status: {}, page: {}, size: {}", status, page, size);
        if (status != null && !status.isEmpty()) {
            return orderRepository.findByStatus(OrderStatus.valueOf(status.toUpperCase()),
                    PageRequest.of(page, size));
        }
        return orderRepository.findAll(PageRequest.of(page, size)).getContent();
    }

    public Order getOrderById(Long id) {
        logger.info("Fetching order by ID: {}", id);
        return orderRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Order not found: " + id));
    }

    // Analytics
    public InventoryAnalytics getInventoryAnalytics() {
        logger.info("Generating inventory analytics");

        InventoryAnalytics analytics = new InventoryAnalytics();

        // Calculate total inventory value using DB aggregation (Performance Fix)
        BigDecimal totalValue = inventoryRepository.getTotalInventoryValue();
        analytics.setTotalInventoryValue(totalValue != null ? totalValue : BigDecimal.ZERO);

        // Note: Other metrics still use in-memory calculation for now as they are
        // complex
        // In production, these should also be moved to DB queries
        List<Inventory> allInventory = inventoryRepository.findAll();

        // Calculate average inventory turnover
        double avgTurnover = allInventory.stream()
                .mapToDouble(Inventory::getTurnoverRate)
                .average()
                .orElse(0.0);
        analytics.setAverageTurnoverRate(avgTurnover);

        // Count low stock items (less than 10 units)
        long lowStockCount = allInventory.stream()
                .filter(item -> item.getQuantity() < 10)
                .count();
        analytics.setLowStockItemsCount((int) lowStockCount);

        // Calculate inventory by category
        Map<String, Integer> inventoryByCategory = allInventory.stream()
                .collect(Collectors.groupingBy(
                        item -> item.getCategory() != null ? item.getCategory() : "Uncategorized",
                        Collectors.summingInt(Inventory::getQuantity)));
        analytics.setInventoryByCategory(inventoryByCategory);

        return analytics;
    }

    // Private helper methods

    private ShipmentTracking buildTrackingInfo(Shipment shipment) {
        logger.debug("Building tracking info for shipment ID: {}", shipment.getId());
        ShipmentTracking tracking = new ShipmentTracking();
        tracking.setShipmentId(shipment.getId());
        tracking.setStatus(shipment.getStatus());
        tracking.setOrigin(shipment.getOrigin());
        tracking.setDestination(shipment.getDestination());
        tracking.setCreatedAt(shipment.getCreatedAt());
        tracking.setUpdatedAt(shipment.getUpdatedAt());

        // Add tracking events based on shipment status history
        tracking.setEvents(generateTrackingEvents(shipment));

        return tracking;
    }

    private List<TrackingEvent> generateTrackingEvents(Shipment shipment) {
        // Fix: Use real tracking events. For now, we only show creation.
        // Future: Fetch from TrackingEventRepository
        return List.of(
                new TrackingEvent("Shipment Created", shipment.getCreatedAt(), "Order has been created"));
    }

    private BigDecimal calculateOrderAmount(List<OrderItem> items) {
        return items.stream()
                .map(item -> item.getUnitPrice() != null
                        ? item.getUnitPrice().multiply(BigDecimal.valueOf(item.getQuantity()))
                        : BigDecimal.ZERO)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}