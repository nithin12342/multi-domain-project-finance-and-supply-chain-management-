package com.supplychain.finance.service;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.Gauge;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.time.Duration;
import java.util.concurrent.atomic.AtomicInteger;

@Service
public class PerformanceMetricsService {

    @Autowired
    private MeterRegistry meterRegistry;

    private final AtomicInteger activeUsers = new AtomicInteger(0);
    private final AtomicInteger activeConnections = new AtomicInteger(0);

    private Counter invoiceCreatedCounter;
    private Counter paymentProcessedCounter;
    private Counter aiPredictionCounter;
    private Counter blockchainTransactionCounter;

    private Timer apiResponseTimer;
    private Timer databaseQueryTimer;
    private Timer blockchainTransactionTimer;

    @PostConstruct
    public void init() {
        // Counters
        invoiceCreatedCounter = Counter.builder("invoices_created_total")
                .description("Total number of invoices created")
                .register(meterRegistry);

        paymentProcessedCounter = Counter.builder("payments_processed_total")
                .description("Total number of payments processed")
                .register(meterRegistry);

        aiPredictionCounter = Counter.builder("ai_predictions_total")
                .description("Total number of AI predictions made")
                .register(meterRegistry);

        blockchainTransactionCounter = Counter.builder("blockchain_transactions_total")
                .description("Total number of blockchain transactions")
                .register(meterRegistry);

        // Timers
        apiResponseTimer = Timer.builder("api_response_time")
                .description("API response time")
                .register(meterRegistry);

        databaseQueryTimer = Timer.builder("database_query_time")
                .description("Database query execution time")
                .register(meterRegistry);

        blockchainTransactionTimer = Timer.builder("blockchain_transaction_time")
                .description("Blockchain transaction execution time")
                .register(meterRegistry);

        // Gauges
        Gauge.builder("active_users", activeUsers, AtomicInteger::doubleValue)
                .description("Number of currently active users")
                .register(meterRegistry);

        Gauge.builder("active_database_connections", activeConnections, AtomicInteger::doubleValue)
                .description("Number of active database connections")
                .register(meterRegistry);
    }

    public void recordInvoiceCreated() {
        invoiceCreatedCounter.increment();
    }

    public void recordPaymentProcessed() {
        paymentProcessedCounter.increment();
    }

    public void recordAiPrediction() {
        aiPredictionCounter.increment();
    }

    public void recordBlockchainTransaction() {
        blockchainTransactionCounter.increment();
    }

    public Timer.Sample startApiTimer() {
        return Timer.start(meterRegistry);
    }

    public void stopApiTimer(Timer.Sample sample) {
        sample.stop(apiResponseTimer);
    }

    public Timer.Sample startDatabaseTimer() {
        return Timer.start(meterRegistry);
    }

    public void stopDatabaseTimer(Timer.Sample sample) {
        sample.stop(databaseQueryTimer);
    }

    public Timer.Sample startBlockchainTimer() {
        return Timer.start(meterRegistry);
    }

    public void stopBlockchainTimer(Timer.Sample sample) {
        sample.stop(blockchainTransactionTimer);
    }

    public void incrementActiveUsers() {
        activeUsers.incrementAndGet();
    }

    public void decrementActiveUsers() {
        activeUsers.decrementAndGet();
    }

    public void setActiveConnections(int connections) {
        activeConnections.set(connections);
    }
}
