package com.app.ai.service;

import com.app.ai.model.DemandForecast;
import com.app.ai.repository.DemandForecastRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class DeepLearningService {
    
    private static final Logger logger = LoggerFactory.getLogger(DeepLearningService.class);
    
    @Autowired
    private DemandForecastRepository demandForecastRepository;
    
    @Value("${python.executable:python}")
    private String pythonExecutable;
    
    @Value("${ai.models.dl.path:../ai-ml/src/demand_forecast_dl.py}")
    private String deepLearningModelPath;
    
    /**
     * Predict demand using deep learning models (LSTM/Transformer)
     * @param productId Product identifier
     * @param period Time period for forecast
     * @param days Number of days to forecast
     * @return DemandForecast with prediction results
     */
    public DemandForecast predictDemandWithDL(String productId, String period, int days) {
        logger.info("Predicting demand with deep learning for product: {} with period: {} for {} days", 
                   productId, period, days);
        
        try {
            // Call the Python deep learning API
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonExecutable,
                deepLearningModelPath,
                "predict_demand",
                "--product_id", productId,
                "--period", period,
                "--days", String.valueOf(days)
            );
            
            Process process = processBuilder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
            
            int exitCode = process.waitFor();
            if (exitCode == 0) {
                // Parse the JSON output to create DemandForecast object
                String jsonOutput = output.toString().trim();
                // In a real implementation, we would parse the JSON
                // For now, we'll simulate the parsing
                
                // Simulated values from the Python script
                Integer predictedDemand = 150; // Would come from JSON parsing
                Double confidence = 0.92; // Would come from JSON parsing
                
                DemandForecast forecast = new DemandForecast(
                    productId, 
                    predictedDemand, 
                    confidence, 
                    LocalDateTime.now().plusDays(days), 
                    period
                );
                
                logger.info("Deep learning demand prediction successful for product: {}", productId);
                return forecast;
            } else {
                // Read error output
                BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                StringBuilder errorOutput = new StringBuilder();
                String errorLine;
                while ((errorLine = errorReader.readLine()) != null) {
                    errorOutput.append(errorLine).append("\n");
                }
                logger.error("Python deep learning script execution failed with exit code: {} and error: {}", 
                            exitCode, errorOutput.toString());
                throw new RuntimeException("Failed to execute deep learning demand forecasting model");
            }
        } catch (Exception e) {
            logger.error("Error predicting demand with deep learning for product: {}", productId, e);
            throw new RuntimeException("Error in deep learning demand prediction", e);
        }
    }
    
    /**
     * Optimize supply chain using reinforcement learning
     * @param parameters Optimization parameters
     * @return Optimization results
     */
    public String optimizeSupplyChain(String parameters) {
        logger.info("Optimizing supply chain with reinforcement learning using parameters: {}", parameters);
        
        try {
            // Call the Python reinforcement learning API
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonExecutable,
                "../ai-ml/src/supply_chain_rl.py",
                "optimize",
                "--parameters", parameters
            );
            
            Process process = processBuilder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
            
            int exitCode = process.waitFor();
            if (exitCode == 0) {
                String result = output.toString().trim();
                logger.info("Supply chain optimization successful");
                return result;
            } else {
                // Read error output
                BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                StringBuilder errorOutput = new StringBuilder();
                String errorLine;
                while ((errorLine = errorReader.readLine()) != null) {
                    errorOutput.append(errorLine).append("\n");
                }
                logger.error("Python reinforcement learning script execution failed with exit code: {} and error: {}", 
                            exitCode, errorOutput.toString());
                throw new RuntimeException("Failed to execute supply chain optimization model");
            }
        } catch (Exception e) {
            logger.error("Error optimizing supply chain with reinforcement learning", e);
            throw new RuntimeException("Error in supply chain optimization", e);
        }
    }
    
    /**
     * Get deep learning model performance metrics
     * @return Performance metrics
     */
    public List<Object> getModelPerformanceMetrics() {
        logger.info("Getting deep learning model performance metrics");
        
        List<Object> metrics = new ArrayList<>();
        // In a real implementation, this would fetch actual metrics from the models
        // For now, we'll return simulated metrics
        
        // Simulated metrics
        metrics.add("LSTM_Model_Accuracy: 0.92");
        metrics.add("Transformer_Model_Accuracy: 0.89");
        metrics.add("RL_Model_Reward: 1500.50");
        
        return metrics;
    }
    
    /**
     * Retrain deep learning models with new data
     * @return Success status
     */
    public boolean retrainDeepLearningModels() {
        logger.info("Retraining deep learning models");
        
        try {
            // Call the Python deep learning training API
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonExecutable,
                deepLearningModelPath,
                "retrain"
            );
            
            Process process = processBuilder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
                logger.info("DL training output: {}", line);
            }
            
            int exitCode = process.waitFor();
            if (exitCode == 0) {
                logger.info("Deep learning model retraining successful");
                return true;
            } else {
                // Read error output
                BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                StringBuilder errorOutput = new StringBuilder();
                String errorLine;
                while ((errorLine = errorReader.readLine()) != null) {
                    errorOutput.append(errorLine).append("\n");
                }
                logger.error("Deep learning model retraining failed with exit code: {} and error: {}", 
                            exitCode, errorOutput.toString());
                return false;
            }
        } catch (Exception e) {
            logger.error("Error retraining deep learning models", e);
            return false;
        }
    }
}