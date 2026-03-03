import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np

class TabularFeatureDataset(Dataset):
    """
    Universal dataset unloader for the structurally flattened CSV outputs created by data_pipeline.py.
    """
    def __init__(self, csv_path, target_col, ignore_cols=None):
        """
        csv_path: Path to features_spectral_*.csv or structural_fraud_features.csv
        target_col: The exact string name of the column storing the regression/classification target.
        ignore_cols: List of string names indicating metadata columns (like chunk_id or engine_id) to detach from the X tensors.
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
            
        self.X = X_df.values.astype(np.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return (torch.tensor(self.X[idx]), 
                torch.tensor(self.y[idx]), 
                self.metadata[idx])

def create_dataloaders(csv_path, target_col, ignore_cols=None, batch_size=32, validation_split=0.2):
    """Generates the isolated Train/Validation dataloaders for the Master Training script."""
    full_dataset = TabularFeatureDataset(csv_path, target_col, ignore_cols)
    
    val_size = int(len(full_dataset) * validation_split)
    train_size = len(full_dataset) - val_size
    train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    return train_loader, val_loader
