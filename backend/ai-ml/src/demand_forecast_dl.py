"""
Deep Learning Models for Demand Forecasting and Supply Chain Optimization

This module implements advanced deep learning models for:
1. Time Series Demand Forecasting using LSTM and Transformer architectures
2. Supply Chain Optimization using Reinforcement Learning
3. Multi-Modal Fusion for incorporating various data sources
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout, Attention, MultiHeadAttention, LayerNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
import torch.optim as optim
from typing import Tuple, List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DemandForecastLSTM:
    """LSTM-based model for demand forecasting"""
    
    def __init__(self, sequence_length: int = 30, n_features: int = 10, 
                 lstm_units: List[int] = [50, 50], dropout_rate: float = 0.2):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.lstm_units = lstm_units
        self.dropout_rate = dropout_rate
        self.model = None
        self.scaler = MinMaxScaler()
        
    def build_model(self) -> tf.keras.Model:
        """Build LSTM model for demand forecasting"""
        inputs = Input(shape=(self.sequence_length, self.n_features))
        
        # First LSTM layer
        x = LSTM(self.lstm_units[0], return_sequences=True, dropout=self.dropout_rate)(inputs)
        
        # Additional LSTM layers
        for units in self.lstm_units[1:-1]:
            x = LSTM(units, return_sequences=True, dropout=self.dropout_rate)(x)
        
        # Last LSTM layer
        x = LSTM(self.lstm_units[-1], dropout=self.dropout_rate)(x)
        
        # Dense layers for prediction
        x = Dense(50, activation='relu')(x)
        x = Dropout(self.dropout_rate)(x)
        outputs = Dense(1, activation='linear')(x)  # Single value prediction
        
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        self.model = model
        return model
    
    def prepare_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare data for LSTM training"""
        # Scale the data
        scaled_data = self.scaler.fit_transform(data)
        
        X, y = [], []
        for i in range(self.sequence_length, len(scaled_data)):
            X.append(scaled_data[i-self.sequence_length:i])
            y.append(scaled_data[i, 0])  # Assuming first column is demand
            
        return np.array(X), np.array(y)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, 
              X_val: np.ndarray, y_val: np.ndarray, 
              epochs: int = 100, batch_size: int = 32) -> Dict[str, Any]:
        """Train the LSTM model"""
        if self.model is None:
            self.build_model()
        
        # Callbacks
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-7)
        
        # Train the model
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        return history.history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model"""
        if self.model is None:
            raise ValueError("Model not trained yet. Please train the model first.")
        
        predictions = self.model.predict(X)
        # Inverse transform to get actual values
        # Note: This assumes demand is the first feature
        dummy_array = np.zeros((len(predictions), self.n_features))
        dummy_array[:, 0] = predictions.flatten()
        actual_predictions = self.scaler.inverse_transform(dummy_array)[:, 0]
        
        return actual_predictions

class AttentionForecastingModel:
    """Transformer-based model for demand forecasting with attention mechanism"""
    
    def __init__(self, sequence_length: int = 30, n_features: int = 10, 
                 d_model: int = 128, n_heads: int = 8, n_layers: int = 4):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.d_model = d_model
        self.n_heads = n_heads
        self.n_layers = n_layers
        self.model = None
        self.scaler = MinMaxScaler()
        
    def build_model(self) -> tf.keras.Model:
        """Build Transformer model for demand forecasting"""
        inputs = Input(shape=(self.sequence_length, self.n_features))
        
        # Linear projection to d_model
        x = Dense(self.d_model)(inputs)
        
        # Transformer encoder layers
        for _ in range(self.n_layers):
            # Multi-head attention
            attn_output = MultiHeadAttention(
                num_heads=self.n_heads, 
                key_dim=self.d_model // self.n_heads
            )(x, x)
            
            # Add & Norm
            x = LayerNormalization()(x + attn_output)
            
            # Feed forward
            ffn = Dense(self.d_model * 4, activation='relu')(x)
            ffn = Dense(self.d_model)(ffn)
            
            # Add & Norm
            x = LayerNormalization()(x + ffn)
        
        # Global average pooling
        x = tf.keras.layers.GlobalAveragePooling1D()(x)
        
        # Output layers
        x = Dense(64, activation='relu')(x)
        x = Dropout(0.2)(x)
        outputs = Dense(1, activation='linear')(x)
        
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        self.model = model
        return model
    
    def prepare_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare data for Transformer training"""
        # Scale the data
        scaled_data = self.scaler.fit_transform(data)
        
        X, y = [], []
        for i in range(self.sequence_length, len(scaled_data)):
            X.append(scaled_data[i-self.sequence_length:i])
            y.append(scaled_data[i, 0])  # Assuming first column is demand
            
        return np.array(X), np.array(y)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, 
              X_val: np.ndarray, y_val: np.ndarray, 
              epochs: int = 100, batch_size: int = 32) -> Dict[str, Any]:
        """Train the Transformer model"""
        if self.model is None:
            self.build_model()
        
        # Callbacks
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-7)
        
        # Train the model
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        return history.history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model"""
        if self.model is None:
            raise ValueError("Model not trained yet. Please train the model first.")
        
        predictions = self.model.predict(X)
        # Inverse transform to get actual values
        # Note: This assumes demand is the first feature
        dummy_array = np.zeros((len(predictions), self.n_features))
        dummy_array[:, 0] = predictions.flatten()
        actual_predictions = self.scaler.inverse_transform(dummy_array)[:, 0]
        
        return actual_predictions

class SupplyChainOptimizationRL:
    """Reinforcement Learning model for supply chain optimization"""
    
    def __init__(self, state_dim: int, action_dim: int, hidden_dim: int = 128):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.hidden_dim = hidden_dim
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._build_model().to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        
    def _build_model(self) -> nn.Module:
        """Build the neural network for RL"""
        class PolicyNetwork(nn.Module):
            def __init__(self, state_dim, action_dim, hidden_dim):
                super(PolicyNetwork, self).__init__()
                self.network = nn.Sequential(
                    nn.Linear(state_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Linear(hidden_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Linear(hidden_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Linear(hidden_dim, action_dim),
                    nn.Softmax(dim=-1)
                )
            
            def forward(self, state):
                return self.network(state)
        
        return PolicyNetwork(self.state_dim, self.action_dim, self.hidden_dim)
    
    def select_action(self, state: np.ndarray) -> int:
        """Select action based on current state"""
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        probs = self.model(state)
        action_probs = torch.distributions.Categorical(probs)
        action = action_probs.sample()
        return action.item()
    
    def update(self, states: List[np.ndarray], actions: List[int], rewards: List[float]):
        """Update the policy based on collected experiences"""
        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        
        # Calculate loss
        probs = self.model(states)
        action_probs = torch.distributions.Categorical(probs)
        log_probs = action_probs.log_prob(actions)
        loss = (-log_probs * rewards).mean()
        
        # Update model
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item()

class MultiModalSupplyChainModel:
    """Multi-modal model combining various data sources for supply chain optimization"""
    
    def __init__(self, ts_features: int = 10, cat_features: int = 5, 
                 text_features: int = 100, sequence_length: int = 30):
        self.ts_features = ts_features
        self.cat_features = cat_features
        self.text_features = text_features
        self.sequence_length = sequence_length
        self.model = None
        
    def build_model(self) -> tf.keras.Model:
        """Build multi-modal model"""
        # Time series input (LSTM branch)
        ts_input = Input(shape=(self.sequence_length, self.ts_features), name='ts_input')
        ts_lstm = LSTM(64, return_sequences=True)(ts_input)
        ts_lstm = LSTM(32)(ts_lstm)
        
        # Categorical input (Dense branch)
        cat_input = Input(shape=(self.cat_features,), name='cat_input')
        cat_dense = Dense(32, activation='relu')(cat_input)
        cat_dense = Dense(16, activation='relu')(cat_dense)
        
        # Text input (Dense branch)
        text_input = Input(shape=(self.text_features,), name='text_input')
        text_dense = Dense(128, activation='relu')(text_input)
        text_dense = Dense(64, activation='relu')(text_dense)
        text_dense = Dense(32, activation='relu')(text_dense)
        
        # Combine all branches
        combined = tf.keras.layers.concatenate([ts_lstm, cat_dense, text_dense])
        
        # Final dense layers
        combined = Dense(64, activation='relu')(combined)
        combined = Dropout(0.3)(combined)
        combined = Dense(32, activation='relu')(combined)
        combined = Dropout(0.2)(combined)
        
        # Output layers for different tasks
        demand_output = Dense(1, activation='linear', name='demand_output')(combined)
        inventory_output = Dense(1, activation='linear', name='inventory_output')(combined)
        risk_output = Dense(1, activation='sigmoid', name='risk_output')(combined)
        
        model = Model(
            inputs=[ts_input, cat_input, text_input],
            outputs=[demand_output, inventory_output, risk_output]
        )
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss={
                'demand_output': 'mse',
                'inventory_output': 'mse',
                'risk_output': 'binary_crossentropy'
            },
            metrics={
                'demand_output': 'mae',
                'inventory_output': 'mae',
                'risk_output': 'accuracy'
            }
        )
        
        self.model = model
        return model
    
    def train(self, X_train: Dict[str, np.ndarray], 
              y_train: Dict[str, np.ndarray],
              X_val: Dict[str, np.ndarray], 
              y_val: Dict[str, np.ndarray],
              epochs: int = 100, batch_size: int = 32) -> Dict[str, Any]:
        """Train the multi-modal model"""
        if self.model is None:
            self.build_model()
        
        # Callbacks
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-7)
        
        # Train the model
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        return history.history

# Example usage
if __name__ == "__main__":
    # Example usage of the models
    logger.info("Initializing deep learning models for supply chain optimization")
    
    # Example data generation for demonstration
    np.random.seed(42)
    n_samples = 1000
    
    # Generate sample time series data
    dates = pd.date_range('2020-01-01', periods=n_samples, freq='D')
    demand_data = np.random.poisson(100, n_samples) + np.sin(np.arange(n_samples) * 2 * np.pi / 365) * 20
    price_data = 10 + np.random.normal(0, 1, n_samples)
    marketing_data = np.random.exponential(5, n_samples)
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'demand': demand_data,
        'price': price_data,
        'marketing_spend': marketing_data,
        'competitor_price': price_data + np.random.normal(0, 0.5, n_samples),
        'inventory_level': np.random.poisson(500, n_samples),
        'lead_time': np.random.exponential(5, n_samples),
        'season': np.sin(np.arange(n_samples) * 2 * np.pi / 90),
        'promo_flag': np.random.binomial(1, 0.1, n_samples),
        'economic_index': np.random.normal(100, 10, n_samples)
    })
    
    # LSTM Model Example
    logger.info("Training LSTM model for demand forecasting")
    lstm_model = DemandForecastLSTM(sequence_length=30, n_features=10)
    
    # Prepare data
    feature_columns = ['demand', 'price', 'marketing_spend', 'competitor_price', 
                      'inventory_level', 'lead_time', 'season', 'promo_flag', 
                      'economic_index', 'dummy_feature']
    
    # Add dummy feature to match n_features
    df['dummy_feature'] = np.random.normal(0, 1, len(df))
    
    # Split data
    train_size = int(0.8 * len(df))
    train_data = df[feature_columns].iloc[:train_size]
    test_data = df[feature_columns].iloc[train_size:]
    
    # Prepare training data
    X_train, y_train = lstm_model.prepare_data(train_data)
    X_test, y_test = lstm_model.prepare_data(test_data)
    
    # Split training data for validation
    val_size = int(0.2 * len(X_train))
    X_val, y_val = X_train[-val_size:], y_train[-val_size:]
    X_train, y_train = X_train[:-val_size], y_train[:-val_size]
    
    # Train model
    history = lstm_model.train(X_train, y_train, X_val, y_val, epochs=50, batch_size=32)
    logger.info("LSTM model training completed")
    
    # Make predictions
    predictions = lstm_model.predict(X_test[:10])
    logger.info(f"LSTM Predictions: {predictions}")
    
    # Transformer Model Example
    logger.info("Training Transformer model for demand forecasting")
    transformer_model = AttentionForecastingModel(sequence_length=30, n_features=10)
    
    # Prepare data for transformer
    X_train_t, y_train_t = transformer_model.prepare_data(train_data)
    X_test_t, y_test_t = transformer_model.prepare_data(test_data)
    
    # Split training data for validation
    X_val_t, y_val_t = X_train_t[-val_size:], y_train_t[-val_size:]
    X_train_t, y_train_t = X_train_t[:-val_size], y_train_t[:-val_size]
    
    # Train model
    history_t = transformer_model.train(X_train_t, y_train_t, X_val_t, y_val_t, epochs=50, batch_size=32)
    logger.info("Transformer model training completed")
    
    # Make predictions
    predictions_t = transformer_model.predict(X_test_t[:10])
    logger.info(f"Transformer Predictions: {predictions_t}")
    
    logger.info("Deep learning models for demand forecasting initialized successfully")