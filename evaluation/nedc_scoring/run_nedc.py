#!/usr/bin/env python3
"""
Orchestrate the complete NEDC evaluation pipeline for SeizureTransformer.
Converts predictions to NEDC format and runs official NEDC scorer.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


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
    env["NEDC_NFC"] = str(nedc_root)
    env["PATH"] = f"{nedc_root}/bin:{env.get('PATH', '')}"
    env["PYTHONPATH"] = f"{nedc_root}/lib:{env.get('PYTHONPATH', '')}"

    return env


def run_conversion(
    checkpoint_file,
    output_dir,
    force=False,
    threshold: float | None = None,
    kernel: int | None = None,
    min_duration_sec: float | None = None,
    merge_gap_sec: float | None = None,
):
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
        "--checkpoint",
        str(checkpoint_file),
        "--outdir",
        str(output_dir),
    ]
    if threshold is not None:
        cmd += ["--threshold", str(threshold)]
    if kernel is not None:
        cmd += ["--kernel", str(kernel)]
    if min_duration_sec is not None:
        cmd += ["--min_duration_sec", str(min_duration_sec)]
    if merge_gap_sec is not None:
        cmd += ["--merge_gap_sec", str(merge_gap_sec)]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error converting predictions:")
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
        print("Error: List files not found. Run conversion first.")
        return 1

    # Set up NEDC environment
    env = setup_nedc_environment()

    # Create results directory
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # Build NEDC command
    nedc_binary = Path(env["NEDC_NFC"]) / "bin" / "nedc_eeg_eval"

    if not nedc_binary.exists():
        print(f"Error: NEDC binary not found at {nedc_binary}")
        return 1

    cmd = [str(nedc_binary), str(ref_list), str(hyp_list), "-o", str(results_dir)]

    print(f"Running: {' '.join(cmd)}")
    print(f"Results will be saved to: {results_dir}")

    # Run NEDC scorer
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error running NEDC scorer:")
        print(result.stderr)
        return result.returncode

    print(result.stdout)

    # Parse and display key metrics
    parse_nedc_output(results_dir)

    return 0


def extract_and_save_metrics(results_dir, metrics_file):
    """Extract machine-readable metrics from NEDC output and save to JSON."""
    metrics: dict[str, any] = {
        "timestamp": datetime.now().isoformat(),
        "taes": {},
        "ovlp": {},
        "epoch": {},
    }

    # Parse TAES metrics (most important)
    summary_file = results_dir / "summary.txt"
    if summary_file.exists():
        with open(summary_file) as f:
            content = f.read()

        # Extract TAES metrics with robust regex
        taes_sens_match = re.search(r"Sensitivity \(TPR, Recall\):\s+([\d.]+)%", content)
        taes_fa_match = re.search(r"Total False Alarm Rate:\s+([\d.]+)\s+per 24 hours", content)
        taes_f1_match = re.search(r"F1 Score:\s+([\d.]+)", content)

        if taes_sens_match:
            metrics["taes"]["sensitivity_percent"] = float(taes_sens_match.group(1))
        if taes_fa_match:
            metrics["taes"]["fa_per_24h"] = float(taes_fa_match.group(1))
        if taes_f1_match:
            metrics["taes"]["f1_score"] = float(taes_f1_match.group(1))

    # Clinical assessment
    fa_rate = metrics["taes"].get("fa_per_24h", float("inf"))
    sensitivity = metrics["taes"].get("sensitivity_percent", 0)

    metrics["clinical_assessment"] = {
        "clinically_viable": fa_rate <= 10,
        "sensitivity_acceptable": sensitivity >= 50,
        "deployment_ready": fa_rate <= 10 and sensitivity >= 50,
    }

    # Save metrics
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=2)

    return metrics


def parse_nedc_output(results_dir):
    """
    Parse and display key metrics from NEDC output.

    Args:
        results_dir: Directory containing NEDC results
    """
    print("\n" + "=" * 70)
    print("KEY METRICS")
    print("=" * 70)

    # Extract metrics first
    metrics_file = results_dir / "metrics.json"
    metrics = extract_and_save_metrics(results_dir, metrics_file)

    # Display key TAES metrics
    if metrics["taes"]:
        print("\n🎯 TAES Results:")
        if "sensitivity_percent" in metrics["taes"]:
            print(f"   Sensitivity: {metrics['taes']['sensitivity_percent']:.2f}%")
        if "fa_per_24h" in metrics["taes"]:
            print(f"   False Alarms/24h: {metrics['taes']['fa_per_24h']:.2f}")
        if "f1_score" in metrics["taes"]:
            print(f"   F1 Score: {metrics['taes']['f1_score']:.3f}")

    # Clinical assessment
    assessment = metrics["clinical_assessment"]
    viable = "✅" if assessment["clinically_viable"] else "❌"
    print(f"\n🏥 Clinical Viability: {viable}")
    print(f"   FA/24h ≤ 10: {assessment['clinically_viable']}")
    print(f"   Sensitivity ≥ 50%: {assessment['sensitivity_acceptable']}")
    print(f"   Deployment Ready: {assessment['deployment_ready']}")

    print(f"\n📊 Machine-readable metrics: {metrics_file}")
    print(f"📁 Full results saved to: {results_dir}")


def run_full_pipeline(
    checkpoint_file,
    output_dir,
    force=False,
    threshold: float | None = None,
    kernel: int | None = None,
    min_duration_sec: float | None = None,
    merge_gap_sec: float | None = None,
):
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
    ret = run_conversion(
        checkpoint_file,
        output_dir,
        force,
        threshold=threshold,
        kernel=kernel,
        min_duration_sec=min_duration_sec,
        merge_gap_sec=merge_gap_sec,
    )
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
  # Run full pipeline with explicit paths
  python evaluation/nedc_scoring/run_nedc.py \
    --checkpoint experiments/eval/baseline/checkpoint.pkl \
    --outdir experiments/eval/baseline/nedc_results

  # Force overwrite existing output
  python evaluation/nedc_scoring/run_nedc.py --force ...
        """,
    )

    parser.add_argument(
        "--checkpoint",
        type=str,
        default="experiments/eval/baseline/checkpoint.pkl",
        help="Path to checkpoint.pkl file",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default="evaluation/nedc_scoring/output",
        help="Output directory for NEDC files",
    )
    parser.add_argument("--force", action="store_true", help="Force overwrite existing output")
    # Conversion tuning parameters
    parser.add_argument("--threshold", type=float, default=None, help="Probability threshold")
    parser.add_argument(
        "--kernel", type=int, default=None, help="Morphological kernel size (samples)"
    )
    parser.add_argument(
        "--min_duration_sec", type=float, default=None, help="Minimum event duration (s)"
    )
    parser.add_argument(
        "--merge_gap_sec",
        type=float,
        default=None,
        help="Merge events with gaps less than this (s)",
    )
    parser.add_argument(
        "--convert-only", action="store_true", help="Only run conversion, skip NEDC scoring"
    )
    parser.add_argument(
        "--score-only", action="store_true", help="Only run NEDC scoring (assumes conversion done)"
    )

    args = parser.parse_args()

    # Validate checkpoint exists
    checkpoint_file = Path(args.checkpoint)
    if not checkpoint_file.exists() and not args.score_only:
        print(f"Error: Checkpoint not found: {checkpoint_file}")
        return 1

    # Run appropriate pipeline components
    if args.convert_only:
        return run_conversion(
            checkpoint_file,
            args.outdir,
            args.force,
            threshold=args.threshold,
            kernel=args.kernel,
            min_duration_sec=args.min_duration_sec,
            merge_gap_sec=args.merge_gap_sec,
        )
    elif args.score_only:
        return run_nedc_scorer(args.outdir)
    else:
        return run_full_pipeline(
            checkpoint_file,
            args.outdir,
            args.force,
            threshold=args.threshold,
            kernel=args.kernel,
            min_duration_sec=args.min_duration_sec,
            merge_gap_sec=args.merge_gap_sec,
        )


if __name__ == "__main__":
    exit(main())
