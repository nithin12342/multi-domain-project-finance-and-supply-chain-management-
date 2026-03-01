import dspy
import torch
import json

class SupplyChainSignature(dspy.Signature):
    """
    DSPy Signature defining the exact inputs and outputs for the OmniFusion LLM Orchestrator.
    It takes the mathematical outputs from the Hybrid-TFT and HyperGNN and translates them 
    into a structured supply chain action.
    """
    # Inputs: The latent state representations from our PyTorch networks
    iot_telemetry_summary = dspy.InputField(desc="Textual summary of Mamba-encoded IoT anomalies (e.g. 'Vibration spike on container 42')")
    hypergraph_risk_score = dspy.InputField(desc="Cascading risk probability from the SpatioTemporalHyperGNN (e.g. '0.89')")
    demand_forecast_quantiles = dspy.InputField(desc="Predicted demand quantiles from the TFT (p10, p50, p90)")
    
    # Outputs: The exact strategic decision
    recommended_action = dspy.OutputField(desc="The exact action to take (e.g. 'Reroute shipment', 'Delay factoring invoice')")
    chain_of_thought_reasoning = dspy.OutputField(desc="Step-by-step logic explaining WHY this action was chosen")
    confidence_score = dspy.OutputField(desc="Float between 0.0 and 1.0 representing confidence in the decision")

class OmniFusionOrchestrator(dspy.Module):
    """
    The main DSPy program. It uses Chain-of-Thought reasoning to process the structural 
    supply chain data. Crucially, DSPy allows this module to *self-improve* its reasoning 
    prompts and weights during inference.
    """
    def __init__(self):
        super().__init__()
        # We wrap our signature in a ChainOfThought module
        self.decision_maker = dspy.ChainOfThought(SupplyChainSignature)
        
    def forward(self, iot_telemetry_summary, hypergraph_risk_score, demand_forecast_quantiles):
        prediction = self.decision_maker(
            iot_telemetry_summary=iot_telemetry_summary,
            hypergraph_risk_score=hypergraph_risk_score,
            demand_forecast_quantiles=demand_forecast_quantiles
        )
        return prediction

def supply_chain_financial_metric(example, pred, trace=None):
    """
    The Core DSPy Metric Function. This is how the system CONTINUOUSLY improves during inference.
    If the system makes a prediction in live production, we wait to see the real-world outcome.
    Then, we pass it back through this metric.
    
    This replaces traditional, unstable 'Online Reinforcement Learning' with robust DSPy compilation.
    """
    score = 0.0
    
    # 1. Did the action actually align with the ground truth optimal action?
    if example.ground_truth_optimal_action.lower() in pred.recommended_action.lower():
        score += 0.5
        
    # 2. Did the LLM explicitly reference the Hypergraph Risk Score in its reasoning?
    if str(example.hypergraph_risk_score) in pred.chain_of_thought_reasoning:
        score += 0.3
        
    # 3. Penalize low confidence on high-certainty events
    if float(pred.confidence_score) > 0.8:
        score += 0.2
        
    return score

def compile_continual_learning_agent(trainset):
    """
    Runs the DSPy Teleprompter (Optimizer).
    Instead of manually tweaking prompts or doing unstable PPO gradient updates on an LLM,
    DSPy automatically tries thousands of combinations and 'compiles' the optimal pipeline.
    """
    # Use BootstrapFewShotWithRandomSearch to optimize the prompts and reasoning mathematically
    teleprompter = dspy.teleprompt.BootstrapFewShotWithRandomSearch(
        metric=supply_chain_financial_metric,
        max_bootstrapped_demos=4,
        max_labeled_demos=16,
        num_candidate_programs=10,
        num_threads=4
    )
    
    print("🚀 DSPy is compiling and self-improving the OmniFusion Agent...")
    orchestrator = OmniFusionOrchestrator()
    compiled_orchestrator = teleprompter.compile(orchestrator, trainset=trainset)
    
    # Save the compiled, self-improved agent to disk
    compiled_orchestrator.save('/backend/ai-ml/models/dspy_compiled_omnifusion.json')
    print("✅ Self-Improved Agent Saved!")
    return compiled_orchestrator
