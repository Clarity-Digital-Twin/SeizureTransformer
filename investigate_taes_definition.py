#!/usr/bin/env python3
"""Investigate exact TAES definition - maybe we're misunderstanding TP/FP/FN."""

import sys
from pathlib import Path
import json

# Check a specific file with known events
ref_file = Path("experiments/eval/baseline/nedc_results_frozen_temple/ref/aaaaafcf_s009_t009.csv_bi")
hyp_file = Path("experiments/eval/baseline/nedc_results_frozen_temple/hyp/aaaaafcf_s009_t009.csv_bi")

# Count events
ref_events = []
hyp_events = []

with open(ref_file) as f:
    for line in f:
        if not line.startswith("#") and not line.startswith("channel") and line.strip():
            parts = line.strip().split(",")
            if len(parts) >= 5:
                ref_events.append((float(parts[1]), float(parts[2])))

with open(hyp_file) as f:
    for line in f:
        if not line.startswith("#") and not line.startswith("channel") and line.strip():
            parts = line.strip().split(",")
            if len(parts) >= 5:
                hyp_events.append((float(parts[1]), float(parts[2])))

print(f"File: {ref_file.stem}")
print(f"Reference events: {len(ref_events)}")
print(f"Hypothesis events: {len(hyp_events)}")

# Check for any overlap
ref_matched = set()
hyp_matched = set()

for h_idx, (h_start, h_stop) in enumerate(hyp_events):
    for r_idx, (r_start, r_stop) in enumerate(ref_events):
        # Any overlap?
        if h_start < r_stop and h_stop > r_start:
            ref_matched.add(r_idx)
            hyp_matched.add(h_idx)

print(f"\nWith any-any matching:")
print(f"  Ref events matched: {len(ref_matched)}/{len(ref_events)}")
print(f"  Hyp events matched: {len(hyp_matched)}/{len(hyp_events)}")
print(f"  TP (refs detected): {len(ref_matched)}")
print(f"  FP (hyps unmatched): {len(hyp_events) - len(hyp_matched)}")
print(f"  FN (refs missed): {len(ref_events) - len(ref_matched)}")

# Maybe Temple counts EVENTS differently?
# Perhaps "TP" in Temple means matched hypothesis events, not matched references?
print("\n" + "="*60)
print("Alternative interpretation (Temple might use):")
print("  TP = Number of HYPOTHESIS events that match a reference")
print("  FP = Number of HYPOTHESIS events that don't match")
print("  FN = Number of REFERENCE events not matched")
print(f"\nWith this interpretation:")
print(f"  TP: {len(hyp_matched)}")
print(f"  FP: {len(hyp_events) - len(hyp_matched)}")
print(f"  FN: {len(ref_events) - len(ref_matched)}")