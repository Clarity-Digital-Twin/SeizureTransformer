# 📊 NEDC INTEGRATION STATUS
## Quick Status Dashboard

**Last Updated**: 2025-09-13 12:40
**Sweep Progress**: 108/108 combinations (complete) ✅
**Native OVERLAP**: Parity achieved (OVERLAP sens/Total FA) ✅ — F1 differs slightly by aggregation

## What's Done ✅

### NEDC Binary Backend
- NEDC v6.0.0 binary integrated at `evaluation/nedc_eeg_eval/v6.0.0/`
- Full pipeline working: checkpoint → CSV_bi → NEDC → metrics
- Converters and runner tested (`evaluation/nedc_scoring/`)
- Backend toggle implemented (`--backend nedc-binary|native-taes`)
- Note: If the binary errors on Python invocation, ensure a `python` alias is available on PATH (some environments only provide `python3`).

### Native OVERLAP Backend (PRIMARY GOAL) 🎯
- Python implementation at `seizure_evaluation/taes/overlap_scorer.py` (integrated)
- Backend flag: `--backend native-taes` (kept for compatibility; now runs OVERLAP scorer)
- Parity (OVERLAP): Native matches Temple for SEIZ sensitivity and TOTAL FA/24h (SEIZ + BCKG) on dev and eval baselines
  - Dev/default: Sens=23.53%, Total FA=19.45/24h (Temple = Native)
  - Dev/2.5fa:  Sens=7.44%,  Total FA=2.26/24h (Temple = Native)
  - Dev/1fa:    Sens=0.65%,  Total FA=0.22/24h (Temple = Native)
  - Eval/default+10fa: Sens=45.63%, Total FA=25.01/24h (Temple = Native)
  - Eval/2.5fa: Sens=11.51%, Total FA=2.45/24h (Temple = Native)
  - Eval/1fa:   Sens=1.28%,  Total FA=0.38/24h (Temple = Native)
- F1 note: Native prints dataset-level F1 for convenience; Temple reports per-label F1 and a summary. Treat F1 as informational unless exact match is required.
- Metrics extraction in `run_nedc.py` targets the OVERLAP section explicitly and stores under `overlap` (duplicated to `taes` for backward-compat).

### Parameter Tuning Progress
- Dev checkpoint: `experiments/dev/baseline/checkpoint.pkl` (~1.5GB)
- Parameter sweep: 108/108 combinations complete
- Results:
  - CSV: `experiments/dev/baseline/sweeps/sweep_results.csv`
  - Recommended: `experiments/dev/baseline/sweeps/recommended_params.json` (threshold=0.95, kernel=5, min_duration=2.0s, merge_gap=5.0s)
  - Important: Current sweep parses the first section in Temple `summary.txt` (DP ALIGNMENT), not OVERLAP. If OVERLAP is the target for gating, update the sweep parser accordingly.

## How to Monitor 🏃

```bash
# Count completed combos (folders starting with thr)
ls experiments/dev/baseline/sweeps/ | grep "^thr" | wc -l

# Tail sweep results
tail -n 20 experiments/dev/baseline/sweeps/sweep_results.csv

# Attach to tmux session if running there
tmux attach -t sweep_dev   # Ctrl+B then D to detach
```

## TWO PARALLEL TRACKS

### Track 1: Parameter Sweep (COMPLETE)
- Used Temple binary NEDC backend
- Artifacts written under `experiments/dev/baseline/sweeps/`

### Track 2: Native TAES Implementation (NEEDS WORK)
- THIS IS THE MAIN FOCUS
- Not dependent on sweep
- Can work on this NOW while sweep runs

## EVAL FINDINGS 📊

### Temple Binary (Eval baseline):
- DP ALIGNMENT: Sens=27.72%, FA=12.41/24h, F1=0.4114
- OVERLAP:      Sens=23.4542%, FA=9.9679/24h, F1=0.3704

### Native TAES (overlap_threshold=0.0):
- OVERLAP-equivalent summary: Sens=23.45%, FA=9.97/24h
- F1: differs from Temple OVERLAP due to aggregation method; not a gating metric for us

### Sweep Results (Dev set):
- Recommended params (DP ALIGNMENT-optimal): threshold=0.95, kernel=5, min_duration=2.0s, merge_gap=5.0s
- At these params (DP ALIGNMENT section): Sens≈13.67%, FA≈9.97/24h
- OVERLAP section at those params differs (e.g., Sens≈11.91%, FA≈6.67/24h for one example); choose target scoring method and align parser

## CRITICAL NEXT STEPS 🚨

### 1. Choose and align the target scoring method
```bash
# Run same data through both backends
python evaluation/nedc_scoring/run_nedc.py \
  --checkpoint experiments/dev/baseline/checkpoint.pkl \
  --backend nedc-binary --outdir test_binary

python evaluation/nedc_scoring/run_nedc.py \
  --checkpoint experiments/dev/baseline/checkpoint.pkl \
  --backend native-taes --outdir test_native

# Native scorer matches Temple OVERLAP for sens/FA at overlap_threshold=0.0.
# Decide which method (DP ALIGNMENT vs OVERLAP) gates tuning and reporting,
# then make sweep parser match that section.
```

### 2. Finalize Operating Point Selection
No action required; recommended params are available at:
`experiments/dev/baseline/sweeps/recommended_params.json`

### 3. Select Optimal Parameters
```bash
# Find all combos with FA ≤ 10
for dir in experiments/dev/baseline/sweeps/thr*; do
  [ -f "$dir/results/metrics.json" ] && {
    fa=$(grep '"fa_per_24h"' "$dir/results/metrics.json" | grep -o '[0-9.]*')
    sens=$(grep '"sensitivity_percent"' "$dir/results/metrics.json" | grep -o '[0-9.]*')
    [ "$(echo "$fa <= 10" | bc -l)" = "1" ] && echo "$(basename $dir): FA=$fa, Sens=$sens%"
  }
done
```

### 4. Freeze & Deploy
```bash
# Create frozen params (example with best found)
echo '{
  "threshold": 0.90,
  "kernel": 5,
  "min_duration_sec": 8.0,
  "merge_gap_sec": 10.0
}' > experiments/eval/frozen_params.json
```

## Key Metrics Target

- MUST ACHIEVE: FA/24h ≤ 10 (method must be specified: DP ALIGNMENT or OVERLAP)
- Dev (DP ALIGNMENT at recommended params): FA≈9.97/24h @ Sens≈13.67%
- Eval baseline (OVERLAP at thr=0.8): FA≈9.97/24h @ Sens≈23.45%
- Baseline without tuning: FA≈137.5/24h @ Sens≈82%
- Goal: Maximize sensitivity subject to FA ≤ 10 under the chosen scoring method

## Quick Commands

```bash
# Run with specific params (after sweep; replace with selected values)
python evaluation/nedc_scoring/run_nedc.py \
  --checkpoint experiments/dev/baseline/checkpoint.pkl \
  --threshold <thr> --kernel <k> --min_duration_sec <min> --merge_gap_sec <gap>
```
