import torch.nn as nn

class FraudDetectionMLP(nn.Module):
    """
    SOTA Multi-Layer Perceptron optimized for tabular Graph Centrality features.
    Input Dimension: 15 (pagerank, clustering, density, degree, reciprocity, amount stats)
    """
    def __init__(self, input_dim=15, hidden_dim=128):
        super(FraudDetectionMLP, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.3),
            
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.BatchNorm1d(hidden_dim // 2),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.3),
            
            nn.Linear(hidden_dim // 2, hidden_dim // 4),
            nn.BatchNorm1d(hidden_dim // 4),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.2),
            
            nn.Linear(hidden_dim // 4, 1) # Output raw logits for BCEWithLogitsLoss
        )

    def forward(self, x):
        return self.network(x)


class NasaRulPredictor(nn.Module):
    """
    SOTA MLP designed to process the flattened 120-dimensional Spectral FFT and EMA slope array.
    Input Dimension: 120 (24 sensors * 5 engineered telemetry features)
    """
    def __init__(self, input_dim=120, hidden_dim=256):
        super(NasaRulPredictor, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.GELU(),
            nn.Dropout(0.4),
            
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.BatchNorm1d(hidden_dim // 2),
            nn.GELU(),
            nn.Dropout(0.4),
            
            nn.Linear(hidden_dim // 2, hidden_dim // 4),
            nn.BatchNorm1d(hidden_dim // 4),
            nn.GELU(),
            nn.Dropout(0.2),
            
            nn.Linear(hidden_dim // 4, 1) # Continuous output for Remaining Useful Life (MSELoss)
        )

    def forward(self, x):
        return self.network(x)
