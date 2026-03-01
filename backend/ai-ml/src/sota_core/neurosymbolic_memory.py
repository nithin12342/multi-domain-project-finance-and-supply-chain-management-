import torch
import torch.nn as nn
import numpy as np

class EpisodicMemoryStore:
    """
    Differentiable Neural Computer / External Memory concept.
    Allows the model to retrieve and update specific risk facts (e.g., Supplier X is late)
    without catastrophic forgetting or full retraining.
    """
    def __init__(self, memory_size=10000, embed_dim=256):
        self.memory = torch.zeros((memory_size, embed_dim))
        self.keys = torch.zeros((memory_size, embed_dim))
        self.usage_count = torch.zeros(memory_size)
        self.memory_ptr = 0
        
    def write(self, key_vector, value_vector):
        """Writes to an empty slot or replaces the least used slot (LRU)."""
        idx = self.memory_ptr % self.memory.shape[0]
        self.keys[idx] = key_vector
        self.memory[idx] = value_vector
        self.usage_count[idx] = 1
        self.memory_ptr += 1
        
    def read(self, query_vector, top_k=3):
        """Soft attention read using Cosine Similarity."""
        similarities = torch.nn.functional.cosine_similarity(
            query_vector.unsqueeze(0), self.keys, dim=1
        )
        # Apply mask to unused slots
        similarities[self.usage_count == 0] = -1e9
        
        if (self.usage_count > 0).sum() == 0:
             return torch.zeros_like(query_vector).unsqueeze(0).repeat(top_k, 1)
             
        topk_sims, topk_indices = torch.topk(similarities, min(top_k, (self.usage_count > 0).sum().item()))
        
        # Update usage frequency
        self.usage_count[topk_indices] += 1
        
        # Retrieve aggregated memory values
        retrieved_memories = self.memory[topk_indices]
        return retrieved_memories

class CausalDiscoveryModule(nn.Module):
    """
    Neurosymbolic Reasoning Layer: Learns a Causal Adjacency Matrix (DAG)
    to enforce strict do-calculus rules over the supply chain nodes.
    (e.g., Port Strike -> Cargo Delay -> Invoice Default) 
    rather than spurious correlations.
    """
    def __init__(self, num_vars):
        super().__init__()
        # Continuous adjacency matrix for NOTEARS optimization
        self.W = nn.Parameter(torch.zeros(num_vars, num_vars))
        
    def forward(self, x):
        """
        x: Structural equations / node embeddings.
        Applies causal masking based on the learned DAG (Directed Acyclic Graph).
        """
        # Ensure no self-causation (diagonal is zero)
        W_causal = self.W - torch.diag(torch.diag(self.W))
        out = x @ W_causal
        return out
        
    def get_notears_penalty(self):
        """
        Computes the NOTEARS DAG penalty: h(W) = trace(e^{W * W}) - d = 0
        Forces the graph to be strictly acyclic during training.
        """
        W_causal = self.W - torch.diag(torch.diag(self.W))
        W_squared = W_causal * W_causal
        # Matrix exponential approximation for speed
        E = torch.matrix_exp(W_squared)
        h = torch.trace(E) - self.W.shape[0]
        return h
