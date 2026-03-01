package com.supplychain.finance.performance;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.test.web.server.LocalServerPort;
import java.time.Duration;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;
import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(properties = {
    "spring.profiles.active=test"
})
public class PerformanceTest {

    @LocalServerPort
    private int port;

    @Autowired
    private TestRestTemplate restTemplate;

    private final String BASE_URL = "http://localhost:";

    @Test
    public void shouldHandleConcurrentRequests() throws InterruptedException {
        int numberOfThreads = 50;
        int requestsPerThread = 10;
        ExecutorService executor = Executors.newFixedThreadPool(numberOfThreads);

        long startTime = System.currentTimeMillis();

        CompletableFuture<Void>[] futures = IntStream.range(0, numberOfThreads)
                .mapToObj(i -> CompletableFuture.runAsync(() -> {
                    for (int j = 0; j < requestsPerThread; j++) {
                        String url = BASE_URL + port + "/api/finance/invoices";
                        var response = restTemplate.getForEntity(url, String.class);
                        assertThat(response.getStatusCode().value()).isEqualTo(200);
                    }
                }, executor))
                .toArray(CompletableFuture[]::new);

        // Wait for all requests to complete
        CompletableFuture.allOf(futures).join();

        long endTime = System.currentTimeMillis();
        long totalTime = endTime - startTime;

        System.out.println("Total time for " + (numberOfThreads * requestsPerThread) +
                          " requests: " + totalTime + "ms");
        System.out.println("Average time per request: " +
                          (totalTime / (numberOfThreads * requestsPerThread)) + "ms");

        // Performance assertion
        assertThat(totalTime).isLessThan(10000); // Should complete within 10 seconds

        executor.shutdown();
    }

    @Test
    public void shouldHandleLargeDataSets() {
        // Test with large invoice datasets
        String url = BASE_URL + port + "/api/finance/invoices/bulk";

        // Create large JSON payload
        StringBuilder largeJson = new StringBuilder("[");
        for (int i = 1; i <= 1000; i++) {
            largeJson.append(String.format("""
                {
                    "id": %d,
                    "amount": %.2f,
                    "supplierId": "SUP%03d",
                    "status": "PENDING"
                }""", i, 1000.0 + i, i));
            if (i < 1000) largeJson.append(",");
        }
        largeJson.append("]");

        long startTime = System.currentTimeMillis();
        var response = restTemplate.postForEntity(url, largeJson.toString(), String.class);
        long endTime = System.currentTimeMillis();

        assertThat(response.getStatusCode().value()).isEqualTo(200);
        assertThat(endTime - startTime).isLessThan(5000); // Should process within 5 seconds
    }

    @Test
    public void shouldMaintainPerformanceUnderLoad() {
        // Simulate sustained load
        ExecutorService executor = Executors.newFixedThreadPool(20);

        for (int i = 0; i < 100; i++) {
            CompletableFuture.runAsync(() -> {
                long requestStart = System.currentTimeMillis();
                String url = BASE_URL + port + "/api/ai/predict";
                var response = restTemplate.getForEntity(url, String.class);
                long requestEnd = System.currentTimeMillis();

                assertThat(response.getStatusCode().value()).isEqualTo(200);
                assertThat(requestEnd - requestStart).isLessThan(2000); // 2 second SLA
            }, executor);
        }

        executor.shutdown();
        // Wait a bit for completion
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
