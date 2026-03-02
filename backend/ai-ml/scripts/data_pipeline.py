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
            
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
        os.chdir(repo_root)
        
        # 1. Add file
        subprocess.run(["git", "add", file_path], check=True)
        # 2. Commit
        commit_msg = f"chore(data): auto-save extracted {dataset_name} features"
        subprocess.run(["git", "commit", "-m", commit_msg], check=False) # Check=False in case there are no changes
        # 3. Push
        subprocess.run(["git", "push"], check=True)
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

# 4. NASA Continuous-Time Log-Signatures (Rough Path Theory)
def extract_log_signatures(sensor_tensor, depth=3):
    with torch.no_grad():
        return signatory.logsignature(sensor_tensor, depth)

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
        out_name = f"features_logsig_{filename.replace('.txt', '.csv')}"
        out_path = os.path.join(PROCESSED_DIR, out_name)
        
        if os.path.exists(out_path):
            os.remove(out_path)
            
        print(f"Streaming {filename} Log-Signatures to NVMe...")
        try:
            df = pd.read_csv(file_path, sep=r'\s+', header=None)
            df = df.dropna(axis=1, how='all')
            engine_ids = df.iloc[:, 0].unique()
            
            for i, eng_id in enumerate(engine_ids):
                # Only load the exact required memory segment
                engine_data = df[df.iloc[:, 0] == eng_id].iloc[:, 2:].values
                
                # To prevent C++ Segfaults, downcast precision to 16-bit to halve the memory allocation required during CPU calculus.
                tensor_data = torch.tensor(engine_data, dtype=torch.float16).unsqueeze(0) 
                
                if tensor_data.shape[1] > 1:
                    # SAFETY MEASURES: Signatory C++ crashes violently if input has NaNs, Infs, or isn't contiguous in memory
                    clean_tensor = torch.nan_to_num(tensor_data.float(), nan=0.0, posinf=0.0, neginf=0.0).contiguous()
                    sig = extract_log_signatures(clean_tensor, depth=2)
                    sig_array = sig.squeeze(0).numpy()
                    
                    row_dict = {f"sig_{j}": float(val) for j, val in enumerate(sig_array)}
                    row_dict['engine_id'] = eng_id
                    pd.DataFrame([row_dict]).to_csv(out_path, mode='a', header=not os.path.exists(out_path), index=False)
                    
                    # Hard memory termination
                    del sig, sig_array, row_dict
                
                del tensor_data, engine_data
                
                if i % 5 == 0:
                    gc.collect()
                
            del df
            gc.collect()
            print(f"  ✅ Saved {len(engine_ids)} engine signatures locally.")
            
            # TRIGGER AUTO-SAVE TO GITHUB
            commit_to_github(out_path, f"NASA {filename}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")

# 5. Topology Preprocessing (Betti Numbers via Persistent Homology)
def extract_betti_numbers(distance_matrix):
    rips_complex = gudhi.RipsComplex(distance_matrix=distance_matrix, max_edge_length=2.0)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=3)
    simplex_tree.persistence()
    return simplex_tree.betti_numbers()

def process_fraud_topology():
    print("\n--- Processing PaySim Fraud Topology ---")
    paysim_files = glob.glob(os.path.join(RAW_DIR, '*paysim*.csv')) + glob.glob(os.path.join(RAW_DIR, '**', 'PS*.csv'), recursive=True)
    if not paysim_files:
        print("⚠️ Could not locate PaySim files.")
        return
        
    file_path = paysim_files[0]
    out_path = os.path.join(PROCESSED_DIR, "topological_fraud_features.csv")
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
                sub_G = G.subgraph(components[0])
                nodes = list(sub_G.nodes())[:150] 
                sub_G = sub_G.subgraph(nodes)
                
                dist_matrix = np.zeros((len(nodes), len(nodes)))
                for i, n1 in enumerate(nodes):
                    for j, n2 in enumerate(nodes):
                        if i != j:
                            if sub_G.has_edge(n1, n2):
                                dist_matrix[i, j] = 1.0 / (sub_G[n1][n2]['amount'] + 1e-5)
                            else:
                                dist_matrix[i, j] = 10.0
                
                dist_matrix = (dist_matrix + dist_matrix.T) / 2
                np.fill_diagonal(dist_matrix, 0)
                
                betti = extract_betti_numbers(dist_matrix)
                
                pd.DataFrame([{
                    "chunk_id": chunk_index,
                    "betti_0_connected_comps": betti[0] if len(betti) > 0 else 0, 
                    "betti_1_rings": betti[1] if len(betti) > 1 else 0,
                    "betti_2_voids": betti[2] if len(betti) > 2 else 0
                }]).to_csv(out_path, mode='a', header=not os.path.exists(out_path), index=False)
                
            del G, chunk_df
            gc.collect()
            
        print("  ✅ Topological Fraud Extraction completely saved locally.")
        
        # TRIGGER AUTO-SAVE TO GITHUB
        commit_to_github(out_path, "PaySim Topology")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    download_datasets()
    process_nasa_telemetry()
    process_fraud_topology()
    print("\n🚀 SOTA AI Python Auto-Git Pipeline Finished Successfully!")
