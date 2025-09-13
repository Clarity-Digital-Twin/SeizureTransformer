# Experiments Directory Structure

This directory tracks all experimental runs, parameter tuning, and model evaluations with full reproducibility.

## Directory Organization

```
experiments/
├── dev/                    # Dev split tuning experiments
│   ├── baseline/           # Default parameters (threshold=0.8, etc)
│   ├── sweep_2025-01-13/   # Parameter sweep runs (timestamped)
│   └── archive/            # Old/failed experiments
├── eval/                   # Final eval split runs (run once each)
│   ├── baseline/           # Default parameters on eval
│   ├── tuned_v1/           # First tuned parameters on eval
│   └── final/              # Final submitted results
└── archive/                # Historical experiments and failed runs
```

## Experiment Naming Convention

**Format**: `{split}_{description}_{timestamp}`

Examples:
- `dev_baseline_2025-01-13`
- `dev_sweep_fa10_2025-01-13` 
- `eval_tuned_v1_2025-01-14`

## Required Files Per Experiment

Each experiment directory must contain:

1. **`run_config.json`** - Exact parameters used
2. **`checkpoint.pkl`** - Raw model predictions 
3. **`nedc_results/`** - NEDC scoring outputs
4. **`summary.json`** - Key metrics extracted
5. **`command_log.txt`** - Exact commands run
6. **`notes.md`** - Human observations/decisions

## Experiment Tracking Workflow

### Dev Split Experiments
```bash
# 1. Create timestamped experiment
EXPNAME="dev_sweep_fa10_$(date +%Y-%m-%d)"
mkdir -p experiments/dev/$EXPNAME

# 2. Run experiment with logging
python evaluation/tusz/run_tusz_eval.py \
  --data_dir /path/to/TUSZ/dev \
  --out_dir experiments/dev/$EXPNAME \
  --device auto 2>&1 | tee experiments/dev/$EXPNAME/command_log.txt

# 3. Parameter sweep with results tracking
python evaluation/nedc_scoring/sweep_operating_point.py \
  --checkpoint experiments/dev/$EXPNAME/checkpoint.pkl \
  --outdir_base experiments/dev/$EXPNAME/nedc_sweeps \
  --target_fa_per_24h 10

# 4. Archive experiment
echo "FA target: 10/24h, Grid: thr=0.5-0.9, kernel=5-11" > experiments/dev/$EXPNAME/notes.md
```

### Eval Split Experiments (Final)
```bash
# Only run once per parameter set
EXPNAME="eval_tuned_v1_$(date +%Y-%m-%d)"
mkdir -p experiments/eval/$EXPNAME

# Use frozen parameters from dev
python evaluation/nedc_scoring/run_nedc.py \
  --checkpoint experiments/eval/$EXPNAME/checkpoint.pkl \
  --threshold 0.6 --kernel 11 --min_duration_sec 4 \
  --outdir experiments/eval/$EXPNAME/nedc_results
```

## Current Status

- **Dev experiments**: Need to run parameter sweeps
- **Eval experiments**: Have baseline results in `evaluation/tusz/`
- **Migration needed**: Move existing results to proper experiment structure

## Tools Integration

- **Sweep tool**: `evaluation/nedc_scoring/sweep_operating_point.py`
- **Experiment comparison**: `python scripts/experiment_tracker.py compare --split {dev|eval}`
- **Best model selection**: Based on dev results, frozen for eval
