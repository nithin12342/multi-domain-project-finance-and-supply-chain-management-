# DeFi Service

This service provides integration with advanced DeFi protocols for supply chain finance applications.

## Features

- Liquidity pool management (AMM)
- Yield farming and staking
- Flash loans
- Cross-chain bridge functionality
- Token swapping

## Prerequisites

- Java 17
- Maven 3.8+
- Ethereum node (Ganache, Hardhat, or mainnet/testnet)
- AdvancedDeFiProtocols smart contract deployed to the blockchain

## Configuration

The service can be configured using the following environment variables or application.properties:

```properties
# DeFi Service Configuration
server.port=8086

# Blockchain Configuration
blockchain.node.url=http://localhost:8545
blockchain.wallet.private-key=your-private-key-here
defi.contract.address=your-contract-address-here

# Kafka Configuration
spring.kafka.bootstrap-servers=localhost:9092
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
docker build -t defi-service .
docker run -p 8086:8086 defi-service
```

## API Endpoints

### Liquidity Pool Management

- `POST /api/defi/liquidity-pool` - Create a new liquidity pool
- `POST /api/defi/liquidity-pool/add` - Add liquidity to a pool
- `POST /api/defi/liquidity-pool/remove` - Remove liquidity from a pool
- `POST /api/defi/swap` - Execute a token swap

### Yield Farming

- `POST /api/defi/yield-farm` - Create a new yield farm
- `POST /api/defi/yield-farm/stake` - Stake tokens in a yield farm
- `POST /api/defi/yield-farm/claim` - Claim rewards from a yield farm

### Flash Loans

- `POST /api/defi/flash-loan` - Execute a flash loan

### Cross-Chain Bridge

- `POST /api/defi/bridge/lock` - Lock tokens for cross-chain transfer
- `POST /api/defi/bridge/release` - Release tokens from cross-chain transfer

### Getters

- `GET /api/defi/liquidity-pool/count` - Get the number of liquidity pools
- `GET /api/defi/yield-farm/count` - Get the number of yield farms

## Smart Contract Integration

The service integrates with the `AdvancedDeFiProtocols.sol` smart contract which provides:

1. **Automated Market Maker (AMM)** - Constant product formula for token swaps
2. **Yield Farming** - Staking rewards for liquidity providers
3. **Flash Loans** - Uncollateralized loans for arbitrage opportunities
4. **Cross-Chain Bridge** - Token transfer between different blockchain networks

## Event Integration

The service can emit events for integration with other services:

- LiquidityAdded
- LiquidityRemoved
- SwapExecuted
- YieldFarmCreated
- Staked
- RewardsClaimed
- FlashLoanExecuted
- CrossChainTransfer

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