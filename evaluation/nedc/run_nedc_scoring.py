#!/usr/bin/env python3
"""
Wrapper for NEDC official scoring tools.
Converts SeizureTransformer output to NEDC format and runs scoring.
"""

import sys
import subprocess
from pathlib import Path

# Point to NEDC tools in reference_repos
NEDC_PATH = Path(__file__).parent.parent.parent / "reference_repos/nedc/nedc_eeg_eval/v6.0.0"
NEDC_SCRIPT = NEDC_PATH / "src/nedc_eeg_eval/nedc_eeg_eval.py"

def convert_to_nedc_format(predictions, output_dir):
    """Convert model predictions to NEDC hypothesis format."""
    # NEDC expects .hyp files with format:
    # start_time end_time label confidence
    pass

def run_nedc_scoring(ref_file, hyp_file):
    """Run NEDC scoring tool."""
    cmd = [
        "python", str(NEDC_SCRIPT),
        "-r", ref_file,  # Reference annotations  
        "-h", hyp_file,  # Hypothesis predictions
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def parse_nedc_output(output):
    """Parse NEDC scoring output for key metrics."""
    # Extract TAES metrics, FA/24h, sensitivity, etc.
    pass

if __name__ == "__main__":
    print("NEDC scoring wrapper - to be implemented after TUSZ eval completes")
    print(f"NEDC tools located at: {NEDC_PATH}")
    print(f"This will convert SeizureTransformer output to NEDC format and score")