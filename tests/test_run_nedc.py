#!/usr/bin/env python3
"""
Tests for run_nedc.py module.
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from evaluation.nedc_eeg_eval.nedc_scoring.run_nedc import (
    extract_and_save_metrics,
    parse_nedc_output,
    run_nedc_scorer,
    setup_nedc_environment,
)


class TestSetupNedcEnvironment:
    def test_setup_environment(self):
        """Test NEDC environment setup."""
        env = setup_nedc_environment()

        assert "NEDC_NFC" in env
        assert "evaluation/nedc_eeg_eval/v6.0.0" in env["NEDC_NFC"]
        assert "PATH" in env
        assert "PYTHONPATH" in env
        assert "/lib:" in env["PYTHONPATH"]

    def test_nedc_path_exists(self):
        """Test that NEDC installation directory is checked."""
        # The v6.0.0 directory should exist in the repo
        env = setup_nedc_environment()
        nedc_path = Path(env["NEDC_NFC"])
        assert nedc_path.exists()
        assert (nedc_path / "bin").exists()


class TestParseNedcOutput:
    def test_parse_empty_output(self):
        """Test parsing empty NEDC output."""
        metrics = parse_nedc_output("")
        assert metrics == {}

    def test_parse_taes_summary(self):
        """Test parsing TAES scoring summary."""
        output = """
        ================================================================================
        NEDC TAES SCORING SUMMARY
        ================================================================================
        Sensitivity (TPR):                            72.34%
        False Alarms per 24 Hours (FP/24h):          15.23
        ================================================================================
        """

        metrics = parse_nedc_output(output)
        assert "taes" in metrics
        assert metrics["taes"]["sensitivity"] == 72.34
        assert metrics["taes"]["fa_per_24h"] == 15.23

    def test_parse_overlap_summary(self):
        """Test parsing overlap scoring summary."""
        output = """
        ================================================================================
        NEDC OVERLAP SCORING SUMMARY
        ================================================================================
        Epoch-Based Metrics:
          Sensitivity (SEN):                          68.45%
          Specificity (SPC):                          92.31%
          False Positive Rate (FPR):                   7.69%
          Precision (PRE):                            45.67%

        Any-Overlap Metrics:
          Sensitivity:                                85.12%
          Precision:                                  72.89%
          F1 Score:                                   0.7853
          False Alarms per 24 Hours:                   8.45
        ================================================================================
        """

        metrics = parse_nedc_output(output)

        assert "epoch_based" in metrics
        assert metrics["epoch_based"]["sensitivity"] == 68.45
        assert metrics["epoch_based"]["specificity"] == 92.31
        assert metrics["epoch_based"]["fpr"] == 7.69
        assert metrics["epoch_based"]["precision"] == 45.67

        assert "any_overlap" in metrics
        assert metrics["any_overlap"]["sensitivity"] == 85.12
        assert metrics["any_overlap"]["precision"] == 72.89
        assert metrics["any_overlap"]["f1_score"] == 0.7853
        assert metrics["any_overlap"]["fa_per_24h"] == 8.45

    def test_parse_combined_output(self):
        """Test parsing output with both TAES and overlap metrics."""
        output = """
        ================================================================================
        NEDC TAES SCORING SUMMARY
        ================================================================================
        Sensitivity (TPR):                            70.00%
        False Alarms per 24 Hours (FP/24h):          12.50
        ================================================================================

        ================================================================================
        NEDC OVERLAP SCORING SUMMARY
        ================================================================================
        Any-Overlap Metrics:
          Sensitivity:                                80.00%
          False Alarms per 24 Hours:                  10.00
        ================================================================================
        """

        metrics = parse_nedc_output(output)

        assert "taes" in metrics
        assert metrics["taes"]["sensitivity"] == 70.00
        assert metrics["taes"]["fa_per_24h"] == 12.50

        assert "any_overlap" in metrics
        assert metrics["any_overlap"]["sensitivity"] == 80.00
        assert metrics["any_overlap"]["fa_per_24h"] == 10.00

    def test_parse_with_extra_text(self):
        """Test parsing with additional text around summaries."""
        output = """
        Some preprocessing output...
        Loading files...

        ================================================================================
        NEDC TAES SCORING SUMMARY
        ================================================================================
        Sensitivity (TPR):                            65.43%
        False Alarms per 24 Hours (FP/24h):          20.15
        ================================================================================

        Some postprocessing output...
        Done!
        """

        metrics = parse_nedc_output(output)
        assert metrics["taes"]["sensitivity"] == 65.43
        assert metrics["taes"]["fa_per_24h"] == 20.15


class TestExtractAndSaveMetrics:
    def test_extract_from_summary_file(self):
        """Test extracting metrics from summary.txt file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results_dir = Path(tmpdir) / "results"
            results_dir.mkdir()

            summary_content = """
            ================================================================================
            NEDC TAES SCORING SUMMARY
            ================================================================================
            Sensitivity (TPR):                            75.50%
            False Alarms per 24 Hours (FP/24h):          18.25
            ================================================================================
            """

            (results_dir / "summary.txt").write_text(summary_content)
            metrics_file = results_dir / "metrics.json"

            metrics = extract_and_save_metrics(results_dir, metrics_file)

            assert metrics["taes"]["sensitivity"] == 75.50
            assert metrics["taes"]["fa_per_24h"] == 18.25

    def test_extract_no_summary_file(self):
        """Test handling when summary.txt doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results_dir = Path(tmpdir) / "results"
            metrics_file = results_dir / "metrics.json"

            metrics = extract_and_save_metrics(results_dir, metrics_file)
            assert metrics == {}

    def test_extract_with_metrics_json(self):
        """Test that metrics.json is created when extracting."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results_dir = Path(tmpdir) / "results"
            results_dir.mkdir()

            summary_content = """
            ================================================================================
            NEDC OVERLAP SCORING SUMMARY
            ================================================================================
            Any-Overlap Metrics:
              Sensitivity:                                90.00%
              F1 Score:                                   0.8500
            ================================================================================
            """

            (results_dir / "summary.txt").write_text(summary_content)
            metrics_file = results_dir / "metrics.json"

            metrics = extract_and_save_metrics(results_dir, metrics_file)

            # Check metrics.json was created
            assert metrics_file.exists()

            # Verify content
            saved_metrics = json.loads(metrics_file.read_text())
            assert saved_metrics["any_overlap"]["sensitivity"] == 90.00
            assert saved_metrics["any_overlap"]["f1_score"] == 0.8500


class TestRunNedcScorer:
    @patch("subprocess.run")
    def test_run_scorer_success(self, mock_run):
        """Test successful NEDC scorer execution."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Success",
            stderr=""
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            lists_dir = output_dir / "lists"
            lists_dir.mkdir(parents=True)

            # Create dummy list files
            (lists_dir / "ref.list").write_text("/path/to/ref.csv_bi\n")
            (lists_dir / "hyp.list").write_text("/path/to/hyp.csv_bi\n")

            # Mock environment setup
            with patch("evaluation.nedc_eeg_eval.nedc_scoring.run_nedc.setup_nedc_environment") as mock_env:
                mock_env.return_value = {"NEDC_NFC": "/mock/nedc"}

                returncode = run_nedc_scorer(output_dir, backend="nedc")

                assert returncode == 0
                mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_run_scorer_failure(self, mock_run):
        """Test NEDC scorer execution failure."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Error: Failed to process"
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            lists_dir = output_dir / "lists"
            lists_dir.mkdir(parents=True)

            (lists_dir / "ref.list").write_text("/path/to/ref.csv_bi\n")
            (lists_dir / "hyp.list").write_text("/path/to/hyp.csv_bi\n")

            with patch("evaluation.nedc_eeg_eval.nedc_scoring.run_nedc.setup_nedc_environment") as mock_env:
                mock_env.return_value = {"NEDC_NFC": "/mock/nedc"}

                returncode = run_nedc_scorer(output_dir, backend="nedc")

                assert returncode == 1

    def test_missing_list_files(self):
        """Test error when list files are missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            with patch("evaluation.nedc_eeg_eval.nedc_scoring.run_nedc.setup_nedc_environment") as mock_env:
                mock_env.return_value = {"NEDC_NFC": "/mock/nedc"}

                returncode = run_nedc_scorer(output_dir, backend="nedc")

                # Should fail due to missing list files
                assert returncode != 0