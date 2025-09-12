#!/usr/bin/env python3
"""
Orchestrate the complete NEDC evaluation pipeline for SeizureTransformer.
Converts predictions to NEDC format and runs official NEDC scorer.
"""

import argparse
import subprocess
import sys
from pathlib import Path
import os
import json
from datetime import datetime


def setup_nedc_environment():
    """
    Set up NEDC environment variables.
    
    Returns:
        dict: Environment variables for NEDC
    """
    # Get the base directory of this script
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent
    
    # NEDC installation path
    nedc_root = repo_root / "evaluation" / "nedc_eeg_eval" / "v6.0.0"
    
    if not nedc_root.exists():
        raise FileNotFoundError(f"NEDC not found at {nedc_root}")
    
    # Set up environment
    env = os.environ.copy()
    env['NEDC_NFC'] = str(nedc_root)
    env['PATH'] = f"{nedc_root}/bin:{env.get('PATH', '')}"
    env['PYTHONPATH'] = f"{nedc_root}/lib:{env.get('PYTHONPATH', '')}"
    
    return env


def run_conversion(checkpoint_file, output_dir, force=False):
    """
    Convert checkpoint.pkl to NEDC CSV_bi format.
    
    Args:
        checkpoint_file: Path to checkpoint.pkl
        output_dir: Output directory for NEDC files
        force: Overwrite existing output
        
    Returns:
        int: Return code (0 for success)
    """
    print("=" * 70)
    print("STEP 1: Converting SeizureTransformer predictions to NEDC format")
    print("=" * 70)
    
    output_dir = Path(output_dir)
    
    # Check if output already exists
    if output_dir.exists() and not force:
        hyp_dir = output_dir / "hyp"
        ref_dir = output_dir / "ref"
        lists_dir = output_dir / "lists"
        
        if hyp_dir.exists() and ref_dir.exists() and lists_dir.exists():
            print(f"Output already exists at {output_dir}")
            print("Use --force to overwrite")
            return 0
    
    # Run conversion script
    cmd = [
        sys.executable,
        "evaluation/nedc_scoring/convert_predictions.py",
        "--checkpoint", str(checkpoint_file),
        "--outdir", str(output_dir)
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error converting predictions:")
        print(result.stderr)
        return result.returncode
    
    print(result.stdout)
    return 0


def run_nedc_scorer(output_dir):
    """
    Run NEDC official scorer on converted files.
    
    Args:
        output_dir: Directory containing NEDC files
        scoring_method: Scoring method (TAES, OVLP, EPOCH, IRA)
        
    Returns:
        int: Return code (0 for success)
    """
    print("\n" + "=" * 70)
    print("STEP 2: Running NEDC official scorer")
    print("=" * 70)
    
    output_dir = Path(output_dir)
    
    # Check that conversion output exists
    ref_list = output_dir / "lists" / "ref.list"
    hyp_list = output_dir / "lists" / "hyp.list"
    
    if not ref_list.exists() or not hyp_list.exists():
        print(f"Error: List files not found. Run conversion first.")
        return 1
    
    # Set up NEDC environment
    env = setup_nedc_environment()
    
    # Create results directory
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Build NEDC command
    nedc_binary = Path(env['NEDC_NFC']) / "bin" / "nedc_eeg_eval"
    
    if not nedc_binary.exists():
        print(f"Error: NEDC binary not found at {nedc_binary}")
        return 1
    
    cmd = [
        str(nedc_binary),
        str(ref_list),
        str(hyp_list),
        "-o", str(results_dir),
        "-s", scoring_method
    ]
    
    print(f"Running: {' '.join(cmd)}")
    print(f"Results will be saved to: {results_dir}")
    
    # Run NEDC scorer
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error running NEDC scorer:")
        print(result.stderr)
        return result.returncode
    
    print(result.stdout)
    
    # Parse and display key metrics
    parse_nedc_output(results_dir)
    
    return 0


def parse_nedc_output(results_dir):
    """
    Parse and display key metrics from NEDC output.
    
    Args:
        results_dir: Directory containing NEDC results
        scoring_method: The scoring method used
    """
    print("\n" + "=" * 70)
    print("KEY METRICS")
    print("=" * 70)
    
    # Known summary files from NEDC
    preferred = [
        "summary_taes.txt",
        "summary_ovlp.txt",
        "summary_epoch.txt",
        "summary.txt",
    ]

    for name in preferred:
        sf = results_dir / name
        if sf.exists():
            print(f"\nReading: {sf.name}")
            try:
                with open(sf, 'r') as f:
                    content = f.read()
                    print(content[:800])  # show first 800 chars for quick view
            except Exception as e:
                print(f"Could not read {sf}: {e}")
    
    print(f"\nFull results saved to: {results_dir}")


def run_full_pipeline(checkpoint_file, output_dir, force=False):
    """
    Run the complete NEDC evaluation pipeline.
    
    Args:
        checkpoint_file: Path to checkpoint.pkl
        output_dir: Output directory
        scoring_method: NEDC scoring method
        force: Overwrite existing output
        
    Returns:
        int: Return code (0 for success)
    """
    print("\n" + "=" * 70)
    print("NEDC EVALUATION PIPELINE FOR SEIZURETRANSFORMER")
    print("=" * 70)
    print(f"Checkpoint: {checkpoint_file}")
    print(f"Output: {output_dir}")
    
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Convert predictions
    ret = run_conversion(checkpoint_file, output_dir, force)
    if ret != 0:
        print("Conversion failed")
        return ret
    
    # Step 2: Run NEDC scorer
    ret = run_nedc_scorer(output_dir)
    if ret != 0:
        print("NEDC scoring failed")
        return ret
    
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print(f"Ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Run NEDC evaluation pipeline for SeizureTransformer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full pipeline with default settings
  python evaluation/nedc_scoring/run_nedc.py
  
  # Use specific checkpoint and output
  python evaluation/nedc_scoring/run_nedc.py \\
    --checkpoint evaluation/tusz/checkpoint.pkl \\
    --outdir evaluation/nedc_scoring/output
  
  # Run with different scoring method
  python evaluation/nedc_scoring/run_nedc.py --method OVLP
  
  # Force overwrite existing output
  python evaluation/nedc_scoring/run_nedc.py --force
        """
    )
    
    parser.add_argument(
        "--checkpoint",
        type=str,
        default="evaluation/tusz/checkpoint.pkl",
        help="Path to checkpoint.pkl file"
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default="evaluation/nedc_scoring/output",
        help="Output directory for NEDC files"
    )
    # NEDC runs all methods; no method flag needed
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite existing output"
    )
    parser.add_argument(
        "--convert-only",
        action="store_true",
        help="Only run conversion, skip NEDC scoring"
    )
    parser.add_argument(
        "--score-only",
        action="store_true",
        help="Only run NEDC scoring (assumes conversion done)"
    )
    
    args = parser.parse_args()
    
    # Validate checkpoint exists
    checkpoint_file = Path(args.checkpoint)
    if not checkpoint_file.exists() and not args.score_only:
        print(f"Error: Checkpoint not found: {checkpoint_file}")
        return 1
    
    # Run appropriate pipeline components
    if args.convert_only:
        return run_conversion(checkpoint_file, args.outdir, args.force)
    elif args.score_only:
        return run_nedc_scorer(args.outdir)
    else:
        return run_full_pipeline(
            checkpoint_file,
            args.outdir,
            args.force,
        )


if __name__ == "__main__":
    exit(main())
