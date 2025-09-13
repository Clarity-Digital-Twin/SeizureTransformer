#!/usr/bin/env python3
"""
Fixed Native Python implementation of TAES (Time-Aligned Event Scoring).
Matches Temple NEDC v6.0.0 behavior exactly.

Key fixes:
1. Any-any matching: Multiple hypotheses can match the same reference
2. Overlap threshold: ANY overlap counts (>0 seconds)
3. Correct TP/FP/FN counting for any-any matching
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Set
import numpy as np


@dataclass
class Event:
    """Represents a seizure event with start/stop times."""
    start_time: float
    stop_time: float
    label: str = "seiz"
    confidence: float = 1.0

    @property
    def duration(self) -> float:
        """Event duration in seconds."""
        return self.stop_time - self.start_time


@dataclass
class TAESMetrics:
    """TAES evaluation metrics."""
    true_positives: int  # Number of reference events detected
    false_positives: int  # Number of hypothesis events not matching any reference
    false_negatives: int  # Number of reference events not detected
    total_duration_sec: float

    @property
    def sensitivity(self) -> float:
        """Sensitivity (TPR, Recall) as percentage."""
        if self.true_positives + self.false_negatives == 0:
            return 0.0
        return 100.0 * self.true_positives / (self.true_positives + self.false_negatives)

    @property
    def fa_per_24h(self) -> float:
        """False alarms per 24 hours."""
        if self.total_duration_sec == 0:
            return float('inf')
        return self.false_positives * 86400.0 / self.total_duration_sec

    @property
    def f1_score(self) -> float:
        """F1 score (harmonic mean of precision and recall)."""
        prec = 100.0 * self.true_positives / (self.true_positives + self.false_positives) if (self.true_positives + self.false_positives) > 0 else 0.0
        rec = self.sensitivity
        if prec + rec == 0:
            return 0.0
        return 2 * (prec/100 * rec/100) / (prec/100 + rec/100)


class FixedTAESScorer:
    """
    Fixed TAES implementation matching Temple NEDC v6.0.0 exactly.

    Key difference from original: Uses any-any matching where multiple
    hypothesis events can match the same reference event.
    """

    def __init__(self, min_overlap_sec: float = 0.0):
        """
        Initialize TAES scorer.

        Args:
            min_overlap_sec: Minimum overlap in seconds (Temple uses ANY overlap > 0)
        """
        self.min_overlap_sec = min_overlap_sec

    def score_events(
        self,
        ref_events: List[Event],
        hyp_events: List[Event],
        total_duration_sec: float
    ) -> TAESMetrics:
        """
        Score hypothesis events against reference events using any-any matching.

        In Temple NEDC's TAES:
        - TP = Number of reference events that have at least one overlapping hypothesis
        - FP = Number of hypothesis events that don't overlap any reference
        - FN = Number of reference events with no overlapping hypothesis

        Args:
            ref_events: Ground truth seizure events
            hyp_events: Predicted seizure events
            total_duration_sec: Total recording duration in seconds

        Returns:
            TAESMetrics with scoring results
        """
        # Track which events matched
        ref_matched = set()  # Indices of reference events that matched
        hyp_matched = set()  # Indices of hypothesis events that matched

        # Check each hypothesis against all references
        for h_idx, hyp in enumerate(hyp_events):
            for r_idx, ref in enumerate(ref_events):
                # Calculate overlap
                overlap_start = max(hyp.start_time, ref.start_time)
                overlap_stop = min(hyp.stop_time, ref.stop_time)
                overlap_duration = max(0, overlap_stop - overlap_start)

                # Any overlap counts
                if overlap_duration > self.min_overlap_sec:
                    ref_matched.add(r_idx)
                    hyp_matched.add(h_idx)

        # Calculate metrics
        # TP = references that were detected (at least one hyp matched)
        true_positives = len(ref_matched)

        # FN = references that were NOT detected
        false_negatives = len(ref_events) - true_positives

        # FP = hypotheses that didn't match any reference
        false_positives = len(hyp_events) - len(hyp_matched)

        return TAESMetrics(
            true_positives=true_positives,
            false_positives=false_positives,
            false_negatives=false_negatives,
            total_duration_sec=total_duration_sec
        )

    def score_from_files(
        self,
        ref_csv_bi: Path,
        hyp_csv_bi: Path
    ) -> TAESMetrics:
        """
        Score events from CSV_bi files.

        Args:
            ref_csv_bi: Path to reference CSV_bi file
            hyp_csv_bi: Path to hypothesis CSV_bi file

        Returns:
            TAESMetrics with scoring results
        """
        ref_events, ref_duration = self._parse_csv_bi(ref_csv_bi)
        hyp_events, hyp_duration = self._parse_csv_bi(hyp_csv_bi)

        # Use reference duration for scoring
        return self.score_events(ref_events, hyp_events, ref_duration)

    def _parse_csv_bi(self, csv_bi_path: Path) -> Tuple[List[Event], float]:
        """Parse events from CSV_bi file."""
        events = []
        duration = 0.0

        with open(csv_bi_path, 'r') as f:
            for line in f:
                line = line.strip()

                # Parse duration from header
                if line.startswith("# duration ="):
                    duration = float(line.split("=")[1].replace("secs", "").strip())

                # Skip headers and empty lines
                if line.startswith("#") or not line or line.startswith("channel"):
                    continue

                # Parse event
                parts = line.split(",")
                if len(parts) >= 5:
                    events.append(Event(
                        start_time=float(parts[1]),
                        stop_time=float(parts[2]),
                        label=parts[3],
                        confidence=float(parts[4])
                    ))

        return events, duration


if __name__ == "__main__":
    import json

    # Test on eval data
    ref_list = Path("experiments/eval/baseline/nedc_results_frozen_temple/lists/ref.list")
    hyp_list = Path("experiments/eval/baseline/nedc_results_frozen_temple/lists/hyp.list")

    # Read list files
    with open(ref_list) as f:
        ref_files = [Path(line.strip()) for line in f if line.strip()]
    with open(hyp_list) as f:
        hyp_files = [Path(line.strip()) for line in f if line.strip()]

    print(f"Scoring {len(ref_files)} file pairs with FIXED any-any matching...")

    scorer = FixedTAESScorer(min_overlap_sec=0.0)

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
    f1 = 2 * (sensitivity/100 * (total_tp/(total_tp+total_fp) if (total_tp+total_fp) > 0 else 0)) / ((sensitivity/100) + (total_tp/(total_tp+total_fp) if (total_tp+total_fp) > 0 else 0)) if ((sensitivity/100) + (total_tp/(total_tp+total_fp) if (total_tp+total_fp) > 0 else 0)) > 0 else 0.0

    print(f"\nFIXED Native TAES Results:")
    print(f"  Total TP: {total_tp}, FP: {total_fp}, FN: {total_fn}")
    print(f"  Total duration: {total_duration/3600:.1f} hours")
    print(f"  Sensitivity: {sensitivity:.2f}%")
    print(f"  FA/24h: {fa_per_24h:.2f}")
    print(f"  F1: {f1:.4f}")

    # Compare with Temple
    print(f"\nTemple NEDC Results (target):")
    with open("experiments/eval/baseline/nedc_results_frozen_temple/results/metrics.json") as f:
        temple_metrics = json.load(f)
    print(f"  Sensitivity: {temple_metrics['taes']['sensitivity_percent']:.2f}%")
    print(f"  FA/24h: {temple_metrics['taes']['fa_per_24h']:.2f}")
    print(f"  F1: {temple_metrics['taes']['f1_score']:.4f}")

    # Check if we match
    sens_diff = abs(sensitivity - temple_metrics['taes']['sensitivity_percent'])
    fa_diff = abs(fa_per_24h - temple_metrics['taes']['fa_per_24h'])
    f1_diff = abs(f1 - temple_metrics['taes']['f1_score'])

    print(f"\nDifferences:")
    print(f"  Sensitivity: {sens_diff:.2f} percentage points")
    print(f"  FA/24h: {fa_diff:.2f}")
    print(f"  F1: {f1_diff:.4f}")

    if sens_diff < 0.5 and fa_diff < 0.5:
        print("\n✅ SUCCESS! Fixed implementation matches Temple NEDC!")
    else:
        print("\n❌ Still not matching. Need more investigation.")