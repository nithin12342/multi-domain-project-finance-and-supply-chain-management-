import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class TabularFeatureDataset(Dataset):
    """
    Universal dataset unloader for the structurally flattened CSV outputs created by data_pipeline.py.
    Now includes StandardScaler normalization for proper gradient flow.
    """
    def __init__(self, csv_path, target_col, ignore_cols=None, scaler=None):
        """
        csv_path: Path to features_spectral_*.csv or structural_fraud_features.csv
        target_col: The exact string name of the column storing the regression/classification target.
        ignore_cols: List of string names indicating metadata columns (like chunk_id or engine_id) to detach from the X tensors.
        scaler: Optional pre-fitted StandardScaler (for validation set to use training set's statistics).
        """
        self.df = pd.read_csv(csv_path).dropna()
        
        # Extract and Drop Target
        self.y = self.df[target_col].values.astype(np.float32)
        X_df = self.df.drop(columns=[target_col])
        
        # Isolate Metadata
        if ignore_cols:
            self.metadata = X_df[ignore_cols].astype(str).agg('-'.join, axis=1).values
            X_df = X_df.drop(columns=ignore_cols, errors='ignore')
        else:
            self.metadata = np.arange(len(self.df)).astype(str)
        
        # Apply StandardScaler normalization
        self.raw_X = X_df.values.astype(np.float32)
        if scaler is not None:
            self.scaler = scaler
            self.X = self.scaler.transform(self.raw_X).astype(np.float32)
        else:
            self.scaler = StandardScaler()
            self.X = self.scaler.fit_transform(self.raw_X).astype(np.float32)


    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return (torch.tensor(self.X[idx]), 
                torch.tensor(self.y[idx]), 
                self.metadata[idx])

def create_dataloaders(csv_path, target_col, ignore_cols=None, batch_size=32, validation_split=0.2, balance_classes=False):
    """Generates the isolated Train/Validation dataloaders for the Master Training script."""
    full_dataset = TabularFeatureDataset(csv_path, target_col, ignore_cols)
    
    val_size = int(len(full_dataset) * validation_split)
    train_size = len(full_dataset) - val_size
    train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])
    
    # Optional: Handle Severe Class Imbalance (e.g. 0.1% Fraud vs 99.9% Legit)
    sampler = None
    if balance_classes:
        # Extract the labels specifically belonging to the training subset
        train_indices = train_dataset.indices
        train_labels = full_dataset.y[train_indices]
        
        # Calculate frequency of each class
        class_counts = np.bincount(train_labels.astype(int))
        # Weight for each class is inversely proportional to its frequency
        class_weights = 1.0 / np.maximum(class_counts, 1e-5)
        
        # Assign the corresponding weight to every individual sample in the training set
        sample_weights = np.array([class_weights[int(label)] for label in train_labels])
        
        # Create PyTorch sampler that over-samples the minority class
        sampler = torch.utils.data.WeightedRandomSampler(
            weights=torch.DoubleTensor(sample_weights), 
            num_samples=len(sample_weights), 
            replacement=True
        )
    
    # If using a custom sampler, we drop standard shuffling
    if sampler is not None:
        train_loader = DataLoader(train_dataset, batch_size=batch_size, sampler=sampler)
    else:
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    return train_loader, val_loader
