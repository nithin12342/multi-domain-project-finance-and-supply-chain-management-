"""
Neural network architectures for the Multi-Domain AI Platform.
FraudDetectionMLP: Adaptive input size (15-100 features), He initialization.
NasaRulPredictor: 120 spectral FFT features for remaining useful life.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class FraudDetectionMLP(nn.Module):
    """
    Binary fraud classifier.
    Input: n_features (15 baseline OR up to 100 advanced features)
    Output: 1 logit (BCEWithLogitsLoss)
    
    Scales hidden dims proportionally so the 100-feature model
    doesn't overfit relative to 15-feature baseline.
    """

    def __init__(self, input_dim: int = 15):
        super().__init__()

        # Dynamic hidden dim: 8× input, capped at 512
        h1 = min(512, input_dim * 8)   # e.g., 100 → 512 (capped)
        h2 = h1 // 2                   # 256
        h3 = h2 // 2                   # 128

        self.network = nn.Sequential(
            # Block 1
            nn.Linear(input_dim, h1),
            nn.BatchNorm1d(h1),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Dropout(0.3),

            # Block 2
            nn.Linear(h1, h2),
            nn.BatchNorm1d(h2),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Dropout(0.3),

            # Block 3
            nn.Linear(h2, h3),
            nn.BatchNorm1d(h3),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Dropout(0.2),

            # Output
            nn.Linear(h3, 1)
        )

        # Weight initialization (He for LeakyReLU)
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, a=0.01,
                                        nonlinearity='leaky_relu')
                nn.init.zeros_(m.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x).squeeze(-1)


class NasaRulPredictor(nn.Module):
    """
    Regression model for predicting Remaining Useful Life (RUL).
    Input Dimension: 120 (24 sensors × 5 spectral features)
    Consumes FFT spectra extracted per engine cycle.
    """
    def __init__(self, input_dim=120, hidden_dim=256):
        super(NasaRulPredictor, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.GELU(),
            nn.Dropout(0.3),

            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.BatchNorm1d(hidden_dim // 2),
            nn.GELU(),
            nn.Dropout(0.3),

            nn.Linear(hidden_dim // 2, hidden_dim // 4),
            nn.BatchNorm1d(hidden_dim // 4),
            nn.GELU(),
            nn.Dropout(0.2),

            nn.Linear(hidden_dim // 4, 1)
        )

    def forward(self, x):
        return self.network(x)
