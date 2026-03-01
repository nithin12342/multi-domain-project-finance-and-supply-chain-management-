import torch
import torch.nn as nn
import math

class MambaLayer(nn.Module):
    """
    Simplified blueprint of a Mamba SSM block.
    In O(L) time, it selectively compressing linear state spaces.
    Requires official 'mamba-ssm' package for true hardware-efficient CUDA kernels.
    """
    def __init__(self, d_model, d_state=16, d_conv=4, expand=2):
        super().__init__()
        self.d_model = d_model
        d_inner = int(expand * d_model)
        
        self.in_proj = nn.Linear(d_model, d_inner * 2, bias=False)
        self.conv1d = nn.Conv1d(d_inner, d_inner, kernel_size=d_conv, padding=d_conv-1, groups=d_inner)
        self.x_proj = nn.Linear(d_inner, d_state * 2 + 1, bias=False)
        self.dt_proj = nn.Linear(1, d_inner, bias=True)
        self.out_proj = nn.Linear(d_inner, d_model, bias=False)

    def forward(self, hidden_states):
        # Extremely simplified conceptual forward pass
        # Actual implementation uses selective scan CUDA kernels
        B, L, D = hidden_states.shape
        xz = self.in_proj(hidden_states)
        x, z = xz.chunk(2, dim=-1)
        
        x = x.transpose(1, 2)
        x = self.conv1d(x)[:, :, :L]
        x = x.transpose(1, 2)
        x = F.silu(x)
        
        # Projected SSM parameters
        delta_A_B = self.x_proj(x)
        
        # ... Selective Scan Operation (omitted for brevity, conceptually acts like an RNN) ...
        # Assume 'y' is the output of the state space model
        y = x # Placeholder for actual selective_scan_fn(x, dt, A, B, C)
        
        y = y * F.silu(z)
        out = self.out_proj(y)
        return out

class HybridMambaAttentionTFT(nn.Module):
    """
    Hybrid Mamba-Attention Temporal Fusion Transformer.
    Uses Mamba for efficient encoding of long IoT telemetry sequences,
    and Sparse Attention for cross-modal fusion with financial signals.
    """
    def __init__(self, iot_dim, finance_dim, d_model=256, num_heads=8):
        super().__init__()
        
        # Projections
        self.iot_proj = nn.Linear(iot_dim, d_model)
        self.fin_proj = nn.Linear(finance_dim, d_model)
        
        # Mamba backbone for long IoT sequence
        self.mamba_blocks = nn.ModuleList([MambaLayer(d_model) for _ in range(3)])
        
        # Transformer Attention for cross-modal fusion
        self.cross_attention = nn.MultiheadAttention(embed_dim=d_model, num_heads=num_heads, batch_first=True)
        
        # Demand Forecasting Head (Quantile output)
        self.quantiles = [0.1, 0.5, 0.9]
        self.forecast_head = nn.Linear(d_model, len(self.quantiles))

    def forward(self, iot_seq, finance_seq):
        """
        iot_seq: [Batch, Long_Seq_Len, iot_dim] (e.g., L=10000)
        finance_seq: [Batch, Short_Seq_Len, finance_dim] (e.g., L=30)
        """
        # 1. Process long IoT telemetry linearly using Mamba
        iot_enc = self.iot_proj(iot_seq)
        for mamba in self.mamba_blocks:
            iot_enc = mamba(iot_enc)
            
        # 2. Project short financial sequence
        fin_enc = self.fin_proj(finance_seq)
        
        # 3. Cross-Modal Fusion via Attention
        # Use finance as Query, IoT as Key/Value (condensing long context to short)
        fused_out, attention_weights = self.cross_attention(fin_enc, iot_enc, iot_enc)
        
        # Take the last fused timestep for prediction
        last_state = fused_out[:, -1, :]
        
        # 4. Predict quantiles (p10, p50, p90)
        predictions = self.forecast_head(last_state)
        
        return predictions, attention_weights
