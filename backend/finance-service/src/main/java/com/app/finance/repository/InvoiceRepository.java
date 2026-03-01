package com.app.finance.repository;

import com.app.finance.model.Invoice;
import com.app.finance.model.InvoiceStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.util.List;

@Repository
public interface InvoiceRepository extends JpaRepository<Invoice, Long> {
    Page<Invoice> findByStatus(InvoiceStatus status, Pageable pageable);
    long countByStatus(InvoiceStatus status);
    
    @Query("SELECT AVG(i.financingAmount) FROM Invoice i WHERE i.financingAmount IS NOT NULL")
    BigDecimal getAverageFinancingAmount();
    
    @Query("SELECT COUNT(i) as count, MONTH(i.dueDate) as month FROM Invoice i WHERE i.dueDate IS NOT NULL GROUP BY MONTH(i.dueDate)")
    List<Object[]> getMonthlyVolume();
}