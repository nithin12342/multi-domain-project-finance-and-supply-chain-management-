package com.supplychain.finance.e2e;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(properties = {
    "spring.profiles.active=test"
})
@Testcontainers
public class SupplyChainE2ETest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:13")
            .withDatabaseName("supplychain_test");

    @Container
    static GenericContainer<?> redis = new GenericContainer<>("redis:6-alpine")
            .withExposedPorts(6379);

    @LocalServerPort
    private int port;

    @Autowired
    private TestRestTemplate restTemplate;

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        registry.add("spring.redis.host", redis::getHost);
        registry.add("spring.redis.port", redis::getFirstMappedPort);
    }

    @Test
    public void shouldCompleteFullSupplyChainFinanceWorkflow() {
        // 1. User authentication
        String authUrl = "http://localhost:" + port + "/api/auth/login";
        String loginJson = """
            {
                "username": "supplier1",
                "password": "password123"
            }
            """;

        var authResponse = restTemplate.postForEntity(authUrl, loginJson, String.class);
        assertThat(authResponse.getStatusCode().value()).isEqualTo(200);

        // 2. Create supplier order
        String orderUrl = "http://localhost:" + port + "/api/supplychain/orders";
        String orderJson = """
            {
                "supplierId": "SUP001",
                "productId": "PROD001",
                "quantity": 100,
                "price": 10.0
            }
            """;

        var orderResponse = restTemplate.postForEntity(orderUrl, orderJson, String.class);
        assertThat(orderResponse.getStatusCode().value()).isEqualTo(201);

        // 3. Create invoice
        String invoiceUrl = "http://localhost:" + port + "/api/finance/invoices";
        String invoiceJson = """
            {
                "orderId": 1,
                "amount": 1000.0,
                "dueDate": "2025-01-30"
            }
            """;

        var invoiceResponse = restTemplate.postForEntity(invoiceUrl, invoiceJson, String.class);
        assertThat(invoiceResponse.getStatusCode().value()).isEqualTo(201);

        // 4. Process payment through blockchain
        String paymentUrl = "http://localhost:" + port + "/api/finance/invoices/1/payment";
        var paymentResponse = restTemplate.postForEntity(paymentUrl, "{}", String.class);
        assertThat(paymentResponse.getStatusCode().value()).isEqualTo(200);

        // 5. Verify AI risk assessment
        String riskUrl = "http://localhost:" + port + "/api/ai/risk-assessment/1";
        var riskResponse = restTemplate.getForEntity(riskUrl, String.class);
        assertThat(riskResponse.getStatusCode().value()).isEqualTo(200);
    }

    @Test
    public void shouldHandleIoTDataIntegration() {
        // Test IoT sensor data integration with supply chain
        String iotUrl = "http://localhost:" + port + "/api/iot/sensors/temperature";
        String sensorJson = """
            {
                "deviceId": "SENSOR001",
                "value": 25.5,
                "timestamp": "2025-01-23T10:00:00Z"
            }
            """;

        var iotResponse = restTemplate.postForEntity(iotUrl, sensorJson, String.class);
        assertThat(iotResponse.getStatusCode().value()).isEqualTo(201);
    }
}
