package com.app.supplychain.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI supplyChainOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Supply Chain Management API")
                        .description("API for managing supply chain operations including inventory, shipments, suppliers, and orders")
                        .version("v1.0")
                        .contact(new Contact()
                                .name("API Support")
                                .email("support@supplychainplatform.com"))
                        .license(new License()
                                .name("Apache 2.0")
                                .url("http://springdoc.org")))
                .servers(List.of(
                        new Server()
                                .url("http://localhost:8080")
                                .description("Development server"),
                        new Server()
                                .url("https://api.supplychainplatform.com")
                                .description("Production server")));
    }
}