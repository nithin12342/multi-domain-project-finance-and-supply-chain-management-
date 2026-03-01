package com.app.finance.exception;

import com.app.common.dto.ApiResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;

@ControllerAdvice
public class GlobalExceptionHandler {
    
    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(InvoiceNotFoundException.class)
    public ResponseEntity<ApiResponse<Void>> handleInvoiceNotFoundException(InvoiceNotFoundException ex, WebRequest request) {
        logger.warn("Invoice not found: {}", ex.getMessage());
        ApiResponse<Void> response = new ApiResponse<>(null, ex.getMessage());
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(InvalidOperationException.class)
    public ResponseEntity<ApiResponse<Void>> handleInvalidOperationException(InvalidOperationException ex, WebRequest request) {
        logger.warn("Invalid operation: {}", ex.getMessage());
        ApiResponse<Void> response = new ApiResponse<>(null, ex.getMessage());
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(RiskTooHighException.class)
    public ResponseEntity<ApiResponse<Void>> handleRiskTooHighException(RiskTooHighException ex, WebRequest request) {
        logger.warn("Risk too high: {}", ex.getMessage());
        ApiResponse<Void> response = new ApiResponse<>(null, ex.getMessage());
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ApiResponse<Void>> handleIllegalArgumentException(IllegalArgumentException ex, WebRequest request) {
        logger.warn("Illegal argument: {}", ex.getMessage());
        ApiResponse<Void> response = new ApiResponse<>(null, "Invalid request data: " + ex.getMessage());
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiResponse<Void>> handleGenericException(Exception ex, WebRequest request) {
        logger.error("Unexpected error occurred: ", ex);
        ApiResponse<Void> response = new ApiResponse<>(null, "An unexpected error occurred. Please try again later.");
        return new ResponseEntity<>(response, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}