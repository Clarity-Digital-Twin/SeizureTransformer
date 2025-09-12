#!/usr/bin/env python3
"""
Evaluate SeizureTransformer on TUSZ eval set.
Reproduces paper's AUROC of 0.876 on TUSZ evaluation data.
"""

import os
import sys
import json
import torch
import numpy as np
from pathlib import Path
from tqdm import tqdm
from sklearn.metrics import roc_auc_score
from datetime import datetime

# Add wu_2025 to path
sys.path.append(str(Path(__file__).parent.parent / "wu_2025/src"))

from wu_2025.utils import load_models, get_dataloader
from epilepsy2bids.eeg import Eeg


def load_tusz_eval_data(data_dir="/mnt/c/Users/JJ/Desktop/Clarity-Digital-Twin/SeizureTransformer/wu_2025/data/tusz/edf/eval"):
    """Load TUSZ eval EDF files and labels."""
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"TUSZ eval data not found at {data_path}")
    
    # Find all EDF files
    edf_files = list(data_path.glob("**/*.edf"))
    print(f"Found {len(edf_files)} EDF files in eval set")
    
    # Group by subject
    subjects = {}
    for edf_path in edf_files:
        # TUSZ naming: 00000258_s002_t000.edf
        parts = edf_path.stem.split("_")
        if len(parts) >= 2:
            subject_id = parts[0]
            if subject_id not in subjects:
                subjects[subject_id] = []
            subjects[subject_id].append(edf_path)
    
    print(f"Found {len(subjects)} unique subjects")
    return subjects


def process_edf_file(edf_path, model, device):
    """Process single EDF file through model."""
    try:
        # Load EDF using epilepsy2bids
        eeg = Eeg.loadEdf(str(edf_path))
        
        # Get data and sampling rate
        data = eeg.data  # Should be (channels, samples)
        fs = eeg.fs
        
        # Check channel count
        if data.shape[0] != 19:
            print(f"Warning: {edf_path.name} has {data.shape[0]} channels, expected 19")
            return None
        
        # Get dataloader (handles preprocessing)
        dataloader = get_dataloader(data, fs=fs, batch_size=1)
        
        # Run inference
        predictions = []
        with torch.no_grad():
            for batch in dataloader:
                batch = batch.to(device)
                output = model(batch)
                predictions.append(output.cpu().numpy())
        
        # Concatenate predictions
        if predictions:
            predictions = np.concatenate(predictions, axis=0)
            return predictions
        
    except Exception as e:
        print(f"Error processing {edf_path.name}: {e}")
    
    return None


def load_labels(edf_path):
    """Load seizure labels for an EDF file."""
    # Look for corresponding .tse file (TUSZ seizure annotations)
    tse_path = edf_path.with_suffix(".tse")
    
    if not tse_path.exists():
        # No seizures in this file
        return []
    
    seizures = []
    with open(tse_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split()
                if len(parts) >= 3:
                    start = float(parts[0])
                    end = float(parts[1])
                    seizures.append((start, end))
    
    return seizures


def compute_metrics(all_predictions, all_labels):
    """Compute AUROC and other metrics."""
    # Flatten predictions and labels
    y_true = []
    y_pred = []
    
    for pred, label in zip(all_predictions, all_labels):
        if pred is not None and label is not None:
            y_pred.extend(pred.flatten())
            y_true.extend(label.flatten())
    
    if not y_true or not y_pred:
        print("No valid predictions to evaluate")
        return {}
    
    # Calculate AUROC
    auroc = roc_auc_score(y_true, y_pred)
    
    # Calculate accuracy at threshold 0.8 (paper's threshold)
    threshold = 0.8
    y_pred_binary = (np.array(y_pred) > threshold).astype(int)
    accuracy = np.mean(np.array(y_true) == y_pred_binary)
    
    # Count seizures and false alarms
    tp = np.sum((np.array(y_true) == 1) & (y_pred_binary == 1))
    fp = np.sum((np.array(y_true) == 0) & (y_pred_binary == 1))
    fn = np.sum((np.array(y_true) == 1) & (y_pred_binary == 0))
    tn = np.sum((np.array(y_true) == 0) & (y_pred_binary == 0))
    
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    
    return {
        "auroc": auroc,
        "accuracy": accuracy,
        "sensitivity": sensitivity,
        "specificity": specificity,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
    }


def main():
    """Run evaluation on TUSZ eval set."""
    print("=" * 60)
    print("SeizureTransformer TUSZ Evaluation")
    print("=" * 60)
    
    # Setup
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Load model
    print("\nLoading model...")
    model = load_models(device)
    model.eval()
    print("Model loaded successfully")
    
    # Load TUSZ eval data
    print("\nLoading TUSZ eval data...")
    try:
        subjects = load_tusz_eval_data()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease ensure TUSZ eval data is at:")
        print("/mnt/c/Users/JJ/Desktop/Clarity-Digital-Twin/SeizureTransformer/wu_2025/data/tusz/edf/eval")
        return
    
    # Process each file
    all_predictions = []
    all_labels = []
    
    print(f"\nProcessing {sum(len(files) for files in subjects.values())} files...")
    
    for subject_id, edf_files in tqdm(subjects.items(), desc="Subjects"):
        for edf_path in edf_files:
            # Get predictions
            predictions = process_edf_file(edf_path, model, device)
            
            if predictions is not None:
                # Get labels
                seizures = load_labels(edf_path)
                
                # Create binary label array
                # Assuming 256Hz and predictions are per-second
                duration_seconds = predictions.shape[-1]
                labels = np.zeros(duration_seconds)
                
                for start, end in seizures:
                    start_idx = int(start)
                    end_idx = int(end)
                    if start_idx < duration_seconds:
                        labels[start_idx:min(end_idx, duration_seconds)] = 1
                
                all_predictions.append(predictions)
                all_labels.append(labels)
    
    # Compute metrics
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    
    metrics = compute_metrics(all_predictions, all_labels)
    
    if metrics:
        print(f"\nAUROC: {metrics['auroc']:.4f}")
        print(f"(Paper reports: 0.876)")
        print(f"\nAccuracy @ 0.8 threshold: {metrics['accuracy']:.4f}")
        print(f"Sensitivity: {metrics['sensitivity']:.4f}")
        print(f"Specificity: {metrics['specificity']:.4f}")
        
        print(f"\nConfusion Matrix:")
        print(f"  TP: {metrics['tp']:,}")
        print(f"  FP: {metrics['fp']:,}")
        print(f"  FN: {metrics['fn']:,}")
        print(f"  TN: {metrics['tn']:,}")
        
        # Save results
        results_path = Path("evaluation/results")
        results_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_path / f"tusz_eval_{timestamp}.json"
        
        with open(results_file, "w") as f:
            json.dump(metrics, f, indent=2)
        
        print(f"\nResults saved to: {results_file}")


if __name__ == "__main__":
    main()