# 🎯 SEIZURE TRANSFORMER TUNING PLAN
## Finding the Optimal Post-Processing Parameters for Clinical Use

**Purpose**: Tune SeizureTransformer's post-processing parameters (threshold, morphology, duration filters) to meet clinical targets (FA/24h ≤ 10) while maximizing sensitivity.

**Scope**: ONLY about tuning the model's output processing. NOT about NEDC integration (see NEDC_INTEGRATION_PLAN.md for that).

## What We're Tuning (Not the Model!)

We're NOT retraining the model. We're tuning these post-processing knobs:
- **Threshold**: Confidence level to call something a seizure (0.5-0.95)
- **Kernel size**: Smoothing window for morphological operations (5, 11, 21 samples)
- **Min duration**: Minimum seizure length to keep (2-8 seconds)
- **Merge gap**: Gap size to merge nearby events (0-10 seconds)

## The Three-Step Process

### Step 1: Dev Set Tuning
**Purpose**: Find best parameters on development set (1832 files)

```bash
# Already complete - we have checkpoint
experiments/dev/baseline/checkpoint.pkl  # 1.5GB of predictions

# Run parameter sweep (CURRENTLY RUNNING)
python evaluation/nedc_scoring/sweep_operating_point.py \
  --checkpoint experiments/dev/baseline/checkpoint.pkl \
  --outdir experiments/dev/baseline/sweeps
```

This tests 108 combinations:
- Thresholds: [0.7, 0.8, 0.9, 0.95]
- Kernels: [5, 11, 21]
- Min durations: [2, 4, 8] seconds
- Merge gaps: [0, 5, 10] seconds

**Current Status**: 40/108 combinations complete (~37%)

### Step 2: Freeze Parameters
**Purpose**: Lock in the best parameters from dev sweep

```bash
# After sweep completes, analyze results
cat experiments/dev/baseline/sweeps/sweep_results.csv

# Pick parameters that give:
# - FA/24h ≤ 10 (HARD REQUIREMENT)
# - Highest sensitivity possible

# Create frozen config
echo '{
  "threshold": 0.8,  # Example from best sweep result
  "kernel": 11,
  "min_duration_sec": 4.0,
  "merge_gap_sec": 5.0
}' > experiments/eval/frozen_params.json
```

### Step 3: Single Eval Run
**Purpose**: Final performance measurement (RUN ONLY ONCE!)

```bash
# Generate eval predictions (if not exists)
python evaluation/tusz/run_tusz_eval.py \
  --data_dir /path/to/TUSZ/eval \
  --out_dir experiments/eval/final

# Apply frozen parameters
python evaluation/nedc_scoring/run_nedc.py \
  --checkpoint experiments/eval/final/checkpoint.pkl \
  --threshold 0.8 --kernel 11 \
  --min_duration_sec 4.0 --merge_gap_sec 5.0 \
  --outdir experiments/eval/final/results
```

## Clinical Targets

**Must achieve**:
- False Alarms: ≤ 10 per 24 hours
- Sensitivity: ≥ 50% (prefer higher)

**Current baseline** (no tuning):
- FA/24h: ~137.5 (way too high!)
- Sensitivity: ~82%

**Expected after tuning**:
- FA/24h: ~8-10
- Sensitivity: ~60-70%

## Timeline

1. **Dev sweep completion**: ~1-2 hours remaining
2. **Parameter selection**: 30 minutes analysis
3. **Eval run**: 2-3 hours (one-time only)

## Key Files

```
experiments/
├── dev/
│   └── baseline/
│       ├── checkpoint.pkl         # Dev predictions (done)
│       └── sweeps/                # Parameter combinations (running)
│           ├── thr0.70_k5_min2.0_gap0.0/
│           ├── thr0.70_k5_min2.0_gap5.0/
│           └── ... (108 total)
└── eval/
    └── final/                     # Will contain frozen param results
```

## Rules

1. **Never tune on eval set** - That's cheating
2. **Single global parameters** - Same settings for all patients
3. **Run eval only once** - No peeking and re-tuning
4. **Document everything** - Full audit trail in experiments/

## Next Actions

- [ ] Wait for sweep to complete (40/108 done)
- [ ] Analyze sweep_results.csv for best FA/sensitivity trade-off
- [ ] Freeze selected parameters
- [ ] Run single eval with frozen params
- [ ] Report final TAES metrics