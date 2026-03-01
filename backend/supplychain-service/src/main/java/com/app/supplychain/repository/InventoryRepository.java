package com.app.supplychain.repository;

import com.app.supplychain.model.Inventory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface InventoryRepository extends JpaRepository<Inventory, Long> {
    List<Inventory> findByLocation(String location, Pageable pageable);

    @org.springframework.data.jpa.repository.Modifying
    @org.springframework.data.jpa.repository.Query("UPDATE Inventory i SET i.quantity = i.quantity - :amount WHERE i.id = :id AND i.quantity >= :amount")
    int deductInventory(@org.springframework.data.repository.query.Param("id") Long id,
            @org.springframework.data.repository.query.Param("amount") int amount);

    @org.springframework.data.jpa.repository.Query("SELECT SUM(i.quantity * i.unitPrice) FROM Inventory i")
    java.math.BigDecimal getTotalInventoryValue();
}
