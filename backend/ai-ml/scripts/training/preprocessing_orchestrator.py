"""
Master pipeline that:
1. Ingests raw CSVs (IEEE-CIS, PaySim, DataCo)
2. Chunks data into graph windows
3. Extracts all 100 features per chunk
4. Validates labels (NO random generation)
5. Outputs structural_fraud_features.csv
"""

import pandas as pd
import numpy as np
import logging
import gc
from pathlib import Path
from typing import List, Dict

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable

from feature_config import CFG, FeatureExtractionConfig
from data_ingestion import DataIngestionPipeline
from graph_builder import TransactionGraphBuilder
from advanced_feature_extractor import AdvancedFeatureExtractor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger(__name__)


def process_single_chunk(
    chunk_id: int,
    chunk_df: pd.DataFrame,
    dataset_type: str,        # 'ieee', 'paysim', 'dataco'
    extractor: AdvancedFeatureExtractor,
    builder: TransactionGraphBuilder
) -> Dict:
    """
    Process one chunk → one feature row.
    Isolated function for parallel execution.

    CRITICAL RULE: isFraud = max(isFraud) in chunk (not random).
    """
    result = {'chunk_id': chunk_id}

    # ── Label derivation (REAL labels only) ──────────────────────────────
    if 'isFraud' in chunk_df.columns:
        result['isFraud'] = int(chunk_df['isFraud'].max())
    else:
        result['isFraud'] = 0
        logger.warning(f"Chunk {chunk_id}: no isFraud column — defaulting to 0.")

    # ── Build graph ───────────────────────────────────────────────────────
    if dataset_type == 'ieee':
        G = builder.build_ieee_graph(chunk_df)
        amounts = chunk_df['TransactionAmt'].fillna(0).tolist()
        is_paysim = False
    elif dataset_type == 'paysim':
        G = builder.build_paysim_graph(chunk_df)
        amounts = chunk_df['amount'].fillna(0).tolist()
        is_paysim = True
    else:
        G = builder.build_supply_chain_graph(chunk_df)
        amounts = [0.0]
        is_paysim = False

    # ── Extract all feature groups ────────────────────────────────────────
    feats = {}

    # [A] Baseline
    feats.update(extractor.extract_baseline_features(G, amounts))

    # [B] Extended Centrality (skip for tiny graphs)
    if G.number_of_nodes() >= 5:
        feats.update(extractor.extract_centrality_features(G))
    else:
        feats.update({k: 0.0 for k in extractor._centrality_keys()})

    # [C] Spectral
    if G.number_of_nodes() >= 4:
        feats.update(extractor.extract_spectral_features(G))
    else:
        feats.update({k: 0.0 for k in extractor._spectral_keys()})

    # [D] TDA
    if G.number_of_nodes() >= 4:
        feats.update(extractor.extract_tda_features(G))
    else:
        feats.update(extractor._tda_fallback(G))

    # [E] Community
    if G.number_of_nodes() >= 4:
        feats.update(extractor.extract_community_features(G))
    else:
        feats.update({k: 0.0 for k in extractor._community_keys()})

    # [F] Temporal (PaySim-specific)
    feats.update(extractor.extract_temporal_features(chunk_df, is_paysim))

    # [G] Motifs
    if G.number_of_nodes() >= 3:
        feats.update(extractor.extract_motif_features(G))
    else:
        feats.update({k: 0.0 for k in extractor._motif_keys()})

    # [H] Path Signatures (on transaction amounts as 1D time series)
    if len(amounts) >= 4:
        feats.update(extractor.extract_path_signature_features(
            np.array(amounts, dtype=np.float32)
        ))
    else:
        feats.update(extractor._signature_fallback(np.array(amounts)))

    result.update(feats)
    return result


class PreprocessingOrchestrator:

    def __init__(self, raw_data_dir: str, config: FeatureExtractionConfig = CFG):
        self.cfg      = config
        self.ingester = DataIngestionPipeline(raw_data_dir)
        self.builder  = TransactionGraphBuilder()
        self.extractor= AdvancedFeatureExtractor(config)
        Path(config.output_dir).mkdir(parents=True, exist_ok=True)

    def run_ieee_pipeline(self) -> pd.DataFrame:
        """Full IEEE-CIS preprocessing pipeline."""
        logger.info("═" * 60)
        logger.info("PIPELINE: IEEE-CIS Fraud Detection")
        logger.info("═" * 60)

        df = self.ingester.load_ieee_cis()
        self.ingester.validate_labels(df, 'isFraud')

        # Chunk by TransactionID order (temporal sliding window)
        n_chunks = len(df) // self.cfg.chunk_size
        all_rows = []

        for i in tqdm(range(n_chunks), desc="IEEE-CIS chunks"):
            start = i * (self.cfg.chunk_size - self.cfg.chunk_overlap)
            end   = start + self.cfg.chunk_size
            chunk = df.iloc[start:end].copy()
            if len(chunk) < self.cfg.min_chunk_nodes:
                continue
            row = process_single_chunk(i, chunk, 'ieee',
                                       self.extractor, self.builder)
            all_rows.append(row)

            # Memory guard: force GC every 100 chunks
            if i % 100 == 0:
                gc.collect()

        result_df = pd.DataFrame(all_rows)
        del df
        gc.collect()
        return result_df

    def run_paysim_pipeline(self) -> pd.DataFrame:
        """PaySim chunked pipeline (6.3M rows, memory-safe)."""
        logger.info("═" * 60)
        logger.info("PIPELINE: PaySim Financial Transactions")
        logger.info("═" * 60)

        all_rows = []
        global_chunk_id = 0

        for raw_chunk in self.ingester.load_paysim_chunked(chunksize=500_000):
            # Sub-chunk the 500K block by CFG.chunk_size for graph construction
            n_sub = len(raw_chunk) // self.cfg.chunk_size
            for j in range(n_sub):
                sub = raw_chunk.iloc[
                    j * self.cfg.chunk_size:(j + 1) * self.cfg.chunk_size
                ].copy()
                if len(sub) < self.cfg.min_chunk_nodes:
                    continue
                row = process_single_chunk(
                    global_chunk_id, sub, 'paysim',
                    self.extractor, self.builder
                )
                all_rows.append(row)
                global_chunk_id += 1

            gc.collect()

        return pd.DataFrame(all_rows)

    def run_full_pipeline(self) -> None:
        """
        Run both IEEE and PaySim, combine, validate, and save.
        """
        dfs = []
        
        try:
            ieee_df = self.run_ieee_pipeline()
            if len(ieee_df) > 0:
                dfs.append(ieee_df)
                logger.info(f"IEEE-CIS: {len(ieee_df)} chunks extracted")
        except Exception as e:
            logger.warning(f"IEEE-CIS pipeline failed: {e}")
        
        try:
            paysim_df = self.run_paysim_pipeline()
            if len(paysim_df) > 0:
                dfs.append(paysim_df)
                logger.info(f"PaySim: {len(paysim_df)} chunks extracted")
        except Exception as e:
            logger.warning(f"PaySim pipeline failed: {e}")
        
        if not dfs:
            logger.error("No datasets were processed successfully!")
            return

        combined = pd.concat(dfs, ignore_index=True)
        combined['chunk_id'] = range(len(combined))

        # ── Post-processing ───────────────────────────────────────────────
        combined = self._clean_and_validate(combined)

        # ── Save ──────────────────────────────────────────────────────────
        out_path = Path(self.cfg.output_dir) / self.cfg.fraud_feature_file
        combined.to_csv(out_path, index=False)
        logger.info(f"✅ Saved {len(combined)} rows × {len(combined.columns)} "
                    f"features → {out_path}")

        self._print_quality_report(combined)

    def _clean_and_validate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Final data quality pass before output:
        - Replace inf/nan with 0 (not mean imputation — zero is meaningful here)
        - Clip extreme outliers to 99.9th percentile
        - Verify isFraud column integrity
        """
        assert 'isFraud' in df.columns, "CRITICAL: isFraud missing from output!"
        assert df['isFraud'].isin([0, 1]).all(), \
            "CRITICAL: Non-binary isFraud values detected!"

        # Replace problematic values
        feature_cols = [c for c in df.columns
                        if c not in ['chunk_id', 'isFraud']]
        df[feature_cols] = df[feature_cols].replace(
            [np.inf, -np.inf], np.nan
        ).fillna(0.0)

        # Clip outliers (preserve sign, clip magnitude)
        for col in feature_cols:
            upper = df[col].quantile(0.999)
            lower = df[col].quantile(0.001)
            df[col] = df[col].clip(lower=lower, upper=upper)

        logger.info(f"Cleaned dataset: {df.shape}, "
                    f"Fraud rate: {df['isFraud'].mean():.4f}")
        return df

    def _print_quality_report(self, df: pd.DataFrame) -> None:
        fraud_rate  = df['isFraud'].mean()
        n_features  = len(df.columns) - 2  # exclude chunk_id, isFraud
        n_rows      = len(df)
        nan_count   = df.isnull().sum().sum()

        print("\n" + "═" * 60)
        print("📊 PREPROCESSING QUALITY REPORT")
        print("═" * 60)
        print(f"  Total rows (chunks):  {n_rows:,}")
        print(f"  Feature columns:      {n_features}")
        print(f"  Fraud rate:           {fraud_rate:.4f} ({fraud_rate*100:.2f}%)")
        print(f"  Remaining NaN cells:  {nan_count}")
        print(f"  Label source:         REAL (max isFraud per chunk)")
        print("═" * 60)

        if fraud_rate < 0.001:
            print("⚠️  WARNING: Very low fraud rate — enable Hard Sample Mining.")
        if n_features < 50:
            print("⚠️  WARNING: Feature count below 50 — check extraction modules.")
        if n_rows < 1000:
            print("⚠️  WARNING: Row count below 1000 — increase chunk overlap or reduce chunk_size.")


# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    raw_dir = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
    orchestrator = PreprocessingOrchestrator(raw_data_dir=raw_dir)
    orchestrator.run_full_pipeline()
