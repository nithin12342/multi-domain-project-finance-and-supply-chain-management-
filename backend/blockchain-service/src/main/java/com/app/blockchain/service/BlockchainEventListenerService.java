package com.app.blockchain.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.core.DefaultBlockParameterName;
import org.web3j.protocol.core.DefaultBlockParameter;
import org.web3j.protocol.core.methods.response.EthBlock;
import org.web3j.protocol.core.methods.response.Log;
import org.web3j.utils.Numeric;
import java.math.BigInteger;
import java.util.List;

@Service
public class BlockchainEventListenerService {

    private static final Logger logger = LoggerFactory.getLogger(BlockchainEventListenerService.class);

    @Autowired
    private Web3j web3j;

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    private BigInteger lastProcessedBlock = BigInteger.ZERO;

    @Scheduled(fixedDelay = 10000) // Check every 10 seconds
    public void listenForBlockchainEvents() {
        try {
            // Get the latest block number
            BigInteger latestBlock = web3j.ethBlockNumber().send().getBlockNumber();

            // If this is the first run, start from a few blocks back
            if (lastProcessedBlock.equals(BigInteger.ZERO)) {
                lastProcessedBlock = latestBlock.subtract(BigInteger.valueOf(10));
                if (lastProcessedBlock.compareTo(BigInteger.ZERO) < 0) {
                    lastProcessedBlock = BigInteger.ZERO;
                }
            }

            // Process blocks from last processed to latest
            for (BigInteger blockNumber = lastProcessedBlock.add(BigInteger.ONE); blockNumber
                    .compareTo(latestBlock) <= 0; blockNumber = blockNumber.add(BigInteger.ONE)) {

                processBlock(blockNumber);
                lastProcessedBlock = blockNumber;
            }

        } catch (Exception e) {
            logger.error("Error listening for blockchain events", e);
        }
    }

    private void processBlock(BigInteger blockNumber) {
        try {
            EthBlock block = web3j.ethGetBlockByNumber(
                    DefaultBlockParameter.valueOf(blockNumber), true).send();

            if (block.getBlock() != null && block.getBlock().getTransactions() != null) {
                List<EthBlock.TransactionResult> transactions = block.getBlock().getTransactions();

                for (EthBlock.TransactionResult transactionResult : transactions) {
                    EthBlock.TransactionObject transaction = (EthBlock.TransactionObject) transactionResult.get();

                    // Note: Event logs are actually retrieved from TransactionReceipts, not the
                    // TransactionObject.
                    // For brevity in block processing, we might fetch the receipt here if needed:
                    // Optional<TransactionReceipt> receipt =
                    // web3j.ethGetTransactionReceipt(transaction.getHash()).send().getTransactionReceipt();
                }
            }
        } catch (Exception e) {
            logger.error("Error processing block " + blockNumber, e);
        }
    }

    private void processEventLog(Log log) {
        try {
            String topic = log.getTopics().get(0);

            // Process different event types based on their signature topics
            if (topic.equals(Numeric.toHexString(
                    org.web3j.crypto.Hash.sha3("InvoiceCreated(uint256,address,address,uint256)".getBytes())))) {
                handleInvoiceCreatedEvent(log);
            } else if (topic.equals(Numeric
                    .toHexString(org.web3j.crypto.Hash.sha3("InvoiceFinanced(uint256,address,uint256)".getBytes())))) {
                handleInvoiceFinancedEvent(log);
            } else if (topic.equals(Numeric
                    .toHexString(org.web3j.crypto.Hash.sha3("InvoicePaid(uint256,address,uint256)".getBytes())))) {
                handleInvoicePaidEvent(log);
            } else if (topic.equals(Numeric.toHexString(
                    org.web3j.crypto.Hash.sha3("ShipmentCreated(uint256,address,address,string)".getBytes())))) {
                handleShipmentCreatedEvent(log);
            } else if (topic.equals(
                    Numeric.toHexString(org.web3j.crypto.Hash.sha3("ShipmentUpdated(uint256,string)".getBytes())))) {
                handleShipmentUpdatedEvent(log);
            } else if (topic.equals(Numeric.toHexString(org.web3j.crypto.Hash
                    .sha3("CrossChainTransfer(uint256,uint256,address,address,uint256,bytes32)".getBytes())))) {
                handleCrossChainTransferEvent(log);
            } else if (topic
                    .equals(Numeric.toHexString(org.web3j.crypto.Hash.sha3("ZKPVerified(uint256,bool)".getBytes())))) {
                handleZKPVerifiedEvent(log);
            }
        } catch (Exception e) {
            logger.error("Error processing event log", e);
        }
    }

    private void handleInvoiceCreatedEvent(Log log) {
        try {
            // Parse event data and emit to Kafka
            String eventData = "InvoiceCreated: " + log.toString();
            kafkaTemplate.send("blockchain-events", eventData);
            logger.info("InvoiceCreated event processed: " + eventData);
        } catch (Exception e) {
            logger.error("Error handling InvoiceCreated event", e);
        }
    }

    private void handleInvoiceFinancedEvent(Log log) {
        try {
            // Parse event data and emit to Kafka
            String eventData = "InvoiceFinanced: " + log.toString();
            kafkaTemplate.send("blockchain-events", eventData);
            logger.info("InvoiceFinanced event processed: " + eventData);
        } catch (Exception e) {
            logger.error("Error handling InvoiceFinanced event", e);
        }
    }

    private void handleInvoicePaidEvent(Log log) {
        try {
            // Parse event data and emit to Kafka
            String eventData = "InvoicePaid: " + log.toString();
            kafkaTemplate.send("blockchain-events", eventData);
            logger.info("InvoicePaid event processed: " + eventData);
        } catch (Exception e) {
            logger.error("Error handling InvoicePaid event", e);
        }
    }

    private void handleShipmentCreatedEvent(Log log) {
        try {
            // Parse event data and emit to Kafka
            String eventData = "ShipmentCreated: " + log.toString();
            kafkaTemplate.send("blockchain-events", eventData);
            logger.info("ShipmentCreated event processed: " + eventData);
        } catch (Exception e) {
            logger.error("Error handling ShipmentCreated event", e);
        }
    }

    private void handleShipmentUpdatedEvent(Log log) {
        try {
            // Parse event data and emit to Kafka
            String eventData = "ShipmentUpdated: " + log.toString();
            kafkaTemplate.send("blockchain-events", eventData);
            logger.info("ShipmentUpdated event processed: " + eventData);
        } catch (Exception e) {
            logger.error("Error handling ShipmentUpdated event", e);
        }
    }

    private void handleCrossChainTransferEvent(Log log) {
        try {
            // Parse event data and emit to Kafka
            String eventData = "CrossChainTransfer: " + log.toString();
            kafkaTemplate.send("blockchain-events", eventData);
            logger.info("CrossChainTransfer event processed: " + eventData);
        } catch (Exception e) {
            logger.error("Error handling CrossChainTransfer event", e);
        }
    }

    private void handleZKPVerifiedEvent(Log log) {
        try {
            // Parse event data and emit to Kafka
            String eventData = "ZKPVerified: " + log.toString();
            kafkaTemplate.send("blockchain-events", eventData);
            logger.info("ZKPVerified event processed: " + eventData);
        } catch (Exception e) {
            logger.error("Error handling ZKPVerified event", e);
        }
    }
}