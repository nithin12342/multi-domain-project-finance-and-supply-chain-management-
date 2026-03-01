package com.app.defi.controller;

import com.app.defi.service.DeFiService;
import com.app.common.dto.ApiResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.math.BigInteger;

@RestController
@RequestMapping("/api/defi")
public class DeFiController {
    
    @Autowired
    private DeFiService defiService;
    
    // Liquidity Pool Endpoints
    
    @PostMapping("/liquidity-pool")
    public ApiResponse<String> createLiquidityPool(
            @RequestParam String tokenA,
            @RequestParam String tokenB,
            @RequestParam BigInteger fee) {
        try {
            String transactionHash = defiService.createLiquidityPool(tokenA, tokenB, fee);
            return new ApiResponse<>(true, "Liquidity pool created successfully", transactionHash);
        } catch (Exception e) {
            return new ApiResponse<>(false, "Failed to create liquidity pool: " + e.getMessage(), null);
        }
    }
    
    @PostMapping("/liquidity-pool/add")
    public ApiResponse<String> addLiquidity(
            @RequestParam String poolId,
            @RequestParam BigInteger amountA,
            @RequestParam BigInteger amountB) {
        try {
            byte[] poolIdBytes = hexStringToByteArray(poolId);
            String transactionHash = defiService.addLiquidity(poolIdBytes, amountA, amountB);
            return new ApiResponse<>(true, "Liquidity added successfully", transactionHash);
        } catch (Exception e) {
            return new ApiResponse<>(false, "Failed to add liquidity: " + e.getMessage(), null);
        }
    }
    
    @PostMapping("/liquidity-pool/remove")
    public ApiResponse<String> removeLiquidity(
            @RequestParam String poolId,
            @RequestParam BigInteger shares) {
        try {
            byte[] poolIdBytes = hexStringToByteArray(poolId);
            String transactionHash = defiService.removeLiquidity(poolIdBytes, shares);
            return new ApiResponse<>(true, "Liquidity removed successfully", transactionHash);
        } catch (Exception e) {
            return new ApiResponse<>(false, "Failed to remove liquidity: " + e.getMessage(), null);
        }
    }
    
    @PostMapping("/swap")
    public ApiResponse<String> swap(
            @RequestParam String poolId,
            @RequestParam String tokenIn,
            @RequestParam BigInteger amountIn,
            @RequestParam BigInteger minAmountOut) {
        try {
            byte[] poolIdBytes = hexStringToByteArray(poolId);
            String transactionHash = defiService.swap(poolIdBytes, tokenIn, amountIn, minAmountOut);
            return new ApiResponse<>(true, "Swap executed successfully", transactionHash);
        } catch (Exception e) {
            return new ApiResponse<>(false, "Failed to execute swap: " + e.getMessage(), null);
        }
    }
    
    // Yield Farming Endpoints
    
    @PostMapping("/yield-farm")
    public ApiResponse<String> createYieldFarm(
            @RequestParam String stakingToken,
            @RequestParam String rewardToken,
            @RequestParam BigInteger rewardRate,
            @RequestParam BigInteger duration) {
        try {
            String transactionHash = defiService.createYieldFarm(stakingToken, rewardToken, rewardRate, duration);
            return new ApiResponse<>(true, "Yield farm created successfully", transactionHash);
        } catch (Exception e) {
            return new ApiResponse<>(false, "Failed to create yield farm: " + e.getMessage(), null);
        }
    }
    
    @PostMapping("/yield-farm/stake")
    public ApiResponse<String> stake(
            @RequestParam String farmId,
            @RequestParam BigInteger amount) {
        try {
            byte[] farmIdBytes = hexStringToByteArray(farmId);
            String transactionHash = defiService.stake(farmIdBytes, amount);
            return new ApiResponse<>(true, "Tokens staked successfully", transactionHash);
        } catch (Exception e) {
            return new ApiResponse<>(false, "Failed to stake tokens: " + e.getMessage(), null);
        }
    }
    
    @PostMapping("/yield-farm/claim")
    public ApiResponse<String> claimRewards(@RequestParam String farmId) {
        try {
            byte[] farmIdBytes = hexStringToByteArray(farmId);
            String transactionHash = defiService.claimRewards(farmIdBytes);
            return new ApiResponse<>(true, "Rewards claimed successfully", transactionHash);
        } catch (Exception e) {
            return new ApiResponse<>(false, "Failed to claim rewards: " + e.getMessage(), null);
        }
    }
    
    // Flash Loan Endpoints
    
    @PostMapping("/flash-loan")
    public ApiResponse<String> flashLoan(
            @RequestParam String token,
            @RequestParam BigInteger amount,
            @RequestParam String data) {
        try {
            byte[] dataBytes = hexStringToByteArray(data);
            String transactionHash = defiService.flashLoan(token, amount, dataBytes);
            return new ApiResponse<>(true, "Flash loan executed successfully", transactionHash);
        } catch (Exception e) {
            return new ApiResponse<>(false, "Failed to execute flash loan: " + e.getMessage(), null);
        }
    }
    
    // Cross-Chain Bridge Endpoints
    
    @PostMapping("/bridge/lock")
    public ApiResponse<String> lockTokensForBridge(
            @RequestParam BigInteger targetChain,
            @RequestParam String token,
            @RequestParam BigInteger amount,
            @RequestParam String recipient) {
        try {
            String transactionHash = defiService.lockTokensForBridge(targetChain, token, amount, recipient);
            return new ApiResponse<>(true, "Tokens locked for bridge successfully", transactionHash);
        } catch (Exception e) {
            return new ApiResponse<>(false, "Failed to lock tokens for bridge: " + e.getMessage(), null);
        }
    }
    
    @PostMapping("/bridge/release")
    public ApiResponse<String> releaseTokensFromBridge(
            @RequestParam BigInteger sourceChain,
            @RequestParam String token,
            @RequestParam BigInteger amount,
            @RequestParam String recipient,
            @RequestParam String txHash,
            @RequestParam String signature) {
        try {
            byte[] txHashBytes = hexStringToByteArray(txHash);
            byte[] signatureBytes = hexStringToByteArray(signature);
            String transactionHash = defiService.releaseTokensFromBridge(sourceChain, token, amount, recipient, txHashBytes, signatureBytes);
            return new ApiResponse<>(true, "Tokens released from bridge successfully", transactionHash);
        } catch (Exception e) {
            return new ApiResponse<>(false, "Failed to release tokens from bridge: " + e.getMessage(), null);
        }
    }
    
    // Getter Endpoints
    
    @GetMapping("/liquidity-pool/count")
    public ApiResponse<BigInteger> getLiquidityPoolCount() {
        try {
            BigInteger count = defiService.getLiquidityPoolCount();
            return new ApiResponse<>(true, "Liquidity pool count retrieved successfully", count);
        } catch (Exception e) {
            return new ApiResponse<>(false, "Failed to get liquidity pool count: " + e.getMessage(), null);
        }
    }
    
    @GetMapping("/yield-farm/count")
    public ApiResponse<BigInteger> getYieldFarmCount() {
        try {
            BigInteger count = defiService.getYieldFarmCount();
            return new ApiResponse<>(true, "Yield farm count retrieved successfully", count);
        } catch (Exception e) {
            return new ApiResponse<>(false, "Failed to get yield farm count: " + e.getMessage(), null);
        }
    }
    
    // Helper method to convert hex string to byte array
    private byte[] hexStringToByteArray(String s) {
        int len = s.length();
        byte[] data = new byte[len / 2];
        for (int i = 0; i < len; i += 2) {
            data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
                    + Character.digit(s.charAt(i+1), 16));
        }
        return data;
    }
}