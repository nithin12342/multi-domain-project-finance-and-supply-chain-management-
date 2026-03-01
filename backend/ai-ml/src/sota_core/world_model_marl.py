import torch
import torch.nn as nn
from torch.distributions import Normal

class RSSM(nn.Module):
    """
    Recurrent State Space Model (Core of DreamerV3 World Models).
    Learns to predict future states in an abstract latent space without requiring
    interaction with the actual environment during 'dreaming' phases.
    """
    def __init__(self, action_dim, obs_dim, embed_dim=256, det_size=200, stoch_size=32):
        super().__init__()
        self.det_size = det_size
        self.stoch_size = stoch_size
        
        # Encoder (Observation -> Embedding)
        self.encoder = nn.Sequential(
            nn.Linear(obs_dim, embed_dim),
            nn.ELU(),
            nn.Linear(embed_dim, embed_dim)
        )
        
        # Recurrent Dynamics Model (RNN transition)
        self.rnn = nn.GRUCell(embed_dim + action_dim, det_size)
        
        # Representation Model (Posterior): observation + deterministic state -> stochastic state
        self.rep_model = nn.Sequential(
            nn.Linear(embed_dim + det_size, embed_dim),
            nn.ELU(),
            nn.Linear(embed_dim, stoch_size * 2) # mean and variance
        )
        
        # Transition Model (Prior): deterministic state -> projected stochastic state
        self.trans_model = nn.Sequential(
            nn.Linear(det_size, embed_dim),
            nn.ELU(),
            nn.Linear(embed_dim, stoch_size * 2)
        )
        
        # Mixture of Recursion (MoR) Halting Router
        # Evaluates if more recursive refinement is needed for the current latent state
        self.mor_router = nn.Sequential(
            nn.Linear(det_size + stoch_size, 64),
            nn.ELU(),
            nn.Linear(64, 1),
            nn.Sigmoid() # Outputs probability to HALT (1 = halt, 0 = recurse)
        )
        
        # Maximum allowed recursion depth
        self.max_recurse_depth = 5
        
    def observe(self, obs, action, prev_state):
        """Posterior inference step (incorporates real observational data) with Mixture of Recursion"""
        prev_det, prev_stoch = prev_state
        
        # Encode actual observation
        embed = self.encoder(obs)
        
        # Base input for recurrence
        current_det = prev_det
        current_stoch = prev_stoch
        
        # Mixture of Recursion (MoR) Loop
        # Dynamically refines the internal state up to max_recurse_depth based on complexity
        for depth in range(self.max_recurse_depth):
            # Recurrent step
            rnn_input = torch.cat([current_stoch, action], dim=-1)
            next_det = self.rnn(rnn_input, current_det)
            
            # Get posterior stochastic state
            rep_input = torch.cat([embed, next_det], dim=-1)
            stats = self.rep_model(rep_input)
            mean, std = stats.chunk(2, dim=-1)
            std = torch.nn.functional.softplus(std) + 0.1
            
            # Reparameterization trick
            dist = Normal(mean, std)
            next_stoch = dist.rsample()
            
            # Check halting condition
            halt_prob = self.mor_router(torch.cat([next_det, next_stoch], dim=-1))
            
            if halt_prob.mean().item() > 0.5: # Simple threshold logic for halting
                break
                
            # Prepare for next potential recursive step (action becomes zero-vector as it's an internal deliberation step)
            current_det = next_det
            current_stoch = next_stoch
            action = torch.zeros_like(action) 
            
        return (next_det, next_stoch), dist
        
    def imagine(self, action, prev_state):
        """Prior inference step (predicting futures without actual observations) with Mixture of Recursion"""
        prev_det, prev_stoch = prev_state
        
        current_det = prev_det
        current_stoch = prev_stoch
        
        # Mixture of Recursion (MoR) Loop
        for depth in range(self.max_recurse_depth):
            # Recurrent step
            rnn_input = torch.cat([current_stoch, action], dim=-1)
            next_det = self.rnn(rnn_input, current_det)
            
            # Get prior stochastic state
            stats = self.trans_model(next_det)
            mean, std = stats.chunk(2, dim=-1)
            std = torch.nn.functional.softplus(std) + 0.1
            
            dist = Normal(mean, std)
            next_stoch = dist.rsample()
            
            # Check halting condition
            halt_prob = self.mor_router(torch.cat([next_det, next_stoch], dim=-1))
            
            if halt_prob.mean().item() > 0.5:
                break
                
            current_det = next_det
            current_stoch = next_stoch
            action = torch.zeros_like(action)
            
        return (next_det, next_stoch), dist

class ProcessRewardModel(nn.Module):
    """
    Evaluates intermediate reasoning and planning steps of MARL agents 
    rather than just evaluating final scalar outcomes (like end-of-quarter profit).
    """
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.scorer = nn.Sequential(
            nn.Linear(state_dim + action_dim, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )
        
    def forward(self, abstract_state, action):
        return self.scorer(torch.cat([abstract_state, action], dim=-1))

class MARLWorldModelAgent(nn.Module):
    """
    A single autonomous Agent (e.g., Finance Agent or Inventory Agent)
    equipped with a World Model to imagine trajectories before acting.
    """
    def __init__(self, obs_dim, action_dim):
        super().__init__()
        self.world_model = RSSM(action_dim, obs_dim)
        
        # Actor/Critic Networks operate purely on the abstract latent states
        latent_dim = self.world_model.det_size + self.world_model.stoch_size
        
        self.actor = nn.Sequential(
            nn.Linear(latent_dim, 128),
            nn.ELU(),
            nn.Linear(128, action_dim),
            nn.Softmax(dim=-1)
        )
        
        self.critic = nn.Sequential(
            nn.Linear(latent_dim, 128),
            nn.ELU(),
            nn.Linear(128, 1)
        )
        
        # Process-Reward mechanism for fine-grained action critique
        self.prm = ProcessRewardModel(latent_dim, action_dim)
        
    def get_action(self, obs, prev_state):
        # 1. Update internal state based on true environment observation
        next_state, _ = self.world_model.observe(obs, torch.zeros_like(self.actor[-2].out_features), prev_state) 
        latent = torch.cat(next_state, dim=-1)
        
        # 2. Select optimal action from the Actor policy
        action_probs = self.actor(latent)
        
        return action_probs, next_state
