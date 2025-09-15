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
    # FIX: nedc_scoring is in evaluation/nedc_eeg_eval/nedc_scoring
    # so parent is nedc_eeg_eval
    nedc_eeg_eval_dir = script_dir.parent

    # NEDC installation path
    nedc_root = nedc_eeg_eval_dir / "v6.0.0"

    if not nedc_root.exists():
        raise FileNotFoundError(f"NEDC not found at {nedc_root}")

    # Set up environment
    env = os.environ.copy()
    env["NEDC_NFC"] = str(nedc_root)
    env["PATH"] = f"{nedc_root}/bin:{env.get('PATH', '')}"
    # FIX: NEDC modules are directly in lib/ not lib/python/
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
        merge_gap_sec: DEPRECATED - must be None or 0. Non-zero values are blocked.

    Args:
        checkpoint_file: Path to checkpoint.pkl
        output_dir: Output directory for NEDC files
        force: Overwrite existing output

    Returns:
        int: Return code (0 for success)
    """
    # Phase 1 enforcement: Block non-zero merge_gap
    if merge_gap_sec not in (None, 0, 0.0):
        print(f"ERROR: merge_gap_sec={merge_gap_sec} is not allowed.")
        print("Event merging has been deprecated to ensure NEDC/Temple compliance.")
        print("Use merge_gap_sec=None or 0 for all evaluations.")
        print("See docs/technical/MERGE_GAP_POLICY.md for details.")
        return 1

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
    # Prefer module execution for predictable imports
    cmd = [
        sys.executable,
        "-m",
        "evaluation.nedc_eeg_eval.nedc_scoring.convert_predictions",
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
    # merge_gap_sec is deprecated and blocked above

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error converting predictions:")
        print(result.stderr)
        return result.returncode

    print(result.stdout)
    return 0


def run_nedc_scorer(
    output_dir,
    backend="nedc-binary",
    threshold=None,
    kernel=None,
    min_duration_sec=None,
    merge_gap_sec=None,
):
    """
    Run NEDC official scorer on converted files.

    Args:
        output_dir: Directory containing NEDC files
        backend: Scoring backend ("nedc-binary" or "native-overlap")
        threshold: Probability threshold used (for metadata)
        kernel: Morphological kernel size used (for metadata)
        min_duration_sec: Minimum duration used (for metadata)
        merge_gap_sec: Merge gap used (for metadata)

    Returns:
        int: Return code (0 for success)
    """
    print("\n" + "=" * 70)
    print(f"STEP 2: Running NEDC scorer (backend: {backend})")
    print("=" * 70)

    output_dir = Path(output_dir)

    # Check that conversion output exists
    ref_list = output_dir / "lists" / "ref.list"
    hyp_list = output_dir / "lists" / "hyp.list"

    if not ref_list.exists() or not hyp_list.exists():
        print("Error: List files not found. Run conversion first.")
        return 1

    # Create results directory
    results_dir = output_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    if backend == "nedc-binary":
        # Set up NEDC environment
        env = setup_nedc_environment()

        # Build NEDC command
        nedc_binary = Path(env["NEDC_NFC"]) / "bin" / "nedc_eeg_eval"

        if not nedc_binary.exists():
            print(f"Error: NEDC binary not found at {nedc_binary}")
            return 1

        # Use current Python interpreter to run Temple's Python entrypoint
        cmd = [sys.executable, str(nedc_binary), str(ref_list), str(hyp_list), "-o", str(results_dir)]

        print(f"Running: {' '.join(cmd)}")
        print(f"Results will be saved to: {results_dir}")

        # Run NEDC scorer
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)

        if result.returncode != 0:
            print("Error running NEDC scorer:")
            # Surface both stderr and stdout for easier debugging
            if result.stderr:
                print("[stderr]")
                print(result.stderr)
            if result.stdout:
                print("[stdout]")
                print(result.stdout)
            return result.returncode

        print(result.stdout)
    elif backend in ("native-overlap", "native-taes"):
        # Native Python OVERLAP implementation
        base_path = Path(__file__).resolve()
        repo_root = base_path.parents[3]
        eval_dir = base_path.parents[2]
        for p in (str(repo_root), str(eval_dir)):
            if p not in sys.path:
                sys.path.insert(0, p)
        from seizure_evaluation.ovlp.overlap_scorer import OverlapScorer

        print("Running native Python OVERLAP scorer...")

        # Initialize OVERLAP scorer (matches Temple NEDC OVERLAP section)
        scorer = OverlapScorer()

        # Process each file pair
        total_metrics = {
            "hits": 0,
            "misses": 0,
            "false_alarms": 0,  # SEIZ-only FAs
            "bckg_false_alarms": 0,  # BCKG FAs (for Temple total)
            "total_duration": 0.0,
        }

        # Read list files to get CSV_bi paths
        with open(ref_list) as f:
            ref_files = [Path(line.strip()) for line in f if line.strip()]
        with open(hyp_list) as f:
            hyp_files = [Path(line.strip()) for line in f if line.strip()]

        # Score each file pair
        for ref_csv, hyp_csv in zip(ref_files, hyp_files, strict=False):
            if ref_csv.stem == hyp_csv.stem:
                metrics = scorer.score_from_files(ref_csv, hyp_csv)
                total_metrics["hits"] += metrics.hits
                total_metrics["misses"] += metrics.misses
                total_metrics["false_alarms"] += metrics.false_alarms
                # include background FAs to match Temple's Total False Alarm Rate
                total_metrics["bckg_false_alarms"] += getattr(metrics, "bckg_false_alarms", 0)
                total_metrics["total_duration"] += metrics.total_duration_sec

        # Write summary file for compatibility
        summary_file = results_dir / "summary.txt"
        with open(summary_file, "w") as f:
            # Calculate aggregate metrics (map OVERLAP to TP/FP/FN for compatibility)
            tp = total_metrics["hits"]  # Hits are true positives
            fp = total_metrics["false_alarms"]  # False alarms are false positives
            fn = total_metrics["misses"]  # Misses are false negatives
            duration = total_metrics["total_duration"]

            sensitivity = 100.0 * tp / (tp + fn) if (tp + fn) > 0 else 0.0
            precision = 100.0 * tp / (tp + fp) if (tp + fp) > 0 else 0.0
            f1 = (
                2 * precision * sensitivity / (precision + sensitivity)
                if (precision + sensitivity) > 0
                else 0.0
            )

            f.write("=== NATIVE OVERLAP SCORING RESULTS ===\n\n")
            f.write(f"Sensitivity (TPR, Recall): {sensitivity:.2f}%\n")
            # Temple reports TOTAL False Alarms across labels in OVERLAP summary
            fa_per_24h_total = (
                (total_metrics["false_alarms"] + total_metrics["bckg_false_alarms"])
                * 86400.0
                / duration
                if duration > 0
                else 0.0
            )
            f.write(f"Total False Alarm Rate: {fa_per_24h_total:.2f} per 24 hours\n")
            f.write(f"F1 Score: {f1 / 100:.3f}\n")

        print(f"Native OVERLAP scoring complete. Results in {summary_file}")
    else:
        print(f"Error: Unknown backend '{backend}'")
        print("Valid backends: nedc-binary, native-overlap, native-taes (alias)")
        return 1

    # merge_gap_sec is deprecated and blocked, so no disclaimer needed

    # Parse and display key metrics with operating point params
    parse_nedc_output(
        results_dir,
        backend=backend,
        threshold=threshold,
        kernel=kernel,
        min_duration_sec=min_duration_sec,
        merge_gap_sec=merge_gap_sec,
    )

    return 0


def extract_and_save_metrics(results_dir, metrics_file, backend="nedc-binary", fa_reporting: str = "seiz"):
    """Extract machine-readable metrics from NEDC output and save to JSON.

    Guarantees a stable schema with keys: "overlap" and "taes" (duplicate of overlap
    for backward-compat), and always writes metrics_file creating its parent dir.
    """
    import platform
    from typing import Any

    # Get git commit SHA if available
    try:
        git_sha = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=False
        ).stdout.strip()[:8]
    except:
        git_sha = "unknown"

    # Get Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    metrics: dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "provenance": {
            "git_commit": git_sha,
            "python_version": py_version,
            "platform": platform.platform(),
            "os": platform.system(),
            "backend": backend,
            "nedc_version": "v6.0.0",
        },
        "taes": {},  # kept for backward-compat; will mirror selected reporting
        "overlap": {},
    }

    # Parse metrics from correct section
    results_dir = Path(results_dir)
    summary_file = results_dir / "summary.txt"
    if summary_file.exists():
        with open(summary_file) as f:
            content = f.read()

        # Handle both Temple binary and native outputs
        if backend in ("native-overlap", "native-taes"):
            # Native outputs simpler format
            sens_match = re.search(r"Sensitivity \(TPR, Recall\):\s+([\d.]+)%", content)
            # Native summary prints Total FA; we will store it as total and also
            # prefer SEIZ-only if we compute it from lists below
            fa_match = re.search(r"Total False Alarm Rate:\s+([\d.]+)\s+per 24 hours", content)
            f1_match = re.search(r"F1 Score:\s+([\d.]+)", content)

            metrics["overlap"] = {}
            if sens_match:
                metrics["overlap"]["sensitivity_percent"] = float(sens_match.group(1))
            if fa_match:
                metrics["overlap"]["fa_per_24h_total"] = float(fa_match.group(1))
            if f1_match:
                metrics["overlap"]["f1_score"] = float(f1_match.group(1))
        else:
            # Extract OVERLAP metrics from Temple binary output
            overlap_section_match = re.search(
                r"NEDC OVERLAP SCORING SUMMARY.*?(?=NEDC|$)", content, re.DOTALL
            )

            if overlap_section_match:
                overlap_content = overlap_section_match.group(0)

                # Extract metrics from OVERLAP section
                sens_match = re.search(r"Sensitivity \(TPR, Recall\):\s+([\d.]+)%", overlap_content)
                fa_total_match = re.search(
                    r"Total False Alarm Rate:\s+([\d.]+)\s+per 24 hours", overlap_content
                )
                f1_match = re.search(r"F1 Score(?: \(F Ratio\))?:\s+([\d.]+)", overlap_content)

                # Store as "overlap" metrics (more accurate naming)
                metrics["overlap"] = {}
                if sens_match:
                    metrics["overlap"]["sensitivity_percent"] = float(sens_match.group(1))
                if fa_total_match:
                    metrics["overlap"]["fa_per_24h_total"] = float(fa_total_match.group(1))
                if f1_match:
                    metrics["overlap"]["f1_score"] = float(f1_match.group(1))

        # Compute SEIZ-only OVERLAP FA/24h by scoring lists via native scorer
        try:
            lists_dir = results_dir.parent / "lists"
            ref_list = lists_dir / "ref.list"
            hyp_list = lists_dir / "hyp.list"
            if ref_list.exists() and hyp_list.exists():
                from seizure_evaluation.ovlp.overlap_scorer import OverlapScorer

                scorer = OverlapScorer()
                hits = misses = fa = 0
                total_dur = 0.0
                refs = [Path(p.strip()) for p in ref_list.read_text().splitlines() if p.strip()]
                hyps = [Path(p.strip()) for p in hyp_list.read_text().splitlines() if p.strip()]
                for r, h in zip(refs, hyps, strict=False):
                    m = scorer.score_from_files(r, h)
                    hits += m.hits
                    misses += m.misses
                    fa += m.false_alarms  # SEIZ-only false alarms
                    total_dur += m.total_duration_sec
                if total_dur > 0:
                    fa24_seiz = fa * 86400.0 / total_dur
                    sens_seiz = 100.0 * hits / (hits + misses) if (hits + misses) > 0 else 0.0
                    metrics.setdefault("overlap", {})
                    metrics["overlap"]["fa_per_24h_seiz"] = round(fa24_seiz, 4)
                    metrics["overlap"]["sensitivity_percent_seiz"] = round(sens_seiz, 4)
        except Exception:
            pass

        # Select primary FA to expose as fa_per_24h based on reporting policy
        fa_primary = None
        if fa_reporting == "seiz":
            fa_primary = metrics.get("overlap", {}).get("fa_per_24h_seiz")
        elif fa_reporting == "total":
            fa_primary = metrics.get("overlap", {}).get("fa_per_24h_total")
        elif fa_reporting == "both":
            # prefer SEIZ for primary display, keep total as separate key
            fa_primary = metrics.get("overlap", {}).get("fa_per_24h_seiz") or metrics.get("overlap", {}).get("fa_per_24h_total")
        if fa_primary is not None:
            metrics["overlap"]["fa_per_24h"] = fa_primary

        # Backward-compat: mirror overlap metrics into "taes" key (historical quirk)
        if "overlap" in metrics:
            metrics["taes"] = metrics["overlap"].copy()

    # Clinical assessment
    fa_rate = metrics["taes"].get("fa_per_24h", float("inf"))
    sensitivity = metrics["taes"].get("sensitivity_percent", 0)

    metrics["clinical_assessment"] = {
        "clinically_viable": fa_rate <= 10,
        "sensitivity_acceptable": sensitivity >= 50,
        "deployment_ready": fa_rate <= 10 and sensitivity >= 50,
    }

    # Save metrics
    metrics_file = Path(metrics_file)
    metrics_file.parent.mkdir(parents=True, exist_ok=True)
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=2)

    return metrics


def parse_nedc_output(
    results_dir,
    backend="nedc-binary",
    threshold=None,
    kernel=None,
    min_duration_sec=None,
    merge_gap_sec=None,
    fa_reporting: str = "seiz",
):
    """
    Parse and display key metrics from NEDC output.

    Args:
        results_dir: Directory containing NEDC results
        threshold: Probability threshold used
        kernel: Morphological kernel size used
        min_duration_sec: Minimum duration used
        merge_gap_sec: Merge gap used
    """
    print("\n" + "=" * 70)
    print("KEY METRICS")
    print("=" * 70)

    # Extract metrics first
    metrics_file = results_dir / "metrics.json"
    metrics = extract_and_save_metrics(results_dir, metrics_file, backend, fa_reporting=fa_reporting)

    # Add operating point params to metrics
    if any([threshold, kernel, min_duration_sec, merge_gap_sec]):
        metrics["operating_point"] = {
            "threshold": threshold or 0.8,
            "kernel": kernel or 5,
            "min_duration_sec": min_duration_sec or 2.0,
            "merge_gap_sec": 0.0,  # Always 0 now that non-zero is blocked
        }
        # Re-save with operating point
        with open(metrics_file, "w") as f:
            json.dump(metrics, f, indent=2)

        # Also save a small manifest for quick inspection
        try:
            op_manifest = results_dir / "operating_point.json"
            with open(op_manifest, "w") as f:
                json.dump(metrics["operating_point"], f, indent=2)
        except Exception:
            pass

    # Display key OVERLAP metrics (stored under "overlap" and duplicated to "taes")
    if metrics["taes"]:
        print("\n🎯 OVERLAP Results:")
        if "sensitivity_percent" in metrics["taes"]:
            print(f"   Sensitivity (SEIZ): {metrics['taes']['sensitivity_percent']:.2f}%")
        # Primary FA per reporting policy
        if "fa_per_24h" in metrics["taes"]:
            label = "False Alarms/24h (SEIZ)" if fa_reporting in ("seiz","both") else "False Alarms/24h (TOTAL)"
            print(f"   {label}: {metrics['taes']['fa_per_24h']:.2f}")
        # Optionally show both if available
        if fa_reporting == "both":
            if "fa_per_24h_total" in metrics["taes"]:
                print(f"   False Alarms/24h (TOTAL): {metrics['taes']['fa_per_24h_total']:.2f}")
            if "fa_per_24h_seiz" in metrics["taes"]:
                print(f"   False Alarms/24h (SEIZ): {metrics['taes']['fa_per_24h_seiz']:.2f}")
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
    backend="nedc-binary",
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

    # Step 2: Run NEDC scorer with operating point params for metadata
    ret = run_nedc_scorer(
        output_dir,
        backend=backend,
        threshold=threshold,
        kernel=kernel,
        min_duration_sec=min_duration_sec,
        merge_gap_sec=merge_gap_sec,
    )
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
  python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py \
    --checkpoint experiments/eval/baseline/checkpoint.pkl \
    --outdir experiments/eval/baseline/nedc_results

  # Force overwrite existing output
  python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py --force ...
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
        default="experiments/dev/baseline/nedc_results",
        help="Output directory for NEDC files (under experiments/**)",
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
        help="DEPRECATED: Merge events with gaps less than this (s). WARNING: This violates NEDC/Temple evaluation standards and artificially reduces FA by 4X. Use None for academic compliance.",
    )
    parser.add_argument(
        "--convert-only", action="store_true", help="Only run conversion, skip NEDC scoring"
    )
    parser.add_argument(
        "--score-only", action="store_true", help="Only run NEDC scoring (assumes conversion done)"
    )
    parser.add_argument(
        "--backend",
        type=str,
        default="nedc-binary",
        choices=["nedc-binary", "native-overlap", "native-taes"],
        help="Scoring backend to use (default: nedc-binary). 'native-taes' is an alias of 'native-overlap' for compatibility.",
    )
    parser.add_argument(
        "--fa_reporting",
        type=str,
        default="seiz",
        choices=["seiz", "total", "both"],
        help="Which FA/24h to report as primary: SEIZ-only, TOTAL, or BOTH (display both; primary=SEIZ).",
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
        return run_nedc_scorer(args.outdir, backend=args.backend, fa_reporting=args.fa_reporting)
    else:
        return run_full_pipeline(
            checkpoint_file,
            args.outdir,
            args.force,
            threshold=args.threshold,
            kernel=args.kernel,
            min_duration_sec=args.min_duration_sec,
            merge_gap_sec=args.merge_gap_sec,
            backend=args.backend,
        )


if __name__ == "__main__":
    exit(main())
