package com.app.ai.controller;

import com.app.ai.service.ModelMonitoringService;
// ApiResponse is used as fully qualified: com.app.common.dto.ApiResponse
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/ai/monitoring")
@Tag(name = "Model Monitoring", description = "Model Monitoring and Performance Tracking")
public class ModelMonitoringController {

    @Autowired
    private ModelMonitoringService modelMonitoringService;

    @GetMapping("/performance")
    @Operation(summary = "Get model performance metrics", description = "Retrieve current performance metrics for all AI/ML models")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Model performance metrics retrieved successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.common.dto.ApiResponse.class))),
            @ApiResponse(responseCode = "500", description = "Internal server error")
    })
    public ResponseEntity<com.app.common.dto.ApiResponse<ModelMonitoringService.ModelPerformanceMetrics>> getModelPerformanceMetrics() {
        try {
            ModelMonitoringService.ModelPerformanceMetrics metrics = modelMonitoringService
                    .getModelPerformanceMetrics();
            return ResponseEntity.ok(
                    new com.app.common.dto.ApiResponse<>(metrics, "Model performance metrics retrieved successfully"));
        } catch (Exception e) {
            return ResponseEntity.internalServerError()
                    .body(new com.app.common.dto.ApiResponse<>(null,
                            "Error retrieving model performance metrics: " + e.getMessage()));
        }
    }

    @PostMapping("/retrain")
    @Operation(summary = "Trigger model retraining", description = "Manually trigger retraining of all AI/ML models")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Model retraining initiated successfully", content = @Content(mediaType = "application/json", schema = @Schema(implementation = com.app.common.dto.ApiResponse.class))),
            @ApiResponse(responseCode = "500", description = "Internal server error")
    })
    public ResponseEntity<com.app.common.dto.ApiResponse<Boolean>> triggerModelRetraining() {
        try {
            // This will trigger the retraining in the monitoring service
            modelMonitoringService.monitorModelPerformance();
            return ResponseEntity
                    .ok(new com.app.common.dto.ApiResponse<>(true, "Model retraining initiated successfully"));
        } catch (Exception e) {
            return ResponseEntity.internalServerError()
                    .body(new com.app.common.dto.ApiResponse<>(false,
                            "Error initiating model retraining: " + e.getMessage()));
        }
    }
}