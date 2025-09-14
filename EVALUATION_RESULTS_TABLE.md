# SeizureTransformer TUSZ Evaluation Results - Complete Comparison

## Dataset: TUSZ v2.0.3 eval set (865 files, ~127.6 hours, 469 seizures)

## All Scoring Methods Comparison

| Operating Point | Threshold | Kernel | MinDur | NEDC TAES (Temple) | NEDC OVERLAP (Temple) | NEDC OVERLAP (Native)* | SzCORE Any-Overlap |
|-----------------|-----------|--------|--------|--------------------|-----------------------|-----------------------|-------------------|
| **Default (paper)** | 0.800 | 5 | 2.0s | 24.71% / 60.83 FA | **45.63% / 25.01 FA** | 45.63% / 25.01 FA | **52.35% / 8.46 FA** |
| **10 FA target** | 0.880 | 7 | 2.5s | 16.62% / 94.48 FA | 35.61% / 56.05 FA | 35.61% / 56.05 FA | 41.76% / 3.57 FA |
| **2.5 FA target** | 0.930 | 11 | 5.0s | 4.13% / 38.60 FA | 11.51% / 2.45 FA | 11.51% / 2.44 FA | 27.94% / 1.32 FA |
| **1 FA target** | 0.950 | 15 | 7.0s | 0.41% / 34.85 FA | 1.28% / 0.38 FA | 1.28% / 0.38 FA | **17.65% / 0.56 FA** |

Format: Sensitivity% / FA per 24h

† Note: 10FA rerun completed with correct params (`--threshold 0.88 --kernel 7 --min_duration_sec 2.5`).

## Scoring Method Definitions

| Method | Description | Key Parameters |
|--------|-------------|---------------|
| **NEDC TAES** | Temple's strictest clinical standard with fractional time-alignment scoring | Exact temporal alignment required (v6.0.0) |
| **NEDC OVERLAP** | Temple's overlap-based scoring (any overlap within bounds) | Total FA/24h includes SEIZ + BCKG |
| **NEDC OVERLAP (Native)*** | Our Python implementation of OVERLAP scoring | Achieves parity with Temple OVERLAP (±0.01%) |
| **SzCORE Any-Overlap** | EpilepsyBench competition scoring | 30s pre, 60s post tolerance; merge <90s; any overlap counts |

## Key Findings

### 1. Default Parameters (0.8/5/2.0)
- **NEDC TAES (Temple)**: 24.71% sensitivity, 60.83 FA/24h (total)
- **NEDC OVERLAP (Temple)**: 45.63% sensitivity, 25.01 FA/24h (total)
- **SzCORE**: 52.35% sensitivity, 8.46 FA/24h (competition scoring)
- **Key Gap**: ~7.2x fewer FAs for SzCORE vs TAES total (60.83 → 8.46)
- **Note**: Temple OVERLAP total FA (25.01) > SzCORE FA (8.46)

### 2. Aggressive Tuning (0.95/15/7.0)
- **NEDC TAES (Temple)**: 0.41% sensitivity, 34.85 FA/24h (total)
- **NEDC OVERLAP (Temple)**: 1.28% sensitivity, 0.38 FA/24h (total)
- **SzCORE**: 17.65% sensitivity, 0.56 FA/24h
- **Finding**: <1 FA/24h achievable with SzCORE and Temple OVERLAP; TAES remains much stricter

### 3. Scoring Method Impact (Default Parameters)
- **TAES total FA vs SzCORE**: 60.83 vs 8.46 FA/24h = ~7.2x gap
- **OVERLAP total FA vs SzCORE**: 25.01 vs 8.46 FA/24h = ~3.0x gap
- **Counts vs percents**: Temple uses 469 targets; SzCORE summary used 340 targets in checkpoint annotations. Percentages are comparable; raw counts differ.
- **Why?** SzCORE uses 30s/60s tolerance with 90s merge (more permissive) vs Temple boundary rules
- Clinical (NEDC) vs competition (SzCORE) target different use-cases

## Files Evaluated
- Total: 865 files
- Processed: 864 files
- Skipped: 1 file (format error)
- Total seizures: 469 in ground truth

## Next Steps
1. ~~Extract NEDC OVERLAP scores from existing Temple binary results~~ ✅ DONE
2. ~~Run SzCORE on 10 FA and 2.5 FA operating points~~ ✅ DONE
3. Rerun 10FA with correct params — DONE
4. Create visualization comparing all scoring methods
5. Document clinical implications of each metric

## Notes
- All results from held-out eval set (no training data leakage)
- Native OVERLAP implementation parity-checked with Temple binaries
- SzCORE results use official `timescoring` package
- Thresholds tuned on dev set, validated on eval set
- *Native column shows our Python OVERLAP implementation (NOT TAES) - see TECHNICAL_DEBT_NATIVE_SCORER.md

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

#### Native OVERLAP Results
```bash
# Files: experiments/eval/baseline/results_*_nedc_native/metrics.json
# Extract OVERLAP metrics (stored under 'taes' key for backward compatibility):
cat metrics.json | jq '.taes | {sensitivity, fp_per_24h}'
# Note: Despite the 'taes' key name, these are OVERLAP metrics
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

**⚠️ CRITICAL: 10FA row needs rerun with correct parameters!**
```bash
# FIX 10FA: Run these commands to get correct 10FA results
python evaluation/nedc_scoring/run_nedc.py \
  --checkpoint experiments/eval/baseline/checkpoint.pkl \
  --outdir experiments/eval/baseline/results_10fa_nedc_binary \
  --threshold 0.88 --kernel 7 --min_duration_sec 2.5 \
  --backend nedc-binary --force

python evaluation/nedc_scoring/run_nedc.py \
  --checkpoint experiments/eval/baseline/checkpoint.pkl \
  --outdir experiments/eval/baseline/results_10fa_nedc_native \
  --threshold 0.88 --kernel 7 --min_duration_sec 2.5 \
  --backend native-overlap --force
```

```bash
# 1. Run SzCORE scoring (default)
python -m evaluation.szcore_scoring.run_szcore \
  --checkpoint experiments/eval/baseline/checkpoint.pkl \
  --outdir experiments/eval/baseline/szcore_results \
  --threshold 0.8 --kernel 5 --min_duration_sec 2.0

# 2. Run NEDC Temple binary (produces TAES/OVERLAP/DPALIGN/EPOCH)
cd evaluation/nedc_scoring
make all CHECKPOINT=../../experiments/eval/baseline/checkpoint.pkl

# 3. Extract NEDC OVERLAP (Temple) totals
sed -n '/NEDC OVERLAP SCORING SUMMARY/,/NEDC/p' experiments/eval/baseline/results_default_nedc_binary/results/summary.txt | \
  awk '/SUMMARY:/,0' | sed -n '1,40p'
# Look for: "Total False Alarm Rate: 25.0138 per 24 hours" and Sensitivity in PER LABEL: SEIZ (45.6290%)

# 4. Run SzCORE for other operating points
python -m evaluation.szcore_scoring.run_szcore \
  --checkpoint experiments/eval/baseline/checkpoint.pkl \
  --outdir experiments/eval/baseline/results_10fa_szcore \
  --threshold 0.88 --kernel 7 --min_duration_sec 2.5
python -m evaluation.szcore_scoring.run_szcore \
  --checkpoint experiments/eval/baseline/checkpoint.pkl \
  --outdir experiments/eval/baseline/results_2.5fa_szcore \
  --threshold 0.93 --kernel 11 --min_duration_sec 5.0
```
