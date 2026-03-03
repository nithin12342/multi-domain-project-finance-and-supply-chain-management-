import os
import pandas as pd
import torch
import wandb
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

from .config import HARD_SAMPLES_DIR, CHECKPOINT_DIR
from .mlops_telemetry import log_hardware_metrics, track_gradient_health, save_telemetry_to_drive, generate_text_confusion_matrix

def master_federated_epoch(model, dataloader, optimizer, criterion, epoch, phase="Train"):
    """
    Blueprint for advanced federated training logic with Hard Sample Mining and Telemetry integration.
    """
    model.train() if phase == "Train" else model.eval()
    
    all_preds, all_labels = [], []
    running_loss = 0.0
    successful_samples, failed_samples = [], []
    
    # Process micro-epochs securely to avoid Colab RAM Timeouts
    for batch_idx, batch_data in enumerate(dataloader):
        
        # Depending on dataloader complexity, unpack inputs, labels and metadata
        if len(batch_data) == 3:
            inputs, labels, raw_data_metadata = batch_data
        else:
            inputs, labels = batch_data
            raw_data_metadata = [f"batch_{batch_idx}_idx_{i}" for i in range(len(labels))]

        if torch.cuda.is_available():
            inputs, labels = inputs.cuda(), labels.cuda()
            
        if phase == "Train":
            optimizer.zero_grad()
            
        with torch.set_grad_enabled(phase == "Train"):
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            if phase == "Train":
                loss.backward()
                _ = track_gradient_health(model) # Health Tracker
                optimizer.step()
                
            # Extract highest probability predictions (Assumes Output is Logits for Classification)
            if len(outputs.shape) > 1 and outputs.shape[1] > 1:
                _, preds = torch.max(outputs, 1)
            else:
                # Binary Classification Sigmoid output handling
                preds = (torch.sigmoid(outputs) > 0.5).long().squeeze()
                
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            running_loss += loss.item()
            
            # ========== HARD SAMPLE MINING ==========
            # Isolate the exact rows that the AI predicted wrong
            for i in range(len(preds)):
                sample_record = {
                    "Epoch": epoch, 
                    "Batch": batch_idx, 
                    "Raw_Metadata": str(raw_data_metadata[i]), 
                    "Predicted": int(preds[i].item()), 
                    "Actual": int(labels[i].item()), 
                    "Loss": float(loss.item())
                }
                if preds[i] == labels[i]:
                    successful_samples.append(sample_record)
                else:
                    failed_samples.append(sample_record)
                    
        # Check hardware health every 10 batches to prevent 15GB GPU limits
        if batch_idx % 10 == 0:
            log_hardware_metrics()
            
    # ========== Metrics & Drive Logging ==========
    epoch_loss = running_loss / len(dataloader)
    precision, recall, f1, _ = precision_recall_fscore_support(all_labels, all_preds, average='weighted', zero_division=0)
    accuracy = accuracy_score(all_labels, all_preds)
    
    # Log to WandB Dashboard and Google Drive fallback log
    metrics = {f"{phase}_Loss": epoch_loss, f"{phase}_Acc": accuracy, f"{phase}_F1": f1}
    wandb.log(metrics)
    save_telemetry_to_drive(metrics, f"epoch_{phase}")
    
    # Log Hard Samples physically to Google Drive
    if failed_samples:
        fail_df = pd.DataFrame(failed_samples)
        fail_path = os.path.join(HARD_SAMPLES_DIR, f"failed_samples_{phase}_epoch_{epoch}.csv")
        fail_df.to_csv(fail_path, index=False)
        print(f"⚠️ Logged {len(failed_samples)} Failed Samples to {fail_path}")
        
    # Log Textual Confusion Matrix to Drive
    generate_text_confusion_matrix(all_labels, all_preds, phase=phase)
    
    # Save Master Checkpoint
    if phase == "Train":
        model_name = model.__class__.__name__
        save_path = os.path.join(CHECKPOINT_DIR, f"{model_name}_SOTA_weights.pt")
        torch.save(model.state_dict(), save_path)
        print(f"💾 Saved {model_name} Global Weights to: {save_path}")
        
    return epoch_loss, f1
