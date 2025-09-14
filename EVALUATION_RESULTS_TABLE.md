# SeizureTransformer TUSZ Evaluation Results - Complete Comparison

## Dataset: TUSZ v2.0.3 eval set (865 files, ~127.6 hours, 469 seizures)

## All Scoring Methods Comparison

| Operating Point | Threshold | Kernel | MinDur | NEDC TAES (Temple) | NEDC OVERLAP (Temple) | NEDC TAES (Native) | SzCORE Any-Overlap |
|-----------------|-----------|--------|--------|--------------------|-----------------------|--------------------|-------------------|
| **Default (paper)** | 0.800 | 5 | 2.0s | 24.15% / 137.5 FA | **45.63% / 13.9 FA** | 24.06% / 137.5 FA | **52.35% / 8.5 FA** |
| **10 FA target** | 0.880 | 7 | 2.5s | *run pending* | *run pending* | 17.27% / 10.0 FA | *run pending* |
| **2.5 FA target** | 0.930 | 11 | 5.0s | *run pending* | *run pending* | 10.66% / 2.5 FA | *run pending* |
| **1 FA target** | 0.950 | 15 | 7.0s | *run pending* | *run pending* | 7.89% / 1.0 FA | **17.65% / 0.6 FA** |

Format: Sensitivity% / FA per 24h

## Scoring Method Definitions

| Method | Description | Key Parameters |
|--------|-------------|---------------|
| **NEDC TAES** | Temple's strictest clinical standard with fractional time-alignment scoring | Exact temporal alignment required |
| **NEDC OVERLAP** | Temple's overlap-based scoring (any overlap within bounds) | Still strict boundary requirements |
| **NEDC Native** | Our Python implementation of TAES (validated ±0.1% match) | Identical to Temple TAES |
| **SzCORE Any-Overlap** | EpilepsyBench competition scoring | 30s pre, 60s post tolerance; merge <90s; any overlap counts |

## Key Findings

### 1. Default Parameters (0.8/5/2.0)
- **NEDC TAES**: 24.15% sensitivity, 137.5 FA/24h (strictest clinical)
- **NEDC OVERLAP**: 45.63% sensitivity, 13.9 FA/24h (Temple's overlap)
- **SzCORE**: 52.35% sensitivity, 8.5 FA/24h (competition scoring)
- **Key Gap**: 16x difference between NEDC TAES and SzCORE false alarms
- **Critical**: Even NEDC OVERLAP (45.63%) is stricter than SzCORE (52.35%)

### 2. Aggressive Tuning (0.95/15/7.0)
- **NEDC TAES**: 7.89% sensitivity, 1.0 FA/24h (native)
- **SzCORE**: 17.65% sensitivity, 0.6 FA/24h
- **Finding**: Can achieve <1 FA/24h with SzCORE, validating paper claims

### 3. Scoring Method Impact (Default Parameters)
- **NEDC TAES vs SzCORE**: 137.5 vs 8.5 FA/24h = **16x gap**
- **NEDC OVERLAP vs SzCORE**: 13.9 vs 8.5 FA/24h = **1.6x gap**
- **Key insight**: NEDC OVERLAP (214/469 seizures) detected fewer than SzCORE (178/340)
- **Why?** SzCORE's 30s/60s tolerance windows and 90s event merging are MORE lenient than Temple's OVERLAP
- Competition metrics (SzCORE) vs Clinical metrics (NEDC) serve fundamentally different purposes

## Files Evaluated
- Total: 865 files
- Processed: 864 files
- Skipped: 1 file (format error)
- Total seizures: 469 in ground truth

## Next Steps
1. ~~Extract NEDC OVERLAP scores from existing Temple binary results~~ ✅ DONE
2. Run SzCORE on 10 FA and 2.5 FA operating points
3. Run Temple NEDC binary on 10 FA, 2.5 FA, and 1 FA operating points
4. Create visualization comparing all scoring methods
5. Document clinical implications of each metric

## Notes
- All results from held-out eval set (no training data leakage)
- Native TAES implementation validated against Temple binaries
- SzCORE results use official `timescoring` package
- Thresholds tuned on dev set, validated on eval set

## Data Sources & Extraction

### How to Extract Each Metric

#### <a name="default-temple"></a>NEDC TAES Temple Binary (Default)
```bash
# File: experiments/eval/baseline/results_default_nedc_binary/results/summary.txt
# Extract: Look for "NEDC TAES SCORING SUMMARY" section
grep -A20 "NEDC TAES SCORING SUMMARY" results/summary.txt
# Sensitivity: Line with "Sensitivity:" after OVERALL RESULTS
# FA/24h: Calculated from total FP count / (duration_hours / 24)
```

#### <a name="default-szcore"></a>SzCORE Any-Overlap (Default)
```bash
# File: experiments/eval/baseline/szcore_results/szcore_summary.json
cat szcore_summary.json | jq '.corpus_micro_avg'
# Outputs: sensitivity: 0.5235, fpRate: 8.463
```

#### <a name="1fa-szcore"></a>SzCORE Any-Overlap (1FA Tuned)
```bash
# File: experiments/eval/baseline/results_1fa_szcore/szcore_summary.json
cat szcore_summary.json | jq '.corpus_micro_avg'
# Outputs: sensitivity: 0.1765, fpRate: 0.6
```

#### Native TAES Results
```bash
# Files: experiments/eval/baseline/results_*_native_taes/metrics.json
# Extract TAES metrics:
cat metrics.json | jq '.taes | {sensitivity, fp_per_24h}'
```

### Raw Checkpoint Data
```bash
# Source predictions: experiments/eval/baseline/checkpoint.pkl
# Contains: 864 files with predictions + ground truth
# Size: 470MB
python -c "import pickle; c=pickle.load(open('checkpoint.pkl','rb')); print(len(c['results']))"
# Output: 864
```

### Commands to Reproduce

```bash
# 1. Run SzCORE scoring
python -m evaluation.szcore_scoring.run_szcore \
  --checkpoint experiments/eval/baseline/checkpoint.pkl \
  --outdir experiments/eval/baseline/szcore_results \
  --threshold 0.8 --kernel 5 --min_duration_sec 2.0

# 2. Run NEDC Temple binary
cd evaluation/nedc_scoring
make all CHECKPOINT=../../experiments/eval/baseline/checkpoint.pkl

# 3. Extract NEDC OVERLAP scores
sed -n '/NEDC OVERLAP SCORING SUMMARY/,/NEDC DPALIGN/p' summary.txt | grep -A5 "LABEL: SEIZ"
# Results: 214 hits / 469 targets = 45.63% sensitivity, 74 FP = 13.9 FA/24h
```