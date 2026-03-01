package com.app.supplychain.client;

import com.app.supplychain.dto.ApiResponse;
import com.app.supplychain.model.DemandForecast;
import com.app.supplychain.model.RiskAssessment;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.List;

@FeignClient(name = "ai-service", url = "${ai.service.url:http://localhost:8082}")
public interface AIServiceClient {
    
    @PostMapping("/api/ai/demand-forecast")
    ApiResponse<DemandForecast> predictDemand(@RequestBody DemandForecastRequest request);
    
    @GetMapping("/api/ai/demand-forecast/product/{productId}")
    ApiResponse<List<DemandForecast>> getDemandForecastsByProduct(@PathVariable("productId") String productId);
    
    @PostMapping("/api/ai/risk-assessment/{supplierId}")
    ApiResponse<RiskAssessment> assessRisk(@PathVariable("supplierId") String supplierId);
    
    @GetMapping("/api/ai/risk-assessment/supplier/{supplierId}")
    ApiResponse<List<RiskAssessment>> getRiskAssessmentsBySupplier(@PathVariable("supplierId") String supplierId);
}