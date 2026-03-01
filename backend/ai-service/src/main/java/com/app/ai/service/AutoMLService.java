package com.app.ai.service;

import com.app.ai.model.DemandForecast;
import com.app.ai.model.FraudDetection;
import com.app.ai.model.RiskAssessment;
import com.app.ai.repository.DemandForecastRepository;
import com.app.ai.repository.FraudDetectionRepository;
import com.app.ai.repository.RiskAssessmentRepository;
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
public class AutoMLService {
    
    private static final Logger logger = LoggerFactory.getLogger(AutoMLService.class);
    
    @Autowired
    private DemandForecastRepository demandForecastRepository;
    
    @Autowired
    private FraudDetectionRepository fraudDetectionRepository;
    
    @Autowired
    private RiskAssessmentRepository riskAssessmentRepository;
    
    @Value("${python.executable:python}")
    private String pythonExecutable;
    
    @Value("${ai.models.automl.path:../ai-ml/advanced/automl-pipeline.py}")
    private String autoMLScriptPath;
    
    /**
     * Run AutoML pipeline for demand forecasting
     * @param datasetPath Path to the dataset
     * @param targetColumn Target column name
     * @return AutoML results
     */
    public Map<String, Object> runDemandForecastAutoML(String datasetPath, String targetColumn) {
        logger.info("Running AutoML pipeline for demand forecasting with dataset: {}", datasetPath);
        
        try {
            // Call the Python AutoML API
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonExecutable,
                autoMLScriptPath,
                "run_automl",
                "--task", "demand_forecast",
                "--dataset", datasetPath,
                "--target", targetColumn
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
                logger.info("AutoML demand forecasting completed successfully");
                
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
                logger.error("Python AutoML script execution failed with exit code: {} and error: {}", 
                            exitCode, errorOutput.toString());
                
                Map<String, Object> results = new HashMap<>();
                results.put("status", "error");
                results.put("error", errorOutput.toString());
                return results;
            }
        } catch (Exception e) {
            logger.error("Error running AutoML for demand forecasting", e);
            Map<String, Object> results = new HashMap<>();
            results.put("status", "error");
            results.put("error", e.getMessage());
            return results;
        }
    }
    
    /**
     * Run AutoML pipeline for fraud detection
     * @param datasetPath Path to the dataset
     * @param targetColumn Target column name
     * @return AutoML results
     */
    public Map<String, Object> runFraudDetectionAutoML(String datasetPath, String targetColumn) {
        logger.info("Running AutoML pipeline for fraud detection with dataset: {}", datasetPath);
        
        try {
            // Call the Python AutoML API
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonExecutable,
                autoMLScriptPath,
                "run_automl",
                "--task", "fraud_detection",
                "--dataset", datasetPath,
                "--target", targetColumn
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
                logger.info("AutoML fraud detection completed successfully");
                
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
                logger.error("Python AutoML script execution failed with exit code: {} and error: {}", 
                            exitCode, errorOutput.toString());
                
                Map<String, Object> results = new HashMap<>();
                results.put("status", "error");
                results.put("error", errorOutput.toString());
                return results;
            }
        } catch (Exception e) {
            logger.error("Error running AutoML for fraud detection", e);
            Map<String, Object> results = new HashMap<>();
            results.put("status", "error");
            results.put("error", e.getMessage());
            return results;
        }
    }
    
    /**
     * Run AutoML pipeline for risk assessment
     * @param datasetPath Path to the dataset
     * @param targetColumn Target column name
     * @return AutoML results
     */
    public Map<String, Object> runRiskAssessmentAutoML(String datasetPath, String targetColumn) {
        logger.info("Running AutoML pipeline for risk assessment with dataset: {}", datasetPath);
        
        try {
            // Call the Python AutoML API
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonExecutable,
                autoMLScriptPath,
                "run_automl",
                "--task", "risk_assessment",
                "--dataset", datasetPath,
                "--target", targetColumn
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
                logger.info("AutoML risk assessment completed successfully");
                
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
                logger.error("Python AutoML script execution failed with exit code: {} and error: {}", 
                            exitCode, errorOutput.toString());
                
                Map<String, Object> results = new HashMap<>();
                results.put("status", "error");
                results.put("error", errorOutput.toString());
                return results;
            }
        } catch (Exception e) {
            logger.error("Error running AutoML for risk assessment", e);
            Map<String, Object> results = new HashMap<>();
            results.put("status", "error");
            results.put("error", e.getMessage());
            return results;
        }
    }
    
    /**
     * Get AutoML pipeline status and metrics
     * @return Pipeline status and metrics
     */
    public Map<String, Object> getAutoMLPipelineStatus() {
        logger.info("Getting AutoML pipeline status");
        
        Map<String, Object> status = new HashMap<>();
        status.put("pipeline_status", "active");
        status.put("last_run", LocalDateTime.now());
        status.put("supported_tasks", new String[]{"demand_forecast", "fraud_detection", "risk_assessment"});
        
        // Add some mock metrics
        status.put("models_trained", 15);
        status.put("best_accuracy", 0.94);
        status.put("avg_training_time", "12.5 minutes");
        
        return status;
    }
    
    /**
     * Retrain all AutoML models with new data
     * @return Success status
     */
    public boolean retrainAutoMLModels() {
        logger.info("Retraining all AutoML models");
        
        try {
            // Call the Python AutoML training API
            ProcessBuilder processBuilder = new ProcessBuilder(
                pythonExecutable,
                autoMLScriptPath,
                "retrain_all"
            );
            
            Process process = processBuilder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
                logger.info("AutoML retraining output: {}", line);
            }
            
            int exitCode = process.waitFor();
            if (exitCode == 0) {
                logger.info("AutoML model retraining successful");
                return true;
            } else {
                // Read error output
                BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                StringBuilder errorOutput = new StringBuilder();
                String errorLine;
                while ((errorLine = errorReader.readLine()) != null) {
                    errorOutput.append(errorLine).append("\n");
                }
                logger.error("AutoML model retraining failed with exit code: {} and error: {}", 
                            exitCode, errorOutput.toString());
                return false;
            }
        } catch (Exception e) {
            logger.error("Error retraining AutoML models", e);
            return false;
        }
    }
}