package com.app.finance.service;

import com.app.finance.model.InvoiceStatus;
import com.app.finance.model.RiskAssessment;
import com.app.finance.repository.InvoiceRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class RiskAssessmentService {

    private static final Logger logger = LoggerFactory.getLogger(RiskAssessmentService.class);

    private static final double MINIMUM_ACCEPTABLE_SCORE = 70.0;

    @Autowired
    private InvoiceRepository invoiceRepository;

    public RiskAssessment assessRisk(String supplierId) {
        logger.info("Assessing risk for supplier: {}", supplierId);
        try {
            long totalInvoices = invoiceRepository.countBySupplier(supplierId);

            // If new supplier, base score is mid-range
            if (totalInvoices == 0) {
                RiskAssessment risk = new RiskAssessment();
                risk.setSupplierId(supplierId);
                risk.setScore(50.0);
                risk.setAssessmentDetails("New supplier: No historical invoice data available.");
                return risk;
            }

            long overdueInvoices = invoiceRepository.countBySupplierAndStatus(supplierId, InvoiceStatus.OVERDUE);
            long paidInvoices = invoiceRepository.countBySupplierAndStatus(supplierId, InvoiceStatus.PAID);

            // Base score is 50.0
            double score = 50.0;

            // Add 5 points for every successfully paid invoice
            score += paidInvoices * 5.0;
            // Subtract 15 points for every overdue/defaulted invoice
            score -= overdueInvoices * 15.0;

            // Ensure score stays within bounds (0-100)
            score = Math.max(0.0, Math.min(100.0, score));

            RiskAssessment risk = new RiskAssessment();
            risk.setSupplierId(supplierId);
            risk.setScore(score);
            risk.setAssessmentDetails("Score based on " + totalInvoices + " total invoices (" + paidInvoices + " paid, "
                    + overdueInvoices + " overdue).");

            logger.info("Risk assessment completed for supplier: {} with score: {}", supplierId, score);
            return risk;
        } catch (Exception e) {
            logger.error("Error assessing risk for supplier: {}", supplierId, e);
            throw e;
        }
    }

    public double getMinimumAcceptableScore() {
        return MINIMUM_ACCEPTABLE_SCORE;
    }
}