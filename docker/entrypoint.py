#!/usr/bin/env python3
"""
Container entrypoint that routes to the correct pipeline without touching
upstream Wu's code. Modes:

- eval     Run TUSZ evaluation pipeline (recommended)
- nedc     Run NEDC scoring on saved predictions
- convert  Convert predictions (checkpoint.pkl) to NEDC CSV_bi
- wu       Run Wu's original CLI (strict channel name validation)
"""

import os
import sys
import subprocess
from pathlib import Path


def print_help() -> None:
    print("SeizureTransformer Docker Container")
    print("=" * 50)
    print("Usage modes:")
    print("  eval     - Run TUSZ evaluation pipeline (recommended)")
    print("  nedc     - Run NEDC scoring on predictions")
    print("  convert  - Convert predictions to NEDC format")
    print("  wu       - Wu original CLI (fails on TUSZ/Siena)")
    print()
    print("Examples:")
    print("  docker run --rm -v $PWD/data:/data image eval --help")
    print("  docker run --rm -v $PWD/experiments:/experiments image nedc --help")


def main() -> int:
    if len(sys.argv) < 2:
        print_help()
        return 0

    mode = sys.argv[1]
    args = sys.argv[2:]

    if mode == "eval":
        cmd = [
            sys.executable,
            "/app/evaluation/tusz/run_tusz_eval.py",
        ] + args
    elif mode == "nedc":
        cmd = [
            sys.executable,
            "/app/evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py",
        ] + args
    elif mode == "convert":
        cmd = [
            sys.executable,
            "/app/evaluation/nedc_eeg_eval/nedc_scoring/convert_predictions.py",
        ] + args
    elif mode == "wu":
        print("WARNING: Wu CLI requires exact electrode names (Fp1, F3, etc)")
        print("         It will fail on TUSZ/Siena data due to naming.")
        cmd = [sys.executable, "-m", "wu_2025"] + args
    else:
        print(f"Unknown mode: {mode}")
        print_help()
        return 1

    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())

