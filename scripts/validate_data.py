#!/usr/bin/env python3
"""
Production Data Validator for SeizureTransformer Pipeline
Validates EDF files for compatibility with evaluation pipeline
Date: September 2025
"""

import argparse
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pyedflib
from tqdm import tqdm


class DataValidator:
    """Validates EDF data for SeizureTransformer compatibility."""

    # Expected channel configurations
    WU_EXPECTED_CHANNELS = [
        "Fp1",
        "F3",
        "C3",
        "P3",
        "O1",
        "F7",
        "T3",
        "T5",
        "Fz",
        "Cz",
        "Pz",
        "Fp2",
        "F4",
        "C4",
        "P4",
        "O2",
        "F8",
        "T4",
        "T6",
    ]

    TUSZ_CHANNEL_PATTERNS = [
        "FP1",
        "F3",
        "C3",
        "P3",
        "O1",
        "F7",
        "T3",
        "T5",
        "FZ",
        "CZ",
        "PZ",
        "FP2",
        "F4",
        "C4",
        "P4",
        "O2",
        "F8",
        "T4",
        "T6",
    ]

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.validation_results: dict[str, Any] = {
            "total_files": 0,
            "valid_files": 0,
            "invalid_files": 0,
            "errors": [],
            "warnings": [],
        }

    def validate_file(self, edf_path: Path) -> tuple[bool, str]:
        """
        Validate a single EDF file.

        Returns:
            (is_valid, message) tuple
        """
        try:
            with pyedflib.EdfReader(str(edf_path)) as f:
                # Check basic properties
                n_channels = f.signals_in_file
                channel_names = f.getSignalLabels()
                sample_rates = [f.getSampleFrequency(i) for i in range(n_channels)]
                duration = f.file_duration

                # Validation checks
                issues = []

                # 1. Check channel count
                valid_channels = self._extract_valid_channels(channel_names)
                if len(valid_channels) != 19:
                    issues.append(f"Expected 19 valid channels, found {len(valid_channels)}")

                # 2. Check channel order matches expected pattern
                if not self._check_channel_order(valid_channels):
                    issues.append("Channel order doesn't match expected pattern")

                # 3. Check sample rates
                unique_rates = set(sample_rates)
                if len(unique_rates) > 2:  # Allow for some variation
                    issues.append(f"Multiple sample rates detected: {unique_rates}")

                # 4. Check duration
                if duration < 10:  # Less than 10 seconds
                    issues.append(f"Recording too short: {duration:.1f} seconds")

                # 5. Check for data corruption
                for i in range(min(n_channels, 5)):  # Check first 5 channels
                    try:
                        signal = f.readSignal(i, 0, 100)  # Read first 100 samples
                        if np.all(signal == 0) or np.any(np.isnan(signal)):
                            issues.append(f"Channel {i} appears corrupted")
                    except:
                        issues.append(f"Cannot read channel {i}")

                if issues:
                    return False, "; ".join(issues)
                return True, "Valid"

        except Exception as e:
            return False, f"Error reading file: {str(e)}"

    def _extract_valid_channels(self, channel_names: list[str]) -> list[str]:
        """Extract the 19 valid EEG channels from all channels."""
        valid = []
        for ch in channel_names:
            # Remove prefixes and suffixes
            cleaned = ch.upper().replace("EEG ", "").replace("-REF", "").replace("-LE", "")
            # Check if it matches expected patterns
            for pattern in self.TUSZ_CHANNEL_PATTERNS:
                if pattern in cleaned or cleaned == pattern:
                    valid.append(cleaned)
                    break
        return valid[:19]  # Take first 19 valid channels

    def _check_channel_order(self, channels: list[str]) -> bool:
        """Check if channel order matches expected pattern."""
        if len(channels) != 19:
            return False

        # Check if channels match TUSZ pattern (case-insensitive)
        for i, (actual, expected) in enumerate(
            zip(channels, self.TUSZ_CHANNEL_PATTERNS, strict=False)
        ):
            actual_clean = actual.upper().replace("EEG ", "").replace("-REF", "").replace("-LE", "")
            if actual_clean != expected:
                if self.verbose:
                    print(f"  Channel mismatch at position {i}: {actual_clean} != {expected}")
                return False
        return True

    def validate_directory(self, data_dir: Path) -> dict[str, Any]:
        """Validate all EDF files in a directory."""
        edf_files = list(data_dir.glob("**/*.edf"))

        if not edf_files:
            print(f"No EDF files found in {data_dir}")
            return self.validation_results

        print(f"Validating {len(edf_files)} EDF files...")

        for edf_path in tqdm(edf_files, desc="Validating"):
            self.validation_results["total_files"] += 1
            is_valid, message = self.validate_file(edf_path)

            if is_valid:
                self.validation_results["valid_files"] += 1
            else:
                self.validation_results["invalid_files"] += 1
                self.validation_results["errors"].append(
                    {"file": str(edf_path.relative_to(data_dir)), "error": message}
                )

        return self.validation_results

    def print_report(self):
        """Print validation report."""
        print("\n" + "=" * 60)
        print("VALIDATION REPORT")
        print("=" * 60)

        total = self.validation_results["total_files"]
        valid = self.validation_results["valid_files"]
        invalid = self.validation_results["invalid_files"]

        print(f"Total files:   {total}")
        print(f"Valid files:   {valid} ({valid / total * 100:.1f}%)")
        print(f"Invalid files: {invalid} ({invalid / total * 100:.1f}%)")

        if self.validation_results["errors"]:
            print("\nERRORS (first 10):")
            for error in self.validation_results["errors"][:10]:
                print(f"  {error['file']}: {error['error']}")

        if self.validation_results["warnings"]:
            print("\nWARNINGS:")
            for warning in self.validation_results["warnings"]:
                print(f"  {warning}")

        print("\n" + "=" * 60)

        # Return exit code
        return 0 if invalid == 0 else 1


def main():
    """Main entry point for data validation."""
    parser = argparse.ArgumentParser(description="Validate EDF data for SeizureTransformer")
    parser.add_argument(
        "--data_dir", type=str, required=True, help="Directory containing EDF files"
    )
    parser.add_argument(
        "--check_channels", action="store_true", help="Validate channel names and order"
    )
    parser.add_argument(
        "--check_format", action="store_true", help="Check EDF format compatibility"
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        print(f"Error: {data_dir} does not exist")
        sys.exit(1)

    validator = DataValidator(verbose=args.verbose)
    validator.validate_directory(data_dir)
    exit_code = validator.print_report()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
