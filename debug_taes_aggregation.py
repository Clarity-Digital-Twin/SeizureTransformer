#!/usr/bin/env python3
"""Debug TAES aggregation by running native scorer on all eval files."""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seizure_evaluation.taes.scorer import TAESScorer

# Use the same files that were scored by both backends
ref_list = Path("experiments/eval/baseline/nedc_results_frozen_temple/lists/ref.list")
hyp_list = Path("experiments/eval/baseline/nedc_results_frozen_temple/lists/hyp.list")

# Read list files
with open(ref_list) as f:
    ref_files = [Path(line.strip()) for line in f if line.strip()]
with open(hyp_list) as f:
    hyp_files = [Path(line.strip()) for line in f if line.strip()]

print(f"Found {len(ref_files)} file pairs to score")

# Test different overlap thresholds
for threshold in [0.0, 0.1, 0.5]:
    scorer = TAESScorer(overlap_threshold=threshold)

    # Aggregate metrics
    total_tp = 0
    total_fp = 0
    total_fn = 0
    total_duration = 0.0

    # Score each file pair
    for ref_csv, hyp_csv in zip(ref_files, hyp_files):
        if ref_csv.stem == hyp_csv.stem:
            metrics = scorer.score_from_files(ref_csv, hyp_csv)
            total_tp += metrics.true_positives
            total_fp += metrics.false_positives
            total_fn += metrics.false_negatives
            total_duration += metrics.total_duration_sec

    # Calculate final metrics
    sensitivity = 100.0 * total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    fa_per_24h = total_fp * 86400.0 / total_duration if total_duration > 0 else 0.0

    print(f"\nOverlap threshold: {threshold}")
    print(f"  Total TP: {total_tp}, FP: {total_fp}, FN: {total_fn}")
    print(f"  Total duration: {total_duration/3600:.1f} hours")
    print(f"  Sensitivity: {sensitivity:.2f}%")
    print(f"  FA/24h: {fa_per_24h:.2f}")

# Compare with Temple results
print("\n" + "="*60)
print("Temple NEDC results (from metrics.json):")
with open("experiments/eval/baseline/nedc_results_frozen_temple/results/metrics.json") as f:
    temple_metrics = json.load(f)
print(f"  Sensitivity: {temple_metrics['taes']['sensitivity_percent']:.2f}%")
print(f"  FA/24h: {temple_metrics['taes']['fa_per_24h']:.2f}")