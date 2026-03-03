import torch
import pynvml
import psutil
from sklearn.metrics import confusion_matrix
from datetime import datetime
import json
import os
import wandb

from .config import LOGS_DIR, MATRICES_DIR

# Initialize NVML for hardware tracking on Google Colab GPUs
try:
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0) if torch.cuda.is_available() else None
except Exception:
    handle = None

def save_telemetry_to_drive(metric_dict, context=""):
    """Saves telemetry exactly as it goes to WandB into a local Google Drive fallback log."""
    log_path = os.path.join(LOGS_DIR, f"telemetry_log_{datetime.now().strftime('%Y%m%d')}.jsonl")
    metric_copy = metric_dict.copy()
    metric_copy['timestamp'] = datetime.now().isoformat()
    metric_copy['context'] = context
    
    with open(log_path, 'a') as f:
        f.write(json.dumps(metric_copy) + '\n')

def log_hardware_metrics():
    """Reads native GPU thermal and memory stats to prevent Colab throttle crashes."""
    metrics = {'cpu_percent': psutil.cpu_percent(), 'ram_gb': psutil.virtual_memory().used / 1e9}
    if handle is not None:
        try:
            info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            metrics['gpu_vram_gb'] = info.used / 1e9
            metrics['gpu_utilization_percent'] = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        except Exception:
            pass
            
    wandb.log(metrics)
    save_telemetry_to_drive(metrics, "hardware")
    return metrics

def track_gradient_health(model):
    """Calculates global gradient norm to detect Exploding/Vanishing gradients in federated nodes."""
    total_norm = 0.0
    for p in model.parameters():
        if p.grad is not None:
            param_norm = p.grad.data.norm(2)
            total_norm += param_norm.item() ** 2
    total_norm = total_norm ** 0.5
    wandb.log({"model_gradient_norm": total_norm})
    save_telemetry_to_drive({"model_gradient_norm": total_norm}, "gradient_health")
    return total_norm

def generate_text_confusion_matrix(y_true, y_pred, phase="Train"):
    """Generates a physical .txt file containing the confusion matrix on Google Drive for immediate auditing."""
    cm = confusion_matrix(y_true, y_pred)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(MATRICES_DIR, f"{phase}_Confusion_Matrix_{timestamp}.txt")
    
    with open(file_path, "w") as f:
        f.write(f"=== {phase} Phase Confusion Matrix ===\n")
        f.write(f"Timestamp: {timestamp}\n\n")
        
        # Explicitly output TP, TN, FP, FN if Binary Classification
        if cm.shape == (2, 2):
            tn, fp, fn, tp = cm.ravel()
            f.write("Detailed Metrics:\n")
            f.write(f"tp : {tp}\n")
            f.write(f"tn : {tn}\n")
            f.write(f"fp : {fp}\n")
            f.write(f"fn : {fn}\n\n")
            
        f.write("Raw Matrix Format: Rows=True Labels, Columns=Predicted Labels\n")
        f.write(str(cm))
        f.write("\n\n=== Interpretation ===\n")
        f.write("tp = True Positive, tn = True Negative, fp = False Positive, fn = False Negative.")
    
    print(f"💾 Saved {phase} Textual Confusion Matrix to: {file_path}")
