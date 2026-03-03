import os

# ---------------------------------------------------------
# Data Infrastructure (GitHub Repo Backend)
# ---------------------------------------------------------
REPO_DIR = '/content/multi-domain-project-finance-and-supply-chain-management-'
PROCESSED_DIR = os.path.join(REPO_DIR, 'backend/data/processed')

# ---------------------------------------------------------
# MLOps Infrastructure Directories (Google Drive Backend)
# ---------------------------------------------------------
BASE_DIR = '/content/drive/MyDrive/SOTA_Cluster_Shared'
CHECKPOINT_DIR = os.path.join(BASE_DIR, 'checkpoints')
LOGS_DIR = os.path.join(BASE_DIR, 'mlops_logs')
HARD_SAMPLES_DIR = os.path.join(BASE_DIR, 'hard_samples')
MATRICES_DIR = os.path.join(BASE_DIR, 'confusion_matrices')

def setup_infrastructure():
    """Validates and creates the Google Drive file structure if it doesn't exist."""
    for path in [CHECKPOINT_DIR, LOGS_DIR, HARD_SAMPLES_DIR, MATRICES_DIR]:
        os.makedirs(path, exist_ok=True)
    print(f"\n✅ MLOps Google Drive Infrastructure verified at: {BASE_DIR}")
