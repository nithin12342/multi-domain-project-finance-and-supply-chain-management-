#!/usr/bin/env python3
"""
===============================================================
CODESPACES DATA PIPELINE: Download + Preprocess + Commit
===============================================================
Run this script in GitHub Codespaces to:
1. Download all 3 Kaggle datasets (IEEE-CIS, PaySim, DataCo)
2. Build transaction graphs and extract features
3. Save processed CSVs to backend/data/processed/
4. Commit and push to GitHub

PREREQUISITES:
  pip install kaggle networkx pandas numpy scikit-learn scipy
  
  Then set up Kaggle credentials:
    export KAGGLE_USERNAME="your_username"
    export KAGGLE_KEY="your_api_key"
  
  Or place kaggle.json at ~/.kaggle/kaggle.json

USAGE:
  python scripts/download_and_preprocess.py
===============================================================
"""

import os
import sys
import subprocess
import warnings
warnings.filterwarnings('ignore')

# ----- CONFIGURATION -----
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(REPO_ROOT, 'backend', 'data', 'raw')
PROCESSED_DIR = os.path.join(REPO_ROOT, 'backend', 'data', 'processed')
CHUNK_SIZE = 200  # transactions per graph chunk

# Kaggle dataset identifiers
DATASETS = {
    'ieee_fraud': 'ieee-fraud-detection',           # Competition dataset
    'paysim': 'ealaxi/paysim1',                     # PaySim dataset
    'dataco': 'shashwatwork/dataco-smart-supply-chain-for-big-data-analysis'
}

def ensure_directories():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    print(f"✅ Directories ready: {RAW_DATA_DIR}")

def download_datasets():
    """Download all 3 Kaggle datasets."""
    print("\n" + "="*60)
    print("📥 DOWNLOADING KAGGLE DATASETS")
    print("="*60)
    
    # Check kaggle CLI
    try:
        subprocess.run(['kaggle', '--version'], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ Kaggle CLI not found. Install with: pip install kaggle")
        print("   Then set KAGGLE_USERNAME and KAGGLE_KEY environment variables")
        sys.exit(1)
    
    # Download IEEE-CIS (competition format)
    ieee_dir = os.path.join(RAW_DATA_DIR, 'ieee_fraud')
    if not os.path.exists(ieee_dir):
        print("\n📦 Downloading IEEE-CIS Fraud Detection...")
        os.makedirs(ieee_dir, exist_ok=True)
        subprocess.run([
            'kaggle', 'competitions', 'download', '-c', DATASETS['ieee_fraud'],
            '-p', ieee_dir
        ], check=False)
        # Unzip
        for f in os.listdir(ieee_dir):
            if f.endswith('.zip'):
                subprocess.run(['unzip', '-o', os.path.join(ieee_dir, f), '-d', ieee_dir], 
                              capture_output=True, check=False)
        print("   ✅ IEEE-CIS downloaded")
    else:
        print(f"   ⏭️ IEEE-CIS already exists at {ieee_dir}")
    
    # Download PaySim
    paysim_dir = os.path.join(RAW_DATA_DIR, 'paysim')
    if not os.path.exists(paysim_dir):
        print("\n📦 Downloading PaySim...")
        os.makedirs(paysim_dir, exist_ok=True)
        subprocess.run([
            'kaggle', 'datasets', 'download', '-d', DATASETS['paysim'],
            '-p', paysim_dir
        ], check=False)
        for f in os.listdir(paysim_dir):
            if f.endswith('.zip'):
                subprocess.run(['unzip', '-o', os.path.join(paysim_dir, f), '-d', paysim_dir],
                              capture_output=True, check=False)
        print("   ✅ PaySim downloaded")
    else:
        print(f"   ⏭️ PaySim already exists at {paysim_dir}")
    
    # Download DataCo
    dataco_dir = os.path.join(RAW_DATA_DIR, 'dataco')
    if not os.path.exists(dataco_dir):
        print("\n📦 Downloading DataCo Supply Chain...")
        os.makedirs(dataco_dir, exist_ok=True)
        subprocess.run([
            'kaggle', 'datasets', 'download', '-d', DATASETS['dataco'],
            '-p', dataco_dir
        ], check=False)
        for f in os.listdir(dataco_dir):
            if f.endswith('.zip'):
                subprocess.run(['unzip', '-o', os.path.join(dataco_dir, f), '-d', dataco_dir],
                              capture_output=True, check=False)
        print("   ✅ DataCo downloaded")
    else:
        print(f"   ⏭️ DataCo already exists at {dataco_dir}")

def process_paysim():
    """Process PaySim into graph features with REAL fraud labels."""
    import pandas as pd
    import numpy as np
    import networkx as nx
    from scipy.stats import entropy as scipy_entropy
    
    print("\n" + "="*60)
    print("🔬 PROCESSING PAYSIM → Graph Features")
    print("="*60)
    
    # Find the CSV
    paysim_dir = os.path.join(RAW_DATA_DIR, 'paysim')
    csv_files = [f for f in os.listdir(paysim_dir) if f.endswith('.csv')]
    if not csv_files:
        print("❌ No CSV found in paysim directory. Skipping.")
        return
    
    csv_path = os.path.join(paysim_dir, csv_files[0])
    print(f"   Reading {csv_path}...")
    
    # Read in chunks to handle ~6M rows without OOM
    df = pd.read_csv(csv_path, nrows=500000)  # Use first 500K for Codespaces RAM limits
    print(f"   Loaded {len(df):,} transactions")
    print(f"   Fraud rate: {df['isFraud'].mean():.4%}")
    
    # Only use TRANSFER and CASH_OUT (fraud-relevant transaction types)
    fraud_types = df[df['type'].isin(['TRANSFER', 'CASH_OUT'])].copy()
    print(f"   Filtered to {len(fraud_types):,} TRANSFER/CASH_OUT transactions")
    
    # Create chunk IDs
    num_chunks = len(fraud_types) // CHUNK_SIZE
    fraud_types = fraud_types.iloc[:num_chunks * CHUNK_SIZE].copy()
    fraud_types['chunk_id'] = np.repeat(np.arange(1, num_chunks + 1), CHUNK_SIZE)
    
    # Extract graph features per chunk
    chunk_features = []
    for chunk_id, chunk_df in fraud_types.groupby('chunk_id'):
        features = _extract_graph_features(chunk_df, sender_col='nameOrig', receiver_col='nameDest', amount_col='amount')
        if features is None:
            continue
        features['chunk_id'] = chunk_id
        features['isFraud'] = int(chunk_df['isFraud'].max())  # REAL label
        chunk_features.append(features)
        
        if chunk_id % 200 == 0:
            print(f"   Processed {chunk_id}/{num_chunks} chunks...")
    
    result_df = pd.DataFrame(chunk_features)
    output_path = os.path.join(PROCESSED_DIR, 'structural_fraud_features.csv')
    result_df.to_csv(output_path, index=False)
    print(f"\n   💾 Saved {len(result_df)} chunks × {len(result_df.columns)} features to {output_path}")
    print(f"   Fraud chunks: {result_df['isFraud'].sum()} ({result_df['isFraud'].mean():.1%})")
    return result_df

def process_ieee_fraud():
    """Process IEEE-CIS Fraud Detection into graph features."""
    import pandas as pd
    import numpy as np
    
    print("\n" + "="*60)
    print("🔬 PROCESSING IEEE-CIS → Graph Features")
    print("="*60)
    
    ieee_dir = os.path.join(RAW_DATA_DIR, 'ieee_fraud')
    txn_file = os.path.join(ieee_dir, 'train_transaction.csv')
    
    if not os.path.exists(txn_file):
        print(f"   ❌ {txn_file} not found. Skipping IEEE-CIS.")
        return None
    
    # Load subset (IEEE-CIS is very wide with 400+ columns)
    cols_needed = ['TransactionID', 'isFraud', 'TransactionAmt', 'card1', 'card2', 'addr1', 'addr2', 'ProductCD']
    df = pd.read_csv(txn_file, usecols=cols_needed, nrows=200000)
    print(f"   Loaded {len(df):,} transactions")
    print(f"   Fraud rate: {df['isFraud'].mean():.4%}")
    
    # Use card1 as sender proxy, card2 as receiver proxy
    df = df.dropna(subset=['card1', 'card2']).copy()
    df['card1'] = df['card1'].astype(int)
    df['card2'] = df['card2'].astype(int)
    
    num_chunks = len(df) // CHUNK_SIZE
    df = df.iloc[:num_chunks * CHUNK_SIZE].copy()
    df['chunk_id'] = np.repeat(np.arange(1, num_chunks + 1), CHUNK_SIZE)
    
    chunk_features = []
    for chunk_id, chunk_df in df.groupby('chunk_id'):
        features = _extract_graph_features(chunk_df, sender_col='card1', receiver_col='card2', amount_col='TransactionAmt')
        if features is None:
            continue
        features['chunk_id'] = chunk_id
        features['isFraud'] = int(chunk_df['isFraud'].max())
        chunk_features.append(features)
        
        if chunk_id % 200 == 0:
            print(f"   Processed {chunk_id}/{num_chunks} chunks...")
    
    result_df = pd.DataFrame(chunk_features)
    output_path = os.path.join(PROCESSED_DIR, 'ieee_fraud_features.csv')
    result_df.to_csv(output_path, index=False)
    print(f"\n   💾 Saved {len(result_df)} chunks to {output_path}")
    print(f"   Fraud chunks: {result_df['isFraud'].sum()} ({result_df['isFraud'].mean():.1%})")
    return result_df

def _extract_graph_features(chunk_df, sender_col, receiver_col, amount_col):
    """Build a directed weighted graph and extract 15 topological features."""
    import networkx as nx
    import numpy as np
    import pandas as pd
    from scipy.stats import entropy as scipy_entropy
    
    G = nx.DiGraph()
    
    for _, row in chunk_df.iterrows():
        s, r = str(row[sender_col]), str(row[receiver_col])
        amt = float(row[amount_col]) if pd.notna(row[amount_col]) else 0.0
        if s == r:
            continue
        if G.has_edge(s, r):
            G[s][r]['weight'] += amt
            G[s][r]['count'] += 1
        else:
            G.add_edge(s, r, weight=amt, count=1)
    
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    
    if num_nodes < 2:
        return None
    
    # PageRank
    try:
        pr = nx.pagerank(G, weight='weight', max_iter=100)
        pr_values = list(pr.values())
    except:
        pr_values = [1.0 / max(num_nodes, 1)] * max(num_nodes, 1)
    
    pagerank_max = max(pr_values)
    pagerank_mean = np.mean(pr_values)
    pagerank_variance = np.var(pr_values)
    pagerank_entropy = scipy_entropy(pr_values) if len(pr_values) > 1 else 0.0
    
    # Clustering
    G_und = G.to_undirected()
    cc = list(nx.clustering(G_und).values())
    
    # Degree
    in_deg = [d for _, d in G.in_degree()]
    out_deg = [d for _, d in G.out_degree()]
    all_deg = in_deg + out_deg
    
    # Components
    num_wcc = nx.number_weakly_connected_components(G)
    largest_wcc = max(nx.weakly_connected_components(G), key=len)
    
    # Amounts
    weights = [d['weight'] for _, _, d in G.edges(data=True)]
    
    # Reciprocity
    recip = nx.reciprocity(G) if num_edges > 0 else 0.0
    
    return {
        'pagerank_max': pagerank_max,
        'pagerank_mean': pagerank_mean,
        'pagerank_variance': pagerank_variance,
        'pagerank_entropy': pagerank_entropy,
        'cluster_coeff_avg': np.mean(cc) if cc else 0.0,
        'cluster_coeff_max': max(cc) if cc else 0.0,
        'cluster_coeff_std': np.std(cc) if cc else 0.0,
        'edge_density': nx.density(G),
        'degree_max': max(all_deg) if all_deg else 0,
        'degree_mean': np.mean(all_deg) if all_deg else 0.0,
        'degree_std': np.std(all_deg) if all_deg else 0.0,
        'largest_wcc_ratio': len(largest_wcc) / num_nodes,
        'amount_std': np.std(weights) if weights else 0.0,
        'amount_skew': float(pd.Series(weights).skew()) if len(weights) > 2 else 0.0,
        'reciprocity': recip
    }

def delete_old_data():
    """Delete old processed CSVs that had bad data."""
    import glob
    old_file = os.path.join(PROCESSED_DIR, 'structural_fraud_features.csv')
    if os.path.exists(old_file):
        os.remove(old_file)
        print(f"🗑️ Deleted old {old_file}")

def git_commit_and_push():
    """Add processed data to .gitignore for raw, commit processed, push."""
    print("\n" + "="*60)
    print("📤 COMMITTING TO GITHUB")
    print("="*60)
    
    # Add raw data to gitignore (too large for Git)
    gitignore_path = os.path.join(REPO_ROOT, '.gitignore')
    with open(gitignore_path, 'r') as f:
        content = f.read()
    
    if 'backend/data/raw/' not in content:
        with open(gitignore_path, 'a') as f:
            f.write('\n# Raw Kaggle datasets (too large for Git)\nbackend/data/raw/\n')
        print("   Added raw data to .gitignore")
    
    subprocess.run(['git', 'add', '-A'], cwd=REPO_ROOT, check=True)
    subprocess.run(['git', 'commit', '-m', 
                    'feat(data): real Kaggle data preprocessing with graph features'], 
                   cwd=REPO_ROOT, check=True)
    subprocess.run(['git', 'push', 'origin', 'master'], cwd=REPO_ROOT, check=True)
    print("   ✅ Pushed to GitHub!")

if __name__ == '__main__':
    print("="*60)
    print("🚀 MULTI-DOMAIN DATA PIPELINE")
    print("="*60)
    
    ensure_directories()
    download_datasets()
    delete_old_data()
    
    # Process whichever datasets downloaded successfully
    paysim_result = process_paysim()
    ieee_result = process_ieee_fraud()
    
    if paysim_result is None and ieee_result is None:
        print("\n❌ No datasets were processed. Check Kaggle credentials.")
        sys.exit(1)
    
    git_commit_and_push()
    
    print("\n" + "="*60)
    print("🎉 PIPELINE COMPLETE!")
    print("="*60)
    print(f"Processed CSVs saved to: {PROCESSED_DIR}")
    print("Now go to Colab and run the Modular Training notebook!")
