# Operating Point Tuning Plan (Dev → Eval)

This document defines how we will tune the SeizureTransformer post‑processing parameters to reduce FA/24h while preserving sensitivity, using the TUH/TUSZ splits in a standard ML workflow.

## Goals
- Keep the model fixed (no retraining).
- Tune only inference post‑processing on the dev split.
- Select a single global operating point (threshold + post‑processing params).
- Evaluate once on the eval split with the tuned parameters and report NEDC TAES.

## Datasets (TUSZ v2.0.3)
- Train: used by the original model authors; we do not retrain here.
- Dev: hyperparameter tuning for post‑processing.
- Eval: held‑out final report (never used during tuning).

## Parameters To Tune (Dev)
- `threshold` (probability): e.g., 0.3–0.95.
- `kernel` (morphology, samples): e.g., 5–31.
- `min_duration_sec`: e.g., 2–10 s.
- `merge_gap_sec` (optional): e.g., 0–30 s (merge events separated by short gaps).

All parameters are now exposed via CLI and supported by the current codebase:
- `evaluation/nedc_scoring/convert_predictions.py` — accepts `--threshold`, `--kernel`, `--min_duration_sec`, `--merge_gap_sec`.
- `evaluation/nedc_scoring/post_processing.py` — applies threshold + morphology + min duration, and optionally merges nearby events.
- `evaluation/nedc_scoring/run_nedc.py` — pass‑through CLI to conversion and runs official scorer.
- `evaluation/nedc_scoring/sweep_operating_point.py` — performs grid sweeps on dev and summarizes TAES trade‑offs.

## Step‑By‑Step Procedure (With Full Experiment Tracking)

**🗂️ All experiments are tracked in `experiments/` directory with full reproducibility.**

1) **Generate dev predictions checkpoint**
```bash
# Create tracked experiment
python scripts/experiment_tracker.py create-config \
  --split dev --description "baseline" \
  --notes "Default parameters baseline on dev split"

# Run dev evaluation with experiment tracking
python evaluation/tusz/run_tusz_eval.py \
  --data_dir /path/to/TUSZ/v2.0.3/dev \
  --out_dir experiments/dev/baseline \
  --device auto
# Produces: experiments/dev/baseline/checkpoint.pkl
```

2) **Sweep operating points on dev**
```bash
# Create sweep experiment
SWEEP_NAME="sweep_fa10_$(date +%Y-%m-%d)"
python scripts/experiment_tracker.py create-config \
  --split dev --description "$SWEEP_NAME" \
  --target_fa_per_24h 10 \
  --notes "Grid search: FA target ≤10/24h"

# Run parameter sweep
python evaluation/nedc_scoring/sweep_operating_point.py \
  --checkpoint experiments/dev/baseline/checkpoint.pkl \
  --outdir_base experiments/dev/$SWEEP_NAME \
  --thresholds 0.5,0.6,0.7,0.8,0.9 \
  --kernels 5,11 \
  --min_durations 2,4 \
  --merge_gaps 0,10 \
  --target_fa_per_24h 10

# Compare all dev experiments
python scripts/experiment_tracker.py compare --split dev
```

3) **Freeze parameters (from dev results)**
```bash
# Record best parameters from sweep
echo "Selected from dev sweep: threshold=0.6, kernel=11, min=4.0, gap=10" \
  > experiments/dev/$SWEEP_NAME/selected_params.txt

# Copy recommended_params.json to eval experiment template
cp experiments/dev/$SWEEP_NAME/recommended_params.json \
   experiments/eval/tuned_v1_params.json
```

4) **Evaluate on eval split once (final)**
```bash
# Create final eval experiment (ONLY RUN ONCE)
EVAL_NAME="tuned_v1_$(date +%Y-%m-%d)"
python scripts/experiment_tracker.py create-config \
  --split eval --description "$EVAL_NAME" \
  --threshold 0.6 --kernel 11 --min_duration_sec 4.0 --merge_gap_sec 10 \
  --notes "Final evaluation with dev-optimized parameters"

# Run TUSZ eval predictions
python evaluation/tusz/run_tusz_eval.py \
  --data_dir /path/to/TUSZ/v2.0.3/eval \
  --out_dir experiments/eval/$EVAL_NAME \
  --device auto

# Convert + score using frozen parameters
python evaluation/nedc_scoring/run_nedc.py \
  --checkpoint experiments/eval/$EVAL_NAME/checkpoint.pkl \
  --outdir experiments/eval/$EVAL_NAME/nedc_results \
  --threshold 0.6 --kernel 11 --min_duration_sec 4.0 --merge_gap_sec 10

# Log final results
python scripts/experiment_tracker.py compare --split eval
```

5) Report
- Use `experiments/eval/$EVAL_NAME/nedc_results/results/summary.txt` (TAES section) as the canonical metrics.
- Include AUROC from `evaluation/tusz/run_tusz_eval.py` summary if desired (note: AUROC is per‑sample; TAES is event‑level).

## Constraints & Notes
- Do not tune on eval; only run it once with the chosen operating point.
- Use a single global setting (no per‑file/patient tuning) for fair reporting.
- If resource‑limited, start with a small grid (threshold × min_duration) before adding morphology/gap merging.

## Rationale
This follows standard ML practice: train on train, tune on dev, test on eval. We do not retrain the model; we only calibrate the eventization and threshold to meet a clinical FA/24h target while maximizing detection sensitivity.
