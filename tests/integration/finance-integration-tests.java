package com.supplychain.finance.integration;

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
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(properties = {
    "spring.profiles.active=test"
})
@Testcontainers
public class FinanceServiceIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:13")
            .withDatabaseName("supplychain_test")
            .withUsername("test")
            .withPassword("test");

    @LocalServerPort
    private int port;

    @Autowired
    private TestRestTemplate restTemplate;

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @BeforeEach
    void setUp() {
        // Setup test data
    }

    @Test
    public void shouldCreateAndRetrieveInvoice() {
        // Test complete invoice lifecycle
        String createUrl = "http://localhost:" + port + "/api/finance/invoices";
        String invoiceJson = """
            {
                "amount": 1000.0,
                "supplierId": "SUP001",
                "buyerId": "BUY001",
                "status": "PENDING"
            }
            """;

        // Create invoice
        var createResponse = restTemplate.postForEntity(createUrl, invoiceJson, String.class);
        assertThat(createResponse.getStatusCode().value()).isEqualTo(201);

        // Retrieve invoice
        String getUrl = "http://localhost:" + port + "/api/finance/invoices/1";
        var getResponse = restTemplate.getForEntity(getUrl, String.class);
        assertThat(getResponse.getStatusCode().value()).isEqualTo(200);
    }

    @Test
    public void shouldHandleBlockchainIntegration() {
        // Test blockchain service integration
        String blockchainUrl = "http://localhost:" + port + "/api/finance/invoices/1/blockchain";
        var response = restTemplate.postForEntity(blockchainUrl, "{}", String.class);
        assertThat(response.getStatusCode().value()).isIn(200, 201);
    }
}
