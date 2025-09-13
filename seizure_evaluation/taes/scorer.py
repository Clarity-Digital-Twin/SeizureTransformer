#!/usr/bin/env python3
"""
Native Python implementation of TAES (Time-Aligned Event Scoring).
Reimplements NEDC's TAES algorithm for full ownership and portability.

Reference: NEDC v6.0.0 TAES scoring methodology
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict, Optional
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

    def overlaps(self, other: "Event", min_overlap: float = 0.0) -> bool:
        """Check if this event overlaps with another."""
        overlap_start = max(self.start_time, other.start_time)
        overlap_stop = min(self.stop_time, other.stop_time)
        overlap_duration = max(0, overlap_stop - overlap_start)
        return overlap_duration >= min_overlap


@dataclass
class TAESMetrics:
    """TAES evaluation metrics."""
    true_positives: int
    false_positives: int
    false_negatives: int
    total_duration_sec: float

    @property
    def sensitivity(self) -> float:
        """Sensitivity (TPR, Recall) as percentage."""
        if self.true_positives + self.false_negatives == 0:
            return 0.0
        return 100.0 * self.true_positives / (self.true_positives + self.false_negatives)

    @property
    def precision(self) -> float:
        """Precision as percentage."""
        if self.true_positives + self.false_positives == 0:
            return 0.0
        return 100.0 * self.true_positives / (self.true_positives + self.false_positives)

    @property
    def f1_score(self) -> float:
        """F1 score (harmonic mean of precision and recall)."""
        prec = self.precision / 100.0
        rec = self.sensitivity / 100.0
        if prec + rec == 0:
            return 0.0
        return 2 * (prec * rec) / (prec + rec)

    @property
    def fa_per_24h(self) -> float:
        """False alarms per 24 hours."""
        if self.total_duration_sec == 0:
            return float('inf')
        return self.false_positives * 86400.0 / self.total_duration_sec


class TAESScorer:
    """
    Time-Aligned Event Scoring (TAES) implementation.
    Matches NEDC v6.0.0 scoring methodology.
    """

    def __init__(self, overlap_threshold: float = 0.0):
        """
        Initialize TAES scorer.

        Args:
            overlap_threshold: Minimum overlap ratio for matching events (0.0-1.0)
                              Default 0.0 matches Temple NEDC OVERLAP scoring
        """
        self.overlap_threshold = overlap_threshold

    def score_events(
        self,
        ref_events: List[Event],
        hyp_events: List[Event],
        total_duration_sec: float
    ) -> TAESMetrics:
        """
        Score hypothesis events against reference events.

        Args:
            ref_events: Ground truth seizure events
            hyp_events: Predicted seizure events
            total_duration_sec: Total recording duration in seconds

        Returns:
            TAESMetrics with scoring results
        """
        # Sort events by start time
        ref_events = sorted(ref_events, key=lambda e: e.start_time)
        hyp_events = sorted(hyp_events, key=lambda e: e.start_time)

        # Match events using greedy algorithm
        ref_matched = [False] * len(ref_events)
        hyp_matched = [False] * len(hyp_events)

        # For each hypothesis event, find best matching reference
        for h_idx, hyp in enumerate(hyp_events):
            best_overlap = 0.0
            best_ref_idx = -1

            for r_idx, ref in enumerate(ref_events):
                if ref_matched[r_idx]:
                    continue

                # Calculate overlap
                overlap_start = max(hyp.start_time, ref.start_time)
                overlap_stop = min(hyp.stop_time, ref.stop_time)
                overlap_duration = max(0, overlap_stop - overlap_start)

                # Calculate overlap ratio (relative to reference)
                if ref.duration > 0:
                    overlap_ratio = overlap_duration / ref.duration
                    if overlap_ratio > best_overlap and overlap_ratio >= self.overlap_threshold:
                        best_overlap = overlap_ratio
                        best_ref_idx = r_idx

            # Mark best match
            if best_ref_idx >= 0:
                ref_matched[best_ref_idx] = True
                hyp_matched[h_idx] = True

        # Calculate metrics
        true_positives = sum(hyp_matched)
        false_positives = len(hyp_events) - true_positives
        false_negatives = len(ref_events) - sum(ref_matched)

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


def compare_with_nedc(
    ref_csv_bi: Path,
    hyp_csv_bi: Path,
    nedc_metrics: Dict[str, float],
    tolerance: float = 0.1
) -> Dict[str, any]:
    """
    Compare native TAES with NEDC results.

    Args:
        ref_csv_bi: Reference CSV_bi file
        hyp_csv_bi: Hypothesis CSV_bi file
        nedc_metrics: NEDC metrics dict with sensitivity, fa_per_24h, f1_score
        tolerance: Maximum allowed difference (percentage points)

    Returns:
        Comparison results with deltas and pass/fail status
    """
    scorer = TAESScorer()
    native_metrics = scorer.score_from_files(ref_csv_bi, hyp_csv_bi)

    comparison = {
        "native": {
            "sensitivity": native_metrics.sensitivity,
            "fa_per_24h": native_metrics.fa_per_24h,
            "f1_score": native_metrics.f1_score
        },
        "nedc": nedc_metrics,
        "deltas": {},
        "within_tolerance": True
    }

    # Calculate deltas
    for metric in ["sensitivity", "fa_per_24h", "f1_score"]:
        if metric in nedc_metrics:
            delta = abs(comparison["native"][metric] - nedc_metrics[metric])
            comparison["deltas"][metric] = delta
            if delta > tolerance:
                comparison["within_tolerance"] = False

    return comparison