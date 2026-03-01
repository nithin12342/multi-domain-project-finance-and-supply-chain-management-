package com.app.blockchain.service;

import org.web3j.crypto.Credentials;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.http.HttpService;
import org.web3j.tx.gas.ContractGasProvider;
import org.web3j.tx.gas.StaticGasProvider;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import java.math.BigInteger;

@Service
public class BlockchainService {
    private final Web3j web3j;
    private final Credentials credentials;
    private SupplyChainFinance contract;
    
    @Value("${blockchain.contract.address}")
    private String contractAddress;
    
    @Value("${blockchain.wallet.private-key}")
    private String privateKey;
    
    @Value("${blockchain.node.url}")
    private String nodeUrl;

    public BlockchainService(@Value("${blockchain.node.url}") String nodeUrl,
                           @Value("${blockchain.wallet.private-key}") String privateKey,
                           @Value("${blockchain.contract.address}") String contractAddress) {
        this.nodeUrl = nodeUrl;
        this.privateKey = privateKey;
        this.contractAddress = contractAddress;
        
        web3j = Web3j.build(new HttpService(nodeUrl));
        credentials = Credentials.create(privateKey);
        
        ContractGasProvider gasProvider = new StaticGasProvider(
            BigInteger.valueOf(20000000000L), // gasPrice
            BigInteger.valueOf(6721975L)      // gasLimit
        );

        try {
            contract = SupplyChainFinance.load(
                contractAddress,
                web3j,
                credentials,
                gasProvider
            );
        } catch (Exception e) {
            throw new BlockchainException("Failed to load contract", e);
        }
    }

    public String createInvoice(String supplier, String buyer, BigInteger amount, BigInteger dueDate) {
        try {
            return contract.createInvoice(supplier, buyer, amount, dueDate)
                .send()
                .getTransactionHash();
        } catch (Exception e) {
            throw new BlockchainException("Failed to create invoice", e);
        }
    }

    public String financeInvoice(BigInteger invoiceId, BigInteger amount) {
        try {
            return contract.financeInvoice(invoiceId)
                .send()
                .getTransactionHash();
        } catch (Exception e) {
            throw new BlockchainException("Failed to finance invoice", e);
        }
    }

    public String createShipment(String supplier, String buyer, String productId, BigInteger quantity) {
        try {
            return contract.createShipment(supplier, buyer, productId, quantity)
                .send()
                .getTransactionHash();
        } catch (Exception e) {
            throw new BlockchainException("Failed to create shipment", e);
        }
    }

    public String updateShipmentStatus(BigInteger shipmentId, String status) {
        try {
            return contract.updateShipmentStatus(shipmentId, status)
                .send()
                .getTransactionHash();
        } catch (Exception e) {
            throw new BlockchainException("Failed to update shipment status", e);
        }
    }

    public InvoiceDetails getInvoice(BigInteger invoiceId) {
        try {
            var result = contract.getInvoice(invoiceId).send();
            return new InvoiceDetails(
                result.id,
                result.supplier,
                result.buyer,
                result.amount,
                result.dueDate,
                result.isPaid,
                result.isFinanced,
                result.financier
            );
        } catch (Exception e) {
            throw new BlockchainException("Failed to get invoice details", e);
        }
    }

    public ShipmentDetails getShipment(BigInteger shipmentId) {
        try {
            var result = contract.getShipment(shipmentId).send();
            return new ShipmentDetails(
                result.id,
                result.supplier,
                result.buyer,
                result.productId,
                result.quantity,
                result.timestamp,
                result.status
            );
        } catch (Exception e) {
            throw new BlockchainException("Failed to get shipment details", e);
        }
    }
}