#!/usr/bin/env python3
"""Test if Temple counts each overlap PAIR as a separate TP."""

from pathlib import Path
import json

def score_taes_pair_counting(ref_files, hyp_files):
    """Score counting each overlap pair."""
    total_tp = 0  # Total overlap pairs
    total_fp = 0  # Hypothesis events with no overlaps
    total_fn = 0  # Reference events with no overlaps
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

        # Count overlaps
        ref_matched = set()
        hyp_matched = set()
        overlap_pairs = 0

        for h_idx, (h_start, h_stop) in enumerate(hyp_events):
            for r_idx, (r_start, r_stop) in enumerate(ref_events):
                # Any overlap
                if h_start < r_stop and h_stop > r_start:
                    ref_matched.add(r_idx)
                    hyp_matched.add(h_idx)
                    overlap_pairs += 1

        # Different counting methods
        # Method 1: Standard (what we've been trying)
        tp1 = len(ref_matched)
        fp1 = len(hyp_events) - len(hyp_matched)
        fn1 = len(ref_events) - len(ref_matched)

        # Method 2: Count pairs
        tp2 = overlap_pairs
        fp2 = len(hyp_events) - len(hyp_matched)
        fn2 = len(ref_events) - len(ref_matched)

        # Method 3: Maybe FP includes all non-matching pairs?
        # This would mean FP = hyp_events * ref_events - overlap_pairs (way too high)

        # Use Method 1 for now
        total_tp += tp1
        total_fp += fp1
        total_fn += fn1
        total_duration += duration

    return total_tp, total_fp, total_fn, total_duration


# Actually, let me check the Temple binary output more carefully
print("Checking Temple NEDC output format...")
temple_summary = Path("experiments/eval/baseline/nedc_results_frozen_temple/results/summary.txt")

if temple_summary.exists():
    print(f"\nTemple summary.txt contents:")
    print("="*60)
    with open(temple_summary) as f:
        content = f.read()
        print(content[:2000])  # First 2000 chars