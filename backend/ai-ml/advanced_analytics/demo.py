"""
Demo script for Advanced Analytics Pipeline
"""

import sys
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from ai_ml.advanced_analytics.analytics_pipeline import AdvancedAnalyticsPipeline

def main():
    """Main demo function"""
    print("=== Advanced Analytics Pipeline Demo ===\n")
    
    # Initialize the analytics pipeline
    print("1. Initializing Advanced Analytics Pipeline...")
    pipeline = AdvancedAnalyticsPipeline()
    
    # Generate sample supply chain data
    print("2. Generating sample supply chain data...")
    sample_data = _generate_sample_data()
    
    # Run comprehensive supply chain analysis
    print("3. Running comprehensive supply chain analysis...")
    results = pipeline.run_supply_chain_analysis(sample_data)
    
    # Display key results
    print("\n=== ANALYSIS RESULTS ===")
    
    # Causal Analysis Summary
    print("\n1. Causal Inference Analysis:")
    causal_results = results.get('causal_analysis', {})
    for category, analysis in causal_results.items():
        print(f"   {category.replace('_', ' ').title()}:")
        if 'recommendations' in analysis:
            for rec in analysis['recommendations'][:2]:  # Show first 2 recommendations
                print(f"     • {rec}")
    
    # Time Series Forecasting Summary
    print("\n2. Time Series Forecasting:")
    forecast_results = results.get('time_series_forecast', {})
    for category, forecasts in forecast_results.items():
        print(f"   {category.replace('_', ' ').title()}:")
        if isinstance(forecasts, dict) and 'recommendations' in forecasts:
            for rec in forecasts['recommendations'][:2]:  # Show first 2 recommendations
                print(f"     • {rec}")
        elif isinstance(forecasts, dict):
            for sub_category, sub_forecasts in forecasts.items():
                if isinstance(sub_forecasts, dict) and 'recommendations' in sub_forecasts:
                    print(f"     {sub_category.replace('_', ' ').title()}:")
                    for rec in sub_forecasts['recommendations'][:1]:  # Show first recommendation
                        print(f"       • {rec}")
    
    # Strategic Insights
    print("\n3. Strategic Insights:")
    insights = results.get('insights', [])
    for i, insight in enumerate(insights[:5]):  # Show first 5 insights
        print(f"   {i+1}. {insight}")
    
    # Key Recommendations
    print("\n4. Key Recommendations:")
    recommendations = results.get('recommendations', [])
    for i, rec in enumerate(recommendations[:5]):  # Show first 5 recommendations
        priority = rec.get('priority', 'medium').upper()
        impact = rec.get('impact', 'medium').upper()
        print(f"   [{priority}/{impact}] {rec.get('text', '')}")
    
    # Generate and display report
    print("\n5. Generating detailed report...")
    report = pipeline.generate_report()
    print("\n=== EXECUTIVE SUMMARY ===")
    # Extract and show just the executive summary
    lines = report.split('\n')
    summary_lines = []
    in_summary = False
    for line in lines:
        if "EXECUTIVE SUMMARY" in line:
            in_summary = True
            summary_lines.append(line)
        elif in_summary and line.strip() == "":
            summary_lines.append(line)
        elif in_summary and "CAUSAL ANALYSIS SUMMARY" in line:
            break
        elif in_summary:
            summary_lines.append(line)
    
    print('\n'.join(summary_lines))
    
    # Export results
    print("\n6. Exporting results...")
    pipeline.export_results('advanced_analytics_demo_results.json')
    print("   Results exported to 'advanced_analytics_demo_results.json'")
    
    print("\n=== Demo Complete ===")

def _generate_sample_data() -> dict:
    """Generate sample supply chain data for demonstration"""
    
    # Generate supplier data
    suppliers = []
    for i in range(50):
        supplier = {
            'id': f'SUP{i:03d}',
            'reliability': np.random.beta(2, 1),  # Most suppliers are reliable
            'delivery_time': np.random.normal(5, 2),  # Average 5 days
            'quality_score': np.random.beta(4, 1),  # Most have good quality
            'cost': np.random.normal(100, 20),  # Average cost
            'geo_risk': np.random.beta(1, 3),  # Most have low geo risk
            'performance_score': np.random.beta(3, 1)  # Most perform well
        }
        suppliers.append(supplier)
    
    # Generate demand history (2 years of monthly data)
    demand_history = []
    base_date = datetime(2022, 1, 1)
    for i in range(24):  # 24 months
        date = base_date + timedelta(days=30*i)
        # Seasonal pattern with trend
        seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * i / 12)
        trend_factor = 1 + 0.02 * i  # 2% growth per month
        noise = np.random.normal(1, 0.1)
        
        demand_a = int(1000 * seasonal_factor * trend_factor * noise)
        demand_b = int(800 * seasonal_factor * trend_factor * noise)
        
        demand_history.append({
            'date': date.isoformat(),
            'product_A': max(0, demand_a),
            'product_B': max(0, demand_b)
        })
    
    # Generate inventory data
    inventory_data = []
    current_inventory = 5000
    for i in range(24):
        date = base_date + timedelta(days=30*i)
        # Simulate inventory changes
        demand = demand_history[i]['product_A'] + demand_history[i]['product_B']
        receipts = int(demand * 1.1)  # 10% safety stock
        current_inventory = max(0, current_inventory - demand + receipts)
        
        inventory_data.append({
            'date': date.isoformat(),
            'inventory_level': current_inventory,
            'demand': demand,
            'receipts': receipts,
            'safety_stock': int(demand * 0.2)
        })
    
    # Generate financial data
    financial_data = []
    revenue = 100000
    for i in range(24):
        date = base_date + timedelta(days=30*i)
        # Revenue growth with seasonality
        seasonal_factor = 1 + 0.15 * np.sin(2 * np.pi * i / 12)
        growth_factor = 1 + 0.015 * i  # 1.5% growth per month
        revenue = int(revenue * seasonal_factor * growth_factor)
        
        # Costs grow slightly slower than revenue
        cost_factor = 1 + 0.012 * i  # 1.2% growth per month
        costs = int(revenue * 0.7 * cost_factor)
        
        financial_data.append({
            'date': date.isoformat(),
            'revenue': revenue,
            'total_cost': costs,
            'gross_profit': revenue - costs,
            'operating_expenses': int(revenue * 0.15)
        })
    
    return {
        'suppliers': suppliers,
        'demand_history': demand_history,
        'inventory_data': inventory_data,
        'financial_data': financial_data
    }

if __name__ == "__main__":
    main()