#!/usr/bin/env python3
"""
Tests for post_processing.py module.
"""

import numpy as np
import pytest

from evaluation.nedc_eeg_eval.nedc_scoring.post_processing import (
    apply_seizure_transformer_postprocessing,
    binary_mask_to_events,
    merge_nearby_events,
)


class TestBinaryMaskToEvents:
    def test_empty_mask(self):
        """Test with all zeros."""
        mask = np.zeros(1000, dtype=bool)
        events = binary_mask_to_events(mask)
        assert events == []

    def test_full_mask(self):
        """Test with all ones."""
        mask = np.ones(1000, dtype=bool)
        events = binary_mask_to_events(mask)
        assert events == [(0, 1000)]

    def test_single_event(self):
        """Test with a single seizure event."""
        mask = np.zeros(1000, dtype=bool)
        mask[100:200] = True
        events = binary_mask_to_events(mask)
        assert events == [(100, 200)]

    def test_multiple_events(self):
        """Test with multiple seizure events."""
        mask = np.zeros(1000, dtype=bool)
        mask[100:200] = True
        mask[300:350] = True
        mask[800:900] = True
        events = binary_mask_to_events(mask)
        assert events == [(100, 200), (300, 350), (800, 900)]

    def test_edge_events(self):
        """Test events at the edges of the array."""
        mask = np.zeros(1000, dtype=bool)
        mask[0:50] = True  # Start edge
        mask[950:1000] = True  # End edge
        events = binary_mask_to_events(mask)
        assert events == [(0, 50), (950, 1000)]

    def test_single_sample_events(self):
        """Test single-sample seizure events."""
        mask = np.zeros(10, dtype=bool)
        mask[2] = True
        mask[5] = True
        mask[8] = True
        events = binary_mask_to_events(mask)
        assert events == [(2, 3), (5, 6), (8, 9)]


class TestMergeNearbyEvents:
    def test_empty_events(self):
        """Test with empty event list."""
        events = []
        merged = merge_nearby_events(events, gap_sec=1.0)
        assert merged == []

    def test_single_event(self):
        """Test with single event."""
        events = [(10.0, 20.0)]
        merged = merge_nearby_events(events, gap_sec=1.0)
        assert merged == [(10.0, 20.0)]

    def test_no_merge_large_gap(self):
        """Test events with gaps larger than threshold."""
        events = [(10.0, 20.0), (25.0, 30.0), (40.0, 45.0)]
        merged = merge_nearby_events(events, gap_sec=2.0)
        assert merged == events  # No merging should occur

    def test_merge_small_gap(self):
        """Test merging events with small gaps."""
        events = [(10.0, 20.0), (20.5, 30.0)]  # 0.5 second gap
        merged = merge_nearby_events(events, gap_sec=1.0)
        assert merged == [(10.0, 30.0)]

    def test_merge_multiple(self):
        """Test merging multiple nearby events."""
        events = [(10.0, 20.0), (20.5, 25.0), (25.8, 30.0)]
        merged = merge_nearby_events(events, gap_sec=1.0)
        assert merged == [(10.0, 30.0)]

    def test_merge_overlapping(self):
        """Test merging overlapping events."""
        events = [(10.0, 20.0), (15.0, 25.0)]  # Overlapping
        merged = merge_nearby_events(events, gap_sec=1.0)
        assert merged == [(10.0, 25.0)]

    def test_merge_exact_gap(self):
        """Test events with gap exactly equal to threshold."""
        events = [(10.0, 20.0), (21.0, 30.0)]  # Exactly 1.0 second gap
        merged = merge_nearby_events(events, gap_sec=1.0)
        assert merged == [(10.0, 30.0)]

    def test_merge_unsorted(self):
        """Test that events are sorted before merging."""
        events = [(30.0, 40.0), (10.0, 20.0), (20.5, 25.0)]
        merged = merge_nearby_events(events, gap_sec=1.0)
        assert merged == [(10.0, 25.0), (30.0, 40.0)]

    def test_merge_complex_scenario(self):
        """Test complex scenario with mixed gaps."""
        events = [
            (10.0, 15.0),  # Group 1
            (15.5, 20.0),  # Group 1 (0.5s gap)
            (21.0, 25.0),  # Group 1 (1.0s gap)
            (30.0, 35.0),  # Group 2 (5.0s gap - separate)
            (35.2, 40.0),  # Group 2 (0.2s gap)
        ]
        merged = merge_nearby_events(events, gap_sec=1.0)
        assert merged == [(10.0, 25.0), (30.0, 40.0)]


class TestApplySeizureTransformerPostprocessing:
    def test_basic_postprocessing(self):
        """Test basic post-processing pipeline."""
        # Create predictions with clear seizure region
        predictions = np.zeros(256 * 10)  # 10 seconds at 256Hz
        predictions[256 * 2 : 256 * 5] = 0.9  # 3-second seizure (2-5s)

        events = apply_seizure_transformer_postprocessing(
            predictions,
            threshold=0.8,
            morph_kernel_size=5,
            min_duration_sec=2.0,
            fs=256,
        )

        assert len(events) == 1
        assert events[0][0] == pytest.approx(2.0, rel=0.1)
        assert events[0][1] == pytest.approx(5.0, rel=0.1)

    def test_threshold_filtering(self):
        """Test that threshold properly filters predictions."""
        predictions = np.ones(256 * 10) * 0.7  # Below threshold

        events = apply_seizure_transformer_postprocessing(
            predictions,
            threshold=0.8,
            morph_kernel_size=5,
            min_duration_sec=1.0,
            fs=256,
        )

        assert events == []  # No events above threshold

    def test_minimum_duration_filtering(self):
        """Test removal of short events."""
        predictions = np.zeros(256 * 10)
        # Create a 1-second event (below 2s minimum)
        predictions[256 * 2 : 256 * 3] = 0.9

        events = apply_seizure_transformer_postprocessing(
            predictions,
            threshold=0.8,
            morph_kernel_size=3,  # Small kernel to preserve short event
            min_duration_sec=2.0,
            fs=256,
        )

        assert events == []  # Event too short

    def test_morphological_operations(self):
        """Test morphological operations clean up noise."""
        predictions = np.zeros(256 * 10)
        # Add main seizure
        predictions[256 * 2 : 256 * 5] = 0.9
        # Add small noise spikes
        predictions[256 * 1 : 256 * 1 + 3] = 0.9  # 3-sample spike
        predictions[256 * 6 : 256 * 6 + 2] = 0.9  # 2-sample spike

        events = apply_seizure_transformer_postprocessing(
            predictions,
            threshold=0.8,
            morph_kernel_size=5,  # Should remove small spikes
            min_duration_sec=2.0,
            fs=256,
        )

        # Only main seizure should remain
        assert len(events) == 1
        assert events[0][0] == pytest.approx(2.0, rel=0.1)

    def test_merge_gap_blocked(self):
        """Test that non-zero merge_gap_sec raises ValueError."""
        predictions = np.zeros(256 * 10)
        predictions[256 * 2 : 256 * 3] = 0.9

        # Test that None and 0 are allowed
        events_none = apply_seizure_transformer_postprocessing(
            predictions,
            threshold=0.8,
            morph_kernel_size=3,
            min_duration_sec=0.5,
            fs=256,
            merge_gap_sec=None,
        )
        assert isinstance(events_none, list)

        events_zero = apply_seizure_transformer_postprocessing(
            predictions,
            threshold=0.8,
            morph_kernel_size=3,
            min_duration_sec=0.5,
            fs=256,
            merge_gap_sec=0.0,
        )
        assert isinstance(events_zero, list)

        # Test that non-zero values raise ValueError
        with pytest.raises(ValueError, match="merge_gap_sec.*not allowed"):
            apply_seizure_transformer_postprocessing(
                predictions,
                threshold=0.8,
                morph_kernel_size=3,
                min_duration_sec=0.5,
                fs=256,
                merge_gap_sec=1.0,  # Non-zero should be blocked
            )

        with pytest.raises(ValueError, match="merge_gap_sec.*not allowed"):
            apply_seizure_transformer_postprocessing(
                predictions,
                threshold=0.8,
                morph_kernel_size=3,
                min_duration_sec=0.5,
                fs=256,
                merge_gap_sec=0.5,  # Non-zero should be blocked
            )

    def test_edge_cases(self):
        """Test edge cases in post-processing."""
        # Empty predictions
        events = apply_seizure_transformer_postprocessing(
            np.array([]),
            threshold=0.8,
            morph_kernel_size=5,
            min_duration_sec=2.0,
            fs=256,
        )
        assert events == []

        # All ones - morphological operations slightly shrink edges
        predictions = np.ones(256 * 10)
        events = apply_seizure_transformer_postprocessing(
            predictions,
            threshold=0.8,
            morph_kernel_size=5,
            min_duration_sec=2.0,
            fs=256,
        )
        assert len(events) == 1
        # Check duration is approximately 10 seconds.
        # Morphological opening/closing with kernel k can shave up to ~k/fs at each edge.
        start, end = events[0]
        k = 5
        fs = 256
        min_duration = 10.0 - 2 * (k / fs)
        assert (end - start) >= (min_duration - 0.05)

    def test_realistic_scenario(self):
        """Test with realistic noisy predictions."""
        np.random.seed(42)
        predictions = np.random.rand(256 * 30)  # 30 seconds of random noise

        # Add clear seizure regions
        predictions[256 * 5 : 256 * 8] = 0.85 + np.random.rand(256 * 3) * 0.1
        predictions[256 * 15 : 256 * 20] = 0.82 + np.random.rand(256 * 5) * 0.15
        predictions[256 * 25 : 256 * 28] = 0.9 + np.random.rand(256 * 3) * 0.05

        events = apply_seizure_transformer_postprocessing(
            predictions,
            threshold=0.8,
            morph_kernel_size=5,
            min_duration_sec=2.0,
            fs=256,
        )

        # Should detect the three clear seizure regions
        assert len(events) == 3
        assert all(end - start >= 2.0 for start, end in events)
