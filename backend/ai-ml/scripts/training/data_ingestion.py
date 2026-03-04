"""
Handles IEEE-CIS (~680K rows), PaySim (~6.3M rows), DataCo (~180K rows)
with memory-efficient chunked loading and schema validation.
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Optional, Tuple, Iterator
import gc

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# IEEE-CIS SCHEMA: Optimized dtypes to fit 590MB into 12GB RAM
# ─────────────────────────────────────────────────────────────────────────────
IEEE_TRANSACTION_DTYPES = {
    'TransactionID': 'int32',
    'isFraud':       'int8',
    'TransactionAmt':'float32',
    'ProductCD':     'category',
    'card1': 'int16', 'card2': 'float32', 'card3': 'float32',
    'card4': 'category', 'card5': 'float32', 'card6': 'category',
    'addr1': 'float32', 'addr2': 'float32',
    'dist1': 'float32', 'dist2': 'float32',
    'P_emaildomain': 'category', 'R_emaildomain': 'category',
    **{f'C{i}': 'float32' for i in range(1, 15)},
    **{f'D{i}': 'float32' for i in range(1, 16)},
    **{f'M{i}': 'category' for i in range(1, 10)},
    **{f'V{i}': 'float32' for i in range(1, 340)},
}

PAYSIM_DTYPES = {
    'step':             'int32',
    'type':             'category',
    'amount':           'float32',
    'nameOrig':         'object',
    'oldbalanceOrg':    'float32',
    'newbalanceOrig':   'float32',
    'nameDest':         'object',
    'oldbalanceDest':   'float32',
    'newbalanceDest':   'float32',
    'isFraud':          'int8',
    'isFlaggedFraud':   'int8',
}


class DataIngestionPipeline:
    """
    Memory-safe loader for all three datasets.
    Uses chunked iteration for PaySim (6.3M rows) to prevent OOM.
    """

    def __init__(self, raw_data_dir: str):
        self.raw_dir = Path(raw_data_dir)

    # ── IEEE-CIS ─────────────────────────────────────────────────────────────
    def load_ieee_cis(self) -> pd.DataFrame:
        """
        Merge transaction + identity tables on TransactionID.
        Reduces V-feature dimensionality via variance thresholding before merge.
        """
        logger.info("Loading IEEE-CIS transaction data...")
        txn_path = self.raw_dir / "train_transaction.csv"
        if not txn_path.exists():
            # Try ieee_fraud subdirectory
            txn_path = self.raw_dir / "ieee_fraud" / "train_transaction.csv"
        
        df_trans = pd.read_csv(
            txn_path,
            dtype=IEEE_TRANSACTION_DTYPES,
            low_memory=True
        )

        # ── Drop near-zero-variance V features BEFORE identity merge ─────────
        # V1-V339 have massive sparsity; keep only columns with >5% non-null
        v_cols = [f'V{i}' for i in range(1, 340)]
        existing_v = [c for c in v_cols if c in df_trans.columns]
        valid_v = [c for c in existing_v
                   if df_trans[c].notna().mean() > 0.05]
        drop_v  = [c for c in existing_v if c not in valid_v]
        df_trans.drop(columns=drop_v, inplace=True)
        logger.info(f"Dropped {len(drop_v)} sparse V-features. Kept {len(valid_v)}.")

        # Try to load identity file
        ident_path = self.raw_dir / "train_identity.csv"
        if not ident_path.exists():
            ident_path = self.raw_dir / "ieee_fraud" / "train_identity.csv"
        
        if ident_path.exists():
            logger.info("Loading IEEE-CIS identity data...")
            df_ident = pd.read_csv(ident_path, low_memory=True)
            df = df_trans.merge(df_ident, on='TransactionID', how='left')
            del df_ident
        else:
            logger.warning("Identity file not found — using transactions only.")
            df = df_trans
        
        del df_trans
        gc.collect()

        logger.info(f"IEEE-CIS merged shape: {df.shape}")
        return df

    # ── PaySim ───────────────────────────────────────────────────────────────
    def load_paysim_chunked(
        self, chunksize: int = 500_000
    ) -> Iterator[pd.DataFrame]:
        """
        Yields PaySim in 500K-row chunks to prevent 6.3M×12col OOM.
        Each chunk is a self-contained time window (by `step`).
        """
        paysim_path = self.raw_dir / "PS_20174392719_1491204439457_log.csv"
        if not paysim_path.exists():
            # Try paysim subdirectory
            paysim_dir = self.raw_dir / "paysim"
            if paysim_dir.exists():
                csv_files = list(paysim_dir.glob("*.csv"))
                if csv_files:
                    paysim_path = csv_files[0]
        
        reader = pd.read_csv(
            paysim_path,
            dtype=PAYSIM_DTYPES,
            chunksize=chunksize,
            low_memory=True
        )
        for chunk in reader:
            # Retain only TRANSFER and CASH_OUT — the fraud-prone types
            chunk = chunk[chunk['type'].isin(['TRANSFER', 'CASH_OUT'])].copy()
            yield chunk

    # ── DataCo Supply Chain ──────────────────────────────────────────────────
    def load_dataco(self) -> pd.DataFrame:
        dataco_path = self.raw_dir / "DataCoSupplyChainDataset.csv"
        if not dataco_path.exists():
            dataco_dir = self.raw_dir / "dataco"
            if dataco_dir.exists():
                csv_files = list(dataco_dir.glob("*.csv"))
                if csv_files:
                    dataco_path = csv_files[0]
        
        df = pd.read_csv(
            dataco_path,
            encoding='unicode_escape',   # Required for this specific Kaggle file
            low_memory=True
        )
        logger.info(f"DataCo shape: {df.shape}")
        return df

    # ── Schema Validation ────────────────────────────────────────────────────
    @staticmethod
    def validate_labels(df: pd.DataFrame, label_col: str = 'isFraud') -> None:
        assert label_col in df.columns, f"Missing label column: {label_col}"
        unique_vals = df[label_col].dropna().unique()
        assert set(unique_vals).issubset({0, 1}), (
            f"Label column must be binary 0/1, found: {unique_vals}"
        )
        fraud_rate = df[label_col].mean()
        logger.info(f"Label validation passed. Fraud rate: {fraud_rate:.4f} "
                    f"({fraud_rate*100:.2f}%)")
        if fraud_rate < 0.001:
            logger.warning("Extremely low fraud rate — "
                           "ensure SMOTE/hard-sample-mining is active.")
