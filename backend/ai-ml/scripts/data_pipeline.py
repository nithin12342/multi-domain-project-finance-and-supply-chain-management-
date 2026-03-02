"""
AGI-Frontier Supply Chain & Finance: Auto-GitHub Data Pipeline
Designed exclusively for GitHub Codespaces (Headless Container Execution)
"""

import os
import json
import glob
import subprocess
import torch
import pandas as pd
import numpy as np
import gudhi
import networkx as nx
import signatory
import gc
from pathlib import Path

# 1. Establish Local Codespace Directory Structure
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))
RAW_DIR = os.path.join(BASE_DIR, 'raw')
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')
SHARDS_DIR = os.path.join(BASE_DIR, 'shards')

for path in [RAW_DIR, PROCESSED_DIR, SHARDS_DIR]:
    os.makedirs(path, exist_ok=True)
    
for sub in ['m5', 'paysim', 'dataco', 'nasa_cmapss']:
    os.makedirs(os.path.join(SHARDS_DIR, sub), exist_ok=True)

print(f"✅ Local Codespace Data Infrastructure Initialized at: {BASE_DIR}")

# 2. Secure Auto-Git Commit System
def commit_to_github(file_path, dataset_name):
    """Adds, commits, and pushes a single processed file gracefully to GitHub."""
    print(f"\n🔄 Auto-Saving {dataset_name} features to GitHub Version Control...")
    try:
        # Check if the file is too large for GitHub free tier (100MB limit)
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > 95:
            print(f"⚠️ Skipping Git Auto-Commit: {file_path} is {file_size_mb:.2f}MB (Approaching 100MB Git limit).")
            return
            
        # The script is in backend/ai-ml/scripts, we need to go up 3 levels to reach the repository root
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
        
        # 1. Add file
        subprocess.run(["git", "add", file_path], cwd=repo_root, check=True)
        # 2. Commit
        commit_msg = f"chore(data): auto-save extracted {dataset_name} features"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_root, check=False) # Check=False in case there are no changes
        # 3. Push
        subprocess.run(["git", "push"], cwd=repo_root, check=True)
        print(f"✅ Successfully Pushed {dataset_name} to GitHub!")
    except Exception as e:
        print(f"❌ Git Auto-Save Failed for {dataset_name}. Error: {e}")


# 3. Secure Kaggle Kaggle Configuration
def configure_kaggle():
    print("\n--- Configuring Kaggle API Authenticator ---")
    kaggle_dir = os.path.expanduser("~/.kaggle")
    os.makedirs(kaggle_dir, exist_ok=True)
    
    kaggle_json_path = os.path.join(kaggle_dir, "kaggle.json")
    
    creds = {
        "username": "nithin1234ag",
        "key": "a4ca19a1a7b1c1fdcff8ed69943901f6"
    }
    
    with open(kaggle_json_path, 'w') as f:
        json.dump(creds, f)
        
    os.chmod(kaggle_json_path, 0o600)
    print("✅ Kaggle Auto-Authenticator Built (~/.kaggle/kaggle.json)")

def download_datasets():
    print("\n--- Downloading 4 Core Kaggle Datasets ---")
    configure_kaggle()
    
    datasets = [
        ("shashwatwork/dataco-smart-supply-chain-for-big-data-analysis", True),
        ("ealaxi/paysim1", True),
        ("behrad3d/nasa-cmaps", True)
    ]
    
    os.chdir(RAW_DIR)
    
    for ds, unzip in datasets:
        cmd = ["kaggle", "datasets", "download", "-d", ds]
        if unzip:
            cmd.append("--unzip")
        print(f"Downloading {ds}...")
        subprocess.run(cmd, check=False) 
        
    print("Downloading M5 Forecasting (Competition)...")
    subprocess.run(["kaggle", "competitions", "download", "-c", "m5-forecasting-accuracy"], check=False)
    if os.path.exists("m5-forecasting-accuracy.zip"):
        subprocess.run(["unzip", "-q", "-o", "m5-forecasting-accuracy.zip", "-d", "m5_data"])
        os.remove("m5-forecasting-accuracy.zip")
        
    print("✅ All Datasets Downloaded & Extracted to Local Storage.")

import scipy.fft
from scipy.stats import linregress

# 4. NASA Spectral and Temporal Degradation Features
def extract_spectral_features(engine_data):
    """Extracts FFT power spectra and EMA slopes for each sensor channel."""
    # engine_data is numpy array [cycles, sensors]
    num_cycles, num_sensors = engine_data.shape
    features = {}
    
    for s in range(num_sensors):
        sensor_series = engine_data[:, s]
        
        # --- 1. Fast Fourier Transform (FFT) Power Spectra ---
        # Extract top 3 dominant frequency amplitudes to capture vibration shifts
        fft_vals = np.abs(scipy.fft.fft(sensor_series))
        # Ignore the DC component (index 0) and take the first half (symmetry)
        half_n = num_cycles // 2
        if half_n > 1:
            fft_amplitudes = fft_vals[1:half_n]
            top_indices = np.argsort(fft_amplitudes)[-3:][::-1] # Top 3
            for i, idx in enumerate(top_indices):
                features[f'sensor_{s}_fft_amp_{i+1}'] = fft_amplitudes[idx]
        else:
            for i in range(3):
                features[f'sensor_{s}_fft_amp_{i+1}'] = 0.0
                
        # --- 2. Exponential Moving Average (EMA) Slopes ---
        # Calculate slope of the 10-cycle and 30-cycle EMA to capture degradation acceleration
        series_obj = pd.Series(sensor_series)
        ema_10 = series_obj.ewm(span=10, adjust=False).mean().values
        ema_30 = series_obj.ewm(span=30, adjust=False).mean().values
        
        if num_cycles > 1:
            x = np.arange(num_cycles)
            slope_10, _, _, _, _ = linregress(x, ema_10)
            slope_30, _, _, _, _ = linregress(x, ema_30)
            features[f'sensor_{s}_ema10_slope'] = slope_10
            features[f'sensor_{s}_ema30_slope'] = slope_30
        else:
            features[f'sensor_{s}_ema10_slope'] = 0.0
            features[f'sensor_{s}_ema30_slope'] = 0.0

    return features

def process_nasa_telemetry():
    print("\n--- Processing NASA IoT Telemetry Logs ---")
    nasa_files = glob.glob(os.path.join(RAW_DIR, '**', 'train_FD*.txt'), recursive=True)
    if not nasa_files:
        nasa_files = glob.glob(os.path.join(RAW_DIR, 'train_FD*.txt'))
        
    if not nasa_files:
        print("⚠️ Could not locate NASA CMAPSS files.")
        return

    for file_path in nasa_files:
        filename = os.path.basename(file_path)
        out_name = f"features_spectral_{filename.replace('.txt', '.csv')}"
        out_path = os.path.join(PROCESSED_DIR, out_name)
        
        if os.path.exists(out_path):
            os.remove(out_path)
            
        print(f"Extracting {filename} FFT Spectra & EMA to NVMe...")
        try:
            df = pd.read_csv(file_path, sep=r'\s+', header=None)
            df = df.dropna(axis=1, how='all')
            engine_ids = df.iloc[:, 0].unique()
            
            for eng_id in engine_ids:
                # Raw sensor data (excluding engine and cycle ID)
                engine_data = df[df.iloc[:, 0] == eng_id].iloc[:, 2:].values
                
                # Extract Memory-Safe Native Python Features
                row_dict = extract_spectral_features(engine_data)
                row_dict['engine_id'] = eng_id
                
                pd.DataFrame([row_dict]).to_csv(out_path, mode='a', header=not os.path.exists(out_path), index=False)
                
            print(f"  ✅ Saved {len(engine_ids)} engine spectra locally.")
            
            # TRIGGER AUTO-SAVE TO GITHUB
            commit_to_github(out_path, f"NASA Spectra {filename}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")

# 5. Topology Preprocessing (Ego-Network Centrality & Community Density)
def extract_graph_centrality(sub_G):
    """Extracts mathematically stable graph features (PageRank, Clustering) from a fraud transaction subgraph."""
    features = {}
    
    # Structure 1: PageRank Centrality (identifies central mule nodes)
    pr = nx.pagerank(sub_G, alpha=0.85, weight='amount')
    pr_values = list(pr.values())
    features['pagerank_max'] = np.max(pr_values) if pr_values else 0.0
    features['pagerank_variance'] = np.var(pr_values) if pr_values else 0.0
    
    # Structure 2: Clustering Coefficient (identifies dense triadic laundering loops)
    clustering = nx.clustering(sub_G, weight='amount')
    clus_values = list(clustering.values())
    features['cluster_coeff_avg'] = np.mean(clus_values) if clus_values else 0.0
    features['cluster_coeff_max'] = np.max(clus_values) if clus_values else 0.0
    
    # Structure 3: Component Density (identifies high volume passing through few nodes)
    num_nodes = sub_G.number_of_nodes()
    num_edges = sub_G.number_of_edges()
    features['edge_density'] = num_edges / (num_nodes ** 2 + 1e-5)
    
    return features


def process_fraud_topology():
    print("\n--- Processing PaySim Fraud Topology ---")
    paysim_files = glob.glob(os.path.join(RAW_DIR, '*paysim*.csv')) + glob.glob(os.path.join(RAW_DIR, '**', 'PS*.csv'), recursive=True)
    if not paysim_files:
        print("⚠️ Could not locate PaySim files.")
        return
        
    file_path = paysim_files[0]
    out_path = os.path.join(PROCESSED_DIR, "structural_fraud_features.csv")
    if os.path.exists(out_path):
        os.remove(out_path)
        
    print(f"Streaming {os.path.basename(file_path)} in 50k row chunks...")
    try:
        chunk_index = 0
        for chunk_df in pd.read_csv(file_path, chunksize=50000):
            chunk_index += 1
            print(f"  Processing Chunk {chunk_index}...")
            
            G = nx.from_pandas_edgelist(chunk_df, 'nameOrig', 'nameDest', ['amount'], create_using=nx.Graph())
            components = sorted(nx.connected_components(G), key=len, reverse=True)
            
            if components:
                # Extract the 150 most connected nodes to simulate the core fraud ring potential
                sub_G = G.subgraph(components[0])
                nodes = list(sub_G.nodes())[:150] 
                sub_G = sub_G.subgraph(nodes)
                
                # Extract Memory-Safe Native Python Features
                row_dict = extract_graph_centrality(sub_G)
                row_dict['chunk_id'] = chunk_index
                
                pd.DataFrame([row_dict]).to_csv(out_path, mode='a', header=not os.path.exists(out_path), index=False)
                
            del G, chunk_df
            
        print("  ✅ Structural Fraud Graph Features completely saved locally.")
        
        # TRIGGER AUTO-SAVE TO GITHUB
        commit_to_github(out_path, "PaySim Topology")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    download_datasets()
    process_nasa_telemetry()
    process_fraud_topology()
    print("\n🚀 SOTA AI Python Auto-Git Pipeline Finished Successfully!")
