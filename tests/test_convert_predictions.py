#!/usr/bin/env python3
"""
Tests for convert_predictions.py module.
"""

import pickle
import tempfile
from pathlib import Path

import numpy as np
import pytest

from evaluation.nedc_eeg_eval.nedc_scoring.convert_predictions import (
    convert_checkpoint_to_nedc,
    create_list_files,
    write_nedc_csv,
)


class TestWriteNedcCsv:
    def test_write_empty_events(self):
        """Test writing CSV_bi with no events."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test.csv_bi"
            write_nedc_csv([], output_file, "test_file", 100.0)

            content = output_file.read_text()
            assert "# version = csv_v1.0.0" in content
            assert "# bname = test_file" in content
            assert "# duration = 100.0000 secs" in content
            assert "channel,start_time,stop_time,label,confidence" in content

            # Should have only headers, no events
            lines = content.strip().split("\n")
            assert len(lines) == 4  # 3 headers + 1 column header

    def test_write_single_event(self):
        """Test writing CSV_bi with one seizure event."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test.csv_bi"
            events = [(10.5, 25.3)]
            write_nedc_csv(events, output_file, "test_file", 100.0)

            content = output_file.read_text()
            assert "TERM,10.5000,25.3000,seiz,1.0000" in content

    def test_write_multiple_events(self):
        """Test writing CSV_bi with multiple seizure events."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test.csv_bi"
            events = [(10.0, 20.0), (30.5, 45.75), (60.123, 70.456)]
            write_nedc_csv(events, output_file, "test_file", 100.0)

            content = output_file.read_text()
            assert "TERM,10.0000,20.0000,seiz,1.0000" in content
            assert "TERM,30.5000,45.7500,seiz,1.0000" in content
            assert "TERM,60.1230,70.4560,seiz,1.0000" in content

    def test_creates_parent_directories(self):
        """Test that parent directories are created if they don't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "nested" / "dirs" / "test.csv_bi"
            events = [(1.0, 2.0)]
            write_nedc_csv(events, output_file, "test_file", 10.0)

            assert output_file.exists()
            assert output_file.parent.exists()


class TestCreateListFiles:
    def test_create_list_files(self):
        """Test creation of ref.list and hyp.list files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            file_ids = ["file1", "file2", "file3"]

            # Create dummy CSV_bi files
            hyp_dir = output_dir / "hyp"
            ref_dir = output_dir / "ref"
            hyp_dir.mkdir(parents=True)
            ref_dir.mkdir(parents=True)

            for file_id in file_ids:
                (hyp_dir / f"{file_id}.csv_bi").touch()
                (ref_dir / f"{file_id}.csv_bi").touch()

            create_list_files(output_dir, file_ids)

            # Check list files exist
            hyp_list = output_dir / "lists" / "hyp.list"
            ref_list = output_dir / "lists" / "ref.list"
            assert hyp_list.exists()
            assert ref_list.exists()

            # Check content
            hyp_content = hyp_list.read_text().strip().split("\n")
            ref_content = ref_list.read_text().strip().split("\n")

            assert len(hyp_content) == 3
            assert len(ref_content) == 3

            # Files should be sorted
            assert "file1.csv_bi" in hyp_content[0]
            assert "file2.csv_bi" in hyp_content[1]
            assert "file3.csv_bi" in hyp_content[2]

    def test_empty_file_list(self):
        """Test handling of empty file list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            create_list_files(output_dir, [])

            hyp_list = output_dir / "lists" / "hyp.list"
            ref_list = output_dir / "lists" / "ref.list"

            assert hyp_list.exists()
            assert ref_list.exists()
            assert hyp_list.read_text() == ""
            assert ref_list.read_text() == ""


class TestConvertCheckpointToNedc:
    def create_test_checkpoint(self, tmpdir, with_errors=False):
        """Helper to create a test checkpoint file."""
        checkpoint = {
            "results": {
                "file1": {
                    "predictions": np.ones(256 * 10),  # 10 seconds at 256Hz
                    "seizure_events": [(2.0, 5.0), (7.0, 9.0)],
                },
                "file2": {
                    "predictions": np.zeros(256 * 20),  # 20 seconds at 256Hz
                    "seizure_events": [],
                },
            }
        }

        if with_errors:
            checkpoint["results"]["file3"] = {
                "error": "Failed to process",
                "predictions": None,
                "seizure_events": [],
            }
            checkpoint["results"]["file4"] = {
                "predictions": None,
                "seizure_events": [(1.0, 2.0)],
            }

        checkpoint_file = Path(tmpdir) / "checkpoint.pkl"
        with open(checkpoint_file, "wb") as f:
            pickle.dump(checkpoint, f)

        return checkpoint_file

    def test_convert_basic_checkpoint(self):
        """Test basic checkpoint conversion."""
        with tempfile.TemporaryDirectory() as tmpdir:
            checkpoint_file = self.create_test_checkpoint(tmpdir)
            output_dir = Path(tmpdir) / "output"

            processed = convert_checkpoint_to_nedc(
                checkpoint_file,
                output_dir,
                threshold=0.5,  # Lower threshold since we're using ones
                morph_kernel_size=3,
                min_duration_sec=1.0,
            )

            assert len(processed) == 2
            assert "file1" in processed
            assert "file2" in processed

            # Check files were created
            assert (output_dir / "hyp" / "file1.csv_bi").exists()
            assert (output_dir / "ref" / "file1.csv_bi").exists()
            assert (output_dir / "hyp" / "file2.csv_bi").exists()
            assert (output_dir / "ref" / "file2.csv_bi").exists()

            # Check list files
            assert (output_dir / "lists" / "hyp.list").exists()
            assert (output_dir / "lists" / "ref.list").exists()

            # Check params file
            assert (output_dir / "params.json").exists()

    def test_convert_with_errors(self):
        """Test conversion skips files with errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            checkpoint_file = self.create_test_checkpoint(tmpdir, with_errors=True)
            output_dir = Path(tmpdir) / "output"

            processed = convert_checkpoint_to_nedc(
                checkpoint_file,
                output_dir,
                threshold=0.5,
            )

            # Should only process valid files
            assert len(processed) == 2
            assert "file1" in processed
            assert "file2" in processed
            assert "file3" not in processed  # Has error
            assert "file4" not in processed  # No predictions

    def test_convert_with_merge_gap(self):
        """Test conversion with merge_gap_sec parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            checkpoint_file = self.create_test_checkpoint(tmpdir)
            output_dir = Path(tmpdir) / "output"

            processed = convert_checkpoint_to_nedc(
                checkpoint_file,
                output_dir,
                threshold=0.5,
                merge_gap_sec=1.0,  # Non-standard parameter
            )

            # Should create warning file
            warning_file = output_dir / "NONSTANDARD_POSTPROCESSING.txt"
            assert warning_file.exists()
            assert "merge_gap_sec is enabled" in warning_file.read_text()

    def test_legacy_checkpoint_format(self):
        """Test handling of checkpoint without 'results' key."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create legacy format (direct dict of results)
            checkpoint = {
                "file1": {
                    "predictions": np.ones(256 * 5),
                    "seizure_events": [(1.0, 3.0)],
                }
            }

            checkpoint_file = Path(tmpdir) / "checkpoint.pkl"
            with open(checkpoint_file, "wb") as f:
                pickle.dump(checkpoint, f)

            output_dir = Path(tmpdir) / "output"
            processed = convert_checkpoint_to_nedc(
                checkpoint_file,
                output_dir,
                threshold=0.5,
            )

            assert len(processed) == 1
            assert "file1" in processed