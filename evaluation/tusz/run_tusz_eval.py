#!/usr/bin/env python3
"""
Bulletproof TUSZ evaluation for SeizureTransformer.
Saves checkpoints and handles errors gracefully.
"""

import json
import pickle
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import roc_auc_score
from tqdm import tqdm

# Add wu_2025 to path
sys.path.append(str(Path(__file__).parent.parent.parent / "wu_2025/src"))

from epilepsy2bids.eeg import Eeg

from wu_2025.utils import get_dataloader, load_models


def process_single_file(edf_path, model, device):
    """Process one EDF file and return (predictions, seq_len) or (None, error)."""
    try:
        # Load EDF - use simple loadEdf like original
        eeg = Eeg.loadEdf(str(edf_path))
        data = eeg.data
        fs = eeg.fs
        seq_len = data.shape[1]

        # Skip if wrong channel count
        if data.shape[0] != 19:
            return None, f"Wrong channels: {data.shape[0]}"

        # Get predictions
        dataloader = get_dataloader(data, fs=fs, batch_size=1)
        predictions = []

        with torch.no_grad():
            for batch in dataloader:
                batch = batch.to(device)
                # Model already outputs probabilities (sigmoid inside architecture)
                output = model(batch)
                predictions.append(output.detach().cpu().numpy())

        if predictions:
            # Flatten all predictions
            predictions = np.concatenate(predictions, axis=0).flatten()
            # Truncate to original sequence length (mirror OSS utils.predict)
            predictions = predictions[:seq_len]
            return (predictions, None)

    except Exception as e:
        return None, str(e)

    return None, "Unknown error"


def load_labels_for_file(edf_path):
    """Load ground truth labels from .csv_bi file. Returns list of (start_sec, end_sec)."""
    csv_bi_path = edf_path.with_suffix(".csv_bi")

    if not csv_bi_path.exists():
        return []  # No seizures in this file

    seizure_events = []
    try:
        with open(csv_bi_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split(",")
                    if len(parts) >= 5 and parts[3] == "seiz":
                        start = float(parts[1])
                        end = float(parts[2])
                        seizure_events.append((start, end))
    except:
        pass

    return seizure_events


def create_binary_labels(seizure_events, duration_samples, fs=256):
    """Convert seizure events in seconds to per-sample binary array at fs Hz."""
    labels = np.zeros(duration_samples, dtype=int)
    if seizure_events:
        for start_sec, end_sec in seizure_events:
            start_idx = int(start_sec * fs)
            end_idx = min(int(end_sec * fs), duration_samples)
            if start_idx < duration_samples:
                labels[start_idx:end_idx] = 1
    return labels


def main():
    """Run bulletproof evaluation."""
    print("=" * 60)
    print("SeizureTransformer TUSZ Evaluation v2 (Bulletproof)")
    print("=" * 60)

    # Setup
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")

    # Load model
    print("\nLoading model...")
    model = load_models(device)
    model.eval()
    print("✅ Model loaded")

    # Find TUSZ eval files
    data_dir = Path("wu_2025/data/tusz/edf/eval")
    edf_files = sorted(data_dir.glob("**/*.edf"))
    print(f"\n✅ Found {len(edf_files)} EDF files")

    # Checkpoint file
    checkpoint_file = Path("evaluation/tusz/checkpoint.pkl")

    # Load checkpoint if exists
    if checkpoint_file.exists():
        print("\n📂 Loading checkpoint...")
        with open(checkpoint_file, "rb") as f:
            checkpoint = pickle.load(f)
        results = checkpoint["results"]
        start_idx = checkpoint["next_idx"]
        print(f"   Resuming from file {start_idx}/{len(edf_files)}")
    else:
        results = {}
        start_idx = 0

    # Process files
    print("\nProcessing files...")
    for idx in tqdm(range(start_idx, len(edf_files)), initial=start_idx, total=len(edf_files)):
        edf_path = edf_files[idx]
        file_id = edf_path.stem

        # Skip if already processed
        if file_id in results:
            continue

        # Process file
        predictions, error = process_single_file(edf_path, model, device)

        # Load labels
        seizure_events = load_labels_for_file(edf_path)

        # Store result
        results[file_id] = {
            "predictions": predictions,
            "seizure_events": seizure_events,
            "error": error
        }

        # Save checkpoint every 10 files
        if idx % 10 == 0:
            with open(checkpoint_file, "wb") as f:
                pickle.dump({
                    "results": results,
                    "next_idx": idx + 1
                }, f)

    # Save final checkpoint
    with open(checkpoint_file, "wb") as f:
        pickle.dump({
            "results": results,
            "next_idx": len(edf_files)
        }, f)

    print("\n" + "=" * 60)
    print("COMPUTING METRICS")
    print("=" * 60)

    # Collect all predictions and labels
    all_preds: list = []
    all_labels: list = []

    for _file_id, result in results.items():
        if result["predictions"] is not None and result["seizure_events"] is not None:
            preds = result["predictions"]

            # Create binary labels
            duration = len(preds)  # samples at 256 Hz
            labels = create_binary_labels(result["seizure_events"], duration, fs=256)

            # Ensure same length
            min_len = min(len(preds), len(labels))
            preds = preds[:min_len]
            labels = labels[:min_len]

            all_preds.extend(preds)
            all_labels.extend(labels)

    # Calculate metrics
    auroc = None
    if all_preds and all_labels:
        all_preds_array = np.array(all_preds)
        all_labels_array = np.array(all_labels)

        print("\n📊 Data Statistics:")
        print(f"   Total samples: {len(all_preds_array):,}")
        print(f"   Seizure samples: {all_labels_array.sum():,} ({100*all_labels_array.mean():.1f}%)")
        print(f"   Non-seizure samples: {(1-all_labels_array).sum():,}")

        # AUROC
        try:
            auroc = roc_auc_score(all_labels_array, all_preds_array)
            print(f"\n🎯 AUROC: {auroc:.4f}")
            print("   Paper claims: 0.876")

            if auroc > 0.85:
                print("   ✅ Close to paper results!")
            else:
                print("   ⚠️ Lower than expected")
        except Exception as e:
            print(f"   Could not calculate AUROC: {e}")

        # Threshold metrics
        threshold = 0.8
        binary_preds = (all_preds_array > threshold).astype(int)

        tp = np.sum((all_labels_array == 1) & (binary_preds == 1))
        fp = np.sum((all_labels_array == 0) & (binary_preds == 1))
        fn = np.sum((all_labels_array == 1) & (binary_preds == 0))
        tn = np.sum((all_labels_array == 0) & (binary_preds == 0))

        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

        print(f"\n📈 At threshold {threshold}:")
        print(f"   Sensitivity: {sensitivity:.3f}")
        print(f"   Specificity: {specificity:.3f}")

        # Save results
        results_file = Path("evaluation/tusz/results.json")
        with open(results_file, "w") as f:
            json.dump({
                "auroc": (float(auroc) if auroc is not None else None),
                "sensitivity": sensitivity,
                "specificity": specificity,
                "threshold": threshold,
                "total_samples": len(all_preds_array),
                "seizure_percentage": float(all_labels_array.mean()),
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)

        print(f"\n✅ Results saved to {results_file}")
    else:
        print("\n❌ No valid predictions to evaluate")

    # Clean up checkpoint
    if checkpoint_file.exists():
        checkpoint_file.rename(checkpoint_file.with_suffix(".pkl.complete"))
        print("\n🧹 Checkpoint saved as .complete")


if __name__ == "__main__":
    main()
