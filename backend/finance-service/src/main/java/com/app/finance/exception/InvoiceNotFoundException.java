package com.app.finance.exception;

public class InvoiceNotFoundException extends RuntimeException {
    public InvoiceNotFoundException(Long id) {
        super("Invoice not found with ID: " + id);
    }
}