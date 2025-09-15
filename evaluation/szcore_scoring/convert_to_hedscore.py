#!/usr/bin/env python3
"""Convert checkpoint.pkl predictions to HED-SCORE TSV format (optional).

This exporter is optional; the SzCORE workflow uses the timescoring.Annotation
API directly. Use this only if you need TSV artifacts for cross-tooling.
"""

from __future__ import annotations

import argparse
import pickle
from pathlib import Path
from typing import Any

import numpy as np

from evaluation.nedc_eeg_eval.nedc_scoring.post_processing import (
    apply_seizure_transformer_postprocessing,
)


def convert_to_hedscore(
    checkpoint_pkl: Path,
    output_dir: Path,
    threshold: float = 0.8,
    kernel: int = 5,
    min_duration_sec: float = 2.0,
    fs: int = 256,
) -> int:
    with open(checkpoint_pkl, "rb") as f:
        ckpt = pickle.load(f)
    results: dict[str, Any] = ckpt.get("results", ckpt)

    output_dir.mkdir(parents=True, exist_ok=True)

    header = "onset\tduration\teventType\tconfidence\tchannels\tdateTime\trecordingDuration"

    count = 0
    for file_id, data in results.items():
        preds = data.get("predictions")
        if preds is None:
            continue
        preds = np.asarray(preds)
        duration_sec = len(preds) / float(fs)

        hyp_events = apply_seizure_transformer_postprocessing(
            predictions=preds,
            threshold=threshold,
            morph_kernel_size=kernel,
            min_duration_sec=min_duration_sec,
            fs=fs,
            merge_gap_sec=None,  # avoid double-merge; SzCORE merges internally
        )

        lines = [header]
        for start_sec, end_sec in hyp_events:
            event_duration = end_sec - start_sec
            # dateTime and channels are not evaluated by timescoring; use placeholders
            lines.append(
                f"{start_sec:.3f}\t{event_duration:.3f}\tsz\tna\tna\t1970-01-01 00:00:00\t{duration_sec:.3f}"
            )

        (output_dir / f"{file_id}.tsv").write_text("\n".join(lines))
        count += 1

    print(f"Wrote {count} HED-SCORE TSV files to {output_dir}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Export HED-SCORE TSVs (optional)")
    p.add_argument(
        "--checkpoint",
        type=str,
        default="experiments/eval/baseline/checkpoint.pkl",
        help="Path to checkpoint.pkl",
    )
    p.add_argument(
        "--outdir",
        type=str,
        default="experiments/eval/baseline/szcore_tsv",
        help="Directory to write TSVs",
    )
    p.add_argument("--threshold", type=float, default=0.8)
    p.add_argument("--kernel", type=int, default=5)
    p.add_argument("--min_duration_sec", type=float, default=2.0)
    p.add_argument("--fs", type=int, default=256)
    args = p.parse_args()

    return convert_to_hedscore(
        checkpoint_pkl=Path(args.checkpoint),
        output_dir=Path(args.outdir),
        threshold=args.threshold,
        kernel=args.kernel,
        min_duration_sec=args.min_duration_sec,
        fs=args.fs,
    )


if __name__ == "__main__":
    raise SystemExit(main())
