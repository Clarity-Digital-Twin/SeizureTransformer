#!/usr/bin/env python3
"""
Test the OVERLAP scorer - our critical Temple NEDC parity implementation.
"""

import sys
from pathlib import Path

import pytest

# Add seizure_evaluation to path
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from seizure_evaluation.taes.overlap_scorer import Event, OverlapScorer  # noqa: E402


class TestOverlapScorer:
    """Test suite for OVERLAP scorer."""

    def test_event_overlap_detection(self):
        """Test Event.overlaps() method."""
        e1 = Event(10.0, 20.0)
        e2 = Event(15.0, 25.0)  # Overlaps
        e3 = Event(25.0, 30.0)  # No overlap
        e4 = Event(5.0, 12.0)  # Overlaps

        assert e1.overlaps(e2) is True
        assert e1.overlaps(e3) is False
        assert e1.overlaps(e4) is True
        assert e2.overlaps(e3) is False

    def test_any_overlap_semantics(self):
        """Test that OVERLAP uses any-overlap (not 1-to-1)."""
        scorer = OverlapScorer()

        # One hyp spanning two refs - both refs should be hits
        ref_events = [Event(10.0, 20.0), Event(30.0, 40.0)]
        hyp_events = [Event(15.0, 35.0)]  # Spans both

        metrics = scorer.score_events(ref_events, hyp_events, 1800.0)

        assert metrics.hits == 2  # Both refs hit
        assert metrics.misses == 0
        assert metrics.false_alarms == 0  # Hyp has overlap

    def test_background_false_alarms(self):
        """Test background complement calculation."""
        scorer = OverlapScorer()

        # Events from 10-20, background should be 0-10 and 20-100
        ref_events = [Event(10.0, 20.0)]
        hyp_events = [Event(10.0, 20.0)]  # Perfect match

        metrics = scorer.score_events(ref_events, hyp_events, 100.0)

        # SEIZ metrics
        assert metrics.hits == 1
        assert metrics.false_alarms == 0

        # Background should have events at 0-10 and 20-100
        # Since hyp matches ref exactly, no BCKG false alarms
        assert metrics.bckg_false_alarms == 0

    def test_total_fa_rate(self):
        """Test Temple's Total False Alarm Rate (SEIZ + BCKG)."""
        scorer = OverlapScorer()

        ref_events = [Event(10.0, 20.0)]
        hyp_events = [Event(30.0, 40.0)]  # No overlap = FA

        metrics = scorer.score_events(ref_events, hyp_events, 86400.0)  # 24 hours

        assert metrics.false_alarms == 1  # SEIZ FA
        assert metrics.total_fa_per_24h == 1.0  # 1 FA in 24h

    def test_sensitivity_calculation(self):
        """Test sensitivity percentage calculation."""
        scorer = OverlapScorer()

        ref_events = [Event(10.0, 20.0), Event(30.0, 40.0), Event(50.0, 60.0)]
        hyp_events = [Event(10.0, 20.0), Event(30.0, 40.0)]  # Missing third

        metrics = scorer.score_events(ref_events, hyp_events, 1800.0)

        assert metrics.hits == 2
        assert metrics.misses == 1
        assert metrics.sensitivity == pytest.approx(66.67, rel=0.01)

    def test_merge_intervals(self):
        """Test interval merging for background calculation."""
        scorer = OverlapScorer()

        # Overlapping events that should merge
        events = [
            Event(10.0, 20.0),
            Event(15.0, 25.0),  # Overlaps first
            Event(30.0, 40.0),  # Separate
        ]

        merged = scorer._merge_intervals(events)
        assert len(merged) == 2
        assert merged[0].start_time == 10.0
        assert merged[0].stop_time == 25.0  # Merged
        assert merged[1].start_time == 30.0
        assert merged[1].stop_time == 40.0

    def test_complement_calculation(self):
        """Test background complement calculation."""
        scorer = OverlapScorer()

        events = [Event(10.0, 20.0), Event(30.0, 40.0)]
        background = scorer._complement_of_events(events, 50.0)

        # Should have 3 background segments: 0-10, 20-30, 40-50
        assert len(background) == 3
        assert background[0].start_time == 0.0
        assert background[0].stop_time == 10.0
        assert background[1].start_time == 20.0
        assert background[1].stop_time == 30.0
        assert background[2].start_time == 40.0
        assert background[2].stop_time == 50.0

    def test_csv_bi_parsing(self):
        """Test parsing CSV_bi files."""
        import tempfile

        scorer = OverlapScorer()

        # Create test CSV_bi file
        csv_content = """# version = csv_v1.0.0
# bname = test
# duration = 1800.0000 secs
channel,start_time,stop_time,label,confidence
TERM,100.0000,200.0000,seiz,1.0000
TERM,300.0000,400.0000,seiz,1.0000
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv_bi", delete=False) as f:
            f.write(csv_content)
            filepath = Path(f.name)

        events, duration = scorer._parse_csv_bi(filepath)

        assert len(events) == 2
        assert duration == 1800.0
        assert events[0].start_time == 100.0
        assert events[0].stop_time == 200.0
        assert events[1].start_time == 300.0
        assert events[1].stop_time == 400.0

        filepath.unlink()

    def test_exact_temple_parity(self):
        """Test a case that should match Temple exactly."""
        scorer = OverlapScorer()

        # From our actual dev baseline
        ref_events = [Event(42.2786, 81.7760)]  # Temple example
        hyp_events = [Event(42.2786, 81.7760)]  # Perfect match

        metrics = scorer.score_events(ref_events, hyp_events, 1800.0)

        assert metrics.hits == 1
        assert metrics.misses == 0
        assert metrics.false_alarms == 0
        assert metrics.sensitivity == 100.0
        assert metrics.fa_per_24h == 0.0
