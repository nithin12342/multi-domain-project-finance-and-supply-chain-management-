"""
Time Series Forecasting for Supply Chain Analytics

This module implements advanced time series forecasting techniques for supply chain applications,
including demand forecasting, inventory optimization, and financial planning.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# For time series analysis, we'll use a simplified approach
# In practice, you would use: from statsmodels.tsa import ...

class TimeSeriesForecaster:
    """Advanced time series forecaster for supply chain applications"""
    
    def __init__(self):
        self.models = {}
        self.forecasts = {}
    
    def prepare_time_series_data(self, data: pd.DataFrame, target_col: str, 
                               date_col: Optional[str] = None) -> pd.Series:
        """
        Prepare time series data for forecasting
        
        Args:
            data: DataFrame with time series data
            target_col: Column name for target variable
            date_col: Column name for date/time (optional)
            
        Returns:
            Prepared time series as pandas Series
        """
        if date_col:
            ts_data = data.set_index(pd.to_datetime(data[date_col]))[target_col]
        else:
            ts_data = data[target_col]
        
        # Handle missing values
        ts_data = ts_data.fillna(method='ffill').fillna(method='bfill')
        
        # Ensure regular frequency
        if not ts_data.index.is_monotonic_increasing:
            ts_data = ts_data.sort_index()
        
        return ts_data
    
    def decompose_time_series(self, ts_data: pd.Series) -> Dict[str, pd.Series]:
        """
        Decompose time series into trend, seasonal, and residual components (simplified)
        
        Args:
            ts_data: Time series data
            
        Returns:
            Dictionary with decomposed components
        """
        # Simple decomposition using moving averages
        trend = ts_data.rolling(window=12, center=True).mean()
        seasonal = ts_data - trend
        residual = ts_data - trend - seasonal.rolling(window=12, center=True).mean()
        
        return {
            'trend': trend,
            'seasonal': seasonal,
            'residual': residual,
            'original': ts_data
        }
    
    def exponential_smoothing_forecast(self, ts_data: pd.Series, 
                                    alpha: float = 0.3, beta: float = 0.3, 
                                    gamma: float = 0.3, seasonal_periods: int = 12,
                                    forecast_horizon: int = 12) -> Dict[str, Any]:
        """
        Exponential smoothing forecast (Holt-Winters method - simplified)
        
        Args:
            ts_data: Time series data
            alpha: Smoothing parameter for level
            beta: Smoothing parameter for trend
            gamma: Smoothing parameter for seasonality
            seasonal_periods: Number of periods in a season
            forecast_horizon: Number of periods to forecast
            
        Returns:
            Dictionary with forecast results
        """
        # Initialize components
        n = len(ts_data)
        level = np.zeros(n)
        trend = np.zeros(n)
        seasonal = np.zeros(n)
        forecast = np.zeros(n)
        
        # Initial values
        level[0] = ts_data.iloc[0]
        trend[0] = 0
        seasonal[:seasonal_periods] = ts_data.iloc[:seasonal_periods] - level[0]
        
        # Holt-Winters algorithm
        for i in range(seasonal_periods, n):
            # Level equation
            level[i] = alpha * (ts_data.iloc[i] - seasonal[i - seasonal_periods]) + \
                      (1 - alpha) * (level[i-1] + trend[i-1])
            
            # Trend equation
            trend[i] = beta * (level[i] - level[i-1]) + (1 - beta) * trend[i-1]
            
            # Seasonal equation
            seasonal[i] = gamma * (ts_data.iloc[i] - level[i]) + \
                         (1 - gamma) * seasonal[i - seasonal_periods]
            
            # Forecast equation
            forecast[i] = level[i] + trend[i] + seasonal[i - seasonal_periods]
        
        # Future forecasts
        future_forecasts = []
        for i in range(1, forecast_horizon + 1):
            seasonal_idx = (n - seasonal_periods + (i - 1) % seasonal_periods)
            future_value = level[-1] + i * trend[-1] + seasonal[seasonal_idx]
            future_forecasts.append(future_value)
        
        # Create future dates
        last_date = ts_data.index[-1]
        freq = pd.infer_freq(ts_data.index)
        if freq is None:
            freq = 'D'  # Default to daily
        
        future_dates = pd.date_range(start=last_date, periods=forecast_horizon + 1, 
                                   freq=freq)[1:]
        
        return {
            'forecast': pd.Series(future_forecasts, index=future_dates),
            'level': level,
            'trend': trend,
            'seasonal': seasonal,
            'fitted_values': forecast,
            'parameters': {'alpha': alpha, 'beta': beta, 'gamma': gamma}
        }
    
    def arima_forecast(self, ts_data: pd.Series, order: Tuple[int, int, int] = (1, 1, 1),
                      forecast_horizon: int = 12) -> Dict[str, Any]:
        """
        ARIMA forecast (simplified implementation)
        
        Args:
            ts_data: Time series data
            order: ARIMA order (p, d, q)
            forecast_horizon: Number of periods to forecast
            
        Returns:
            Dictionary with forecast results
        """
        p, d, q = order
        
        # Difference the series if needed
        diff_data = ts_data
        for _ in range(d):
            diff_data = diff_data.diff().dropna()
        
        # Simple AR model (using last p values)
        n = len(diff_data)
        forecasts = []
        
        for i in range(n, n + forecast_horizon):
            if i < p:
                # Not enough data, use mean
                forecast_val = diff_data.mean()
            else:
                # Use AR model
                recent_values = diff_data.iloc[-p:].values
                # Simple weights (in practice, estimate using regression)
                weights = np.array([1/(j+1) for j in range(p)])
                weights = weights / weights.sum()  # Normalize
                forecast_val = np.dot(recent_values, weights)
            
            forecasts.append(forecast_val)
        
        # Integrate back if differenced
        if d > 0:
            # This is a simplified integration
            last_value = ts_data.iloc[-1]
            integrated_forecasts = [last_value + forecasts[0]]
            for i in range(1, len(forecasts)):
                integrated_forecasts.append(integrated_forecasts[-1] + forecasts[i])
            forecasts = integrated_forecasts
        
        # Create future dates
        last_date = ts_data.index[-1]
        freq = pd.infer_freq(ts_data.index)
        if freq is None:
            freq = 'D'  # Default to daily
        
        future_dates = pd.date_range(start=last_date, periods=forecast_horizon + 1, 
                                   freq=freq)[1:]
        
        return {
            'forecast': pd.Series(forecasts, index=future_dates),
            'order': order,
            'aic': self._calculate_aic(ts_data, forecasts[:len(ts_data)], order)
        }
    
    def _calculate_aic(self, actual: pd.Series, predicted: pd.Series, 
                      order: Tuple[int, int, int]) -> float:
        """Calculate Akaike Information Criterion (simplified)"""
        p, d, q = order
        n = len(actual)
        
        # Calculate residuals
        residuals = actual - predicted[:len(actual)]
        ssr = np.sum(residuals ** 2)
        
        # AIC formula
        k = p + q + 1  # Number of parameters
        aic = n * np.log(ssr / n) + 2 * k
        return aic
    
    def ensemble_forecast(self, ts_data: pd.Series, methods: Optional[List[str]] = None,
                         weights: Optional[List[float]] = None,
                         forecast_horizon: int = 12) -> Dict[str, Any]:
        """
        Ensemble forecast combining multiple methods
        
        Args:
            ts_data: Time series data
            methods: List of forecasting methods to use
            weights: Weights for each method (if None, equal weights)
            forecast_horizon: Number of periods to forecast
            
        Returns:
            Dictionary with ensemble forecast results
        """
        if methods is None:
            methods = ['exponential_smoothing', 'arima']
        
        if weights is None:
            weights = [1/len(methods)] * len(methods)
        
        # Generate forecasts from each method
        forecasts = {}
        for method in methods:
            if method == 'exponential_smoothing':
                result = self.exponential_smoothing_forecast(ts_data, forecast_horizon=forecast_horizon)
                forecasts[method] = result['forecast']
            elif method == 'arima':
                result = self.arima_forecast(ts_data, forecast_horizon=forecast_horizon)
                forecasts[method] = result['forecast']
        
        # Combine forecasts using weights
        if forecasts:
            # Align all forecasts to the same index
            common_index = None
            for forecast in forecasts.values():
                if common_index is None:
                    common_index = forecast.index
                else:
                    common_index = common_index.union(forecast.index)
            
            # Reindex all forecasts to common index
            aligned_forecasts = {}
            for method, forecast in forecasts.items():
                aligned_forecasts[method] = forecast.reindex(common_index)
            
            # Calculate weighted average
            ensemble_forecast = pd.Series(0, index=common_index)
            total_weight = sum(weights[:len(aligned_forecasts)])
            
            for i, (method, forecast) in enumerate(aligned_forecasts.items()):
                if i < len(weights):
                    weight = weights[i] / total_weight
                    ensemble_forecast += forecast * weight
            
            return {
                'forecast': ensemble_forecast,
                'individual_forecasts': forecasts,
                'weights': weights[:len(forecasts)],
                'methods': list(forecasts.keys())
            }
        else:
            return {'forecast': pd.Series(), 'individual_forecasts': {}, 'weights': [], 'methods': []}
    
    def evaluate_forecast(self, actual: pd.Series, predicted: pd.Series) -> Dict[str, float]:
        """
        Evaluate forecast accuracy
        
        Args:
            actual: Actual values
            predicted: Predicted values
            
        Returns:
            Dictionary with evaluation metrics
        """
        # Align series
        common_index = actual.index.intersection(predicted.index)
        actual_aligned = actual[common_index]
        predicted_aligned = predicted[common_index]
        
        # Calculate metrics
        residuals = actual_aligned - predicted_aligned
        mse = np.mean(residuals ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(residuals))
        mape = np.mean(np.abs(residuals / actual_aligned)) * 100
        
        # Mean absolute scaled error (MASE)
        # Naive forecast (random walk)
        naive_forecast = actual_aligned.shift(1)
        naive_residuals = actual_aligned - naive_forecast
        naive_mae = np.mean(np.abs(naive_residuals.dropna()))
        mase = mae / naive_mae if naive_mae != 0 else np.inf
        
        return {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'mape': mape,
            'mase': mase
        }

class SupplyChainTimeSeriesAnalyzer:
    """High-level time series analyzer for supply chain scenarios"""
    
    def __init__(self):
        self.forecaster = TimeSeriesForecaster()
        self.results = {}
    
    def forecast_demand(self, data: pd.DataFrame, product_id: Optional[str] = None,
                       forecast_horizon: int = 12) -> Dict[str, Any]:
        """
        Forecast demand for supply chain planning
        
        Args:
            data: DataFrame with demand history
            product_id: Specific product to forecast (optional)
            forecast_horizon: Number of periods to forecast
            
        Returns:
            Dictionary with demand forecast results
        """
        # Filter by product if specified
        if product_id:
            product_data = data[data['product_id'] == product_id]
        else:
            product_data = data
        
        # Prepare time series data
        ts_data = self.forecaster.prepare_time_series_data(
            product_data, 'demand', 'date'
        )
        
        # Decompose time series
        decomposition = self.forecaster.decompose_time_series(ts_data)
        
        # Generate forecasts using multiple methods
        exp_smooth_result = self.forecaster.exponential_smoothing_forecast(
            ts_data, forecast_horizon=forecast_horizon
        )
        
        arima_result = self.forecaster.arima_forecast(
            ts_data, order=(2, 1, 1), forecast_horizon=forecast_horizon
        )
        
        # Ensemble forecast
        ensemble_result = self.forecaster.ensemble_forecast(
            ts_data, 
            methods=['exponential_smoothing', 'arima'],
            weights=[0.6, 0.4],  # Weight exponential smoothing higher
            forecast_horizon=forecast_horizon
        )
        
        # Evaluate forecasts (using historical data for validation)
        historical_forecast = exp_smooth_result['fitted_values']
        evaluation = self.forecaster.evaluate_forecast(
            ts_data.iloc[len(historical_forecast):], 
            pd.Series(historical_forecast, index=ts_data.index[len(historical_forecast):])
        )
        
        results = {
            'product_id': product_id,
            'decomposition': decomposition,
            'exponential_smoothing': exp_smooth_result,
            'arima': arima_result,
            'ensemble': ensemble_result,
            'evaluation': evaluation,
            'recommendations': self._generate_demand_recommendations(evaluation)
        }
        
        self.results[f'demand_forecast_{product_id}'] = results
        return results
    
    def forecast_inventory_needs(self, data: pd.DataFrame, 
                               forecast_horizon: int = 12) -> Dict[str, Any]:
        """
        Forecast inventory needs for supply chain optimization
        
        Args:
            data: DataFrame with inventory and demand data
            forecast_horizon: Number of periods to forecast
            
        Returns:
            Dictionary with inventory forecast results
        """
        # Prepare time series data for inventory levels
        inventory_ts = self.forecaster.prepare_time_series_data(
            data, 'inventory_level', 'date'
        )
        
        # Prepare time series data for demand
        demand_ts = self.forecaster.prepare_time_series_data(
            data, 'demand', 'date'
        )
        
        # Forecast demand
        demand_forecast = self.forecaster.exponential_smoothing_forecast(
            demand_ts, forecast_horizon=forecast_horizon
        )
        
        # Calculate safety stock requirements
        demand_std = demand_ts.std()
        lead_time = data['lead_time'].mean() if 'lead_time' in data.columns else 7
        service_level = 1.65  # 95% service level
        safety_stock = service_level * demand_std * np.sqrt(lead_time)
        
        # Calculate reorder point
        avg_demand = demand_ts.mean()
        reorder_point = avg_demand * lead_time + safety_stock
        
        # Project future inventory needs
        current_inventory = inventory_ts.iloc[-1]
        future_inventory = []
        future_dates = demand_forecast['forecast'].index
        
        inventory_level = current_inventory
        for i, (date, demand) in enumerate(demand_forecast['forecast'].items()):
            inventory_level -= demand
            future_inventory.append(inventory_level)
            
            # Check if reorder is needed
            if inventory_level <= reorder_point and i < len(future_inventory) - 1:
                # Reorder (simplified - assume immediate replenishment)
                inventory_level += reorder_point
        
        inventory_projection = pd.Series(future_inventory, index=future_dates)
        
        results = {
            'inventory_projection': inventory_projection,
            'demand_forecast': demand_forecast['forecast'],
            'safety_stock': safety_stock,
            'reorder_point': reorder_point,
            'current_inventory': current_inventory,
            'recommendations': self._generate_inventory_recommendations(
                inventory_projection, safety_stock, reorder_point
            )
        }
        
        self.results['inventory_forecast'] = results
        return results
    
    def forecast_financial_metrics(self, data: pd.DataFrame,
                                 forecast_horizon: int = 12) -> Dict[str, Any]:
        """
        Forecast financial metrics for supply chain finance
        
        Args:
            data: DataFrame with financial data
            forecast_horizon: Number of periods to forecast
            
        Returns:
            Dictionary with financial forecast results
        """
        # Forecast revenue
        revenue_ts = self.forecaster.prepare_time_series_data(
            data, 'revenue', 'date'
        )
        
        revenue_forecast = self.forecaster.exponential_smoothing_forecast(
            revenue_ts, forecast_horizon=forecast_horizon
        )
        
        # Forecast costs
        cost_ts = self.forecaster.prepare_time_series_data(
            data, 'total_cost', 'date'
        )
        
        cost_forecast = self.forecaster.exponential_smoothing_forecast(
            cost_ts, forecast_horizon=forecast_horizon
        )
        
        # Calculate profit forecast
        profit_forecast = revenue_forecast['forecast'] - cost_forecast['forecast']
        
        # Calculate financial ratios
        profit_margin = profit_forecast / revenue_forecast['forecast']
        cost_ratio = cost_forecast['forecast'] / revenue_forecast['forecast']
        
        results = {
            'revenue_forecast': revenue_forecast['forecast'],
            'cost_forecast': cost_forecast['forecast'],
            'profit_forecast': profit_forecast,
            'profit_margin': profit_margin,
            'cost_ratio': cost_ratio,
            'recommendations': self._generate_financial_recommendations(
                revenue_forecast['forecast'],
                cost_forecast['forecast'],
                profit_forecast
            )
        }
        
        self.results['financial_forecast'] = results
        return results
    
    def _generate_demand_recommendations(self, evaluation: Dict[str, float]) -> List[str]:
        """Generate recommendations based on demand forecast evaluation"""
        recommendations = []
        
        if evaluation['mape'] > 20:
            recommendations.append(
                "High forecast error detected. Consider incorporating external factors "
                "such as market trends, promotions, or economic indicators."
            )
        
        if evaluation['mase'] > 1:
            recommendations.append(
                "Forecast performance is worse than naive method. Review model selection "
                "and consider seasonal or trend components."
            )
        
        return recommendations
    
    def _generate_inventory_recommendations(self, inventory_projection: pd.Series,
                                          safety_stock: float, reorder_point: float) -> List[str]:
        """Generate recommendations based on inventory forecast"""
        recommendations = []
        
        # Check for stockouts
        min_inventory = inventory_projection.min()
        if min_inventory < 0:
            recommendations.append(
                f"Projected stockout of {abs(min_inventory):.0f} units detected. "
                "Consider increasing safety stock or adjusting reorder point."
            )
        
        # Check safety stock adequacy
        if safety_stock < inventory_projection.std():
            recommendations.append(
                "Current safety stock may be insufficient for demand variability. "
                "Consider increasing safety stock levels."
            )
        
        return recommendations
    
    def _generate_financial_recommendations(self, revenue_forecast: pd.Series,
                                          cost_forecast: pd.Series,
                                          profit_forecast: pd.Series) -> List[str]:
        """Generate recommendations based on financial forecast"""
        recommendations = []
        
        # Check profit trends
        profit_growth = (profit_forecast.iloc[-1] - profit_forecast.iloc[0]) / profit_forecast.iloc[0] * 100
        
        if profit_growth < 0:
            recommendations.append(
                f"Projected profit decline of {abs(profit_growth):.1f}%. "
                "Review cost structure and pricing strategy."
            )
        elif profit_growth < 5:
            recommendations.append(
                f"Modest profit growth of {profit_growth:.1f}%. "
                "Explore opportunities for revenue growth or cost optimization."
            )
        
        # Check cost trends
        cost_growth = (cost_forecast.iloc[-1] - cost_forecast.iloc[0]) / cost_forecast.iloc[0] * 100
        revenue_growth = (revenue_forecast.iloc[-1] - revenue_forecast.iloc[0]) / revenue_forecast.iloc[0] * 100
        
        if cost_growth > revenue_growth:
            recommendations.append(
                "Costs are growing faster than revenue. Focus on cost control measures."
            )
        
        return recommendations