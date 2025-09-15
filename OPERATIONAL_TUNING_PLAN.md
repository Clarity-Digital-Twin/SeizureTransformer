# Operational Parameter Tuning Plan
**Created**: September 14, 2025
**Purpose**: Systematic parameter tuning with clear tracking

## 🎯 Tuning Strategy

### Fixed Parameters (DO NOT CHANGE)
```python
KERNEL_SIZE = 5  # Wu et al. default - DO NOT INCREASE!
```

### Parameters to Tune
```python
# Include paper default (0.80, 2.0)
thresholds = [0.80, 0.85, 0.90, 0.92, 0.94, 0.96, 0.98]
min_durations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]

# Paper default: threshold=0.80, kernel=5, min_duration=2.0
# Source: Wu et al. 2025, "80% threshold" (Table I)
```

### Target Operating Points
1. **Paper Default**: 0.80/5/2.0 → ~100.06 FA/24h (NEDC OVERLAP baseline)
2. **10 FA/24h** (±1.0 tolerance) - Record EXACT value (e.g., 10.2)
3. **2.5 FA/24h** (±0.5 tolerance) - Record EXACT value (e.g., 2.6)
4. **1 FA/24h** (±0.2 tolerance) - Record EXACT value (e.g., 0.9)

## 📊 Scoring Methods to Run

For EACH parameter combination, we run ALL 4 scorers:

1. **Temple NEDC Binary TAES** (`nedc-binary-taes`)
   - Strictest clinical standard
   - Time-aligned fractional scoring

2. **Temple NEDC Binary OVERLAP** (`nedc-binary-overlap`)
   - Any-overlap binary scoring
   - Temple's implementation

3. **Native OVERLAP** (`native-overlap`)
   - Our Python implementation
   - Should match Temple OVERLAP ±0.1%

4. **SzCORE Any-Overlap** (`szcore`)
   - Competition standard
   - 30s/60s tolerance windows

## 🔧 Execution Commands

### Step 1: Parameter Sweep Script
```bash
#!/bin/bash
# sweep_all_params.sh

CHECKPOINT="/mnt/c/Users/JJ/Desktop/Clarity-Digital-Twin/SeizureTransformer/experiments/eval/baseline/checkpoint.pkl"
KERNEL=5  # FIXED - DO NOT CHANGE

for thresh in 0.80 0.85 0.90 0.92 0.94 0.96 0.98 0.99; do
  for min_dur in 2.0 3.0 4.0 5.0 6.0 7.0 8.0; do

    OUTPUT_DIR="results_t${thresh}_k${KERNEL}_m${min_dur}"

    echo "========================================="
    echo "Testing: thresh=$thresh, kernel=$KERNEL, min_dur=$min_dur"
    echo "========================================="

    # Run NEDC (Temple binary)
    python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py \
      --checkpoint $CHECKPOINT \
      --outdir $OUTPUT_DIR/nedc_taes \
      --backend nedc-binary \
      --threshold $thresh --kernel $KERNEL --min_duration_sec $min_dur

    # Run Native OVERLAP (parity with Temple OVERLAP)
    python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py \
      --checkpoint $CHECKPOINT \
      --outdir $OUTPUT_DIR/native_overlap \
      --backend native-taes \
      --threshold $thresh --kernel $KERNEL --min_duration_sec $min_dur

    # Run SzCORE Any-Overlap
    python -m evaluation.szcore_scoring.run_szcore \
      --checkpoint $CHECKPOINT \
      --outdir $OUTPUT_DIR/szcore \
      --threshold $thresh --kernel $KERNEL --min_duration_sec $min_dur

  done
done
```

### Step 2: Results Collection
```python
# collect_results.py
import json
import glob

results = []
for result_dir in glob.glob("results_t*_k*_m*"):
    # Extract parameters from dirname
    parts = result_dir.split('_')
    thresh = float(parts[1][1:])
    kernel = int(parts[2][1:])
    min_dur = float(parts[3][1:])

    # Collect metrics from each scorer
    metrics = {
        'threshold': thresh,
        'kernel': kernel,
        'min_duration': min_dur,
        'taes': load_taes_metrics(result_dir),
        'overlap_temple': load_overlap_temple(result_dir),
        'overlap_native': load_overlap_native(result_dir),
        'szcore': load_szcore_metrics(result_dir)
    }
    results.append(metrics)

# Save to tracking table
save_results_table(results)
```

## 📋 Results Tracking Table

Results will be tracked in `docs/evaluation/TUNING_RESULTS_TRACKER.md`:

| Params | TAES Sen/FA | Overlap Temple Sen/FA | Overlap Native Sen/FA | SzCORE Sen/FA | Best For (Exact FA) |
|--------|-------------|----------------------|----------------------|---------------|--------------------|
| t0.80_k5_m2.0 | TBD/TBD | 45.63/100.06 | 45.63/100.06 | 52.35/8.46 | Paper Default (100.06) |
| t0.85_k5_m3.0 | TBD | TBD | TBD | TBD | - |
| t0.90_k5_m4.0 | TBD | TBD | TBD | TBD | - |
| ... | ... | ... | ... | ... | ... |

## ⚠️ Critical Rules

1. **NEVER increase kernel above 5** - it increases FA!
2. **Always run all 4 scorers** - for complete comparison
3. **Record exact parameters** - no ambiguity
4. **Test on eval set only** - dev set for initial exploration
5. **Verify event counts** - sanity check for each run

## 🎬 Execution Order

1. **Clean slate**: Archive all old results ✅
2. **Run sweep**: Execute parameter combinations
3. **Collect metrics**: Parse all results systematically
4. **Find targets**: Identify params that hit 10/2.5/1 FA targets
5. **Update docs**: Final verified numbers in README

## 📝 Output Files Structure

```
experiments/eval/baseline/
├── archived_bad_params/     # Old incorrect results
├── checkpoint.pkl           # Base predictions
├── results_default/         # Verified default params
└── sweep_results/           # New systematic sweep
    ├── results_t0.80_k5_m2.0/
    │   ├── nedc_taes/
    │   ├── nedc_overlap/
    │   ├── native_overlap/
    │   └── szcore/
    ├── results_t0.85_k5_m3.0/
    └── ...
```

## 🚀 Ready to Execute?

Once this plan is approved:
1. Create the sweep script
2. Run systematically
3. Track everything in the table
4. No more confusion!
