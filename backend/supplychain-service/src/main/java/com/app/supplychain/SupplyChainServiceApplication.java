package com.app.supplychain;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
@EnableFeignClients(basePackages = "com.app.supplychain.client")
public class SupplyChainServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(SupplyChainServiceApplication.class, args);
    }
}