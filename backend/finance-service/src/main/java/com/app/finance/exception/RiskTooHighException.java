package com.app.finance.exception;

public class RiskTooHighException extends RuntimeException {
    public RiskTooHighException(String message) {
        super(message);
    }
}