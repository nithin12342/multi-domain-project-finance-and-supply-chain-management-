# Blockchain Service

This service provides integration with blockchain smart contracts for supply chain and finance operations.

## Features

- Integration with Ethereum-based smart contracts
- Invoice management on blockchain
- Shipment tracking on blockchain
- Cross-chain bridge functionality
- Zero-knowledge proof verification

## Prerequisites

- Java 17
- Maven 3.8+
- Ethereum node (Ganache, Hardhat, or mainnet/testnet)
- Smart contracts deployed to the blockchain

## Configuration

The service can be configured using the following environment variables or application.properties:

```properties
# Blockchain Configuration
blockchain.node.url=http://localhost:8545
blockchain.wallet.private-key=your-private-key-here
blockchain.contract.address=your-contract-address-here

# Server Configuration
server.port=8085
```

## Building the Service

```bash
mvn clean package
```

## Running the Service

```bash
mvn spring-boot:run
```

Or using Docker:

```bash
docker build -t blockchain-service .
docker run -p 8085:8085 blockchain-service
```

## API Endpoints

### Invoice Management

- `POST /api/blockchain/invoice` - Create a new invoice
- `POST /api/blockchain/invoice/{id}/finance` - Finance an invoice
- `GET /api/blockchain/invoice/{id}` - Get invoice details

### Shipment Management

- `POST /api/blockchain/shipment` - Create a new shipment
- `PUT /api/blockchain/shipment/{id}/status` - Update shipment status
- `GET /api/blockchain/shipment/{id}` - Get shipment details

## Smart Contract Integration

The service integrates with the following smart contracts:

1. `SupplyChainFinance.sol` - Main contract for supply chain and finance operations
2. `SupplyChainZKP.sol` - Zero-knowledge proof verification
3. `CrossChainBridge.sol` - Cross-chain asset transfer

## Event Integration

The service listens for blockchain events and can emit events for integration with other services:

- InvoiceCreated
- InvoiceFinanced
- InvoicePaid
- ShipmentCreated
- ShipmentUpdated
- CrossChainTransfer
- ZKPVerified

## Testing

Run unit tests:

```bash
mvn test
```

## Monitoring

The service exposes metrics via Spring Boot Actuator:

- Health: `/actuator/health`
- Info: `/actuator/info`
- Metrics: `/actuator/metrics`