# 📊 NEDC INTEGRATION STATUS
## Quick Status Dashboard

Date: 2025-09-13
Note: This status document shows how to check progress. Replace examples with your live values.

## What's Done ✅

### NEDC Backend Integration
- NEDC v6.0.0 binary integrated at `evaluation/nedc_eeg_eval/v6.0.0/`
- Full pipeline working: checkpoint → CSV_bi → NEDC → metrics
- Converters and runner tested (`evaluation/nedc_scoring/`)
- Backend toggle implemented (`--backend nedc-binary|native-taes`)

### Parameter Tuning Progress
- Dev checkpoint generated (`experiments/dev/baseline/checkpoint.pkl`)
- Parameter sweep launched via `evaluation/nedc_scoring/sweep_operating_point.py`
- Typical grid: 4 thresholds × 3 kernels × 3 durations × 3 gaps = 108 combos

## How to Monitor 🏃

```bash
# Count completed combos (folders starting with thr)
ls experiments/dev/baseline/sweeps/ | grep "^thr" | wc -l

# Tail sweep results
tail -n 20 experiments/dev/baseline/sweeps/sweep_results.csv

# Attach to tmux session if running there
tmux attach -t sweep_dev   # Ctrl+B then D to detach
```

## Next Steps ⏳

1. Wait for sweep completion (monitor with commands above)
2. Analyze results: choose params with FA ≤ 10 and max sensitivity
3. Freeze parameters: write `experiments/eval/frozen_params.json`
4. Single eval run: apply frozen params to eval set (ONE TIME ONLY)

## Key Metrics Target

- Must achieve: FA/24h ≤ 10
- Prefer: Sensitivity ≥ 50% (higher is better)

## Files to Watch

```
experiments/dev/baseline/sweeps/
├── sweep_results.csv          # All results
├── thr0.70_k5_min2.0_gap0.0/  # Example combo workdir
└── ...                        # One dir per combo
```

## Optional: Native TAES Progress

Python reimplementation at `seizure_evaluation/taes/scorer.py`:
- Integrated with `--backend native-taes`
- Needs conformance validation against NEDC

## Quick Commands

```bash
# Run with specific params (after sweep; replace with selected values)
python evaluation/nedc_scoring/run_nedc.py \
  --checkpoint experiments/dev/baseline/checkpoint.pkl \
  --threshold <thr> --kernel <k> --min_duration_sec <min> --merge_gap_sec <gap>
```
