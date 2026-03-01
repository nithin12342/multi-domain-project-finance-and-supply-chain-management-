package com.app.finance.service;

import com.app.finance.model.Invoice;
import com.app.finance.model.InvoiceStatus;
import com.app.finance.model.RiskAssessment;
import com.app.finance.dto.AnalyticsData;
import com.app.finance.dto.FinanceRequest;
import com.app.finance.dto.InvoiceRequest;
import com.app.finance.repository.InvoiceRepository;
import com.app.finance.exception.InvoiceNotFoundException;
import com.app.finance.exception.InvalidOperationException;
import com.app.finance.exception.RiskTooHighException;
import com.app.finance.exception.InvalidRequestException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.time.LocalDate;

@Service
public class FinanceService {

    private static final Logger logger = LoggerFactory.getLogger(FinanceService.class);

    @Autowired
    private InvoiceRepository invoiceRepository;

    @Autowired
    private com.app.finance.client.BlockchainClient blockchainClient;

    @Autowired
    private RiskAssessmentService riskAssessmentService;

    @Transactional
    public Invoice createInvoice(InvoiceRequest request) {
        logger.info("Creating invoice");
        try {
            // Validate request
            validateInvoiceRequest(request);

            // Create invoice
            Invoice invoice = new Invoice();
            invoice.setSupplier(request.getSupplier());
            invoice.setBuyer(request.getBuyer());
            invoice.setAmount(request.getAmount());
            invoice.setDueDate(request.getDueDate());
            invoice.setStatus(InvoiceStatus.PENDING);

            // Save to database
            invoice = invoiceRepository.save(invoice);
            logger.info("Invoice created with ID: {}", invoice.getId());

            // Create blockchain record (Async/Resilient call)
            try {
                blockchainClient.createInvoice(
                        invoice.getSupplier(),
                        invoice.getBuyer(),
                        invoice.getAmount().toBigInteger(),
                        java.math.BigInteger.valueOf(invoice.getDueDate().toEpochDay()) // Simplified for example
                );
            } catch (Exception e) {
                logger.error("Failed to sync invoice creation to blockchain", e);
                // Non-blocking failure: App continues even if blockchain sync fails
            }

            return invoice;
        } catch (Exception e) {
            logger.error("Error creating invoice", e);
            throw e;
        }
    }

    public List<Invoice> getInvoices(String status, int page, int size) {
        logger.info("Fetching invoices with status: {}, page: {}, size: {}", status, page, size);
        try {
            List<Invoice> invoices;
            if (status != null) {
                invoices = invoiceRepository.findByStatus(
                        InvoiceStatus.valueOf(status.toUpperCase()),
                        PageRequest.of(page, size)).getContent();
            } else {
                invoices = invoiceRepository.findAll(PageRequest.of(page, size)).getContent();
            }
            logger.info("Successfully fetched {} invoices", invoices.size());
            return invoices;
        } catch (Exception e) {
            logger.error("Error fetching invoices", e);
            throw e;
        }
    }

    @Transactional
    public Invoice financeInvoice(Long id, FinanceRequest request) {
        logger.info("Financing invoice with ID: {}", id);
        try {
            Invoice invoice = invoiceRepository.findById(id)
                    .orElseThrow(() -> new InvoiceNotFoundException(id));

            // Check if invoice can be financed
            if (!canBeFinanced(invoice)) {
                throw new InvalidOperationException("Invoice cannot be financed");
            }

            // Assess risk
            RiskAssessment risk = riskAssessmentService.assessRisk(invoice.getSupplier());
            if (risk.getScore() < riskAssessmentService.getMinimumAcceptableScore()) {
                throw new RiskTooHighException("Risk score too low for financing");
            }

            // Update invoice
            invoice.setFinancingAmount(request.getAmount());
            invoice.setFinancier(request.getFinancier());
            invoice.setStatus(InvoiceStatus.FINANCED);

            // Update blockchain
            try {
                blockchainClient.financeInvoice(
                        java.math.BigInteger.valueOf(invoice.getId()),
                        invoice.getFinancingAmount().toBigInteger());
            } catch (Exception e) {
                logger.error("Failed to sync invoice financing to blockchain", e);
            }

            invoice = invoiceRepository.save(invoice);
            logger.info("Invoice {} successfully financed", id);
            return invoice;
        } catch (Exception e) {
            logger.error("Error financing invoice with ID: {}", id, e);
            throw e;
        }
    }

    @Transactional
    public Invoice approveInvoice(Long id) {
        logger.info("Approving invoice with ID: {}", id);
        try {
            Invoice invoice = invoiceRepository.findById(id)
                    .orElseThrow(() -> new InvoiceNotFoundException(id));

            invoice.setStatus(InvoiceStatus.APPROVED);
            invoice = invoiceRepository.save(invoice);
            logger.info("Invoice {} approved", id);

            // Update blockchain (No endpoint for approve in controller yet, skipping)
            // blockchainClient.approveInvoice(...)

            return invoice;
        } catch (Exception e) {
            logger.error("Error approving invoice with ID: {}", id, e);
            throw e;
        }
    }

    public AnalyticsData getAnalytics() {
        logger.info("Fetching analytics data");
        try {
            AnalyticsData data = new AnalyticsData();
            data.setTotalInvoices(invoiceRepository.count());
            data.setTotalFinanced(invoiceRepository.countByStatus(InvoiceStatus.FINANCED));
            data.setAverageFinancingAmount(invoiceRepository.getAverageFinancingAmount());
            // Convert List<Object[]> to Map<String, Object>
            List<Object[]> rawVolume = invoiceRepository.getMonthlyVolume();
            Map<String, Object> monthlyVolume = new HashMap<>();
            if (rawVolume != null) {
                for (Object[] row : rawVolume) {
                    monthlyVolume.put(String.valueOf(row[1]), row[0]);
                }
            }
            data.setMonthlyVolume(monthlyVolume);
            logger.info("Successfully fetched analytics data");
            return data;
        } catch (Exception e) {
            logger.error("Error fetching analytics data", e);
            throw e;
        }
    }

    private void validateInvoiceRequest(InvoiceRequest request) {
        logger.debug("Validating invoice request");
        try {
            if (request.getAmount() == null || request.getAmount().compareTo(java.math.BigDecimal.ZERO) <= 0) {
                throw new InvalidRequestException("Amount must be positive");
            }
            if (request.getDueDate().isBefore(LocalDate.now())) {
                throw new InvalidRequestException("Due date must be in the future");
            }
            logger.debug("Invoice request validation passed");
        } catch (Exception e) {
            logger.error("Invoice request validation failed", e);
            throw e;
        }
    }

    private boolean canBeFinanced(Invoice invoice) {
        logger.debug("Checking if invoice {} can be financed", invoice.getId());
        boolean canBeFinanced = invoice.getStatus() == InvoiceStatus.PENDING &&
                !invoice.isFinanced() &&
                invoice.getDueDate().isAfter(LocalDate.now());
        logger.debug("Invoice {} can be financed: {}", invoice.getId(), canBeFinanced);
        return canBeFinanced;
    }
}