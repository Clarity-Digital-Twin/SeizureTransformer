#!/usr/bin/env python3
"""
Test the NEDC pipeline with a small subset of data.
Validates that all components work correctly before full run.
"""

import pickle
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import numpy as np


def create_test_checkpoint(output_file, num_files=5):
    """
    Create a small test checkpoint for pipeline validation.

    Args:
        output_file: Path to save test checkpoint
        num_files: Number of test files to include
    """
    print(f"Creating test checkpoint with {num_files} files...")

    # Create synthetic test data
    test_results = {}

    for i in range(num_files):
        file_id = f"test_file_{i:03d}_s001_t000"

        # Create random predictions (10 minutes at 256 Hz)
        duration_samples = 10 * 60 * 256  # 10 minutes
        predictions = np.random.random(duration_samples)

        # Add some high probability regions to simulate seizures
        if i % 2 == 0:  # Half the files have seizures
            # Add 2 seizure events
            seizure_start1 = duration_samples // 4
            seizure_end1 = seizure_start1 + 256 * 20  # 20 second seizure
            predictions[seizure_start1:seizure_end1] = (
                0.9 + np.random.random(seizure_end1 - seizure_start1) * 0.1
            )

            seizure_start2 = duration_samples // 2
            seizure_end2 = seizure_start2 + 256 * 30  # 30 second seizure
            predictions[seizure_start2:seizure_end2] = (
                0.85 + np.random.random(seizure_end2 - seizure_start2) * 0.15
            )

            # Ground truth events (in seconds)
            seizure_events = [
                (seizure_start1 / 256, seizure_end1 / 256),
                (seizure_start2 / 256, seizure_end2 / 256),
            ]
        else:
            seizure_events = []

        test_results[file_id] = {
            "predictions": predictions,
            "seizure_events": seizure_events,
            "error": None,
        }

    # Save checkpoint
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "wb") as f:
        pickle.dump({"results": test_results}, f)

    print(f"Test checkpoint saved to: {output_file}")
    return test_results


def validate_conversion(test_checkpoint, output_dir):
    """
    Test the conversion script.

    Args:
        test_checkpoint: Path to test checkpoint
        output_dir: Output directory

    Returns:
        bool: True if validation passed
    """
    print("\n" + "=" * 60)
    print("TESTING: Conversion to NEDC format")
    print("=" * 60)

    cmd = [
        sys.executable,
        "evaluation/nedc_eeg_eval/nedc_scoring/convert_predictions.py",
        "--checkpoint",
        str(test_checkpoint),
        "--outdir",
        str(output_dir),
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("FAILED: Conversion script error")
        print(result.stderr)
        return False

    print(result.stdout)

    # Validate output structure
    output_dir = Path(output_dir)
    hyp_dir = output_dir / "hyp"
    ref_dir = output_dir / "ref"
    lists_dir = output_dir / "lists"

    if not hyp_dir.exists():
        print("FAILED: hyp/ directory not created")
        return False

    if not ref_dir.exists():
        print("FAILED: ref/ directory not created")
        return False

    if not lists_dir.exists():
        print("FAILED: lists/ directory not created")
        return False

    # Check for CSV_bi files
    hyp_files = list(hyp_dir.glob("*.csv_bi"))
    ref_files = list(ref_dir.glob("*.csv_bi"))

    print(f"Found {len(hyp_files)} hypothesis files")
    print(f"Found {len(ref_files)} reference files")

    if len(hyp_files) == 0:
        print("FAILED: No hypothesis CSV_bi files created")
        return False

    if len(ref_files) == 0:
        print("FAILED: No reference CSV_bi files created")
        return False

    # Check list files
    hyp_list = lists_dir / "hyp.list"
    ref_list = lists_dir / "ref.list"

    if not hyp_list.exists():
        print("FAILED: hyp.list not created")
        return False

    if not ref_list.exists():
        print("FAILED: ref.list not created")
        return False

    # Validate CSV_bi format
    sample_file = hyp_files[0]
    with open(sample_file) as f:
        content = f.read()

    if "# version = csv_v1.0.0" not in content:
        print("FAILED: Invalid CSV_bi header")
        return False

    if "channel,start_time,stop_time,label,confidence" not in content:
        print("FAILED: Invalid CSV_bi columns")
        return False

    print("PASSED: Conversion validation successful")
    return True


def validate_nedc_binary():
    """
    Check if NEDC binary is available.

    Returns:
        bool: True if NEDC binary found
    """
    print("\n" + "=" * 60)
    print("TESTING: NEDC binary availability")
    print("=" * 60)

    # Check environment setup
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent
    nedc_root = repo_root / "evaluation" / "nedc_eeg_eval" / "v6.0.0"
    nedc_binary = nedc_root / "bin" / "nedc_eeg_eval"

    if not nedc_root.exists():
        print(f"FAILED: NEDC not found at {nedc_root}")
        return False

    if not nedc_binary.exists():
        print(f"FAILED: NEDC binary not found at {nedc_binary}")
        print("Note: NEDC binaries may need to be built/installed separately")
        return False

    print(f"PASSED: NEDC binary found at {nedc_binary}")
    return True


def run_full_test():
    """
    Run complete pipeline test.

    Returns:
        int: Exit code (0 for success)
    """
    print("=" * 60)
    print("NEDC PIPELINE TEST")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Set up test paths (always relative to this script's directory)
    base_dir = Path(__file__).resolve().parent
    test_dir = base_dir / "test_output"
    test_checkpoint = test_dir / "test_checkpoint.pkl"

    # Clean up previous test
    if test_dir.exists():
        import shutil

        shutil.rmtree(test_dir)

    # Step 1: Create test data
    create_test_checkpoint(test_checkpoint, num_files=5)

    # Step 2: Test conversion
    if not validate_conversion(test_checkpoint, test_dir):
        print("\nTEST FAILED: Conversion validation failed")
        return 1

    # Step 3: Check NEDC binary
    if not validate_nedc_binary():
        print("\nTEST INCOMPLETE: NEDC binary not available")
        print("Conversion works, but cannot test full scoring pipeline")
        print("This is expected if NEDC binaries are not installed")
        return 0

    # Step 4: Test full pipeline
    print("\n" + "=" * 60)
    print("TESTING: Full pipeline execution")
    print("=" * 60)

    cmd = [
        sys.executable,
        "evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py",
        "--checkpoint",
        str(test_checkpoint),
        "--outdir",
        str(test_dir),
        "--force",
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("FAILED: Pipeline execution error")
        print(result.stderr)
        return 1

    print(result.stdout)

    # Check for results
    results_dir = test_dir / "results"
    if results_dir.exists():
        print("PASSED: Results directory created")
        result_files = list(results_dir.glob("*"))
        print(f"Found {len(result_files)} result files")
    else:
        print("WARNING: Results directory not created (NEDC may not have run)")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print(f"Ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    return 0


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Test NEDC pipeline with synthetic data")
    parser.add_argument(
        "--keep-output", action="store_true", help="Keep test output directory after completion"
    )

    args = parser.parse_args()

    ret = run_full_test()

    if not args.keep_output and ret == 0:
        # Clean up test output
        test_dir = Path("evaluation/nedc_eeg_eval/nedc_scoring/test_output")
        if test_dir.exists():
            import shutil

            shutil.rmtree(test_dir)
            print("\nTest output cleaned up")

    return ret


if __name__ == "__main__":
    exit(main())
