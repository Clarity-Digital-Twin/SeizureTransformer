#!/usr/bin/env python3
"""
Wrapper for NEDC official scoring tools.
Converts SeizureTransformer output to NEDC format and runs scoring.

Note: This is a thin wrapper around the in-repo NEDC v6.0.0 tools
located under `evaluation/nedc_eeg_eval/v6.0.0`.
"""

import os
import subprocess
from pathlib import Path

# Point to in-repo NEDC tools
NEDC_PATH = Path(__file__).parent.parent / "nedc_eeg_eval/v6.0.0"
NEDC_BIN = NEDC_PATH / "bin/nedc_eeg_eval"

def convert_to_nedc_format(predictions, output_dir):
    """Convert model predictions to NEDC hypothesis format."""
    # NEDC expects .hyp files with format:
    # start_time end_time label confidence
    pass

def run_nedc_scoring(ref_file, hyp_file, outdir: Path | None = None):
    """Run NEDC scoring tool."""
    cmd = [str(NEDC_BIN), ref_file, hyp_file]
    if outdir is not None:
        cmd.extend(["-o", str(outdir)])

    env = os.environ.copy()
    env.setdefault("NEDC_NFC", str(NEDC_PATH))
    env["PATH"] = f"{NEDC_PATH / 'bin'}:{env.get('PATH','')}"
    env["PYTHONPATH"] = f"{NEDC_PATH / 'lib'}:{env.get('PYTHONPATH','')}"

    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return result.stdout

def parse_nedc_output(output):
    """Parse NEDC scoring output for key metrics."""
    # Extract TAES metrics, FA/24h, sensitivity, etc.
    pass

if __name__ == "__main__":
    print("NEDC scoring wrapper - to be implemented after TUSZ eval completes")
    print(f"NEDC tools located at: {NEDC_PATH}")
    print("This will convert SeizureTransformer output to NEDC format and score")
