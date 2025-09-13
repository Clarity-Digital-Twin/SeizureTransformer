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
# Dev checkpoint (complete)
experiments/dev/baseline/checkpoint.pkl  # ~1.5GB of predictions

# Run parameter sweep (complete)
python evaluation/nedc_scoring/sweep_operating_point.py \
  --checkpoint experiments/dev/baseline/checkpoint.pkl \
  --outdir_base experiments/dev/baseline/sweeps \
  --thresholds 0.70,0.80,0.90,0.95 \
  --kernels 5,11,21 \
  --min_durations 2,4,8 \
  --merge_gaps 0,5,10 \
  --target_fa_per_24h 10
```

This tests 108 combinations and writes:
- `experiments/dev/baseline/sweeps/sweep_results.csv`
- `experiments/dev/baseline/sweeps/recommended_params.json`

**Current Status**: 108/108 combinations complete ✅

### Step 2: Freeze Parameters
**Purpose**: Lock in the best parameters from dev sweep

```bash
# Inspect results
sed -n '1,20p' experiments/dev/baseline/sweeps/sweep_results.csv

# Pick parameters that give:
# - FA/24h ≤ 10 (HARD REQUIREMENT)
# - Highest sensitivity possible among feasible combos

# Recommended (from sweep):
cat experiments/dev/baseline/sweeps/recommended_params.json

# Freeze chosen parameters for eval
cp experiments/dev/baseline/sweeps/recommended_params.json \
   experiments/eval/frozen_params.json
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
- Sensitivity: as high as possible subject to FA ≤ 10

**Observed baseline** (no tuning, TAES):
- FA/24h: ~137.5
- Sensitivity: ~82%

**Observed after sweep (dev set, TAES):**
- Feasible FA ≤ 10 found, but sensitivity is currently low (≈8–12%)
- Example feasible: threshold=0.95, kernel=5, min_duration=2.0s, merge_gap=5.0s

**Recent Evaluation Results (2025-09-13):**
- Temple binary (thr=0.8, k=5, min=2s): Sens=23.45%, FA=9.97/24h, F1=0.370 ✅
- Native TAES (thr=0.95, k=5, min=2s): Sens=7.68%, FA=23.89/24h, F1=0.114 ❌
- Note: Native with thr=0.95 has worse FA than Temple with thr=0.8 (bug in threshold application?)

## Timeline

1. Dev sweep completion: done
2. Parameter selection: done (see recommended_params.json)
3. Eval run: pending (single, with frozen params)

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

## Targeting 1 FA/24h Operating Point

**Goal**: Find parameters that achieve ~1 FA/24h for ultra-low false alarm operation

**Expected tradeoffs**:
- Current best: 23.45% sensitivity at 10 FA/24h (Temple, thr=0.8)
- For 1 FA/24h: Expect sensitivity to drop to ~5-10%
- Need much higher threshold (0.98-0.99) and longer min_duration (8-16s)

**Sweep strategy**:
```bash
# Fine-grained sweep for 1 FA/24h target
python evaluation/nedc_scoring/sweep_operating_point.py \
  --checkpoint experiments/eval/baseline/checkpoint.pkl \
  --outdir_base experiments/eval/baseline/sweeps_1fa \
  --thresholds 0.95,0.97,0.98,0.99 \
  --kernels 5,11,21 \
  --min_durations 4,8,12,16 \
  --merge_gaps 5,10 \
  --target_fa_per_24h 1
```

## Next Actions

- [ ] Run sweep targeting 1 FA/24h operating point
- [ ] Document parity between Temple binary and native TAES
- [ ] Fix native TAES threshold bug (thr=0.95 giving worse FA than thr=0.8)
- [ ] Copy frozen params to `experiments/eval/frozen_params.json`
- [ ] Run single eval with frozen params on eval split
- [ ] Report final TAES metrics (sensitivity, FA/24h, F1)
