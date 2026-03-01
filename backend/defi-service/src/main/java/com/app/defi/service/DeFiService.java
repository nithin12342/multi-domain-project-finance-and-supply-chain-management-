package com.app.defi.service;

import com.app.defi.contract.AdvancedDeFiProtocols;
import com.app.defi.exception.DeFiServiceException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.web3j.crypto.Credentials;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.http.HttpService;
import org.web3j.tx.gas.ContractGasProvider;
import org.web3j.tx.gas.StaticGasProvider;
import java.math.BigInteger;

@Service
public class DeFiService {
    
    private final Web3j web3j;
    private final Credentials credentials;
    private AdvancedDeFiProtocols contract;
    
    @Value("${blockchain.node.url}")
    private String nodeUrl;
    
    @Value("${blockchain.wallet.private-key}")
    private String privateKey;
    
    @Value("${defi.contract.address}")
    private String contractAddress;

    public DeFiService(@Value("${blockchain.node.url}") String nodeUrl,
                      @Value("${blockchain.wallet.private-key}") String privateKey,
                      @Value("${defi.contract.address}") String contractAddress) {
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
            contract = AdvancedDeFiProtocols.load(
                contractAddress,
                web3j,
                credentials,
                gasProvider
            );
        } catch (Exception e) {
            throw new DeFiServiceException("Failed to load DeFi contract", e);
        }
    }

    // Liquidity Pool Functions
    
    public String createLiquidityPool(String tokenA, String tokenB, BigInteger fee) {
        try {
            return contract.createLiquidityPool(tokenA, tokenB, fee)
                .send()
                .getTransactionHash();
        } catch (Exception e) {
            throw new DeFiServiceException("Failed to create liquidity pool", e);
        }
    }

    public String addLiquidity(byte[] poolId, BigInteger amountA, BigInteger amountB) {
        try {
            return contract.addLiquidity(poolId, amountA, amountB)
                .send()
                .getTransactionHash();
        } catch (Exception e) {
            throw new DeFiServiceException("Failed to add liquidity", e);
        }
    }

    public String removeLiquidity(byte[] poolId, BigInteger shares) {
        try {
            return contract.removeLiquidity(poolId, shares)
                .send()
                .getTransactionHash();
        } catch (Exception e) {
            throw new DeFiServiceException("Failed to remove liquidity", e);
        }
    }

    public String swap(byte[] poolId, String tokenIn, BigInteger amountIn, BigInteger minAmountOut) {
        try {
            return contract.swap(poolId, tokenIn, amountIn, minAmountOut)
                .send()
                .getTransactionHash();
        } catch (Exception e) {
            throw new DeFiServiceException("Failed to execute swap", e);
        }
    }

    // Yield Farming Functions
    
    public String createYieldFarm(String stakingToken, String rewardToken, BigInteger rewardRate, BigInteger duration) {
        try {
            return contract.createYieldFarm(stakingToken, rewardToken, rewardRate, duration)
                .send()
                .getTransactionHash();
        } catch (Exception e) {
            throw new DeFiServiceException("Failed to create yield farm", e);
        }
    }

    public String stake(byte[] farmId, BigInteger amount) {
        try {
            return contract.stake(farmId, amount)
                .send()
                .getTransactionHash();
        } catch (Exception e) {
            throw new DeFiServiceException("Failed to stake tokens", e);
        }
    }

    public String claimRewards(byte[] farmId) {
        try {
            return contract.claimRewards(farmId)
                .send()
                .getTransactionHash();
        } catch (Exception e) {
            throw new DeFiServiceException("Failed to claim rewards", e);
        }
    }

    // Flash Loan Functions
    
    public String flashLoan(String token, BigInteger amount, byte[] data) {
        try {
            return contract.flashLoan(token, amount, data)
                .send()
                .getTransactionHash();
        } catch (Exception e) {
            throw new DeFiServiceException("Failed to execute flash loan", e);
        }
    }

    // Cross-Chain Bridge Functions
    
    public String lockTokensForBridge(BigInteger targetChain, String token, BigInteger amount, String recipient) {
        try {
            return contract.lockTokensForBridge(targetChain, token, amount, recipient)
                .send()
                .getTransactionHash();
        } catch (Exception e) {
            throw new DeFiServiceException("Failed to lock tokens for bridge", e);
        }
    }

    public String releaseTokensFromBridge(BigInteger sourceChain, String token, BigInteger amount, String recipient, byte[] txHash, byte[] signature) {
        try {
            return contract.releaseTokensFromBridge(sourceChain, token, amount, recipient, txHash, signature)
                .send()
                .getTransactionHash();
        } catch (Exception e) {
            throw new DeFiServiceException("Failed to release tokens from bridge", e);
        }
    }

    // Getters
    
    public BigInteger getLiquidityPoolCount() {
        try {
            return contract.liquidityPoolCount().send();
        } catch (Exception e) {
            throw new DeFiServiceException("Failed to get liquidity pool count", e);
        }
    }

    public BigInteger getYieldFarmCount() {
        try {
            return contract.yieldFarmCount().send();
        } catch (Exception e) {
            throw new DeFiServiceException("Failed to get yield farm count", e);
        }
    }
}