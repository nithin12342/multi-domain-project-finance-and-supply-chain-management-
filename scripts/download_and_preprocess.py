#!/usr/bin/env python3
"""
===============================================================
CODESPACES DATA PIPELINE: Download + Preprocess + Commit
===============================================================
Run this script in GitHub Codespaces to:
1. Download all 3 Kaggle datasets (IEEE-CIS, PaySim, DataCo)
2. Run the full 100-feature preprocessing orchestrator
3. Save processed CSVs to backend/data/processed/
4. Commit and push to GitHub

PREREQUISITES:
  pip install networkx scikit-learn scipy pandas numpy python-louvain tqdm
  pip install gudhi esig imbalanced-learn joblib pyarrow  # optional but recommended
  pip install kaggle
  
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

# ----- CONFIGURATION -----
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(REPO_ROOT, 'backend', 'data', 'raw')
PROCESSED_DIR = os.path.join(REPO_ROOT, 'backend', 'data', 'processed')

# Add training scripts to path for orchestrator imports
sys.path.insert(0, os.path.join(REPO_ROOT, 'backend', 'ai-ml', 'scripts', 'training'))

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
    print("\n" + "=" * 60)
    print("📥 DOWNLOADING KAGGLE DATASETS")
    print("=" * 60)

    # Check kaggle CLI
    try:
        subprocess.run(['kaggle', '--version'], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ Kaggle CLI not found. Install with: pip install kaggle")
        print("   Then set KAGGLE_USERNAME and KAGGLE_KEY environment variables")
        sys.exit(1)

    # Download IEEE-CIS (competition format)
    ieee_dir = os.path.join(RAW_DATA_DIR, 'ieee_fraud')
    if not os.path.exists(ieee_dir) or not os.listdir(ieee_dir):
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
    if not os.path.exists(paysim_dir) or not os.listdir(paysim_dir):
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
    if not os.path.exists(dataco_dir) or not os.listdir(dataco_dir):
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


def delete_old_data():
    """Delete old processed CSVs that had bad data."""
    old_file = os.path.join(PROCESSED_DIR, 'structural_fraud_features.csv')
    if os.path.exists(old_file):
        os.remove(old_file)
        print(f"🗑️ Deleted old {old_file}")


def run_advanced_pipeline():
    """Run the full 100-feature preprocessing orchestrator."""
    print("\n" + "=" * 60)
    print("🔬 RUNNING 100-FEATURE EXTRACTION PIPELINE")
    print("=" * 60)

    from feature_config import CFG
    # Override output dir to absolute path
    CFG.output_dir = PROCESSED_DIR

    from preprocessing_orchestrator import PreprocessingOrchestrator
    orchestrator = PreprocessingOrchestrator(raw_data_dir=RAW_DATA_DIR, config=CFG)
    orchestrator.run_full_pipeline()


def git_commit_and_push():
    """Add processed data to .gitignore for raw, commit processed, push."""
    print("\n" + "=" * 60)
    print("📤 COMMITTING TO GITHUB")
    print("=" * 60)

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
                    'feat(data): 100-feature graph extraction with real Kaggle labels'],
                   cwd=REPO_ROOT, check=True)
    subprocess.run(['git', 'push', 'origin', 'master'], cwd=REPO_ROOT, check=True)
    print("   ✅ Pushed to GitHub!")


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 MULTI-DOMAIN 100-FEATURE DATA PIPELINE")
    print("=" * 60)

    ensure_directories()
    download_datasets()
    delete_old_data()
    run_advanced_pipeline()
    git_commit_and_push()

    print("\n" + "=" * 60)
    print("🎉 PIPELINE COMPLETE!")
    print("=" * 60)
    print(f"Processed CSVs saved to: {PROCESSED_DIR}")
    print("Now go to Colab and run the Modular Training notebook!")
