package com.app.defi;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class DeFiServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(DeFiServiceApplication.class, args);
    }
}