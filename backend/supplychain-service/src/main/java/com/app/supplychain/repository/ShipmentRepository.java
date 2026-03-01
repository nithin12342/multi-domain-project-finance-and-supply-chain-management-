package com.app.supplychain.repository;

import com.app.supplychain.model.Shipment;
import com.app.supplychain.model.ShipmentStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface ShipmentRepository extends JpaRepository<Shipment, Long> {
    List<Shipment> findByStatus(ShipmentStatus status, Pageable pageable);

    long countByStatusNotIn(List<ShipmentStatus> statuses);

    @org.springframework.data.jpa.repository.Query("SELECT s.status, COUNT(s) FROM Shipment s GROUP BY s.status")
    List<Object[]> countShipmentsByStatus();

    @org.springframework.data.jpa.repository.Query("SELECT COALESCE(SUM(si.quantity * si.unitPrice * 0.05), 0) FROM ShipmentItem si")
    java.math.BigDecimal calculateTotalShippingCosts();
}