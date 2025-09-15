#!/usr/bin/env python3
"""
Convert SeizureTransformer checkpoint to NEDC CSV_bi format.
Creates both hypothesis and reference files.
"""

import argparse
import pickle
from pathlib import Path

# Use a single, stable import path to avoid mypy/no-redef issues and runtime fallbacks.
from evaluation.nedc_eeg_eval.nedc_scoring.post_processing import (
    apply_seizure_transformer_postprocessing,
)


def write_nedc_csv(events, file_path, file_id, duration_sec):
    """
    Write events to NEDC CSV_bi format.

    Args:
        events: List of (start_sec, end_sec) tuples
        file_path: Output CSV_bi file path
        file_id: Base name for the file (e.g., "aaaaaasf_s001_t000")
        duration_sec: Total duration in seconds
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", newline="\n") as f:
        # Write header
        f.write("# version = csv_v1.0.0\n")
        f.write(f"# bname = {file_id}\n")
        f.write(f"# duration = {duration_sec:.4f} secs\n")
        f.write("channel,start_time,stop_time,label,confidence\n")

        # Write events
        for start_sec, end_sec in events:
            # Format with 4 decimal places like NEDC
            f.write(f"TERM,{start_sec:.4f},{end_sec:.4f},seiz,1.0000\n")


def convert_checkpoint_to_nedc(
    checkpoint_file,
    output_dir,
    threshold: float = 0.8,
    morph_kernel_size: int = 5,
    min_duration_sec: float = 2.0,
    merge_gap_sec: float | None = None,
):
    """
    Convert checkpoint.pkl to NEDC CSV_bi format.

    Args:
        checkpoint_file: Path to checkpoint.pkl
        output_dir: Base output directory
    """
    print(f"Loading checkpoint from {checkpoint_file}...")
    with open(checkpoint_file, "rb") as f:
        checkpoint = pickle.load(f)

    # Handle both checkpoint formats (with/without "results" key)
    results = checkpoint.get("results", checkpoint)

    # Create output directories
    hyp_dir = Path(output_dir) / "hyp"
    ref_dir = Path(output_dir) / "ref"
    hyp_dir.mkdir(parents=True, exist_ok=True)
    ref_dir.mkdir(parents=True, exist_ok=True)

    # Track processed files for list generation
    processed_files = []

    print(f"Processing {len(results)} files...")
    for file_id, result in results.items():
        # Skip files with errors
        if result.get("error") is not None:
            print(f"  Skipping {file_id}: {result['error']}")
            continue

        predictions = result.get("predictions")
        seizure_events = result.get("seizure_events", [])

        if predictions is None:
            print(f"  Skipping {file_id}: No predictions")
            continue

        # Calculate duration in seconds
        duration_sec = len(predictions) / 256.0  # 256 Hz sampling

        # Process predictions to get hypothesis events
        hyp_events = apply_seizure_transformer_postprocessing(
            predictions,
            threshold=threshold,
            morph_kernel_size=morph_kernel_size,
            min_duration_sec=min_duration_sec,
            fs=256,
            merge_gap_sec=merge_gap_sec,
        )

        # Write hypothesis file
        hyp_file = hyp_dir / f"{file_id}.csv_bi"
        write_nedc_csv(hyp_events, hyp_file, file_id, duration_sec)

        # Write reference file (ground truth)
        ref_file = ref_dir / f"{file_id}.csv_bi"
        write_nedc_csv(seizure_events, ref_file, file_id, duration_sec)

        processed_files.append(file_id)

        # Progress indicator every 50 files
        if len(processed_files) % 50 == 0:
            print(f"  Processed {len(processed_files)} files...")

    print(f"\nConverted {len(processed_files)} files to NEDC format")
    print(f"Hypothesis files: {hyp_dir}")
    print(f"Reference files: {ref_dir}")

    # Generate list files
    create_list_files(output_dir, processed_files)

    # Write a simple params manifest beside lists/hyp/ref for reproducibility
    try:
        import json
        params = {
            "threshold": threshold,
            "kernel": morph_kernel_size,
            "min_duration_sec": min_duration_sec,
            "merge_gap_sec": merge_gap_sec or 0.0,
        }
        with open(Path(output_dir) / "params.json", "w") as f:
            json.dump(params, f, indent=2)

        # If a nonstandard merge_gap is used, drop a disclaimer file
        if merge_gap_sec not in (None, 0, 0.0):
            (Path(output_dir) / "NONSTANDARD_POSTPROCESSING.txt").write_text(
                "merge_gap_sec is enabled for this conversion. This merges nearby events in\n"
                "post-processing and is NOT part of the paper or NEDC/Temple evaluation.\n"
                "Use merge_gap_sec=None for academic compliance.\n"
            )
    except Exception:
        pass

    return processed_files


def create_list_files(output_dir, file_ids):
    """
    Create ref.list and hyp.list files for NEDC.

    Args:
        output_dir: Base output directory
        file_ids: List of processed file IDs
    """
    output_dir = Path(output_dir)
    lists_dir = output_dir / "lists"
    lists_dir.mkdir(parents=True, exist_ok=True)

    # Get absolute paths
    hyp_dir = output_dir.resolve() / "hyp"
    ref_dir = output_dir.resolve() / "ref"

    # Write hypothesis list
    hyp_list = lists_dir / "hyp.list"
    with open(hyp_list, "w", newline="\n") as f:
        for file_id in sorted(file_ids):
            f.write(f"{hyp_dir / file_id}.csv_bi\n")

    # Write reference list
    ref_list = lists_dir / "ref.list"
    with open(ref_list, "w", newline="\n") as f:
        for file_id in sorted(file_ids):
            f.write(f"{ref_dir / file_id}.csv_bi\n")

    print("\nList files created:")
    print(f"  {hyp_list}")
    print(f"  {ref_list}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert SeizureTransformer predictions to NEDC format"
    )
    parser.add_argument(
        "--checkpoint",
        type=str,
        default="evaluation/tusz/checkpoint.pkl",
        help="Path to checkpoint.pkl file",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default="experiments/dev/baseline/nedc_results",
        help="Output directory for NEDC files (under experiments/**)",
    )
    parser.add_argument("--threshold", type=float, default=0.8, help="Probability threshold")
    parser.add_argument("--kernel", type=int, default=5, help="Morphological kernel size (samples)")
    parser.add_argument(
        "--min_duration_sec", type=float, default=2.0, help="Minimum event duration (s)"
    )
    parser.add_argument(
        "--merge_gap_sec",
        type=float,
        default=None,
        help="DEPRECATED: Merge events with gaps less than this (s). WARNING: Violates NEDC standards. Use None for compliance.",
    )

    args = parser.parse_args()

    checkpoint_file = Path(args.checkpoint)
    if not checkpoint_file.exists():
        print(f"Error: Checkpoint file not found: {checkpoint_file}")
        return 1

    convert_checkpoint_to_nedc(
        checkpoint_file,
        args.outdir,
        threshold=args.threshold,
        morph_kernel_size=args.kernel,
        min_duration_sec=args.min_duration_sec,
        merge_gap_sec=args.merge_gap_sec,
    )
    return 0


if __name__ == "__main__":
    exit(main())
