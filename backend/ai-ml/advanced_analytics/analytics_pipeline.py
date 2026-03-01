"""
Advanced Analytics Pipeline for Supply Chain Finance

This module integrates causal inference and time series forecasting to provide
comprehensive analytics for supply chain finance applications.
"""

import sys
import os
from typing import Dict, List, Any, Optional
import json
import warnings
warnings.filterwarnings('ignore')

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Import our custom modules
# Note: In a real implementation, these would be proper imports
# from .causal_inference import SupplyChainCausalAnalyzer
# from .time_series_forecasting import SupplyChainTimeSeriesAnalyzer

class AdvancedAnalyticsPipeline:
    """Main pipeline for advanced supply chain analytics"""
    
    def __init__(self):
        # In a real implementation, we would initialize the analyzers:
        # self.causal_analyzer = SupplyChainCausalAnalyzer()
        # self.time_series_analyzer = SupplyChainTimeSeriesAnalyzer()
        self.results = {}
        self.insights = []
    
    def run_supply_chain_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run comprehensive supply chain analysis
        
        Args:
            data: Dictionary containing all relevant data
            
        Returns:
            Dictionary with analysis results
        """
        print("Running Advanced Supply Chain Analytics Pipeline...")
        
        # 1. Causal Inference Analysis
        print("1. Performing Causal Inference Analysis...")
        causal_results = self._run_causal_analysis(data)
        
        # 2. Time Series Forecasting
        print("2. Performing Time Series Forecasting...")
        forecast_results = self._run_time_series_analysis(data)
        
        # 3. Generate Insights
        print("3. Generating Strategic Insights...")
        insights = self._generate_insights(causal_results, forecast_results)
        
        # 4. Create Recommendations
        print("4. Creating Actionable Recommendations...")
        recommendations = self._create_recommendations(causal_results, forecast_results, insights)
        
        # Compile results
        results = {
            'causal_analysis': causal_results,
            'time_series_forecast': forecast_results,
            'insights': insights,
            'recommendations': recommendations,
            'timestamp': self._get_current_timestamp()
        }
        
        self.results = results
        return results
    
    def _run_causal_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run causal inference analysis on supply chain data
        
        Args:
            data: Input data dictionary
            
        Returns:
            Causal analysis results
        """
        # In a real implementation, this would call the causal analyzer:
        # return self.causal_analyzer.analyze_supply_chain(data)
        
        # Simulated results for demonstration
        return {
            'supplier_performance': {
                'causal_effects': {
                    'reliability_delivery': {'adjusted_effect': -0.25},
                    'reliability_quality': {'adjusted_effect': 0.31},
                    'delivery_performance': {'adjusted_effect': -0.42},
                    'quality_performance': {'adjusted_effect': 0.38}
                },
                'recommendations': [
                    "High supplier reliability significantly reduces delivery time variability.",
                    "Quality has a stronger impact on supplier performance than delivery time."
                ]
            },
            'inventory_policy': {
                'causal_effects': {
                    'safety_stockout': {'adjusted_effect': -0.18},
                    'safety_holding': {'adjusted_effect': 0.22}
                },
                'recommendations': [
                    "Increasing safety stock levels significantly reduces stockout rates.",
                    "Higher safety stock levels increase holding costs."
                ]
            },
            'pricing_strategy': {
                'causal_effects': {
                    'price_demand': {'adjusted_effect': -0.15},
                    'price_revenue': {'adjusted_effect': 0.08},
                    'competitor_demand': {'adjusted_effect': 0.12}
                },
                'recommendations': [
                    "Price increases lead to decreased demand but may increase revenue per unit.",
                    "Competitor pricing has a positive effect on our demand (market growth)."
                ]
            }
        }
    
    def _run_time_series_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run time series forecasting analysis
        
        Args:
            data: Input data dictionary
            
        Returns:
            Time series analysis results
        """
        # In a real implementation, this would call the time series analyzer:
        # return self.time_series_analyzer.forecast_supply_chain_metrics(data)
        
        # Simulated results for demonstration
        return {
            'demand_forecast': {
                'product_A': {
                    'forecast': [1250, 1320, 1280, 1350, 1400, 1380],
                    'evaluation': {'mape': 12.5, 'mase': 0.8},
                    'recommendations': [
                        "Demand forecast accuracy is good (MAPE < 15%).",
                        "Consider incorporating promotional calendar for better accuracy."
                    ]
                },
                'product_B': {
                    'forecast': [850, 890, 870, 910, 930, 900],
                    'evaluation': {'mape': 18.2, 'mase': 1.2},
                    'recommendations': [
                        "Forecast performance is worse than naive method. Review model selection."
                    ]
                }
            },
            'inventory_forecast': {
                'projection': [5000, 4800, 4600, 4400, 4200, 4000],
                'safety_stock': 850,
                'reorder_point': 1200,
                'recommendations': [
                    "Projected stockout of 200 units in period 4. Increase safety stock.",
                    "Current safety stock may be insufficient for demand variability."
                ]
            },
            'financial_forecast': {
                'revenue': [125000, 132000, 128000, 135000, 140000, 138000],
                'costs': [85000, 89000, 87000, 91000, 93000, 90000],
                'profit': [40000, 43000, 41000, 44000, 47000, 48000],
                'profit_margin': [0.32, 0.326, 0.320, 0.326, 0.336, 0.348],
                'recommendations': [
                    "Projected profit growth of 20% over next 6 periods.",
                    "Profit margin improving - maintain current pricing strategy."
                ]
            }
        }
    
    def _generate_insights(self, causal_results: Dict[str, Any], 
                          forecast_results: Dict[str, Any]) -> List[str]:
        """
        Generate strategic insights from analysis results
        
        Args:
            causal_results: Results from causal analysis
            forecast_results: Results from time series analysis
            
        Returns:
            List of strategic insights
        """
        insights = []
        
        # Supplier insights
        supplier_effects = causal_results['supplier_performance']['causal_effects']
        if supplier_effects['reliability_delivery']['adjusted_effect'] < -0.2:
            insights.append("Supplier reliability is a key driver of delivery performance.")
        
        if supplier_effects['quality_performance']['adjusted_effect'] > 0.3:
            insights.append("Quality improvements have a significant positive impact on performance.")
        
        # Inventory insights
        inventory_effects = causal_results['inventory_policy']['causal_effects']
        if inventory_effects['safety_stockout']['adjusted_effect'] < -0.1:
            insights.append("Safety stock investments effectively reduce stockout risks.")
        
        # Pricing insights
        pricing_effects = causal_results['pricing_strategy']['causal_effects']
        if pricing_effects['price_demand']['adjusted_effect'] > -0.2:
            insights.append("Demand is relatively inelastic to price changes in current market.")
        
        # Forecast insights
        financial_forecast = forecast_results['financial_forecast']
        profit_growth = ((financial_forecast['profit'][-1] - financial_forecast['profit'][0]) / 
                        financial_forecast['profit'][0] * 100)
        if profit_growth > 15:
            insights.append("Strong projected profit growth indicates healthy business performance.")
        
        return insights
    
    def _create_recommendations(self, causal_results: Dict[str, Any], 
                              forecast_results: Dict[str, Any],
                              insights: List[str]) -> List[Dict[str, Any]]:
        """
        Create actionable recommendations based on analysis
        
        Args:
            causal_results: Results from causal analysis
            forecast_results: Results from time series analysis
            insights: Strategic insights
            
        Returns:
            List of recommendations with priority and impact scores
        """
        recommendations = []
        
        # Aggregate recommendations from all analyses
        all_recommendations = []
        
        # From causal analysis
        for analysis_type, results in causal_results.items():
            if 'recommendations' in results:
                all_recommendations.extend(results['recommendations'])
        
        # From forecast analysis
        for analysis_type, results in forecast_results.items():
            if isinstance(results, dict) and 'recommendations' in results:
                all_recommendations.extend(results['recommendations'])
            elif isinstance(results, dict):
                for sub_key, sub_results in results.items():
                    if isinstance(sub_results, dict) and 'recommendations' in sub_results:
                        all_recommendations.extend(sub_results['recommendations'])
        
        # Create structured recommendations with priority scores
        for i, rec_text in enumerate(all_recommendations):
            # Simple priority scoring (in practice, use more sophisticated methods)
            priority = 'high' if 'significant' in rec_text or 'stockout' in rec_text else 'medium'
            impact = 'high' if 'profit' in rec_text or 'revenue' in rec_text else 'medium'
            
            recommendations.append({
                'id': f'rec_{i+1}',
                'text': rec_text,
                'priority': priority,
                'impact': impact,
                'category': self._categorize_recommendation(rec_text),
                'implementation_effort': self._estimate_effort(rec_text)
            })
        
        # Sort by priority
        priority_order = {'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return recommendations
    
    def _categorize_recommendation(self, recommendation: str) -> str:
        """Categorize recommendation by business area"""
        if 'supplier' in recommendation.lower() or 'reliability' in recommendation.lower():
            return 'supplier_management'
        elif 'inventory' in recommendation.lower() or 'stockout' in recommendation.lower() or 'safety stock' in recommendation.lower():
            return 'inventory_optimization'
        elif 'price' in recommendation.lower() or 'revenue' in recommendation.lower() or 'profit' in recommendation.lower():
            return 'financial_performance'
        elif 'demand' in recommendation.lower() or 'forecast' in recommendation.lower():
            return 'demand_planning'
        else:
            return 'general'
    
    def _estimate_effort(self, recommendation: str) -> str:
        """Estimate implementation effort"""
        if 'increase' in recommendation.lower() or 'improve' in recommendation.lower():
            return 'medium'
        elif 'review' in recommendation.lower() or 'consider' in recommendation.lower():
            return 'low'
        else:
            return 'medium'
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def export_results(self, filepath: str) -> None:
        """
        Export results to JSON file
        
        Args:
            filepath: Path to export file
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            print(f"Results exported to {filepath}")
        except Exception as e:
            print(f"Error exporting results: {e}")
    
    def generate_report(self) -> str:
        """
        Generate a human-readable report
        
        Returns:
            Formatted report string
        """
        if not self.results:
            return "No analysis results available. Run analysis first."
        
        report = []
        report.append("=== ADVANCED SUPPLY CHAIN ANALYTICS REPORT ===\n")
        
        # Executive Summary
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 20)
        report.append(f"Analysis completed: {self.results.get('timestamp', 'N/A')}")
        report.append(f"Key insights identified: {len(self.results.get('insights', []))}")
        report.append(f"Actionable recommendations: {len(self.results.get('recommendations', []))}")
        report.append("")
        
        # Causal Analysis Summary
        report.append("CAUSAL ANALYSIS SUMMARY")
        report.append("-" * 25)
        causal_results = self.results.get('causal_analysis', {})
        for category, results in causal_results.items():
            report.append(f"{category.replace('_', ' ').title()}:")
            if 'recommendations' in results:
                for rec in results['recommendations']:
                    report.append(f"  • {rec}")
            report.append("")
        
        # Forecast Summary
        report.append("FORECAST ANALYSIS SUMMARY")
        report.append("-" * 27)
        forecast_results = self.results.get('time_series_forecast', {})
        for category, results in forecast_results.items():
            report.append(f"{category.replace('_', ' ').title()}:")
            if isinstance(results, dict) and 'recommendations' in results:
                for rec in results['recommendations']:
                    report.append(f"  • {rec}")
            elif isinstance(results, dict):
                for sub_key, sub_results in results.items():
                    if isinstance(sub_results, dict) and 'recommendations' in sub_results:
                        report.append(f"  {sub_key.replace('_', ' ').title()}:")
                        for rec in sub_results['recommendations']:
                            report.append(f"    • {rec}")
            report.append("")
        
        # Strategic Insights
        report.append("STRATEGIC INSIGHTS")
        report.append("-" * 18)
        insights = self.results.get('insights', [])
        for insight in insights:
            report.append(f"• {insight}")
        report.append("")
        
        # Recommendations
        report.append("ACTIONABLE RECOMMENDATIONS")
        report.append("-" * 27)
        recommendations = self.results.get('recommendations', [])
        for rec in recommendations:
            priority = rec.get('priority', 'medium').upper()
            impact = rec.get('impact', 'medium').upper()
            report.append(f"[{priority}/{impact}] {rec.get('text', '')}")
            report.append(f"  Category: {rec.get('category', 'general')}")
            report.append(f"  Effort: {rec.get('implementation_effort', 'medium')}")
            report.append("")
        
        return "\n".join(report)

# Example usage
if __name__ == "__main__":
    # Create pipeline instance
    pipeline = AdvancedAnalyticsPipeline()
    
    # Sample data (in practice, this would come from databases or APIs)
    sample_data = {
        'suppliers': [
            {'id': 'S001', 'reliability': 0.95, 'delivery_time': 5, 'quality_score': 4.8},
            {'id': 'S002', 'reliability': 0.85, 'delivery_time': 7, 'quality_score': 4.2}
        ],
        'demand_history': [
            {'date': '2023-01', 'product_A': 1200, 'product_B': 800},
            {'date': '2023-02', 'product_A': 1250, 'product_B': 820}
        ],
        'inventory_data': [
            {'date': '2023-01', 'level': 5000, 'demand': 1200},
            {'date': '2023-02', 'level': 4900, 'demand': 1250}
        ],
        'financial_data': [
            {'date': '2023-01', 'revenue': 120000, 'costs': 80000},
            {'date': '2023-02', 'revenue': 125000, 'costs': 82000}
        ]
    }
    
    # Run analysis
    results = pipeline.run_supply_chain_analysis(sample_data)
    
    # Generate and print report
    report = pipeline.generate_report()
    print(report)
    
    # Export results
    pipeline.export_results('supply_chain_analytics_results.json')