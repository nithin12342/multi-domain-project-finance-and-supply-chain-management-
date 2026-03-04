"""
Designer-Specific Feature Extraction Configuration
Tuned for: FraudDetectionMLP (15→100 features), NasaRulPredictor (spectral)
Constraint: Colab Free Tier (12GB RAM), GitHub Codespaces preprocessing
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import os

@dataclass
class FeatureExtractionConfig:
    # ── Graph Chunking ──────────────────────────────────────────────────────
    chunk_size: int = 500          # Transactions per graph chunk
    chunk_overlap: int = 50        # Sliding window overlap for temporal continuity
    min_chunk_nodes: int = 10      # Discard degenerate micro-graphs
    
    # ── Spectral Features ──────────────────────────────────────────────────
    top_k_eigenvalues: int = 8     # Laplacian spectrum depth
    fiedler_vector_bins: int = 20  # Histogram bins for Fiedler vector distribution
    
    # ── TDA Settings ───────────────────────────────────────────────────────
    max_homology_dim: int = 2      # β₀, β₁, β₂
    persistence_threshold: float = 0.01   # Filter trivial persistence bars
    barcode_vector_size: int = 10  # Fixed-length barcode encoding per dimension
    filtration_steps: int = 50     # Rips complex filtration resolution
    
    # ── Community Detection ────────────────────────────────────────────────
    louvain_resolution: float = 1.0
    max_communities: int = 20      # Cap for feature-size stability
    
    # ── Temporal (PaySim) ──────────────────────────────────────────────────
    velocity_window: int = 10      # Steps for velocity computation
    amount_ewma_alpha: float = 0.3 # Exponential smoothing for amount velocity
    
    # ── Output ─────────────────────────────────────────────────────────────
    output_dir: str = "backend/data/processed"
    fraud_feature_file: str = "structural_fraud_features.csv"
    
    # ── Memory Guard ───────────────────────────────────────────────────────
    max_graph_nodes: int = 2000    # Truncate pathological chunks
    sparse_threshold: int = 500    # Use scipy sparse for graphs above this size

CFG = FeatureExtractionConfig()
