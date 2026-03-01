package com.app.defi.exception;

public class DeFiServiceException extends RuntimeException {
    
    public DeFiServiceException(String message) {
        super(message);
    }
    
    public DeFiServiceException(String message, Throwable cause) {
        super(message, cause);
    }
}