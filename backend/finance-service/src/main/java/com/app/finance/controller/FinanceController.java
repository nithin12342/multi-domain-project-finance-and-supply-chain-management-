package com.app.finance.controller;

import com.app.finance.model.Invoice;
import com.app.finance.service.FinanceService;
import com.app.finance.service.RiskAssessmentService;
import com.app.finance.dto.InvoiceRequest;
import com.app.finance.dto.FinanceRequest;
import com.app.finance.dto.AnalyticsData;
import com.app.finance.model.RiskAssessment;
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

import java.util.List;

@RestController
@RequestMapping("/api/finance")
@Tag(name = "Finance", description = "Finance Management API")
public class FinanceController {

    @Autowired
    private FinanceService financeService;

    @Autowired
    private RiskAssessmentService riskAssessmentService;

    @PostMapping("/invoices")
    @Operation(summary = "Create invoice", description = "Create a new invoice")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Invoice created successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.common.dto.ApiResponse.class))),
            @ApiResponse(responseCode = "400", description = "Invalid invoice data provided")
    })
    public ResponseEntity<com.app.common.dto.ApiResponse<Invoice>> createInvoice(
            @Parameter(description = "Invoice request data") @RequestBody InvoiceRequest request) {
        Invoice invoice = financeService.createInvoice(request);
        return ResponseEntity.ok(new com.app.common.dto.ApiResponse<>(invoice, "Invoice created successfully"));
    }

    @GetMapping("/invoices")
    @Operation(summary = "Get invoices", description = "Retrieve a list of invoices with optional filtering by status")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Successfully retrieved invoices", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.common.dto.ApiResponse.class))),
            @ApiResponse(responseCode = "400", description = "Invalid request parameters")
    })
    public ResponseEntity<com.app.common.dto.ApiResponse<List<Invoice>>> getInvoices(
            @Parameter(description = "Status to filter invoices") @RequestParam(required = false) String status,
            @Parameter(description = "Page number (0-based)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Number of items per page") @RequestParam(defaultValue = "10") int size) {
        List<Invoice> invoices = financeService.getInvoices(status, page, size);
        return ResponseEntity.ok(new com.app.common.dto.ApiResponse<>(invoices, "Invoices retrieved successfully"));
    }

    @PostMapping("/invoices/{id}/finance")
    @Operation(summary = "Finance invoice", description = "Finance an existing invoice")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Invoice financed successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.common.dto.ApiResponse.class))),
            @ApiResponse(responseCode = "400", description = "Invalid finance request or invoice cannot be financed"),
            @ApiResponse(responseCode = "404", description = "Invoice not found")
    })
    public ResponseEntity<com.app.common.dto.ApiResponse<Invoice>> financeInvoice(
            @Parameter(description = "Invoice ID") @PathVariable Long id,
            @Parameter(description = "Finance request data") @RequestBody FinanceRequest request) {

        // SECURITY: Check if user is authorized to finance this invoice
        // TODO: String currentUserRole = SecurityContextHolder...
        // if (!currentUserRole.equals("ROLE_FINANCIER")) throw new
        // AccessDeniedException("Only financiers can finance invoices");

        Invoice invoice = financeService.financeInvoice(id, request);
        return ResponseEntity.ok(new com.app.common.dto.ApiResponse<>(invoice, "Invoice financed successfully"));
    }

    @PostMapping("/invoices/{id}/approve")
    @Operation(summary = "Approve invoice", description = "Approve an existing invoice")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Invoice approved successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.common.dto.ApiResponse.class))),
            @ApiResponse(responseCode = "400", description = "Invalid approval request"),
            @ApiResponse(responseCode = "404", description = "Invoice not found")
    })
    public ResponseEntity<com.app.common.dto.ApiResponse<Invoice>> approveInvoice(
            @Parameter(description = "Invoice ID") @PathVariable Long id) {

        // SECURITY: Check if user is authorized to approve
        // TODO: Check if current user is the buyer of the invoice

        Invoice invoice = financeService.approveInvoice(id);
        return ResponseEntity.ok(new com.app.common.dto.ApiResponse<>(invoice, "Invoice approved successfully"));
    }

    @GetMapping("/analytics")
    @Operation(summary = "Get analytics", description = "Retrieve finance analytics data")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Successfully retrieved analytics", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.common.dto.ApiResponse.class)))
    })
    public ResponseEntity<com.app.common.dto.ApiResponse<AnalyticsData>> getAnalytics() {
        AnalyticsData analytics = financeService.getAnalytics();
        return ResponseEntity.ok(new com.app.common.dto.ApiResponse<>(analytics, "Analytics retrieved successfully"));
    }

    @GetMapping("/risk-assessment")
    @Operation(summary = "Get risk assessment", description = "Retrieve risk assessment for a supplier")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Successfully retrieved risk assessment", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.common.dto.ApiResponse.class))),
            @ApiResponse(responseCode = "400", description = "Invalid supplier ID")
    })
    public ResponseEntity<com.app.common.dto.ApiResponse<RiskAssessment>> getRiskAssessment(
            @Parameter(description = "Supplier ID") @RequestParam Long supplierId) {
        RiskAssessment risk = riskAssessmentService.assessRisk(String.valueOf(supplierId));
        return ResponseEntity.ok(new com.app.common.dto.ApiResponse<>(risk, "Risk assessment completed"));
    }
}