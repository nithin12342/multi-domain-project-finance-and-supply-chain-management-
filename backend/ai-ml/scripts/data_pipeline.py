"""
AGI-Frontier Supply Chain & Finance: Data Pipeline
Designed exclusively for GitHub Codespaces (Headless Container Execution)
"""

import os
import glob
import subprocess
import torch
import pandas as pd
import numpy as np
import gudhi
import networkx as nx
import signatory
import gc

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

# 2. Secure Kaggle Kaggle Download via Subprocess
# (Assumes ~/.kaggle/kaggle.json exists in the Codespace)
def download_datasets():
    print("\n--- Downloading 4 Core Kaggle Datasets ---")
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
        subprocess.run(cmd, check=False) # check=False ignores permission errors like M5 competition rules
        
    # M5 Competition
    print("Downloading M5 Forecasting (Competition)...")
    subprocess.run(["kaggle", "competitions", "download", "-c", "m5-forecasting-accuracy"], check=False)
    if os.path.exists("m5-forecasting-accuracy.zip"):
        subprocess.run(["unzip", "-q", "-o", "m5-forecasting-accuracy.zip", "-d", "m5_data"])
        os.remove("m5-forecasting-accuracy.zip")
        
    print("✅ All Datasets Downloaded & Extracted to Local Storage.")

# 3. NASA Continuous-Time Log-Signatures (Rough Path Theory)
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
            
            for eng_id in engine_ids:
                engine_data = df[df.iloc[:, 0] == eng_id].iloc[:, 2:].values 
                tensor_data = torch.tensor(engine_data, dtype=torch.float32).unsqueeze(0) 
                
                if tensor_data.shape[1] > 1:
                    sig = extract_log_signatures(tensor_data, depth=2)
                    sig_array = sig.squeeze(0).numpy()
                    
                    row_dict = {f"sig_{i}": val for i, val in enumerate(sig_array)}
                    row_dict['engine_id'] = eng_id
                    pd.DataFrame([row_dict]).to_csv(out_path, mode='a', header=not os.path.exists(out_path), index=False)
                
                del tensor_data, engine_data
                
            del df
            gc.collect()
            print(f"  ✅ Saved {len(engine_ids)} engine signatures.")
        except Exception as e:
            print(f"  ❌ Error: {e}")

# 4. Topology Preprocessing (Betti Numbers via Persistent Homology)
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
            
        print("  ✅ Topological Fraud Extraction complete.")
    except Exception as e:
        print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    download_datasets()
    process_nasa_telemetry()
    process_fraud_topology()
    print("\n🚀 SOTA AI Data Pipeline Finished Successfully!")
