"""
SOPHISTICATED 100-FEATURE EXTRACTION ENGINE
==========================================
Categories:
  [A]  15 Baseline features (preserved from original pipeline)
  [B]  12 Extended centrality features
  [C]  13 Spectral graph features (Laplacian eigenvalues, Fiedler)
  [D]  12 TDA features (Betti numbers, persistence statistics)
  [E]  10 Community structure features
  [F]  11 Temporal/velocity features (PaySim-specific)
  [G]   7 Transaction pattern features (motif counts)
  [H]   7 Rough path signature features (pure NumPy iterated integrals)
  [I]  13 Dataset-specific features (type distribution, amount ratios)
  ─────────────────────────────────────────────────────
  Total: 100 features
"""

import networkx as nx
import numpy as np
import pandas as pd
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import scipy.stats as stats
from collections import defaultdict
from typing import Dict, Optional, List
import warnings
import logging

# Optional heavy imports with graceful fallback
try:
    import gudhi
    HAS_GUDHI = True
except ImportError:
    HAS_GUDHI = False
    warnings.warn("gudhi not available — TDA features will use fallback approximations.")

try:
    import community as community_louvain  # python-louvain
    HAS_LOUVAIN = True
except ImportError:
    HAS_LOUVAIN = False

# DISABLED: esig/roughpy 0.2.0 has a C++ bug ("mismatch between number of rows
# in data and number of indices"). Using statistical fallback for [H] features.
# Re-enable when roughpy >= 0.3 is released.
HAS_ESIG = False
_esig_logsig_fn = None

from feature_config import CFG, FeatureExtractionConfig

logger = logging.getLogger(__name__)


class AdvancedFeatureExtractor:
    """
    Extracts 100 designer-grade features from a transaction graph chunk.
    All methods return dict[str, float] for clean DataFrame assembly.
    """

    def __init__(self, config: FeatureExtractionConfig = CFG):
        self.cfg = config

    # ═══════════════════════════════════════════════════════════════════════
    # [A] BASELINE FEATURES (15) — Preserved from original pipeline
    # ═══════════════════════════════════════════════════════════════════════
    def extract_baseline_features(
        self, G: nx.DiGraph, amounts: List[float]
    ) -> Dict[str, float]:

        feats = {}
        if G.number_of_nodes() == 0:
            return self._zero_baseline()

        # PageRank
        try:
            pr = nx.pagerank(G, weight='weight', max_iter=100)
            pr_vals = list(pr.values())
            feats['pagerank_max']      = float(np.max(pr_vals))
            feats['pagerank_mean']     = float(np.mean(pr_vals))
            feats['pagerank_variance'] = float(np.var(pr_vals))
            pr_arr = np.array(pr_vals)
            pr_arr = pr_arr / (pr_arr.sum() + 1e-12)
            feats['pagerank_entropy']  = float(
                -np.sum(pr_arr * np.log(pr_arr + 1e-12))
            )
        except Exception:
            feats.update({k: 0.0 for k in [
                'pagerank_max','pagerank_mean',
                'pagerank_variance','pagerank_entropy'
            ]})

        # Clustering
        G_undir = G.to_undirected()
        try:
            cc = list(nx.clustering(G_undir).values())
            feats['cluster_coeff_avg'] = float(np.mean(cc))
            feats['cluster_coeff_max'] = float(np.max(cc))
            feats['cluster_coeff_std'] = float(np.std(cc))
        except Exception:
            feats.update({k: 0.0 for k in [
                'cluster_coeff_avg','cluster_coeff_max','cluster_coeff_std'
            ]})

        # Structural
        n, m = G.number_of_nodes(), G.number_of_edges()
        feats['edge_density']       = nx.density(G)
        degrees = [d for _, d in G.degree()]
        feats['degree_max']         = float(max(degrees)) if degrees else 0.0
        feats['degree_mean']        = float(np.mean(degrees)) if degrees else 0.0
        feats['degree_std']         = float(np.std(degrees)) if degrees else 0.0

        # Connectivity
        wccs = list(nx.weakly_connected_components(G))
        largest_wcc = max(len(c) for c in wccs) if wccs else 0
        feats['largest_wcc_ratio']  = largest_wcc / n if n > 0 else 0.0

        # Amount statistics
        amt = np.array(amounts, dtype=np.float32)
        feats['amount_std']  = float(np.std(amt)) if len(amt) > 1 else 0.0
        feats['amount_skew'] = float(stats.skew(amt)) if len(amt) > 2 else 0.0

        # Reciprocity
        feats['reciprocity'] = nx.overall_reciprocity(G) if m > 0 else 0.0

        return feats

    # ═══════════════════════════════════════════════════════════════════════
    # [B] EXTENDED CENTRALITY FEATURES (12)
    # ═══════════════════════════════════════════════════════════════════════
    def extract_centrality_features(self, G: nx.DiGraph) -> Dict[str, float]:
        feats = {}
        n = G.number_of_nodes()
        if n < 3:
            return {k: 0.0 for k in self._centrality_keys()}

        # Betweenness centrality — identifies bridge/bottleneck nodes
        # k-sampling for large graphs: O(k*(n+m)) instead of O(n*(n+m))
        try:
            k_sample = min(50, n) if n > 100 else None
            bc = list(nx.betweenness_centrality(G, normalized=True,
                                                 weight='weight',
                                                 k=k_sample).values())
            feats['betweenness_max']    = float(np.max(bc))
            feats['betweenness_mean']   = float(np.mean(bc))
            feats['betweenness_std']    = float(np.std(bc))
            feats['betweenness_gini']   = self._gini_coefficient(bc)
        except Exception:
            feats.update({k: 0.0 for k in [
                'betweenness_max','betweenness_mean',
                'betweenness_std','betweenness_gini'
            ]})

        # Eigenvector centrality — high-influence node detection
        try:
            ec = list(nx.eigenvector_centrality_numpy(G, weight='weight').values())
            feats['eigenvec_centrality_max']  = float(np.max(ec))
            feats['eigenvec_centrality_mean'] = float(np.mean(ec))
            feats['eigenvec_centrality_std']  = float(np.std(ec))
        except Exception:
            feats.update({k: 0.0 for k in [
                'eigenvec_centrality_max',
                'eigenvec_centrality_mean',
                'eigenvec_centrality_std'
            ]})

        # HITS: Hub vs Authority separation
        # Fraud rings often show extreme hub-authority imbalance
        try:
            hubs, authorities = nx.hits(G, max_iter=100, normalized=True)
            hub_vals  = list(hubs.values())
            auth_vals = list(authorities.values())
            feats['hits_hub_max']        = float(np.max(hub_vals))
            feats['hits_authority_max']  = float(np.max(auth_vals))
            # Hub-authority divergence: large gap signals one-directional rings
            feats['hits_hub_auth_ratio'] = (
                feats['hits_hub_max'] / (feats['hits_authority_max'] + 1e-12)
            )
        except Exception:
            feats.update({k: 0.0 for k in [
                'hits_hub_max','hits_authority_max','hits_hub_auth_ratio'
            ]})

        # Katz centrality — path-weighted global influence
        # Skip for large graphs (eigvals is O(n³))
        if n <= 200:
            try:
                A = nx.to_numpy_array(G)
                spectral_radius = np.max(np.abs(np.linalg.eigvals(A))) + 1e-12
                alpha = 0.8 / spectral_radius
                kc = list(nx.katz_centrality_numpy(G, alpha=alpha).values())
                feats['katz_centrality_max']  = float(np.max(kc))
                feats['katz_centrality_mean'] = float(np.mean(kc))
            except Exception:
                feats.update({k: 0.0 for k in [
                    'katz_centrality_max','katz_centrality_mean'
                ]})
        else:
            feats['katz_centrality_max']  = 0.0
            feats['katz_centrality_mean'] = 0.0

        return feats

    # ═══════════════════════════════════════════════════════════════════════
    # [C] SPECTRAL GRAPH FEATURES (14)
    # ═══════════════════════════════════════════════════════════════════════
    def extract_spectral_features(self, G: nx.DiGraph) -> Dict[str, float]:
        """
        Laplacian eigenvalue spectrum reveals global connectivity structure.
        Spectral gap (λ₂ - λ₁) is the Algebraic Connectivity / Fiedler value.
        Small spectral gap = bridge-like structure = fraud ring vulnerability.
        """
        feats = {}
        n = G.number_of_nodes()
        if n < 4:
            return {k: 0.0 for k in self._spectral_keys()}

        try:
            G_undir = G.to_undirected()
            k = min(self.cfg.top_k_eigenvalues, n - 2)

            if n > self.cfg.sparse_threshold:
                # Sparse eigensolver for large graphs (Colab memory guard)
                L = nx.laplacian_matrix(G_undir).astype(float)
                eigenvalues = spla.eigsh(
                    L, k=k, which='SM', return_eigenvectors=False
                )
                eigenvalues = np.sort(np.abs(eigenvalues))
            else:
                L = nx.laplacian_matrix(G_undir).toarray().astype(float)
                eigenvalues = np.linalg.eigvalsh(L)
                eigenvalues = np.sort(eigenvalues)[:k]

            # Fiedler value = λ₂ (algebraic connectivity)
            feats['fiedler_value']       = float(eigenvalues[1]) if len(eigenvalues) > 1 else 0.0
            # Spectral gap: λ₂ - λ₁ (λ₁ ≈ 0 for connected graphs)
            feats['spectral_gap']        = float(eigenvalues[1] - eigenvalues[0]) if len(eigenvalues) > 1 else 0.0
            feats['laplacian_lambda_max']= float(eigenvalues[-1])
            feats['spectral_radius']     = float(eigenvalues[-1])
            
            # Spectral spread: ratio of max to second eigenvalue
            feats['spectral_spread']     = (
                eigenvalues[-1] / (eigenvalues[1] + 1e-12)
                if len(eigenvalues) > 1 else 0.0
            )
            
            # Eigenvalue statistics across top-k spectrum
            feats['eigenvalue_mean']     = float(np.mean(eigenvalues))
            feats['eigenvalue_std']      = float(np.std(eigenvalues))
            feats['eigenvalue_entropy']  = float(stats.entropy(eigenvalues + 1e-12))

            # Fiedler vector distribution (natural bisection indicator)
            if n <= self.cfg.sparse_threshold:
                _, eigenvectors = np.linalg.eigh(L)
                fiedler_vec = eigenvectors[:, 1] if eigenvectors.shape[1] > 1 else eigenvectors[:, 0]
                feats['fiedler_vec_std']     = float(np.std(fiedler_vec))
                feats['fiedler_vec_range']   = float(np.ptp(fiedler_vec))
                # Negative components indicate nodes in the "smaller" partition
                feats['fiedler_neg_fraction']= float(np.mean(fiedler_vec < 0))
            else:
                feats.update({'fiedler_vec_std': 0.0,
                              'fiedler_vec_range': 0.0,
                              'fiedler_neg_fraction': 0.0})

            # Cheeger constant approximation (bottleneck measure)
            # h(G) ≈ λ₂/2 by Cheeger inequality
            feats['cheeger_approx'] = float(feats['fiedler_value'] / 2.0)

            # Energy: sum of squared eigenvalues (graph complexity measure)
            feats['laplacian_energy'] = float(np.sum(eigenvalues ** 2))

        except Exception as e:
            logger.warning(f"Spectral extraction failed: {e}")
            feats = {k: 0.0 for k in self._spectral_keys()}

        return feats

    # ═══════════════════════════════════════════════════════════════════════
    # [D] TDA FEATURES — PERSISTENT HOMOLOGY (12)
    # ═══════════════════════════════════════════════════════════════════════
    def extract_tda_features(self, G: nx.DiGraph) -> Dict[str, float]:
        """
        Topological Data Analysis via Vietoris-Rips complex on graph distance matrix.
        
        β₀ (0th Betti number): Connected components count
        β₁ (1st Betti number): Independent cycles / loops (CRITICAL for fraud rings)
        β₂ (2nd Betti number): Enclosed voids (3D topological cavities)
        
        A fraud ring manifests as β₁ >> 0 (many independent cycles).
        """
        feats = {}
        n = G.number_of_nodes()

        if n < 4 or not HAS_GUDHI:
            # Fallback: use NetworkX cycle count as β₁ proxy
            return self._tda_fallback(G)

        try:
            # Step 1: Compute shortest path distance matrix for Rips filtration
            # Using weighted distances (inverse amount = cost)
            G_weighted = G.copy()
            for u, v, data in G_weighted.edges(data=True):
                # Convert weight to distance: high-amount = close = more suspicious
                data['distance'] = 1.0 / (data.get('weight', 1.0) + 1e-12)

            # Truncate to manageable size for TDA (Rips complex is O(n²))
            # 50 nodes is enough for topological structure; 200 hangs GUDHI
            max_nodes_tda = min(n, 50)
            if n > max_nodes_tda:
                # Sample by degree (keep high-degree fraud-ring nodes)
                top_nodes = sorted(G.degree, key=lambda x: x[1],
                                   reverse=True)[:max_nodes_tda]
                sub_G = G_weighted.subgraph([nd for nd, _ in top_nodes])
            else:
                sub_G = G_weighted

            nodes = list(sub_G.nodes())
            n_sub = len(nodes)
            node_idx = {nd: i for i, nd in enumerate(nodes)}

            # Distance matrix
            dist_matrix = np.full((n_sub, n_sub), np.inf)
            np.fill_diagonal(dist_matrix, 0.0)

            for u, v, data in sub_G.edges(data=True):
                i, j = node_idx[u], node_idx[v]
                d = data.get('distance', 1.0)
                dist_matrix[i][j] = min(dist_matrix[i][j], d)
                dist_matrix[j][i] = min(dist_matrix[j][i], d)  # symmetrize

            # Replace inf with large finite value (disconnected pairs)
            max_finite = np.max(dist_matrix[np.isfinite(dist_matrix)])
            dist_matrix[~np.isfinite(dist_matrix)] = max_finite * 2

            # Step 2: Rips complex filtration via GUDHI
            rips = gudhi.RipsComplex(
                distance_matrix=dist_matrix,
                max_edge_length=max_finite
            )
            st = rips.create_simplex_tree(max_dimension=self.cfg.max_homology_dim)
            st.compute_persistence()

            # Step 3: Extract Betti numbers at mid-filtration
            betti = st.betti_numbers()
            feats['betti_0'] = float(betti[0]) if len(betti) > 0 else 0.0
            feats['betti_1'] = float(betti[1]) if len(betti) > 1 else 0.0  # FRAUD RING SIGNAL
            feats['betti_2'] = float(betti[2]) if len(betti) > 2 else 0.0

            # Step 4: Persistence statistics per homology dimension
            for dim in range(min(self.cfg.max_homology_dim, 2)):
                pairs = st.persistence_intervals_in_dimension(dim)
                if len(pairs) > 0:
                    lifetimes = np.array([
                        (d - b) for b, d in pairs
                        if np.isfinite(d) and (d - b) > self.cfg.persistence_threshold
                    ])
                    if len(lifetimes) > 0:
                        feats[f'persistence_mean_dim{dim}']  = float(np.mean(lifetimes))
                        feats[f'persistence_max_dim{dim}']   = float(np.max(lifetimes))
                        feats[f'persistence_entropy_dim{dim}']= float(
                            stats.entropy(lifetimes / (lifetimes.sum() + 1e-12))
                        )
                    else:
                        feats.update({
                            f'persistence_mean_dim{dim}': 0.0,
                            f'persistence_max_dim{dim}': 0.0,
                            f'persistence_entropy_dim{dim}': 0.0,
                        })
                else:
                    feats.update({
                        f'persistence_mean_dim{dim}': 0.0,
                        f'persistence_max_dim{dim}': 0.0,
                        f'persistence_entropy_dim{dim}': 0.0,
                    })

            # Step 5: Simplex count per dimension (triangle density = ring density)
            feats['simplex_count_dim0'] = float(sum(
                1 for s, _ in st.get_filtration() if len(s) == 1
            ))
            feats['simplex_count_dim1'] = float(sum(
                1 for s, _ in st.get_filtration() if len(s) == 2
            ))
            feats['simplex_count_dim2'] = float(sum(
                1 for s, _ in st.get_filtration() if len(s) == 3
            ))  # TRIANGLE COUNT = 2-simplex count (fraud ring proxy)

        except Exception as e:
            logger.warning(f"TDA failed, using fallback: {e}")
            feats = self._tda_fallback(G)

        return feats

    def _tda_fallback(self, G: nx.DiGraph) -> Dict[str, float]:
        """NetworkX-based topological fallback when GUDHI unavailable."""
        G_undir = G.to_undirected()
        wccs = list(nx.weakly_connected_components(G))
        try:
            cycles = nx.cycle_basis(G_undir)
        except Exception:
            cycles = []
        
        return {
            'betti_0': float(len(wccs)),
            'betti_1': float(len(cycles)),       # Approx β₁
            'betti_2': 0.0,
            'persistence_mean_dim0': 0.0,
            'persistence_max_dim0': float(len(wccs)),
            'persistence_entropy_dim0': 0.0,
            'persistence_mean_dim1': float(np.mean([len(c) for c in cycles])) if cycles else 0.0,
            'persistence_max_dim1': float(max([len(c) for c in cycles])) if cycles else 0.0,
            'persistence_entropy_dim1': 0.0,
            'simplex_count_dim0': float(G.number_of_nodes()),
            'simplex_count_dim1': float(G.number_of_edges()),
            'simplex_count_dim2': float(len(cycles)),
        }

    # ═══════════════════════════════════════════════════════════════════════
    # [E] COMMUNITY STRUCTURE FEATURES (10)
    # ═══════════════════════════════════════════════════════════════════════
    def extract_community_features(self, G: nx.DiGraph) -> Dict[str, float]:
        """
        Fraud rings form unnaturally tight, small communities with
        high intra-community edge density and near-zero inter-community flow.
        Louvain modularity score distinguishes ring-like vs organic structure.
        """
        feats = {}
        G_undir = G.to_undirected()
        n = G_undir.number_of_nodes()

        if n < 4 or not HAS_LOUVAIN:
            return {k: 0.0 for k in self._community_keys()}

        try:
            partition = community_louvain.best_partition(
                G_undir,
                resolution=self.cfg.louvain_resolution,
                weight='weight'
            )
            modularity = community_louvain.modularity(partition, G_undir)

            community_sizes = defaultdict(int)
            for node, comm_id in partition.items():
                community_sizes[comm_id] += 1

            sizes = list(community_sizes.values())
            n_communities = len(sizes)

            feats['louvain_modularity']     = float(modularity)
            feats['n_communities']          = float(n_communities)
            feats['community_size_mean']    = float(np.mean(sizes))
            feats['community_size_std']     = float(np.std(sizes))
            feats['community_size_max']     = float(np.max(sizes))
            feats['community_size_min']     = float(np.min(sizes))
            feats['community_gini']         = self._gini_coefficient(sizes)

            # Intra-community edge ratio
            intra_edges = sum(
                1 for u, v in G_undir.edges()
                if partition.get(u) == partition.get(v)
            )
            feats['intra_community_edge_ratio'] = (
                intra_edges / G_undir.number_of_edges()
                if G_undir.number_of_edges() > 0 else 0.0
            )

            # Singleton ratio: isolated nodes (normal behavior proxy)
            feats['singleton_community_ratio'] = (
                sum(1 for s in sizes if s == 1) / n_communities
                if n_communities > 0 else 0.0
            )

            # Normalized coverage: how much of graph is in top community
            feats['top_community_coverage'] = (
                max(sizes) / n if n > 0 else 0.0
            )

        except Exception as e:
            logger.warning(f"Community detection failed: {e}")
            feats = {k: 0.0 for k in self._community_keys()}

        return feats

    # ═══════════════════════════════════════════════════════════════════════
    # [F] TEMPORAL VELOCITY FEATURES — PaySim Specific (12)
    # ═══════════════════════════════════════════════════════════════════════
    def extract_temporal_features(
        self, chunk: pd.DataFrame, is_paysim: bool = True
    ) -> Dict[str, float]:
        """
        PaySim's `step` column is a time proxy (hours).
        Fraud patterns exhibit abnormal velocity: rapid sequential transfers
        followed by CASH_OUT (layering signature).
        """
        feats = {}
        if not is_paysim or 'step' not in chunk.columns:
            return {k: 0.0 for k in self._temporal_keys()}

        try:
            # Transaction velocity: transactions per time step
            step_counts = chunk.groupby('step').size()
            feats['tx_velocity_max']   = float(step_counts.max())
            feats['tx_velocity_mean']  = float(step_counts.mean())
            feats['tx_velocity_std']   = float(step_counts.std()) if len(step_counts) > 1 else 0.0
            feats['tx_velocity_cv']    = (
                feats['tx_velocity_std'] / (feats['tx_velocity_mean'] + 1e-12)
            )

            # Amount velocity: rate of change using EWMA
            amounts = chunk.sort_values('step')['amount'].values.astype(np.float32)
            ewma = pd.Series(amounts).ewm(alpha=self.cfg.amount_ewma_alpha).mean().values
            amount_deltas = np.diff(ewma)
            feats['amount_velocity_max']  = float(np.max(np.abs(amount_deltas))) if len(amount_deltas) > 0 else 0.0
            feats['amount_velocity_mean'] = float(np.mean(np.abs(amount_deltas))) if len(amount_deltas) > 0 else 0.0

            # Balance anomaly: expected post-balance vs actual
            if all(c in chunk.columns for c in ['oldbalanceOrg','newbalanceOrig','amount']):
                expected_balance = chunk['oldbalanceOrg'] - chunk['amount']
                balance_anomaly  = (chunk['newbalanceOrig'] - expected_balance).abs()
                feats['balance_anomaly_mean'] = float(balance_anomaly.mean())
                feats['balance_anomaly_max']  = float(balance_anomaly.max())
                feats['zero_balance_count']   = float(
                    (chunk['newbalanceOrig'] == 0).sum()
                )
            else:
                feats.update({'balance_anomaly_mean': 0.0,
                              'balance_anomaly_max': 0.0,
                              'zero_balance_count': 0.0})

            # Time-to-reversal: TRANSFER followed by CASH_OUT pattern
            # (Classic layering: move money then immediately cash out)
            if 'type' in chunk.columns:
                transfers  = chunk[chunk['type'] == 'TRANSFER']['step'].values
                cash_outs  = chunk[chunk['type'] == 'CASH_OUT']['step'].values
                if len(transfers) > 0 and len(cash_outs) > 0:
                    # Minimum time gap between any transfer and subsequent cashout
                    gaps = []
                    for t in transfers:
                        subsequent = cash_outs[cash_outs > t]
                        if len(subsequent) > 0:
                            gaps.append(float(np.min(subsequent) - t))
                    feats['time_to_reversal_min']  = float(min(gaps)) if gaps else 999.0
                    feats['time_to_reversal_mean'] = float(np.mean(gaps)) if gaps else 999.0
                else:
                    feats['time_to_reversal_min']  = 999.0
                    feats['time_to_reversal_mean'] = 999.0
            else:
                feats['time_to_reversal_min']  = 999.0
                feats['time_to_reversal_mean'] = 999.0

        except Exception as e:
            logger.warning(f"Temporal feature extraction failed: {e}")
            feats = {k: 0.0 for k in self._temporal_keys()}

        return feats

    # ═══════════════════════════════════════════════════════════════════════
    # [G] MOTIF / PATTERN FEATURES (8)
    # ═══════════════════════════════════════════════════════════════════════
    def extract_motif_features(self, G: nx.DiGraph) -> Dict[str, float]:
        """
        Graph motifs are recurring sub-graph patterns.
        For fraud: triangles and 4-cycles are the key fraud ring signatures.
        A→B→C→A (3-cycle) and A→B→C→D→A (4-cycle) are classic laundering patterns.
        """
        feats = {}
        G_undir = G.to_undirected()
        n = G.number_of_nodes()

        if n < 3:
            return {k: 0.0 for k in self._motif_keys()}

        try:
            # Triangle count (3-node fraud rings)
            triangles = nx.triangles(G_undir)
            total_triangles = sum(triangles.values()) // 3
            feats['triangle_count']      = float(total_triangles)
            feats['triangle_density']    = (
                total_triangles / (n * (n-1) * (n-2) / 6 + 1e-12)
            )

            # Transitivity (global clustering = triangle fraction of triples)
            feats['transitivity'] = nx.transitivity(G_undir)

            # Square (4-cycle) counting — approximation via matrix multiplication
            # A⁴[i,i] counts closed 4-walks, divide by 8 for 4-cycles
            if n <= 500:  # Expensive for large graphs
                A = nx.to_numpy_array(G_undir)
                A2 = A @ A
                A4_diag = np.diag(A2 @ A2)
                # Approximate 4-cycle count
                four_cycles = max(0, (np.sum(A4_diag) - np.sum(A2)) / 8)
                feats['four_cycle_approx'] = float(four_cycles)
            else:
                feats['four_cycle_approx'] = -1.0  # Indicate skipped

            # Bow-tie structure: nodes with both high in-degree and out-degree
            # Characteristic of money mule accounts in layering schemes
            in_degrees  = dict(G.in_degree())
            out_degrees = dict(G.out_degree())
            bow_tie_nodes = sum(
                1 for node in G.nodes()
                if in_degrees[node] > 2 and out_degrees[node] > 2
            )
            feats['bow_tie_node_count']   = float(bow_tie_nodes)
            feats['bow_tie_node_fraction']= float(bow_tie_nodes / n) if n > 0 else 0.0

            # Sink node fraction: nodes with in-degree > 0 but out-degree = 0
            # Indicates terminal cash-out accounts
            sink_nodes = sum(
                1 for node in G.nodes()
                if in_degrees[node] > 0 and out_degrees[node] == 0
            )
            feats['sink_node_fraction'] = float(sink_nodes / n) if n > 0 else 0.0

        except Exception as e:
            logger.warning(f"Motif extraction failed: {e}")
            feats = {k: 0.0 for k in self._motif_keys()}

        return feats

    # ═══════════════════════════════════════════════════════════════════════
    # [H] ROUGH PATH SIGNATURE FEATURES (7) — Pure NumPy Implementation
    # ═══════════════════════════════════════════════════════════════════════
    def extract_path_signature_features(
        self, time_series: np.ndarray, depth: int = 3
    ) -> Dict[str, float]:
        """
        Pure NumPy iterated integral computation for path signatures.
        No external dependency (esig/roughpy) required.

        Computes the signature of a 2D path (time, amount) up to given depth
        using Chen's iterated integral formula directly.

        For a 2D path, depth-3 signature has 2+4+8=14 components.
        We summarize these into 7 statistics.
        """
        if len(time_series) < 4:
            return self._signature_zeros()

        try:
            # Construct 2D path: (normalized_time, normalized_amount)
            n = len(time_series)
            t = np.linspace(0, 1, n)
            std = time_series.std()
            a = (time_series - time_series.mean()) / (std + 1e-12)
            
            # Compute path increments
            dt = np.diff(t)  # shape: (n-1,)
            da = np.diff(a)  # shape: (n-1,)

            # Depth-1 signature: S^1, S^2 (integrals of dt, da)
            sig_depth1 = np.array([np.sum(dt), np.sum(da)])  # 2 components

            # Depth-2 signature: S^{ij} for i,j in {1,2}
            # S^{ij} = Σ_{s<t} dX^i_s * dX^j_t  (iterated integral)
            increments = np.stack([dt, da], axis=1)  # shape: (n-1, 2)
            cumsum = np.cumsum(increments, axis=0)   # running integral
            sig_depth2 = np.zeros(4)  # S^{11}, S^{12}, S^{21}, S^{22}
            for k in range(len(increments)):
                for i in range(2):
                    for j in range(2):
                        sig_depth2[i * 2 + j] += cumsum[k, i] * increments[k, j]

            # Depth-3 signature: S^{ijk} (8 components for 2D)
            sig_depth3 = np.zeros(8)
            cumsum2 = np.zeros((2, 2))  # running depth-2 integral
            for k in range(len(increments)):
                for i in range(2):
                    for j in range(2):
                        for l in range(2):
                            sig_depth3[i*4 + j*2 + l] += cumsum2[i, j] * increments[k, l]
                # Update running depth-2 cumulative
                for i in range(2):
                    for j in range(2):
                        cumsum2[i, j] += cumsum[k, i] * increments[k, j]

            # Full signature: concatenate all depths (2 + 4 + 8 = 14 components)
            full_sig = np.concatenate([sig_depth1, sig_depth2, sig_depth3])

            # Log-signature approximation: log(1 + sig) component-wise
            log_sig = np.sign(full_sig) * np.log1p(np.abs(full_sig))

            return {
                'log_sig_l2_norm':  float(np.linalg.norm(log_sig)),
                'log_sig_l1_norm':  float(np.sum(np.abs(log_sig))),
                'log_sig_max':      float(np.max(log_sig)),
                'log_sig_min':      float(np.min(log_sig)),
                'log_sig_entropy':  float(stats.entropy(np.abs(log_sig) + 1e-12)),
                'log_sig_mean':     float(np.mean(log_sig)),
                'log_sig_std':      float(np.std(log_sig)),
            }

        except Exception as e:
            logger.warning(f"Signature extraction failed: {e}")
            return self._signature_zeros()

    def _signature_zeros(self) -> Dict[str, float]:
        """Zero fallback for signatures (only for very short series)."""
        return {
            'log_sig_l2_norm': 0.0, 'log_sig_l1_norm': 0.0,
            'log_sig_max': 0.0, 'log_sig_min': 0.0,
            'log_sig_entropy': 0.0, 'log_sig_mean': 0.0,
            'log_sig_std': 0.0,
        }

    # ═══════════════════════════════════════════════════════════════════════
    # [I] DATASET-SPECIFIC FEATURES (13)
    # ═══════════════════════════════════════════════════════════════════════
    def extract_dataset_specific_features(
        self, G: nx.DiGraph, chunk: pd.DataFrame, is_paysim: bool = True
    ) -> Dict[str, float]:
        """
        Features derived from raw DataFrame columns, NOT graph structure.
        These capture transaction-level patterns that graphs alone miss.
        """
        feats = {}

        # ── Transaction Type Distribution (5) ─────────────────────────────
        # PaySim has 5 transaction types. Their proportions are strong signals:
        # Fraud concentrates in TRANSFER and CASH_OUT.
        if is_paysim and 'type' in chunk.columns:
            n_rows = len(chunk)
            for tx_type in ['TRANSFER', 'CASH_OUT', 'PAYMENT', 'DEBIT', 'CASH_IN']:
                col_name = f'type_ratio_{tx_type.lower()}'
                feats[col_name] = float(
                    (chunk['type'] == tx_type).sum() / n_rows
                )
        else:
            for tx_type in ['transfer', 'cash_out', 'payment', 'debit', 'cash_in']:
                feats[f'type_ratio_{tx_type}'] = 0.0

        # ── Amount Quantile Ratios (3) ────────────────────────────────────
        # Fraud transactions often have extreme amount distributions
        amt_col = 'amount' if 'amount' in chunk.columns else 'TransactionAmt'
        if amt_col in chunk.columns:
            amounts = chunk[amt_col].fillna(0).values.astype(np.float32)
            if len(amounts) > 0 and amounts.mean() > 0:
                q25, q50, q75, q95 = np.percentile(amounts, [25, 50, 75, 95])
                feats['amount_q95_q50_ratio'] = float(q95 / (q50 + 1e-12))
                feats['amount_q75_q25_ratio'] = float(q75 / (q25 + 1e-12))
                # Concentration: fraction of total amount from top 10% transactions
                sorted_amt = np.sort(amounts)[::-1]
                top_10_pct = max(1, len(sorted_amt) // 10)
                feats['amount_concentration'] = float(
                    sorted_amt[:top_10_pct].sum() / (sorted_amt.sum() + 1e-12)
                )
            else:
                feats['amount_q95_q50_ratio'] = 0.0
                feats['amount_q75_q25_ratio'] = 0.0
                feats['amount_concentration'] = 0.0
        else:
            feats['amount_q95_q50_ratio'] = 0.0
            feats['amount_q75_q25_ratio'] = 0.0
            feats['amount_concentration'] = 0.0

        # ── Degree Asymmetry (3) ──────────────────────────────────────────
        # In fraud networks, some nodes receive many transfers but send few
        n = G.number_of_nodes()
        if n >= 3:
            in_deg  = np.array([d for _, d in G.in_degree()], dtype=float)
            out_deg = np.array([d for _, d in G.out_degree()], dtype=float)
            # Asymmetry: difference between in and out degree
            asymmetry = in_deg - out_deg
            feats['degree_asymmetry_mean'] = float(np.mean(asymmetry))
            feats['degree_asymmetry_max']  = float(np.max(np.abs(asymmetry)))
            # Source-to-sink ratio: nodes with only outgoing vs only incoming
            pure_sources = float(np.sum((out_deg > 0) & (in_deg == 0)))
            pure_sinks   = float(np.sum((in_deg > 0) & (out_deg == 0)))
            feats['source_sink_ratio'] = float(
                pure_sources / (pure_sinks + 1e-12)
            )
        else:
            feats['degree_asymmetry_mean'] = 0.0
            feats['degree_asymmetry_max']  = 0.0
            feats['source_sink_ratio']     = 0.0

        # ── Graph Assortativity (2) ───────────────────────────────────────
        # Assortative = high-degree connects to high-degree (normal commerce)
        # Disassortative = high-degree connects to low-degree (hub-spoke fraud)
        if n >= 5 and G.number_of_edges() >= 3:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', RuntimeWarning)
                try:
                    val = nx.degree_assortativity_coefficient(G)
                    feats['degree_assortativity'] = 0.0 if np.isnan(val) else float(val)
                except Exception:
                    feats['degree_assortativity'] = 0.0
                try:
                    val = nx.degree_pearson_correlation_coefficient(G, weight='weight')
                    feats['weight_assortativity'] = 0.0 if np.isnan(val) else float(val)
                except Exception:
                    feats['weight_assortativity'] = 0.0
        else:
            feats['degree_assortativity'] = 0.0
            feats['weight_assortativity'] = 0.0

        return feats

    # ═══════════════════════════════════════════════════════════════════════
    # UTILITY METHODS
    # ═══════════════════════════════════════════════════════════════════════
    @staticmethod
    def _gini_coefficient(values: list) -> float:
        """Gini coefficient measures inequality. High Gini = skewed distribution."""
        arr = np.array(values, dtype=float)
        if arr.sum() == 0 or len(arr) < 2:
            return 0.0
        arr = np.sort(arr)
        n = len(arr)
        idx = np.arange(1, n + 1)
        return float((2 * np.sum(idx * arr)) / (n * np.sum(arr)) - (n + 1) / n)

    def _zero_baseline(self) -> Dict[str, float]:
        return {k: 0.0 for k in [
            'pagerank_max','pagerank_mean','pagerank_variance','pagerank_entropy',
            'cluster_coeff_avg','cluster_coeff_max','cluster_coeff_std',
            'edge_density','degree_max','degree_mean','degree_std',
            'largest_wcc_ratio','amount_std','amount_skew','reciprocity'
        ]}

    def _centrality_keys(self):
        return [
            'betweenness_max','betweenness_mean','betweenness_std','betweenness_gini',
            'eigenvec_centrality_max','eigenvec_centrality_mean','eigenvec_centrality_std',
            'hits_hub_max','hits_authority_max','hits_hub_auth_ratio',
            'katz_centrality_max','katz_centrality_mean'
        ]

    def _spectral_keys(self):
        return [
            'fiedler_value','spectral_gap','laplacian_lambda_max','spectral_radius',
            'spectral_spread','eigenvalue_mean','eigenvalue_std','eigenvalue_entropy',
            'fiedler_vec_std','fiedler_vec_range','fiedler_neg_fraction',
            'cheeger_approx','laplacian_energy'
        ]

    def _community_keys(self):
        return [
            'louvain_modularity','n_communities','community_size_mean',
            'community_size_std','community_size_max','community_size_min',
            'community_gini','intra_community_edge_ratio',
            'singleton_community_ratio','top_community_coverage'
        ]

    def _temporal_keys(self):
        return [
            'tx_velocity_max','tx_velocity_mean','tx_velocity_std','tx_velocity_cv',
            'amount_velocity_max','amount_velocity_mean',
            'balance_anomaly_mean','balance_anomaly_max','zero_balance_count',
            'time_to_reversal_min','time_to_reversal_mean',
        ]

    def _motif_keys(self):
        return [
            'triangle_count','triangle_density','transitivity',
            'four_cycle_approx','bow_tie_node_count','bow_tie_node_fraction',
            'sink_node_fraction'
        ]

    def _dataset_specific_keys(self):
        return [
            'type_ratio_transfer','type_ratio_cash_out','type_ratio_payment',
            'type_ratio_debit','type_ratio_cash_in',
            'amount_q95_q50_ratio','amount_q75_q25_ratio','amount_concentration',
            'degree_asymmetry_mean','degree_asymmetry_max','source_sink_ratio',
            'degree_assortativity','weight_assortativity'
        ]
