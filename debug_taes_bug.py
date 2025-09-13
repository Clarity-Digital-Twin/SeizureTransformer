#!/usr/bin/env python3
"""Debug the TAES scoring bug by comparing native vs Temple on same data."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from seizure_evaluation.taes.scorer import TAESScorer

# Test with one file pair that has events
ref_file = Path("experiments/eval/baseline/nedc_results_frozen_temple/ref/aaaaafcf_s009_t009.csv_bi")
hyp_file = Path("experiments/eval/baseline/nedc_results_frozen_temple/hyp/aaaaafcf_s009_t009.csv_bi")

# Read the actual files
print("Reading files...")
print(f"Ref: {ref_file}")
print(f"Hyp: {hyp_file}")

# Score with different overlap thresholds
for threshold in [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]:
    scorer = TAESScorer(overlap_threshold=threshold)
    metrics = scorer.score_from_files(ref_file, hyp_file)

    print(f"\nOverlap threshold: {threshold}")
    print(f"  TP: {metrics.true_positives}")
    print(f"  FP: {metrics.false_positives}")
    print(f"  FN: {metrics.false_negatives}")
    print(f"  Sensitivity: {metrics.sensitivity:.2f}%")
    print(f"  FA/24h: {metrics.fa_per_24h:.2f}")

# Check what Temple NEDC actually uses
print("\n" + "="*60)
print("NOTE: Temple NEDC likely uses ANY overlap (threshold ~0.0)")
print("Our native scorer defaulted to 0.5 (50% overlap required)")
print("This would cause massive undercounting of True Positives!")