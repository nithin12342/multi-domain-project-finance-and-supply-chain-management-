import torch
import torch.nn as nn
import torch.nn.functional as F

class MixtureOfExperts(nn.Module):
    """
    Mixture of Experts (MoE) routing layer to specialize sub-networks across 
    supply chain, finance, and IoT domains.
    """
    def __init__(self, input_dim, hidden_dim, num_experts=4, top_k=2):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k
        self.router = nn.Linear(input_dim, num_experts)
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(input_dim, hidden_dim),
                nn.GELU(),
                nn.Linear(hidden_dim, input_dim)
            ) for _ in range(num_experts)
        ])

    def forward(self, x):
        # x shape: [batch_size, input_dim]
        routing_logits = self.router(x)
        routing_probs = F.softmax(routing_logits, dim=-1)
        
        # Select Top-K experts
        topk_probs, topk_indices = torch.topk(routing_probs, self.top_k, dim=-1)
        topk_probs = topk_probs / topk_probs.sum(dim=-1, keepdim=True) # Normalize
        
        output = torch.zeros_like(x)
        for i in range(self.top_k):
            expert_idx = topk_indices[:, i]
            expert_prob = topk_probs[:, i].unsqueeze(-1)
            
            # Route to respective experts (Batching logic simplified for blueprint)
            for expert_id in range(self.num_experts):
                mask = (expert_idx == expert_id)
                if mask.any():
                    expert_input = x[mask]
                    expert_output = self.experts[expert_id](expert_input)
                    output[mask] += expert_output * expert_prob[mask]
                    
        return output

class DynamicHypergraphLayer(nn.Module):
    """
    Hypergraph Neural Network layer. 
    Models higher-order relationships (e.g., multiple suppliers sharing the same shipping lane)
    using the hypergraph incidence matrix H.
    """
    def __init__(self, in_features, out_features):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)
        
    def forward(self, x, H, W):
        """
        x: Node features [num_nodes, in_features]
        H: Incidence matrix [num_nodes, num_hyperedges]
        W: Hyperedge weights [num_hyperedges, num_hyperedges] (Diagonal)
        """
        # Node degree Dv and Hyperedge degree De
        Dv = torch.sum(H, dim=1).clamp(min=1) # Degree of nodes
        De = torch.sum(H, dim=0).clamp(min=1) # Degree of hyperedges
        
        Dv_inv_sqrt = torch.diag(torch.pow(Dv, -0.5))
        De_inv = torch.diag(torch.pow(De, -1.0))
        
        # Hypergraph Laplacian: Dv^{-1/2} * H * W * De^{-1} * H^T * Dv^{-1/2}
        # Note: In production, use sparse matrix multiplication for scale
        L = Dv_inv_sqrt @ H @ W @ De_inv @ H.t() @ Dv_inv_sqrt
        
        # Message passing over hyperedges
        out = L @ self.linear(x)
        return F.gelu(out)

class SpatioTemporalHyperGNN(nn.Module):
    """
    Combines Dynamic Hypergraphs with MoE to model cascading structural risk.
    """
    def __init__(self, node_feature_dim, hidden_dim, num_nodes, num_experts=4):
        super().__init__()
        self.hypergraph_conv1 = DynamicHypergraphLayer(node_feature_dim, hidden_dim)
        self.hypergraph_conv2 = DynamicHypergraphLayer(hidden_dim, hidden_dim)
        
        self.moe_layer = MixtureOfExperts(hidden_dim, hidden_dim * 2, num_experts)
        self.risk_head = nn.Linear(hidden_dim, 1) # Predict probability of default/risk
        
    def forward(self, x_seq, H_seq, W_seq):
        """
        x_seq: Temporal sequence of node features
        H_seq, W_seq: Dynamic topology over time
        """
        batch_size, seq_len, num_nodes, feat_dim = x_seq.shape
        states = []
        
        # Process structural risk at each timestep (Spatial)
        for t in range(seq_len):
            x_t = x_seq[:, t].squeeze(1) 
            H_t = H_seq[t]
            W_t = W_seq[t]
            
            h1 = self.hypergraph_conv1(x_t, H_t, W_t)
            h2 = self.hypergraph_conv2(h1, H_t, W_t)
            
            # Route node representations through MoE (Domain specialization)
            h_moe = self.moe_layer(h2)
            states.append(h_moe.unsqueeze(1))
            
        # Temporal aggregation (Simplified to mean for this blueprint)
        temporal_agg = torch.mean(torch.cat(states, dim=1), dim=1)
        
        risk_scores = torch.sigmoid(self.risk_head(temporal_agg))
        return risk_scores
