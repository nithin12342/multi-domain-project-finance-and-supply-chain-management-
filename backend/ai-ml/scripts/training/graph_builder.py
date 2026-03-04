"""
Builds directed weighted transaction graphs from IEEE-CIS and PaySim chunks.
Designed for: FraudDetectionMLP's 15→100 feature pipeline.

Graph semantics:
  Nodes  → Account identifiers (card hash or account name)
  Edges  → Transactions (directed: sender → receiver)
  Weights→ Transaction amount (normalized log scale)
"""

import networkx as nx
import numpy as np
import pandas as pd
import hashlib
from typing import Tuple, Optional
from feature_config import CFG


class TransactionGraphBuilder:

    # ── IEEE-CIS Graph ────────────────────────────────────────────────────────
    @staticmethod
    def _ieee_node_id(row: pd.Series) -> str:
        """
        Composite node fingerprint from card identity fields.
        card1+card2+addr1 creates a pseudo-account identifier
        without exposing raw PII.
        """
        raw = f"{row.get('card1', '')}_{row.get('card2', '')}_{row.get('addr1', '')}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]

    @classmethod
    def build_ieee_graph(cls, chunk: pd.DataFrame) -> nx.DiGraph:
        """
        Builds directed graph from IEEE-CIS chunk.
        Edge: card_sender → ProductCD_receiver (bipartite proxy)
        Edge weight: log1p(TransactionAmt) for numerical stability
        """
        G = nx.DiGraph()
        for _, row in chunk.iterrows():
            src = cls._ieee_node_id(row)
            # Product code as destination proxy (merchant type)
            dst = f"merch_{row.get('ProductCD', 'UNK')}_{row.get('addr2', '0')}"
            weight = np.log1p(float(row.get('TransactionAmt', 0)))
            
            if G.has_edge(src, dst):
                # Accumulate multiple transactions between same pair
                G[src][dst]['weight']      += weight
                G[src][dst]['tx_count']    += 1
                G[src][dst]['amt_list'].append(weight)
            else:
                G.add_edge(src, dst,
                           weight=weight,
                           tx_count=1,
                           amt_list=[weight])

        # Guard against pathologically large graphs on Colab RAM
        if G.number_of_nodes() > CFG.max_graph_nodes:
            # Keep highest-degree subgraph for feature stability
            top_nodes = sorted(G.degree, key=lambda x: x[1],
                               reverse=True)[:CFG.max_graph_nodes]
            G = G.subgraph([n for n, _ in top_nodes]).copy()

        return G

    # ── PaySim Graph ──────────────────────────────────────────────────────────
    @staticmethod
    def build_paysim_graph(chunk: pd.DataFrame) -> nx.DiGraph:
        """
        PaySim: nameOrig → nameDest directed graph.
        Captures layered money transfer chains (A→B→C→D→A).
        Edge weight: log1p(amount).
        """
        G = nx.DiGraph()
        for _, row in chunk.iterrows():
            src    = row['nameOrig']
            dst    = row['nameDest']
            weight = np.log1p(float(row['amount']))
            step   = int(row['step'])

            if G.has_edge(src, dst):
                G[src][dst]['weight']   += weight
                G[src][dst]['tx_count'] += 1
                G[src][dst]['steps'].append(step)
            else:
                G.add_edge(src, dst,
                           weight=weight,
                           tx_count=1,
                           steps=[step],
                           balance_delta=(
                               float(row['newbalanceOrig'])
                               - float(row['oldbalanceOrg'])
                           ))

        return G

    # ── DataCo Supply Chain Graph ─────────────────────────────────────────────
    @staticmethod
    def build_supply_chain_graph(df: pd.DataFrame) -> nx.DiGraph:
        """
        Tripartite graph: Supplier → Warehouse → Customer
        Edges carry delivery risk and order quantity as weights.
        Used for bottleneck detection, not fraud classification.
        """
        G = nx.DiGraph()
        for _, row in df.iterrows():
            region   = str(row.get('Order Region', 'UNK'))
            market   = str(row.get('Market', 'UNK'))
            customer = str(row.get('Customer Id', 'UNK'))
            qty      = float(row.get('Order Item Quantity', 1))
            risk     = int(row.get('Late_delivery_risk', 0))

            # Region (supplier proxy) → Market (warehouse proxy)
            G.add_edge(f"region_{region}", f"market_{market}",
                       weight=qty, delivery_risk=risk)
            # Market → Customer
            G.add_edge(f"market_{market}", f"cust_{customer}",
                       weight=qty, delivery_risk=risk)

        return G
