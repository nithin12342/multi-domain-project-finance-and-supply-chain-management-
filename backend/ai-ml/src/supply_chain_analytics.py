import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
import joblib

class SupplyChainAnalytics:
    def __init__(self):
        self.demand_model = None
        self.inventory_model = None
        self.risk_model = None
        self.scaler = StandardScaler()

    def train_demand_forecasting(self, historical_data):
        """Train model for demand forecasting"""
        X = historical_data[['season', 'price', 'marketing_spend', 'competitor_price']]
        y = historical_data['demand']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.demand_model = RandomForestRegressor(n_estimators=100)
        self.demand_model.fit(X_train_scaled, y_train)
        
        predictions = self.demand_model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, predictions)
        print(f'Demand Forecast MSE: {mse}')
        
        # Save the model
        joblib.dump(self.demand_model, 'models/demand_forecast_model.joblib')

    def train_inventory_optimization(self, inventory_data):
        """Train model for inventory optimization"""
        X = inventory_data[['demand_rate', 'lead_time', 'holding_cost', 'stockout_cost']]
        y = inventory_data['optimal_quantity']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.inventory_model = RandomForestRegressor(n_estimators=100)
        self.inventory_model.fit(X_train_scaled, y_train)
        
        predictions = self.inventory_model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, predictions)
        print(f'Inventory Optimization MSE: {mse}')
        
        # Save the model
        joblib.dump(self.inventory_model, 'models/inventory_optimization_model.joblib')

    def train_risk_assessment(self, supplier_data):
        """Train model for supplier risk assessment"""
        X = supplier_data[['delivery_time', 'quality_score', 'financial_stability', 'geo_political_risk']]
        y = supplier_data['risk_level']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.risk_model = RandomForestClassifier(n_estimators=100)
        self.risk_model.fit(X_train_scaled, y_train)
        
        predictions = self.risk_model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, predictions)
        print(f'Risk Assessment Accuracy: {accuracy}')
        
        # Save the model
        joblib.dump(self.risk_model, 'models/risk_assessment_model.joblib')

    def predict_demand(self, features):
        """Predict future demand"""
        if self.demand_model is None:
            self.demand_model = joblib.load('models/demand_forecast_model.joblib')
        
        features_scaled = self.scaler.transform(features)
        return self.demand_model.predict(features_scaled)

    def optimize_inventory(self, features):
        """Optimize inventory levels"""
        if self.inventory_model is None:
            self.inventory_model = joblib.load('models/inventory_optimization_model.joblib')
        
        features_scaled = self.scaler.transform(features)
        return self.inventory_model.predict(features_scaled)

    def assess_risk(self, features):
        """Assess supplier risk"""
        if self.risk_model is None:
            self.risk_model = joblib.load('models/risk_assessment_model.joblib')
        
        features_scaled = self.scaler.transform(features)
        return self.risk_model.predict(features_scaled)

    def analyze_supply_chain_performance(self, data):
        """Analyze overall supply chain performance"""
        performance_metrics = {
            'delivery_time_avg': np.mean(data['delivery_time']),
            'delivery_time_std': np.std(data['delivery_time']),
            'order_fulfillment_rate': np.mean(data['fulfilled']) * 100,
            'inventory_turnover': np.sum(data['sales']) / np.mean(data['inventory']),
            'stockout_rate': np.mean(data['stockout']) * 100
        }
        return performance_metrics

    def generate_optimization_recommendations(self, performance_metrics, thresholds):
        """Generate recommendations based on performance metrics"""
        recommendations = []
        
        if performance_metrics['delivery_time_std'] > thresholds['delivery_time_std']:
            recommendations.append("High delivery time variability detected. Consider diversifying suppliers.")
        
        if performance_metrics['order_fulfillment_rate'] < thresholds['order_fulfillment_rate']:
            recommendations.append("Low order fulfillment rate. Review inventory management strategy.")
        
        if performance_metrics['stockout_rate'] > thresholds['stockout_rate']:
            recommendations.append("High stockout rate. Increase safety stock levels.")
        
        return recommendations
