#!/usr/bin/env python3
"""
Sweep operating point (threshold/post-processing) on a dev checkpoint,
convert to NEDC format, run official scorer, and summarize TAES metrics.

Usage:
  python evaluation/nedc_scoring/sweep_operating_point.py \
    --checkpoint evaluation/tusz_dev/checkpoint.pkl \
    --outdir_base evaluation/nedc_scoring/sweeps/dev \
    --thresholds 0.5,0.6,0.7,0.8,0.9 \
    --kernels 5,11 \
    --min_durations 2,4 \
    --merge_gaps 0,10 \
    --target_fa_per_24h 10

Produces CSV summary and recommends the best setting meeting FA target with max sensitivity.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Result:
    threshold: float
    kernel: int
    min_duration: float
    merge_gap: float | None
    taes_sensitivity: float
    taes_fa_per_24h: float
    workdir: Path


def run_once(
    checkpoint: Path,
    outdir: Path,
    threshold: float,
    kernel: int,
    min_duration: float,
    merge_gap: float | None,
) -> Result:
    # Convert
    cmd_conv = [
        "python",
        "evaluation/nedc_scoring/run_nedc.py",
        "--checkpoint",
        str(checkpoint),
        "--outdir",
        str(outdir),
        "--force",
        "--threshold",
        str(threshold),
        "--kernel",
        str(kernel),
        "--min_duration_sec",
        str(min_duration),
    ]
    if merge_gap is not None:
        cmd_conv += ["--merge_gap_sec", str(merge_gap)]

    env = os.environ.copy()
    nedc_root = Path.cwd() / "evaluation" / "nedc_eeg_eval" / "v6.0.0"
    env["NEDC_NFC"] = str(nedc_root)
    env["PATH"] = f"{nedc_root / 'bin'}:{env.get('PATH','')}"
    env["PYTHONPATH"] = f"{nedc_root / 'lib'}:{env.get('PYTHONPATH','')}"

    subprocess.run(cmd_conv, env=env, check=True, capture_output=True, text=True)

    # Score
    cmd_score = [
        "python",
        "evaluation/nedc_scoring/run_nedc.py",
        "--outdir",
        str(outdir),
        "--score-only",
    ]
    subprocess.run(cmd_score, env=env, check=True, capture_output=True, text=True)

    # Parse TAES metrics using robust regex (matches run_nedc.py)
    summary = outdir / "results" / "summary.txt"
    with open(summary) as f:
        content = f.read()

    import re
    taes_sens_match = re.search(r"Sensitivity \(TPR, Recall\):\s+([\d.]+)%", content)
    taes_fa_match = re.search(r"Total False Alarm Rate:\s+([\d.]+)\s+per 24 hours", content)

    if not taes_sens_match or not taes_fa_match:
        raise RuntimeError(f"Could not parse TAES metrics from {summary}")

    taes_sens = float(taes_sens_match.group(1))
    taes_fa = float(taes_fa_match.group(1))

    return Result(
        threshold=threshold,
        kernel=kernel,
        min_duration=min_duration,
        merge_gap=merge_gap,
        taes_sensitivity=taes_sens,
        taes_fa_per_24h=taes_fa,
        workdir=outdir,
    )


def parse_floats_list(s: str) -> list[float]:
    return [float(x) for x in s.split(",") if x.strip()]


def parse_ints_list(s: str) -> list[int]:
    return [int(x) for x in s.split(",") if x.strip()]


def main() -> int:
    p = argparse.ArgumentParser(description="Sweep operating points (dev)")
    p.add_argument("--checkpoint", type=str, required=True)
    p.add_argument("--outdir_base", type=str, required=True)
    p.add_argument("--thresholds", type=str, default="0.6,0.7,0.8,0.9")
    p.add_argument("--kernels", type=str, default="5,11")
    p.add_argument("--min_durations", type=str, default="2,4")
    p.add_argument("--merge_gaps", type=str, default="0,10")
    p.add_argument("--target_fa_per_24h", type=float, default=10.0)
    args = p.parse_args()

    checkpoint = Path(args.checkpoint)
    base = Path(args.outdir_base)
    base.mkdir(parents=True, exist_ok=True)

    thresholds = parse_floats_list(args.thresholds)
    kernels = parse_ints_list(args.kernels)
    min_durations = parse_floats_list(args.min_durations)
    merge_gaps_raw = parse_floats_list(args.merge_gaps)
    merge_gaps: list[float | None] = [None if g == 0 else g for g in merge_gaps_raw]

    results: list[Result] = []
    for thr, ker, mind, gap in itertools.product(thresholds, kernels, min_durations, merge_gaps):
        name = f"thr{thr:.2f}_k{ker}_min{mind:.1f}_gap{(gap if gap is not None else 0):.1f}"
        outdir = base / name
        try:
            res = run_once(checkpoint, outdir, thr, ker, mind, gap)
            results.append(res)
            print(f"OK: {name} -> sens={res.taes_sensitivity:.2f}% FA/24h={res.taes_fa_per_24h:.2f}")
        except subprocess.CalledProcessError as e:
            print(f"ERROR running {name}: {e}")
        except Exception as e:
            print(f"ERROR parsing {name}: {e}")

    # Write CSV
    csv_path = base / "sweep_results.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["threshold", "kernel", "min_duration", "merge_gap", "taes_sensitivity", "taes_fa_per_24h", "workdir"])
        for r in results:
            w.writerow([r.threshold, r.kernel, r.min_duration, r.merge_gap if r.merge_gap is not None else 0, r.taes_sensitivity, r.taes_fa_per_24h, str(r.workdir)])

    # Recommend best: minimize FA/24h subject to FA<=target, maximize sensitivity
    target = args.target_fa_per_24h
    feasible = [r for r in results if r.taes_fa_per_24h <= target]
    if feasible:
        best = max(feasible, key=lambda r: (r.taes_sensitivity, -r.taes_fa_per_24h))
        print("\nRecommended (subject to FA<=target):")
        print(f"  threshold={best.threshold} kernel={best.kernel} min_dur={best.min_duration} merge_gap={best.merge_gap}")
        print(f"  TAES sensitivity={best.taes_sensitivity:.2f}% FA/24h={best.taes_fa_per_24h:.2f}")
        rec_path = base / "recommended_params.json"
        with open(rec_path, "w") as f:
            f.write(
                "{\n"
                f"  \"threshold\": {best.threshold},\n"
                f"  \"kernel\": {best.kernel},\n"
                f"  \"min_duration_sec\": {best.min_duration},\n"
                f"  \"merge_gap_sec\": {0 if best.merge_gap is None else best.merge_gap}\n"
                "}\n"
            )
    else:
        print("\nNo feasible operating point met the FA/24h target. See sweep_results.csv for trade-offs.")

    print(f"\nResults written to: {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

