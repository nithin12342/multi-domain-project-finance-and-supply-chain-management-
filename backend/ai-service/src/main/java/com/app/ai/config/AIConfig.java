package com.app.ai.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class AIConfig {

        @Bean
        public OpenAPI aiServiceOpenAPI() {
                return new OpenAPI()
                                .info(new Info()
                                                .title("AI/ML Service API")
                                                .description("API for AI/ML services including demand forecasting, fraud detection, and risk assessment")
                                                .version("v1.0")
                                                .contact(new Contact()
                                                                .name("AI Service Support")
                                                                .email("ai-support@supplychainplatform.com"))
                                                .license(new License()
                                                                .name("Apache 2.0")
                                                                .url("http://springdoc.org")))
                                .servers(List.of(
                                                new Server()
                                                                .url("http://localhost:8082")
                                                                .description("AI Service Development server"),
                                                new Server()
                                                                .url("https://ai.supplychainplatform.com")
                                                                .description("AI Service Production server")));
        }
}