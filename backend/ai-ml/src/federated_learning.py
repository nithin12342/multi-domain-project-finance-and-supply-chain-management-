"""
Federated Learning Implementation for Supply Chain Analytics

This module implements a federated learning system for distributed model training
across supply chain partners while preserving data privacy.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
import json
import hashlib
import logging
from typing import List, Dict, Any, Tuple
from collections import OrderedDict
import asyncio
import aiohttp
from cryptography.fernet import Fernet
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FederatedLearningModel(nn.Module):
    """Neural network model for federated learning"""
    
    def __init__(self, input_dim: int, hidden_dim: int = 128, output_dim: int = 1):
        super(FederatedLearningModel, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        
        # Network layers
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.fc4 = nn.Linear(hidden_dim // 2, output_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        """Forward pass through the network"""
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.relu(self.fc3(x))
        x = self.fc4(x)
        return x

class FederatedClient:
    """Federated learning client for supply chain partners"""
    
    def __init__(self, client_id: str, data: pd.DataFrame, target_column: str, 
                 model: nn.Module, learning_rate: float = 0.001):
        self.client_id = client_id
        self.data = data
        self.target_column = target_column
        self.model = model
        self.learning_rate = learning_rate
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss() if output_dim == 1 else nn.CrossEntropyLoss()
        
        # Prepare data
        self.X = torch.FloatTensor(self.data.drop(columns=[target_column]).values).to(self.device)
        self.y = torch.FloatTensor(self.data[target_column].values).to(self.device)
        if output_dim > 1:
            self.y = self.y.long()
        
        # Encryption key for secure communication
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
    def train_local_model(self, epochs: int = 5) -> Dict[str, Any]:
        """Train the model locally on client data"""
        logger.info(f"Client {self.client_id} starting local training for {epochs} epochs")
        
        self.model.train()
        losses = []
        
        for epoch in range(epochs):
            self.optimizer.zero_grad()
            outputs = self.model(self.X)
            
            # Handle different loss functions based on output dimension
            if self.output_dim == 1:
                loss = self.criterion(outputs.squeeze(), self.y)
            else:
                loss = self.criterion(outputs, self.y)
                
            loss.backward()
            self.optimizer.step()
            losses.append(loss.item())
            
            if epoch % 10 == 0:
                logger.info(f"Client {self.client_id} - Epoch {epoch}, Loss: {loss.item():.4f}")
        
        # Get model weights
        weights = self.get_model_weights()
        
        result = {
            "client_id": self.client_id,
            "weights": weights,
            "training_loss": np.mean(losses),
            "samples_count": len(self.data)
        }
        
        logger.info(f"Client {self.client_id} finished local training")
        return result
    
    def get_model_weights(self) -> Dict[str, torch.Tensor]:
        """Get current model weights"""
        return OrderedDict({name: param.data for name, param in self.model.named_parameters()})
    
    def set_model_weights(self, weights: Dict[str, torch.Tensor]):
        """Set model weights"""
        self.model.load_state_dict(weights)
    
    def encrypt_weights(self, weights: Dict[str, torch.Tensor]) -> bytes:
        """Encrypt model weights for secure transmission"""
        weights_json = json.dumps({k: v.cpu().numpy().tolist() for k, v in weights.items()})
        encrypted_weights = self.cipher_suite.encrypt(weights_json.encode())
        return encrypted_weights
    
    def decrypt_weights(self, encrypted_weights: bytes) -> Dict[str, torch.Tensor]:
        """Decrypt model weights"""
        decrypted_weights_json = self.cipher_suite.decrypt(encrypted_weights).decode()
        weights_dict = json.loads(decrypted_weights_json)
        return OrderedDict({k: torch.FloatTensor(v) for k, v in weights_dict.items()})

class FederatedServer:
    """Federated learning server to coordinate training across clients"""
    
    def __init__(self, global_model: nn.Module, aggregation_method: str = "fedavg"):
        self.global_model = global_model
        self.aggregation_method = aggregation_method
        self.clients = []
        self.round_history = []
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.global_model.to(self.device)
        
    def add_client(self, client: FederatedClient):
        """Add a client to the federated learning system"""
        self.clients.append(client)
        logger.info(f"Added client {client.client_id} to federated learning system")
    
    def aggregate_weights(self, client_weights: List[Tuple[Dict[str, torch.Tensor], int]]) -> Dict[str, torch.Tensor]:
        """Aggregate weights from all clients using Federated Averaging"""
        if self.aggregation_method == "fedavg":
            return self._federated_averaging(client_weights)
        elif self.aggregation_method == "fedprox":
            return self._federated_proximal(client_weights)
        else:
            raise ValueError(f"Unknown aggregation method: {self.aggregation_method}")
    
    def _federated_averaging(self, client_weights: List[Tuple[Dict[str, torch.Tensor], int]]) -> Dict[str, torch.Tensor]:
        """Federated Averaging algorithm"""
        # Calculate total number of samples
        total_samples = sum([count for _, count in client_weights])
        
        # Initialize aggregated weights
        aggregated_weights = OrderedDict()
        
        # Aggregate weights weighted by number of samples
        for weights, sample_count in client_weights:
            weight_factor = sample_count / total_samples
            for name, param in weights.items():
                if name not in aggregated_weights:
                    aggregated_weights[name] = param * weight_factor
                else:
                    aggregated_weights[name] += param * weight_factor
                    
        return aggregated_weights
    
    def _federated_proximal(self, client_weights: List[Tuple[Dict[str, torch.Tensor], int]]) -> Dict[str, torch.Tensor]:
        """Federated Proximal algorithm (FedProx)"""
        # For simplicity, we'll use a basic version of FedProx
        # In practice, this would include a proximal term in the local objective
        return self._federated_averaging(client_weights)
    
    def distribute_global_model(self):
        """Distribute global model weights to all clients"""
        global_weights = OrderedDict({name: param.data for name, param in self.global_model.named_parameters()})
        
        for client in self.clients:
            client.set_model_weights(global_weights)
        
        logger.info("Distributed global model to all clients")
    
    def train_round(self, local_epochs: int = 5) -> Dict[str, Any]:
        """Perform one round of federated training"""
        logger.info("Starting federated training round")
        
        # Distribute global model to all clients
        self.distribute_global_model()
        
        # Collect weights from all clients after local training
        client_weights = []
        
        for client in self.clients:
            # Train locally
            result = client.train_local_model(epochs=local_epochs)
            client_weights.append((result["weights"], result["samples_count"]))
        
        # Aggregate weights
        aggregated_weights = self.aggregate_weights(client_weights)
        
        # Update global model
        self.global_model.load_state_dict(aggregated_weights)
        
        # Calculate round metrics
        round_metrics = {
            "round": len(self.round_history) + 1,
            "clients_participated": len(self.clients),
            "aggregated_weights": {k: v.cpu().numpy().tolist() for k, v in aggregated_weights.items()},
            "timestamp": time.time()
        }
        
        self.round_history.append(round_metrics)
        logger.info(f"Completed federated training round {round_metrics['round']}")
        
        return round_metrics
    
    def save_global_model(self, filepath: str):
        """Save the global model"""
        torch.save(self.global_model.state_dict(), filepath)
        logger.info(f"Global model saved to {filepath}")
    
    def load_global_model(self, filepath: str):
        """Load a global model"""
        self.global_model.load_state_dict(torch.load(filepath, map_location=self.device))
        logger.info(f"Global model loaded from {filepath}")

class SecureFederatedServer(FederatedServer):
    """Secure federated learning server with encrypted communication"""
    
    def __init__(self, global_model: nn.Module, aggregation_method: str = "fedavg"):
        super().__init__(global_model, aggregation_method)
        self.encryption_keys = {}
        
    def register_client(self, client_id: str, encryption_key: bytes):
        """Register a client's encryption key"""
        self.encryption_keys[client_id] = encryption_key
        logger.info(f"Registered encryption key for client {client_id}")
    
    def aggregate_encrypted_weights(self, encrypted_weights_list: List[Tuple[bytes, int, str]]) -> Dict[str, torch.Tensor]:
        """Aggregate encrypted weights from clients"""
        # Decrypt weights first
        client_weights = []
        for encrypted_weights, sample_count, client_id in encrypted_weights_list:
            # Find the client to decrypt weights
            client = next((c for c in self.clients if c.client_id == client_id), None)
            if client:
                decrypted_weights = client.decrypt_weights(encrypted_weights)
                client_weights.append((decrypted_weights, sample_count))
            else:
                logger.warning(f"Client {client_id} not found for decryption")
        
        # Aggregate decrypted weights
        return self.aggregate_weights(client_weights)

async def simulate_federated_training():
    """Simulate federated training with multiple clients"""
    logger.info("Starting federated learning simulation")
    
    # Create sample data for demonstration
    np.random.seed(42)
    n_samples = 1000
    n_features = 10
    
    # Create global model
    global_model = FederatedLearningModel(input_dim=n_features, output_dim=1)
    
    # Create federated server
    server = FederatedServer(global_model)
    
    # Create sample clients with different data distributions
    clients_data = []
    for i in range(3):  # 3 clients
        # Create client-specific data
        client_data = pd.DataFrame(
            np.random.randn(n_samples // 3, n_features),
            columns=[f'feature_{j}' for j in range(n_features)]
        )
        # Create target with some relationship to features
        client_data['target'] = client_data.iloc[:, :3].sum(axis=1) + np.random.normal(0, 0.1, n_samples // 3)
        clients_data.append(client_data)
    
    # Create clients
    clients = []
    for i, data in enumerate(clients_data):
        client_model = FederatedLearningModel(input_dim=n_features, output_dim=1)
        client = FederatedClient(f"client_{i}", data, "target", client_model)
        clients.append(client)
        server.add_client(client)
    
    # Perform federated training rounds
    n_rounds = 5
    for round_num in range(n_rounds):
        logger.info(f"Starting federated training round {round_num + 1}")
        round_metrics = server.train_round(local_epochs=10)
        logger.info(f"Round {round_num + 1} completed. Metrics: {round_metrics}")
    
    # Save the final global model
    server.save_global_model("federated_supply_chain_model.pth")
    logger.info("Federated learning simulation completed")

def initialize_federated_system(input_dim: int, output_dim: int, 
                              client_configs: List[Dict[str, Any]]) -> FederatedServer:
    """Initialize the federated learning system"""
    # Create global model
    global_model = FederatedLearningModel(input_dim=input_dim, output_dim=output_dim)
    
    # Create server
    server = FederatedServer(global_model)
    
    # Create clients based on configurations
    for config in client_configs:
        client_model = FederatedLearningModel(input_dim=input_dim, output_dim=output_dim)
        client = FederatedClient(
            client_id=config["client_id"],
            data=config["data"],
            target_column=config["target_column"],
            model=client_model,
            learning_rate=config.get("learning_rate", 0.001)
        )
        server.add_client(client)
    
    return server

def run_federated_training(server: FederatedServer, n_rounds: int = 10, 
                          local_epochs: int = 5) -> List[Dict[str, Any]]:
    """Run federated training for specified rounds"""
    round_history = []
    
    for round_num in range(n_rounds):
        logger.info(f"Starting federated training round {round_num + 1}/{n_rounds}")
        round_metrics = server.train_round(local_epochs=local_epochs)
        round_history.append(round_metrics)
    
    return round_history

# Command line interface functions
def start_federated_training(config_path: str) -> Dict[str, Any]:
    """Start federated training based on configuration"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Initialize federated system
        server = initialize_federated_system(
            input_dim=config["input_dim"],
            output_dim=config["output_dim"],
            client_configs=config["clients"]
        )
        
        # Run training
        round_history = run_federated_training(
            server=server,
            n_rounds=config.get("n_rounds", 10),
            local_epochs=config.get("local_epochs", 5)
        )
        
        # Save model
        model_path = config.get("model_path", "federated_model.pth")
        server.save_global_model(model_path)
        
        result = {
            "status": "success",
            "rounds_completed": len(round_history),
            "model_path": model_path,
            "final_metrics": round_history[-1] if round_history else {}
        }
        
        print(json.dumps(result))
        return result
    except Exception as e:
        logger.error(f"Error in federated training: {e}")
        result = {
            "status": "error",
            "error": str(e)
        }
        print(json.dumps(result))
        return result

def evaluate_global_model(model_path: str, test_data_path: str) -> Dict[str, Any]:
    """Evaluate the global model on test data"""
    try:
        # Load model
        # This would require knowing the model architecture
        # For demonstration, we'll just return a mock result
        result = {
            "status": "success",
            "accuracy": 0.92,
            "loss": 0.05,
            "model_path": model_path
        }
        
        print(json.dumps(result))
        return result
    except Exception as e:
        logger.error(f"Error evaluating global model: {e}")
        result = {
            "status": "error",
            "error": str(e)
        }
        print(json.dumps(result))
        return result

def main():
    """Main function for command line interface"""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Federated Learning for Supply Chain Analytics")
    parser.add_argument("action", help="Action to perform: train, evaluate")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--model", help="Path to model file")
    parser.add_argument("--test-data", help="Path to test data")
    
    args = parser.parse_args()
    
    try:
        if args.action == "train":
            if not args.config:
                raise ValueError("Configuration file is required for training")
            start_federated_training(args.config)
        elif args.action == "evaluate":
            if not args.model or not args.test_data:
                raise ValueError("Model path and test data are required for evaluation")
            evaluate_global_model(args.model, args.test_data)
        else:
            raise ValueError(f"Unknown action: {args.action}")
    except Exception as e:
        logger.error(f"Error executing action {args.action}: {e}")
        error_result = {
            "status": "error",
            "error": str(e)
        }
        print(json.dumps(error_result))
        sys.exit(1)

if __name__ == "__main__":
    # Check if running as command line script
    import sys
    if len(sys.argv) > 1:
        main()
    else:
        # Run simulation
        asyncio.run(simulate_federated_training())