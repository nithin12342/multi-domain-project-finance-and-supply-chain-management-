# DEPRECATED FILE - INFORMATION CONSOLIDATED
#
# This README file has been consolidated into the main project README.md
# Please refer to: /README.md for all project information
#
# Backend service documentation is now in the "Architecture Overview" section
# of the main README.md file.
#
# File deprecated as of: October 23, 2025
# Reason: Documentation consolidation for better organization

DEPRECATED - USE MAIN README.md INSTEAD

# Backend Services

This directory contains the backend microservices for the Supply Chain and Finance Platform.

## Services

### Supply Chain Service
- **Port**: 8080
- **Description**: Manages supply chain operations including inventory, shipments, suppliers, and orders
- **API Documentation**: 
  - Swagger UI: http://localhost:8080/swagger-ui.html
  - OpenAPI JSON: http://localhost:8080/api-docs

### Finance Service
- **Port**: 8081
- **Description**: Manages finance operations including invoices, payments, and risk assessment
- **API Documentation**: 
  - Swagger UI: http://localhost:8081/swagger-ui.html
  - OpenAPI JSON: http://localhost:8081/api-docs

## Common Module
Contains shared code between services including DTOs and common utilities.

## Prerequisites

- Java 11 or higher
- Maven 3.6 or higher
- PostgreSQL database

## Building the Services

Each service can be built independently using Maven:

```bash
# Build supply chain service
cd supplychain-service
mvn clean install

# Build finance service
cd finance-service
mvn clean install

# Build common module
cd common
mvn clean install
```

## Running the Services

Each service can be run independently:

```bash
# Run supply chain service
cd supplychain-service
mvn spring-boot:run

# Run finance service
cd finance-service
mvn spring-boot:run
```

## API Documentation

The APIs are documented using OpenAPI 3.0 (Swagger). You can access the interactive documentation at:

- Supply Chain Service: http://localhost:8080/swagger-ui.html
- Finance Service: http://localhost:8081/swagger-ui.html

## Database Configuration

Each service uses PostgreSQL as its database. The default configurations are:

- Supply Chain Service:
  - Database: supplychain_db
  - User: supplychain_user
  - Password: supplychain_password

- Finance Service:
  - Database: finance_db
  - User: finance_user
  - Password: finance_password

## Email Configuration

The supply chain service uses email for notifications. Configure your email settings in the application.properties file.

## Logging

All services use structured logging with different levels for debugging and monitoring.