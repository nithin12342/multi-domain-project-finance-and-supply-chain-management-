package com.app.supplychain.repository;

import com.app.supplychain.model.Supplier;
import com.app.supplychain.model.SupplierStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface SupplierRepository extends JpaRepository<Supplier, Long> {
    List<Supplier> findByStatus(SupplierStatus status);
}