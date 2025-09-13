# Experiments Directory Structure

This directory tracks all experimental runs, parameter tuning, and model evaluations with full reproducibility.

## Current Directory Structure (ACTUAL)

```
experiments/
├── dev/                        # Dev split (1832 EDF files)
│   ├── baseline/               # Default params COMPLETE ✅
│   │   ├── checkpoint.pkl      # 1.5GB, all predictions
│   │   ├── eval_log.txt        # Inference log
│   │   ├── run_config.json     # thr=0.8, k=5, min=2.0
│   │   ├── nedc_results/       # 30.51% sens, 107.29 FA/24h
│   │   └── sweeps/             # Grid search IN PROGRESS 🏃
│   │       ├── thr0.70_*/      # 37/108 combinations done
│   │       └── sweep.log       # Running in tmux
│   └── test_baseline/          # Config test only (no data)
├── eval/                       # Eval split (865 EDF files)
│   └── baseline/               # Default params COMPLETE ✅
│       ├── checkpoint.pkl      # 449MB, all predictions
│       ├── eval_log.txt        # Inference log
│       ├── run_config.json     # thr=0.8, k=5, min=2.0
│       └── summary.json        # 24.15% sens, 137.5 FA/24h
└── archive/                    # (empty - for old experiments)
```

## Key Results Summary

| Split | Experiment | Files | Sensitivity | FA/24h | Status |
|-------|------------|-------|-------------|---------|---------|
| eval  | baseline   | 865   | 24.15%     | 137.5   | ✅ Complete |
| dev   | baseline   | 1832  | 30.51%     | 107.29  | ✅ Complete |
| dev   | sweeps     | 1832  | TBD        | Target≤10 | 🏃 Running (37/108) |

## Parameter Sweep Status

Currently running in tmux session `sweep_dev`:
- **Grid**: threshold × kernel × min_duration × merge_gap
- **Values**: [0.7,0.8,0.9,0.95] × [5,11,21] × [2,4,8] × [0,5,10]
- **Total**: 108 combinations
- **Progress**: 37/108 complete (~34%)
- **Target**: FA/24h ≤ 10 with max sensitivity

Monitor with: `tmux attach -t sweep_dev`

## File Descriptions

### Core Files
- `checkpoint.pkl` - Raw model predictions at 256Hz (per-sample probabilities)
- `run_config.json` - Exact parameters and metadata for reproducibility
- `eval_log.txt` - Inference runtime log with progress
- `nedc_results/` - NEDC scoring outputs (CSV_bi files, lists, results/)

### Sweep Outputs
- `sweeps/thr*_k*_min*_gap*/` - Individual parameter combination results
- `sweeps/sweep_results.csv` - Summary table (will be created at end)
- `sweeps/recommended_params.json` - Best params meeting FA target

## Workflow Commands

### Run NEDC Scoring on Existing Checkpoint
```bash
python evaluation/nedc_scoring/run_nedc.py \
  --checkpoint experiments/dev/baseline/checkpoint.pkl \
  --outdir experiments/dev/baseline/nedc_results \
  --threshold 0.8 --kernel 5 --min_duration_sec 2.0
```

### Run Parameter Sweep (Dev Only)
```bash
python evaluation/nedc_scoring/sweep_operating_point.py \
  --checkpoint experiments/dev/baseline/checkpoint.pkl \
  --outdir_base experiments/dev/baseline/sweeps \
  --thresholds 0.7,0.8,0.9 \
  --kernels 5,11,21 \
  --min_durations 2,4,8 \
  --target_fa_per_24h 10
```

### Final Eval Run (After Tuning)
```bash
# Use best params from dev sweep
python evaluation/nedc_scoring/run_nedc.py \
  --checkpoint experiments/eval/tuned/checkpoint.pkl \
  --outdir experiments/eval/tuned/nedc_results \
  --threshold <best> --kernel <best> --min_duration_sec <best>
```

## Important Notes

1. **Dev vs Eval**: Dev has 2x more files (1832 vs 865) and is "easier" (better baseline metrics)
2. **No Retraining**: We only tune post-processing params, model weights are frozen
3. **One Shot Eval**: Run eval split ONCE with frozen params from dev
4. **Sweep Reuses Predictions**: All 108 combinations use same checkpoint.pkl

## Next Steps

1. ⏳ Wait for sweep completion (~2 more hours)
2. 📊 Analyze `sweep_results.csv` for best params
3. ❄️ Freeze best params as `operating_point.json`
4. 🎯 Run final eval with frozen params
5. 📝 Report final metrics