#!/usr/bin/env python3
"""Test alternative TAES interpretation where TP = matched hypothesis events."""

from pathlib import Path
import json

def score_taes_alternative(ref_files, hyp_files):
    """Score using TP = matched hypotheses interpretation."""
    total_tp = 0  # Matched hypothesis events
    total_fp = 0  # Unmatched hypothesis events
    total_fn = 0  # Unmatched reference events
    total_duration = 0.0

    for ref_file, hyp_file in zip(ref_files, hyp_files):
        if ref_file.stem != hyp_file.stem:
            continue

        # Parse events
        ref_events = []
        hyp_events = []
        duration = 0.0

        with open(ref_file) as f:
            for line in f:
                if line.startswith("# duration ="):
                    duration = float(line.split("=")[1].replace("secs", "").strip())
                elif not line.startswith("#") and not line.startswith("channel") and line.strip():
                    parts = line.strip().split(",")
                    if len(parts) >= 5:
                        ref_events.append((float(parts[1]), float(parts[2])))

        with open(hyp_file) as f:
            for line in f:
                if not line.startswith("#") and not line.startswith("channel") and line.strip():
                    parts = line.strip().split(",")
                    if len(parts) >= 5:
                        hyp_events.append((float(parts[1]), float(parts[2])))

        # Any-any matching
        ref_matched = set()
        hyp_matched = set()

        for h_idx, (h_start, h_stop) in enumerate(hyp_events):
            for r_idx, (r_start, r_stop) in enumerate(ref_events):
                # Any overlap
                if h_start < r_stop and h_stop > r_start:
                    ref_matched.add(r_idx)
                    hyp_matched.add(h_idx)

        # Alternative counting
        total_tp += len(hyp_matched)  # Matched hypotheses
        total_fp += len(hyp_events) - len(hyp_matched)  # Unmatched hypotheses
        total_fn += len(ref_events) - len(ref_matched)  # Unmatched references
        total_duration += duration

    return total_tp, total_fp, total_fn, total_duration


# Test on eval data
ref_list = Path("experiments/eval/baseline/nedc_results_frozen_temple/lists/ref.list")
hyp_list = Path("experiments/eval/baseline/nedc_results_frozen_temple/lists/hyp.list")

with open(ref_list) as f:
    ref_files = [Path(line.strip()) for line in f if line.strip()]
with open(hyp_list) as f:
    hyp_files = [Path(line.strip()) for line in f if line.strip()]

print(f"Testing alternative TAES interpretation on {len(ref_files)} files...")

tp, fp, fn, duration = score_taes_alternative(ref_files, hyp_files)

# Calculate metrics
sensitivity = 100.0 * tp / (tp + fn) if (tp + fn) > 0 else 0.0
fa_per_24h = fp * 86400.0 / duration if duration > 0 else 0.0

print(f"\nAlternative TAES (TP=matched hypotheses):")
print(f"  TP: {tp}, FP: {fp}, FN: {fn}")
print(f"  Duration: {duration/3600:.1f} hours")
print(f"  Sensitivity: {sensitivity:.2f}%")
print(f"  FA/24h: {fa_per_24h:.2f}")

# Temple target
print(f"\nTemple NEDC (target):")
with open("experiments/eval/baseline/nedc_results_frozen_temple/results/metrics.json") as f:
    temple = json.load(f)
print(f"  Sensitivity: {temple['taes']['sensitivity_percent']:.2f}%")
print(f"  FA/24h: {temple['taes']['fa_per_24h']:.2f}")