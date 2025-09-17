SzCORE Scoring (timescoring)

- Purpose: run SzCORE’s Any-Overlap event scoring using the official `timescoring` package on TUSZ predictions.
- Inputs: `checkpoint.pkl` produced by `tusz-eval` (or legacy shim at `evaluation/tusz/run_tusz_eval.py`).
- Output: Micro-averaged corpus metrics and per-file breakdown.

Install
- pip install timescoring
- Optional plotting: pip install "timescoring[plotting]"

Usage
- szcore-run \
  --checkpoint experiments/eval/baseline/checkpoint.pkl \
  --outdir experiments/eval/baseline/szcore_results \
  --threshold 0.8 --kernel 5 --min_duration_sec 2.0

Outputs
- `<outdir>/szcore_summary.json`: micro-averaged TP/FP, sensitivity, precision, F1, FP/24h.
- `<outdir>/per_file.csv`: per-file TP/FP/ref_true/duration and metrics.

Notes
- Post-processing does not merge nearby events (`merge_gap_sec=None`); SzCORE merges internally (`minDurationBetweenEvents=90`).
- SzCORE parameters (defaults): 30s pre, 60s post, minOverlap=0, split >5min, merge <90s.
- Predictions are assumed at 256 Hz (we resample upstream); adjust `--fs` only if you change the pipeline.

