#!/usr/bin/env python3
"""
SzCORE "Any-Overlap" event scoring wrapper using the official `timescoring` package.

- Consumes the checkpoint produced by `evaluation/tusz/run_tusz_eval.py`.
- Converts per-sample probabilities to events via our post-processing.
- Scores with SzCORE defaults (30s pre, 60s post; merge <90s; split >5min; any-overlap).
-
Outputs:
  - JSON summary at `<outdir>/szcore_summary.json` with micro-averaged metrics.
  - Optional per-file CSV with TP/FP counts and durations.

Install dependency:
  pip install timescoring

Note: We intentionally avoid merging gaps in post-processing (merge_gap_sec=None)
because SzCORE merges events internally (minDurationBetweenEvents=90 seconds).
"""

from __future__ import annotations

import argparse
import json
import pickle
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from timescoring.annotations import Annotation
from timescoring.scoring import EventScoring

# Ensure repo root is on sys.path for local package imports
repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

# Reuse our existing post-processing to derive events from probabilities
from evaluation.nedc_eeg_eval.nedc_scoring.post_processing import (  # noqa: E402
    apply_seizure_transformer_postprocessing,
)


@dataclass
class FileScore:
    file_id: str
    tp: int
    fp: int
    ref_true: int
    duration_sec: float
    sensitivity: float
    precision: float
    f1: float
    fp_per_24h: float


def load_checkpoint(checkpoint_pkl: Path) -> dict[str, Any]:
    with open(checkpoint_pkl, "rb") as f:
        ckpt = pickle.load(f)
    # Support either {"results": {...}} or flat mapping
    return ckpt.get("results", ckpt)


def score_file(
    file_id: str,
    predictions: np.ndarray,
    ref_events_sec: list[tuple[float, float]],
    threshold: float,
    morph_kernel_size: int,
    min_duration_sec: float,
    fs: int,
    params: EventScoring.Parameters,
) -> FileScore:
    # IMPORTANT: Do not merge gaps here; SzCORE merges with 90s internally
    hyp_events_sec = apply_seizure_transformer_postprocessing(
        predictions=predictions,
        threshold=threshold,
        morph_kernel_size=morph_kernel_size,
        min_duration_sec=min_duration_sec,
        fs=fs,
        merge_gap_sec=None,
    )

    num_samples = len(predictions)

    ref = Annotation(ref_events_sec, fs=fs, numSamples=num_samples)
    hyp = Annotation(hyp_events_sec, fs=fs, numSamples=num_samples)

    scores = EventScoring(ref, hyp, params)

    duration_sec = scores.numSamples / scores.fs  # at 10 Hz inside EventScoring

    return FileScore(
        file_id=file_id,
        tp=int(scores.tp),
        fp=int(scores.fp),
        ref_true=int(scores.refTrue),
        duration_sec=float(duration_sec),
        sensitivity=float(scores.sensitivity) if not np.isnan(scores.sensitivity) else float("nan"),
        precision=float(scores.precision) if not np.isnan(scores.precision) else float("nan"),
        f1=float(scores.f1) if not np.isnan(scores.f1) else float("nan"),
        fp_per_24h=float(scores.fpRate) if not np.isnan(scores.fpRate) else float("nan"),
    )


def run_szcore_evaluation(
    checkpoint_pkl: Path,
    output_dir: Path,
    threshold: float = 0.8,
    morph_kernel_size: int = 5,
    min_duration_sec: float = 2.0,
    fs: int = 256,
) -> dict[str, Any]:
    results_map = load_checkpoint(checkpoint_pkl)

    # SzCORE default parameters per EpilepsyBench
    params = EventScoring.Parameters(
        toleranceStart=30,
        toleranceEnd=60,
        minOverlap=0,
        maxEventDuration=5 * 60,
        minDurationBetweenEvents=90,
    )

    per_file: list[FileScore] = []

    # Aggregation (micro-average)
    sum_tp = 0
    sum_fp = 0
    sum_ref_true = 0
    sum_seconds = 0.0

    processed = 0
    skipped = 0

    for file_id, data in results_map.items():
        if data.get("error") is not None:
            skipped += 1
            continue
        preds = data.get("predictions")
        gt_events = data.get("seizure_events", [])
        if preds is None:
            skipped += 1
            continue

        file_score = score_file(
            file_id=file_id,
            predictions=np.asarray(preds),
            ref_events_sec=gt_events,
            threshold=threshold,
            morph_kernel_size=morph_kernel_size,
            min_duration_sec=min_duration_sec,
            fs=fs,
            params=params,
        )
        per_file.append(file_score)
        processed += 1

        sum_tp += file_score.tp
        sum_fp += file_score.fp
        sum_ref_true += file_score.ref_true
        sum_seconds += file_score.duration_sec

    sensitivity = (sum_tp / sum_ref_true) if sum_ref_true > 0 else float("nan")
    precision = (sum_tp / (sum_tp + sum_fp)) if (sum_tp + sum_fp) > 0 else float("nan")
    f1 = (
        0.0
        if (np.isnan(sensitivity) or np.isnan(precision) or (sensitivity + precision) == 0)
        else 2 * sensitivity * precision / (sensitivity + precision)
    )
    fp_per_24h = sum_fp / (sum_seconds / 86400.0) if sum_seconds > 0 else float("nan")

    summary: dict[str, Any] = {
        "backend": "szcore-timescoring",
        "parameters": {
            "threshold": threshold,
            "morph_kernel_size": morph_kernel_size,
            "min_duration_sec": min_duration_sec,
            "postproc_merge_gap_sec": None,
            "fs_predictions_hz": fs,
            "szcore": {
                "toleranceStart": params.toleranceStart,
                "toleranceEnd": params.toleranceEnd,
                "minOverlap": params.minOverlap,
                "maxEventDuration": params.maxEventDuration,
                "minDurationBetweenEvents": params.minDurationBetweenEvents,
            },
        },
        "corpus_micro_avg": {
            "files_scored": processed,
            "files_skipped": skipped,
            "tp": int(sum_tp),
            "fp": int(sum_fp),
            "ref_true": int(sum_ref_true),
            "total_duration_sec": float(sum_seconds),
            "sensitivity": float(sensitivity) if not np.isnan(sensitivity) else None,
            "precision": float(precision) if not np.isnan(precision) else None,
            "f1": float(f1),
            "fpRate": float(fp_per_24h) if not np.isnan(fp_per_24h) else None,
        },
    }

    # Write outputs
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "szcore_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Optional: per-file CSV for debugging
    import csv

    with open(output_dir / "per_file.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "file_id",
                "tp",
                "fp",
                "ref_true",
                "duration_sec",
                "sensitivity",
                "precision",
                "f1",
                "fp_per_24h",
            ]
        )
        for fs in per_file:
            w.writerow(
                [
                    fs.file_id,
                    fs.tp,
                    fs.fp,
                    fs.ref_true,
                    f"{fs.duration_sec:.3f}",
                    _fmt(fs.sensitivity),
                    _fmt(fs.precision),
                    _fmt(fs.f1),
                    _fmt(fs.fp_per_24h),
                ]
            )

    return summary


def _fmt(x: float) -> str:
    if x is None or np.isnan(x):
        return ""
    return f"{x:.6f}"


def main() -> int:
    p = argparse.ArgumentParser(description="Run SzCORE scoring via timescoring")
    p.add_argument(
        "--checkpoint",
        type=str,
        default="experiments/eval/baseline/checkpoint.pkl",
        help="Path to checkpoint.pkl from TUSZ evaluation",
    )
    p.add_argument(
        "--outdir",
        type=str,
        default="experiments/eval/baseline/szcore_results",
        help="Directory to save results",
    )
    p.add_argument("--threshold", type=float, default=0.8, help="Probability threshold")
    p.add_argument("--kernel", type=int, default=5, help="Morphological kernel size (samples)")
    p.add_argument("--min_duration_sec", type=float, default=2.0, help="Minimum event duration (s)")
    p.add_argument("--fs", type=int, default=256, help="Sampling rate of predictions (Hz)")
    args = p.parse_args()

    checkpoint = Path(args.checkpoint)
    outdir = Path(args.outdir)
    if not checkpoint.exists():
        print(f"Error: checkpoint not found: {checkpoint}")
        return 1

    print("SzCORE scoring (timescoring) starting...")
    print(f"Checkpoint: {checkpoint}")
    print(f"Outdir:     {outdir}")

    run_szcore_evaluation(
        checkpoint,
        outdir,
        threshold=args.threshold,
        morph_kernel_size=args.kernel,
        min_duration_sec=args.min_duration_sec,
        fs=args.fs,
    )

    print("Done. Results:")
    print(f"  Summary JSON: {outdir / 'szcore_summary.json'}")
    print(f"  Per-file CSV: {outdir / 'per_file.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
