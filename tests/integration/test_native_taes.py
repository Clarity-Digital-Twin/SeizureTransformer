#!/usr/bin/env python3
"""
Test native TAES implementation against NEDC golden outputs.
Ensures our Python implementation matches official scorer.
"""

import json
from pathlib import Path
import pytest
import sys

# Add seizure_evaluation to path
repo_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(repo_root))

from seizure_evaluation.taes.scorer import TAESScorer, compare_with_nedc


@pytest.mark.taes
@pytest.mark.conformance
class TestNativeTAES:
    """Test native TAES scorer conformance with NEDC."""

    def test_taes_on_fixtures(self):
        """Run native TAES on golden fixtures and compare with NEDC."""
        fixture_path = Path(__file__).parent.parent / "fixtures" / "nedc"

        # Check if fixtures exist
        if not fixture_path.exists():
            pytest.skip("NEDC fixtures not found")

        # Load expected NEDC metrics
        expected_metrics_file = fixture_path / "expected_metrics.json"
        if not expected_metrics_file.exists():
            pytest.skip("Expected metrics not found")

        with open(expected_metrics_file) as f:
            nedc_metrics = json.load(f)

        # Run native scorer on each fixture pair
        scorer = TAESScorer()

        ref_dir = fixture_path / "ref"
        hyp_dir = fixture_path / "hyp"

        total_metrics = {
            "true_positives": 0,
            "false_positives": 0,
            "false_negatives": 0,
            "total_duration": 0.0
        }

        for ref_file in sorted(ref_dir.glob("*.csv_bi")):
            hyp_file = hyp_dir / ref_file.name
            if not hyp_file.exists():
                continue

            metrics = scorer.score_from_files(ref_file, hyp_file)
            total_metrics["true_positives"] += metrics.true_positives
            total_metrics["false_positives"] += metrics.false_positives
            total_metrics["false_negatives"] += metrics.false_negatives
            total_metrics["total_duration"] += metrics.total_duration_sec

        # Calculate aggregate metrics
        if total_metrics["total_duration"] > 0:
            native_sensitivity = 100.0 * total_metrics["true_positives"] / (
                total_metrics["true_positives"] + total_metrics["false_negatives"]
            ) if (total_metrics["true_positives"] + total_metrics["false_negatives"]) > 0 else 0.0

            native_fa_per_24h = total_metrics["false_positives"] * 86400.0 / total_metrics["total_duration"]

            # Compare with NEDC (allow 0.1% tolerance)
            if "sensitivity" in nedc_metrics:
                assert abs(native_sensitivity - nedc_metrics["sensitivity"]) < 0.1, (
                    f"Sensitivity mismatch: {native_sensitivity:.2f} vs {nedc_metrics['sensitivity']:.2f}"
                )

            if "fa_per_24h" in nedc_metrics:
                assert abs(native_fa_per_24h - nedc_metrics["fa_per_24h"]) < 0.1, (
                    f"FA/24h mismatch: {native_fa_per_24h:.2f} vs {nedc_metrics['fa_per_24h']:.2f}"
                )

    def test_empty_events(self):
        """Test scorer with no events."""
        scorer = TAESScorer()
        metrics = scorer.score_events([], [], 1800.0)

        assert metrics.true_positives == 0
        assert metrics.false_positives == 0
        assert metrics.false_negatives == 0
        assert metrics.sensitivity == 0.0
        assert metrics.fa_per_24h == 0.0

    def test_perfect_match(self):
        """Test scorer with perfectly matching events."""
        from seizure_evaluation.taes.scorer import Event

        ref_events = [
            Event(10.0, 20.0),
            Event(30.0, 45.0),
            Event(60.0, 75.0)
        ]
        hyp_events = ref_events.copy()

        scorer = TAESScorer()
        metrics = scorer.score_events(ref_events, hyp_events, 1800.0)

        assert metrics.true_positives == 3
        assert metrics.false_positives == 0
        assert metrics.false_negatives == 0
        assert metrics.sensitivity == 100.0
        assert metrics.fa_per_24h == 0.0

    def test_partial_overlap(self):
        """Test scorer with partial overlaps."""
        from seizure_evaluation.taes.scorer import Event

        ref_events = [Event(10.0, 20.0)]  # 10 second event
        hyp_events = [Event(15.0, 25.0)]  # 50% overlap

        scorer = TAESScorer(overlap_threshold=0.5)
        metrics = scorer.score_events(ref_events, hyp_events, 1800.0)

        assert metrics.true_positives == 1  # Meets 50% threshold
        assert metrics.false_positives == 0
        assert metrics.false_negatives == 0