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
import java.util.Map;
import java.util.HashMap;

@Service
public class ReinforcementLearningService {
    
    private static final Logger logger = LoggerFactory.getLogger(ReinforcementLearningService.class);
    
    @Autowired
    private DemandForecastRepository demandForecastRepository;
    
    @Value("${python.executable:python}")
    private String pythonExecutable;
    
    @Value("${ai.models.rl.path:../ai-ml/src/supply_chain_rl.py}")
    private String rlScriptPath;
    
    /**
     * Train reinforcement learning model for inventory optimization
     * @param parameters Training parameters
     * @return Training results
     */
    public Map<String, Object> trainInventoryOptimization(String parameters) {
        logger.info("Training reinforcement learning model for inventory optimization with parameters: {}", parameters);
        
        try {
            // Call the Python RL API
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonExecutable,
                rlScriptPath,
                "train_inventory",
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
                // Parse the JSON output
                String jsonOutput = output.toString().trim();
                logger.info("RL inventory optimization training completed successfully");
                
                // Return results as a map
                Map<String, Object> results = new HashMap<>();
                results.put("status", "success");
                results.put("results", jsonOutput);
                results.put("timestamp", LocalDateTime.now());
                
                return results;
            } else {
                // Read error output
                BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                StringBuilder errorOutput = new StringBuilder();
                String errorLine;
                while ((errorLine = errorReader.readLine()) != null) {
                    errorOutput.append(errorLine).append("\n");
                }
                logger.error("Python RL script execution failed with exit code: {} and error: {}", 
                            exitCode, errorOutput.toString());
                
                Map<String, Object> results = new HashMap<>();
                results.put("status", "error");
                results.put("error", errorOutput.toString());
                return results;
            }
        } catch (Exception e) {
            logger.error("Error training RL model for inventory optimization", e);
            Map<String, Object> results = new HashMap<>();
            results.put("status", "error");
            results.put("error", e.getMessage());
            return results;
        }
    }
    
    /**
     * Optimize supply chain using trained reinforcement learning model
     * @param currentState Current state of the supply chain
     * @return Optimal actions
     */
    public Map<String, Object> optimizeSupplyChain(String currentState) {
        logger.info("Optimizing supply chain using RL model with current state: {}", currentState);
        
        try {
            // Call the Python RL API
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonExecutable,
                rlScriptPath,
                "optimize",
                "--state", currentState
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
                // Parse the JSON output
                String jsonOutput = output.toString().trim();
                logger.info("Supply chain optimization with RL completed successfully");
                
                // Return results as a map
                Map<String, Object> results = new HashMap<>();
                results.put("status", "success");
                results.put("results", jsonOutput);
                results.put("timestamp", LocalDateTime.now());
                
                return results;
            } else {
                // Read error output
                BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                StringBuilder errorOutput = new StringBuilder();
                String errorLine;
                while ((errorLine = errorReader.readLine()) != null) {
                    errorOutput.append(errorLine).append("\n");
                }
                logger.error("Python RL script execution failed with exit code: {} and error: {}", 
                            exitCode, errorOutput.toString());
                
                Map<String, Object> results = new HashMap<>();
                results.put("status", "error");
                results.put("error", errorOutput.toString());
                return results;
            }
        } catch (Exception e) {
            logger.error("Error optimizing supply chain with RL", e);
            Map<String, Object> results = new HashMap<>();
            results.put("status", "error");
            results.put("error", e.getMessage());
            return results;
        }
    }
    
    /**
     * Get reinforcement learning model performance metrics
     * @return Performance metrics
     */
    public Map<String, Object> getRLModelPerformance() {
        logger.info("Getting reinforcement learning model performance metrics");
        
        Map<String, Object> metrics = new HashMap<>();
        metrics.put("model_status", "active");
        metrics.put("last_training", LocalDateTime.now());
        metrics.put("supported_tasks", new String[]{"inventory_optimization", "dynamic_pricing", "supplier_selection"});
        
        // Add some mock metrics
        metrics.put("average_reward", 1250.75);
        metrics.put("training_episodes", 1000);
        metrics.put("exploration_rate", 0.5);
        
        return metrics;
    }
    
    /**
     * Retrain reinforcement learning models with new data
     * @return Success status
     */
    public boolean retrainRLModels() {
        logger.info("Retraining reinforcement learning models");
        
        try {
            // Call the Python RL training API
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonExecutable,
                rlScriptPath,
                "retrain"
            );
            
            Process process = processBuilder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
                logger.info("RL retraining output: {}", line);
            }
            
            int exitCode = process.waitFor();
            if (exitCode == 0) {
                logger.info("RL model retraining successful");
                return true;
            } else {
                // Read error output
                BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                StringBuilder errorOutput = new StringBuilder();
                String errorLine;
                while ((errorLine = errorReader.readLine()) != null) {
                    errorOutput.append(errorLine).append("\n");
                }
                logger.error("RL model retraining failed with exit code: {} and error: {}", 
                            exitCode, errorOutput.toString());
                return false;
            }
        } catch (Exception e) {
            logger.error("Error retraining RL models", e);
            return false;
        }
    }
    
    /**
     * Multi-agent supply chain optimization
     * @param agentStates States of all agents in the supply chain
     * @return Coordinated actions for all agents
     */
    public Map<String, Object> multiAgentOptimization(List<String> agentStates) {
        logger.info("Performing multi-agent supply chain optimization with {} agents", agentStates.size());
        
        try {
            // Convert agent states to a single string parameter
            StringBuilder statesBuilder = new StringBuilder();
            for (int i = 0; i < agentStates.size(); i++) {
                statesBuilder.append(agentStates.get(i));
                if (i < agentStates.size() - 1) {
                    statesBuilder.append(";");
                }
            }
            
            // Call the Python RL API
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonExecutable,
                rlScriptPath,
                "multi_agent_optimize",
                "--states", statesBuilder.toString()
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
                // Parse the JSON output
                String jsonOutput = output.toString().trim();
                logger.info("Multi-agent supply chain optimization completed successfully");
                
                // Return results as a map
                Map<String, Object> results = new HashMap<>();
                results.put("status", "success");
                results.put("results", jsonOutput);
                results.put("timestamp", LocalDateTime.now());
                
                return results;
            } else {
                // Read error output
                BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                StringBuilder errorOutput = new StringBuilder();
                String errorLine;
                while ((errorLine = errorReader.readLine()) != null) {
                    errorOutput.append(errorLine).append("\n");
                }
                logger.error("Python RL script execution failed with exit code: {} and error: {}", 
                            exitCode, errorOutput.toString());
                
                Map<String, Object> results = new HashMap<>();
                results.put("status", "error");
                results.put("error", errorOutput.toString());
                return results;
            }
        } catch (Exception e) {
            logger.error("Error in multi-agent supply chain optimization", e);
            Map<String, Object> results = new HashMap<>();
            results.put("status", "error");
            results.put("error", e.getMessage());
            return results;
        }
    }
}