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
}