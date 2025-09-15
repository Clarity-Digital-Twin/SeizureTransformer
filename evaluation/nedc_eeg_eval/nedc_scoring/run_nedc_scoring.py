#!/usr/bin/env python3
"""
DEPRECATED: Use `evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py` instead.

This legacy stub is kept only to avoid breaking old references. It does not
implement conversion or scoring.
"""

import os
import subprocess
from pathlib import Path

# Point to in-repo NEDC tools
NEDC_PATH = Path(__file__).parent.parent / "nedc_eeg_eval/v6.0.0"
NEDC_BIN = NEDC_PATH / "bin/nedc_eeg_eval"


def convert_to_nedc_format(predictions, output_dir):
    raise NotImplementedError("Deprecated. Use evaluation/nedc_eeg_eval/nedc_scoring/convert_predictions.py")


def run_nedc_scoring(ref_file, hyp_file, outdir: Path | None = None):
    """Run NEDC scoring tool."""
    cmd = [str(NEDC_BIN), ref_file, hyp_file]
    if outdir is not None:
        cmd.extend(["-o", str(outdir)])

    env = os.environ.copy()
    env.setdefault("NEDC_NFC", str(NEDC_PATH))
    env["PATH"] = f"{NEDC_PATH / 'bin'}:{env.get('PATH', '')}"
    env["PYTHONPATH"] = f"{NEDC_PATH / 'lib'}:{env.get('PYTHONPATH', '')}"

    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return result.stdout


def parse_nedc_output(output):
    raise NotImplementedError(
        "Deprecated. Use evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py to parse summaries"
    )


if __name__ == "__main__":
    print("Deprecated. Use evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py")
