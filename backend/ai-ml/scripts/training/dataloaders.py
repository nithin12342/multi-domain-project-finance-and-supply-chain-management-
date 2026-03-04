"""
Updated DataLoader compatible with 100-feature structural_fraud_features.csv.
Includes SMOTE oversampling for fraud imbalance and adaptive StandardScaler.
"""

import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit
from pathlib import Path
import logging

# SMOTE is optional — graceful fallback
try:
    from imblearn.over_sampling import SMOTE
    HAS_SMOTE = True
except ImportError:
    HAS_SMOTE = False

try:
    import joblib
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False

logger = logging.getLogger(__name__)

LABEL_COL   = 'isFraud'
EXCLUDE_COLS = ['chunk_id', 'isFraud']


class FraudGraphDataset(Dataset):
    def __init__(self, X: np.ndarray, y: np.ndarray):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self): return len(self.y)
    def __getitem__(self, idx): return self.X[idx], self.y[idx]


def build_fraud_dataloaders(
    csv_path: str,
    batch_size: int = 64,
    val_split: float = 0.2,
    apply_smote: bool = True,
    scaler_save_path: str = "backend/data/processed/scaler.pkl"
) -> tuple:
    """
    Builds train/val DataLoaders from structural_fraud_features.csv.
    
    Returns:
        train_loader, val_loader, n_features (int)
    """
    df = pd.read_csv(csv_path)
    assert LABEL_COL in df.columns, f"Missing {LABEL_COL} in {csv_path}"

    feature_cols = [c for c in df.columns if c not in EXCLUDE_COLS]
    X = df[feature_cols].values.astype(np.float32)
    y = df[LABEL_COL].values.astype(np.float32)

    logger.info(f"Loaded: {X.shape[0]} samples × {X.shape[1]} features | "
                f"Fraud rate: {y.mean():.4f}")

    # ── Stratified split (preserves fraud rate in both sets) ──────────────
    sss = StratifiedShuffleSplit(n_splits=1, test_size=val_split,
                                  random_state=42)
    train_idx, val_idx = next(sss.split(X, y))
    X_train, y_train = X[train_idx], y[train_idx]
    X_val,   y_val   = X[val_idx],   y[val_idx]

    # ── StandardScaler (fit on train only, transform both) ────────────────
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val   = scaler.transform(X_val)
    
    if HAS_JOBLIB:
        import joblib
        Path(scaler_save_path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(scaler, scaler_save_path)
        logger.info(f"Scaler saved → {scaler_save_path}")

    # ── SMOTE oversampling (train only, post-scaling) ─────────────────────
    if apply_smote and HAS_SMOTE and y_train.mean() < 0.3:
        # Only apply if imbalance is significant (fraud < 30%)
        try:
            smote = SMOTE(
                sampling_strategy=0.3,  # Upsample fraud to 30% of majority
                k_neighbors=min(5, int(y_train.sum()) - 1),
                random_state=42
            )
            X_train, y_train = smote.fit_resample(X_train, y_train)
            logger.info(f"SMOTE applied. New train shape: {X_train.shape}, "
                        f"Fraud rate: {y_train.mean():.4f}")
        except Exception as e:
            logger.warning(f"SMOTE failed, proceeding without: {e}")

    # ── Weighted Sampler for Hard Sample Mining compatibility ─────────────
    class_counts = np.bincount(y_train.astype(int))
    weights = 1.0 / (class_counts + 1e-12)
    sample_weights = weights[y_train.astype(int)]
    sampler = WeightedRandomSampler(
        weights=torch.tensor(sample_weights, dtype=torch.float64),
        num_samples=len(sample_weights),
        replacement=True
    )

    train_dataset = FraudGraphDataset(X_train.astype(np.float32), y_train.astype(np.float32))
    val_dataset   = FraudGraphDataset(X_val.astype(np.float32),   y_val.astype(np.float32))

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        sampler=sampler,       # Weighted sampling instead of shuffle
        num_workers=0,         # 0 for Colab compatibility
        pin_memory=True
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size * 2,
        shuffle=False,
        num_workers=0,
        pin_memory=True
    )

    return train_loader, val_loader, X_train.shape[1]


# ── Legacy compatibility wrapper ─────────────────────────────────────────────
class TabularFeatureDataset(Dataset):
    """Legacy dataset class — use build_fraud_dataloaders() for new code."""
    def __init__(self, csv_path, target_col, ignore_cols=None, scaler=None):
        self.df = pd.read_csv(csv_path).dropna()
        self.y = self.df[target_col].values.astype(np.float32)
        X_df = self.df.drop(columns=[target_col])
        if ignore_cols:
            self.metadata = X_df[ignore_cols].astype(str).agg('-'.join, axis=1).values
            X_df = X_df.drop(columns=ignore_cols, errors='ignore')
        else:
            self.metadata = np.arange(len(self.df)).astype(str)
        
        self.raw_X = X_df.values.astype(np.float32)
        if scaler is not None:
            self.scaler = scaler
            self.X = self.scaler.transform(self.raw_X).astype(np.float32)
        else:
            self.scaler = StandardScaler()
            self.X = self.scaler.fit_transform(self.raw_X).astype(np.float32)

    def __len__(self): return len(self.X)
    def __getitem__(self, idx):
        return (torch.tensor(self.X[idx]), torch.tensor(self.y[idx]),
                self.metadata[idx])
