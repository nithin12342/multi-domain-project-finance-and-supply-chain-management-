"""
Causal Inference for Supply Chain Analytics

This module implements causal inference techniques to understand the true cause-and-effect
relationships in supply chain operations, going beyond simple correlations.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# For causal inference, we'll use a simplified approach since dowhy is complex to install
# In practice, you would use: from dowhy import CausalModel

class CausalInferenceEngine:
    """Causal inference engine for supply chain analytics"""
    
    def __init__(self):
        self.causal_graph = None
        self.treatment_effects = {}
    
    def build_causal_graph(self, variables: List[str], edges: List[Tuple[str, str]]) -> Dict[str, Any]:
        """
        Build a causal graph representation
        
        Args:
            variables: List of variable names
            edges: List of directed edges (cause, effect)
            
        Returns:
            Causal graph representation
        """
        graph = {
            'variables': variables,
            'edges': edges,
            'parents': {var: [] for var in variables},
            'children': {var: [] for var in variables}
        }
        
        # Build parent-child relationships
        for cause, effect in edges:
            if cause in variables and effect in variables:
                graph['parents'][effect].append(cause)
                graph['children'][cause].append(effect)
        
        self.causal_graph = graph
        return graph
    
    def estimate_causal_effect(self, data: pd.DataFrame, treatment: str, outcome: str, 
                             confounders: List[str] = None) -> Dict[str, float]:
        """
        Estimate causal effect using a simplified approach
        
        Args:
            data: DataFrame with variables
            treatment: Treatment variable
            outcome: Outcome variable
            confounders: Confounding variables
            
        Returns:
            Dictionary with causal effect estimates
        """
        if confounders is None:
            confounders = []
        
        # Simple difference-in-means approach
        treated = data[data[treatment] == 1]
        control = data[data[treatment] == 0]
        
        # Unadjusted effect
        unadjusted_effect = treated[outcome].mean() - control[outcome].mean()
        
        # Adjusted effect using linear regression (simplified)
        if confounders:
            # This is a simplified approach - in practice, use proper causal inference libraries
            from sklearn.linear_model import LinearRegression
            
            X = data[confounders + [treatment]]
            y = data[outcome]
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Get coefficient for treatment variable
            treatment_idx = X.columns.get_loc(treatment)
            adjusted_effect = model.coef_[treatment_idx]
        else:
            adjusted_effect = unadjusted_effect
        
        effect_dict = {
            'unadjusted_effect': unadjusted_effect,
            'adjusted_effect': adjusted_effect,
            'treatment_variable': treatment,
            'outcome_variable': outcome
        }
        
        self.treatment_effects[f"{treatment}->{outcome}"] = effect_dict
        return effect_dict
    
    def estimate_ate(self, data: pd.DataFrame, treatment: str, outcome: str) -> float:
        """
        Estimate Average Treatment Effect (ATE)
        
        Args:
            data: DataFrame with treatment and outcome variables
            treatment: Treatment variable (binary)
            outcome: Outcome variable
            
        Returns:
            Average Treatment Effect
        """
        treated_outcomes = data[data[treatment] == 1][outcome]
        control_outcomes = data[data[treatment] == 0][outcome]
        
        ate = treated_outcomes.mean() - control_outcomes.mean()
        return ate
    
    def estimate_att(self, data: pd.DataFrame, treatment: str, outcome: str) -> float:
        """
        Estimate Average Treatment Effect on the Treated (ATT)
        
        Args:
            data: DataFrame with treatment and outcome variables
            treatment: Treatment variable (binary)
            outcome: Outcome variable
            
        Returns:
            Average Treatment Effect on the Treated
        """
        treated_outcomes = data[data[treatment] == 1][outcome]
        control_outcomes = data[data[treatment] == 0][outcome]
        
        # ATT is the same as ATE in randomized experiments
        # In observational studies, it requires more sophisticated methods
        att = treated_outcomes.mean() - control_outcomes.mean()
        return att
    
    def propensity_score_matching(self, data: pd.DataFrame, treatment: str, 
                                covariates: List[str]) -> pd.DataFrame:
        """
        Perform propensity score matching (simplified implementation)
        
        Args:
            data: DataFrame with treatment and covariate variables
            treatment: Treatment variable (binary)
            covariates: List of covariate variables
            
        Returns:
            Matched dataset
        """
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics.pairwise import euclidean_distances
        
        # Estimate propensity scores
        X = data[covariates]
        y = data[treatment]
        
        ps_model = LogisticRegression()
        ps_model.fit(X, y)
        propensity_scores = ps_model.predict_proba(X)[:, 1]
        
        # Add propensity scores to data
        data_with_ps = data.copy()
        data_with_ps['propensity_score'] = propensity_scores
        
        # Simple matching (1:1 nearest neighbor)
        treated = data_with_ps[data_with_ps[treatment] == 1]
        control = data_with_ps[data_with_ps[treatment] == 0]
        
        matched_control = []
        for _, treated_row in treated.iterrows():
            # Find closest control unit
            distances = euclidean_distances(
                treated_row[['propensity_score']].values.reshape(1, -1),
                control[['propensity_score']].values
            ).flatten()
            
            closest_idx = np.argmin(distances)
            matched_control.append(control.iloc[closest_idx])
        
        matched_control_df = pd.DataFrame(matched_control)
        matched_data = pd.concat([treated, matched_control_df], ignore_index=True)
        
        return matched_data
    
    def instrumental_variable_estimation(self, data: pd.DataFrame, treatment: str, 
                                       outcome: str, instrument: str) -> Dict[str, float]:
        """
        Estimate causal effect using instrumental variables (simplified)
        
        Args:
            data: DataFrame with variables
            treatment: Treatment variable
            outcome: Outcome variable
            instrument: Instrumental variable
            
        Returns:
            Dictionary with IV estimates
        """
        from sklearn.linear_model import LinearRegression
        
        # First stage: regress treatment on instrument
        X_inst = data[[instrument]]
        y_treat = data[treatment]
        
        first_stage = LinearRegression()
        first_stage.fit(X_inst, y_treat)
        treatment_pred = first_stage.predict(X_inst)
        
        # Second stage: regress outcome on predicted treatment
        X_treat_pred = treatment_pred.reshape(-1, 1)
        y_outcome = data[outcome]
        
        second_stage = LinearRegression()
        second_stage.fit(X_treat_pred, y_outcome)
        
        iv_estimate = second_stage.coef_[0]
        
        return {
            'iv_estimate': iv_estimate,
            'first_stage_coefficient': first_stage.coef_[0],
            'instrument': instrument
        }
    
    def mediation_analysis(self, data: pd.DataFrame, treatment: str, mediator: str, 
                          outcome: str) -> Dict[str, float]:
        """
        Perform mediation analysis (simplified)
        
        Args:
            data: DataFrame with variables
            treatment: Treatment variable
            mediator: Mediator variable
            outcome: Outcome variable
            
        Returns:
            Dictionary with mediation effects
        """
        from sklearn.linear_model import LinearRegression
        
        # Path a: treatment -> mediator
        model_a = LinearRegression()
        X_a = data[[treatment]]
        y_a = data[mediator]
        model_a.fit(X_a, y_a)
        path_a = model_a.coef_[0]
        
        # Path b: mediator -> outcome (controlling for treatment)
        model_b = LinearRegression()
        X_b = data[[treatment, mediator]]
        y_b = data[outcome]
        model_b.fit(X_b, y_b)
        path_b = model_b.coef_[1]  # Coefficient for mediator
        
        # Total effect
        model_total = LinearRegression()
        X_total = data[[treatment]]
        y_total = data[outcome]
        model_total.fit(X_total, y_total)
        total_effect = model_total.coef_[0]
        
        # Indirect effect (a * b)
        indirect_effect = path_a * path_b
        
        # Direct effect (total - indirect)
        direct_effect = total_effect - indirect_effect
        
        return {
            'indirect_effect': indirect_effect,
            'direct_effect': direct_effect,
            'total_effect': total_effect,
            'path_a': path_a,
            'path_b': path_b
        }

class SupplyChainCausalAnalyzer:
    """High-level causal analyzer for supply chain scenarios"""
    
    def __init__(self):
        self.engine = CausalInferenceEngine()
        self.results = {}
    
    def analyze_supplier_performance(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze causal relationships in supplier performance
        
        Args:
            data: DataFrame with supplier data
            
        Returns:
            Dictionary with causal analysis results
        """
        # Define causal relationships
        variables = ['supplier_reliability', 'delivery_time', 'quality_score', 
                    'cost', 'geo_risk', 'performance_score']
        edges = [
            ('supplier_reliability', 'delivery_time'),
            ('supplier_reliability', 'quality_score'),
            ('delivery_time', 'performance_score'),
            ('quality_score', 'performance_score'),
            ('cost', 'performance_score'),
            ('geo_risk', 'delivery_time')
        ]
        
        # Build causal graph
        graph = self.engine.build_causal_graph(variables, edges)
        
        # Estimate causal effects
        effects = {}
        
        # Effect of reliability on delivery time
        effects['reliability_delivery'] = self.engine.estimate_causal_effect(
            data, 'supplier_reliability', 'delivery_time', ['geo_risk']
        )
        
        # Effect of reliability on quality
        effects['reliability_quality'] = self.engine.estimate_causal_effect(
            data, 'supplier_reliability', 'quality_score'
        )
        
        # Effect of delivery time on performance
        effects['delivery_performance'] = self.engine.estimate_causal_effect(
            data, 'delivery_time', 'performance_score', 
            ['supplier_reliability', 'cost']
        )
        
        # Effect of quality on performance
        effects['quality_performance'] = self.engine.estimate_causal_effect(
            data, 'quality_score', 'performance_score', 
            ['supplier_reliability', 'cost']
        )
        
        results = {
            'causal_graph': graph,
            'causal_effects': effects,
            'recommendations': self._generate_supplier_recommendations(effects)
        }
        
        self.results['supplier_performance'] = results
        return results
    
    def analyze_inventory_policy(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze causal relationships in inventory policy
        
        Args:
            data: DataFrame with inventory data
            
        Returns:
            Dictionary with causal analysis results
        """
        # Define causal relationships
        variables = ['safety_stock_level', 'demand_variability', 'lead_time', 
                    'stockout_rate', 'holding_cost', 'service_level']
        edges = [
            ('safety_stock_level', 'stockout_rate'),
            ('safety_stock_level', 'holding_cost'),
            ('demand_variability', 'stockout_rate'),
            ('lead_time', 'stockout_rate'),
            ('stockout_rate', 'service_level'),
            ('holding_cost', 'service_level')
        ]
        
        # Build causal graph
        graph = self.engine.build_causal_graph(variables, edges)
        
        # Estimate causal effects
        effects = {}
        
        # Effect of safety stock on stockout rate
        effects['safety_stockout'] = self.engine.estimate_causal_effect(
            data, 'safety_stock_level', 'stockout_rate', 
            ['demand_variability', 'lead_time']
        )
        
        # Effect of safety stock on holding cost
        effects['safety_holding'] = self.engine.estimate_causal_effect(
            data, 'safety_stock_level', 'holding_cost'
        )
        
        # Effect of stockout rate on service level
        effects['stockout_service'] = self.engine.estimate_causal_effect(
            data, 'stockout_rate', 'service_level', 
            ['holding_cost']
        )
        
        results = {
            'causal_graph': graph,
            'causal_effects': effects,
            'recommendations': self._generate_inventory_recommendations(effects)
        }
        
        self.results['inventory_policy'] = results
        return results
    
    def analyze_pricing_strategy(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze causal relationships in pricing strategy
        
        Args:
            data: DataFrame with pricing data
            
        Returns:
            Dictionary with causal analysis results
        """
        # Define causal relationships
        variables = ['price', 'competitor_price', 'demand', 'revenue', 
                    'marketing_spend', 'market_share']
        edges = [
            ('price', 'demand'),
            ('price', 'revenue'),
            ('competitor_price', 'demand'),
            ('marketing_spend', 'demand'),
            ('demand', 'revenue'),
            ('revenue', 'market_share')
        ]
        
        # Build causal graph
        graph = self.engine.build_causal_graph(variables, edges)
        
        # Estimate causal effects
        effects = {}
        
        # Effect of price on demand
        effects['price_demand'] = self.engine.estimate_causal_effect(
            data, 'price', 'demand', 
            ['competitor_price', 'marketing_spend']
        )
        
        # Effect of price on revenue
        effects['price_revenue'] = self.engine.estimate_causal_effect(
            data, 'price', 'revenue', 
            ['demand', 'competitor_price']
        )
        
        # Effect of competitor price on demand
        effects['competitor_demand'] = self.engine.estimate_causal_effect(
            data, 'competitor_price', 'demand', 
            ['price', 'marketing_spend']
        )
        
        results = {
            'causal_graph': graph,
            'causal_effects': effects,
            'recommendations': self._generate_pricing_recommendations(effects)
        }
        
        self.results['pricing_strategy'] = results
        return results
    
    def _generate_supplier_recommendations(self, effects: Dict[str, Dict]) -> List[str]:
        """Generate recommendations based on supplier causal analysis"""
        recommendations = []
        
        # Check reliability effects
        if effects['reliability_delivery']['adjusted_effect'] < -0.1:
            recommendations.append(
                "High supplier reliability significantly reduces delivery time variability. "
                "Prioritize reliable suppliers in procurement decisions."
            )
        
        if effects['reliability_quality']['adjusted_effect'] > 0.1:
            recommendations.append(
                "Reliable suppliers provide better quality scores. "
                "Consider reliability as a key factor in supplier evaluation."
            )
        
        # Check performance drivers
        delivery_effect = effects['delivery_performance']['adjusted_effect']
        quality_effect = effects['quality_performance']['adjusted_effect']
        
        if abs(delivery_effect) > abs(quality_effect):
            recommendations.append(
                "Delivery time has a stronger impact on supplier performance than quality. "
                "Focus on improving delivery consistency."
            )
        elif abs(quality_effect) > abs(delivery_effect):
            recommendations.append(
                "Quality has a stronger impact on supplier performance than delivery time. "
                "Emphasize quality control measures."
            )
        
        return recommendations
    
    def _generate_inventory_recommendations(self, effects: Dict[str, Dict]) -> List[str]:
        """Generate recommendations based on inventory causal analysis"""
        recommendations = []
        
        # Check safety stock effects
        stockout_effect = effects['safety_stockout']['adjusted_effect']
        holding_effect = effects['safety_holding']['adjusted_effect']
        
        if stockout_effect < -0.1:
            recommendations.append(
                "Increasing safety stock levels significantly reduces stockout rates. "
                "Consider optimizing safety stock levels to balance costs and service."
            )
        
        if holding_effect > 0.1:
            recommendations.append(
                "Higher safety stock levels increase holding costs. "
                "Implement dynamic safety stock optimization."
            )
        
        return recommendations
    
    def _generate_pricing_recommendations(self, effects: Dict[str, Dict]) -> List[str]:
        """Generate recommendations based on pricing causal analysis"""
        recommendations = []
        
        # Check price effects
        price_demand_effect = effects['price_demand']['adjusted_effect']
        price_revenue_effect = effects['price_revenue']['adjusted_effect']
        
        if price_demand_effect