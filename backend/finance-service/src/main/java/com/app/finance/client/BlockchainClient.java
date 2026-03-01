package com.app.finance.client;

import com.app.common.dto.ApiResponse;
import com.app.finance.model.Invoice;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.math.BigInteger;

@FeignClient(name = "blockchain-service", url = "${blockchain.service.url:http://localhost:8545}")
public interface BlockchainClient {

    @PostMapping("/api/blockchain/invoice")
    ApiResponse<String> createInvoice(
            @RequestParam("supplier") String supplier,
            @RequestParam("buyer") String buyer,
            @RequestParam("amount") BigInteger amount,
            @RequestParam("dueDate") BigInteger dueDate);

    @PostMapping("/api/blockchain/invoice/{id}/finance")
    ApiResponse<String> financeInvoice(
            @PathVariable("id") BigInteger id,
            @RequestParam("amount") BigInteger amount);
}
