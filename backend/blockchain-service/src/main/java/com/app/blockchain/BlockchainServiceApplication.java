package com.app.blockchain;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class BlockchainServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(BlockchainServiceApplication.class, args);
    }
}