#!/usr/bin/env python3
"""
Simplified tests for NEDC modules to improve coverage.
"""

import tempfile
from pathlib import Path

import numpy as np


def test_nedc_environment_setup():
    """Test that NEDC environment can be set up."""
    from evaluation.nedc_eeg_eval.nedc_scoring.run_nedc import setup_nedc_environment

    env = setup_nedc_environment()
    assert "NEDC_NFC" in env
    assert Path(env["NEDC_NFC"]).exists()


def test_extract_and_save_metrics_basic():
    """Test basic metrics extraction functionality."""
    from evaluation.nedc_eeg_eval.nedc_scoring.run_nedc import extract_and_save_metrics

    with tempfile.TemporaryDirectory() as tmpdir:
        results_dir = Path(tmpdir) / "results"
        results_dir.mkdir()

        # Create a summary file with metrics
        summary_content = """
        NEDC OVERLAP SCORING SUMMARY
        ================================================================================
        Sensitivity (TPR, Recall):                    75.50%
        Total False Alarm Rate:                       18.25 per 24 hours
        F1 Score:                                      0.850
        """
        (results_dir / "summary.txt").write_text(summary_content)

        metrics_file = results_dir / "metrics.json"
        metrics = extract_and_save_metrics(results_dir, metrics_file, backend="nedc-binary")

        # Check structure
        assert "timestamp" in metrics
        assert "provenance" in metrics
        assert "clinical_assessment" in metrics

        # Check overlap/taes metrics exist (backward compatibility)
        assert "overlap" in metrics or "taes" in metrics

        # Check file was saved
        assert metrics_file.exists()


def test_parse_nedc_output_directory():
    """Test parse_nedc_output with directory argument."""
    from evaluation.nedc_eeg_eval.nedc_scoring.run_nedc import parse_nedc_output

    with tempfile.TemporaryDirectory() as tmpdir:
        results_dir = Path(tmpdir) / "results"
        results_dir.mkdir()

        summary_content = """
        NEDC OVERLAP SCORING SUMMARY
        ================================================================================
        Sensitivity (TPR, Recall):                    80.00%
        Total False Alarm Rate:                       10.00 per 24 hours
        """
        (results_dir / "summary.txt").write_text(summary_content)

        # This function doesn't return metrics, it just prints them
        # and saves to metrics.json
        parse_nedc_output(results_dir, backend="nedc-binary")

        # Check metrics.json was created
        metrics_file = results_dir / "metrics.json"
        assert metrics_file.exists()


def test_backend_validation():
    """Test that invalid backends are caught."""
    from evaluation.nedc_eeg_eval.nedc_scoring.run_nedc import run_nedc_scorer

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)

        # Should fail with invalid backend
        returncode = run_nedc_scorer(output_dir, backend="invalid-backend")
        assert returncode != 0


def test_post_processing_with_real_data():
    """Test post-processing with realistic data patterns."""
    from evaluation.nedc_eeg_eval.nedc_scoring.post_processing import (
        apply_seizure_transformer_postprocessing,
    )

    # Create 30 seconds of predictions
    np.random.seed(123)
    predictions = np.random.rand(256 * 30) * 0.5  # Mostly below threshold

    # Add three clear seizure regions
    predictions[256 * 5 : 256 * 8] = 0.85  # 3-second seizure
    predictions[256 * 12 : 256 * 15] = 0.82  # 3-second seizure
    predictions[256 * 20 : 256 * 25] = 0.90  # 5-second seizure

    events = apply_seizure_transformer_postprocessing(
        predictions,
        threshold=0.8,
        morph_kernel_size=5,
        min_duration_sec=2.0,
        fs=256,
    )

    # Should detect all three seizures
    assert len(events) == 3

    # All should meet minimum duration
    for start, end in events:
        assert end - start >= 2.0

    # Should be in chronological order
    for i in range(len(events) - 1):
        assert events[i][1] < events[i + 1][0]