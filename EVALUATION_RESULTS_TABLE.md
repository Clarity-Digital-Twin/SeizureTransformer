# SeizureTransformer TUSZ Evaluation Results - Complete Comparison

## Dataset: TUSZ v2.0.3 eval set (865 files, ~127.6 hours, 469 seizures)

## All Scoring Methods Comparison

| Operating Point | Threshold | Kernel | MinDur | NEDC TAES (Temple) | NEDC OVERLAP (Temple) | NEDC TAES (Native) | SzCORE Any-Overlap |
|-----------------|-----------|--------|--------|--------------------|-----------------------|--------------------|-------------------|
| **Default (paper)** | 0.800 | 5 | 2.0s | [24.15% / 137.5 FA](#default-temple) | *pending* | 24.06% / 137.5 FA | [52.35% / 8.5 FA](#default-szcore) |
| **10 FA target** | 0.880 | 7 | 2.5s | *pending* | *pending* | 17.27% / 10.0 FA | *pending* |
| **2.5 FA target** | 0.930 | 11 | 5.0s | *pending* | *pending* | 10.66% / 2.5 FA | *pending* |
| **1 FA target** | 0.950 | 15 | 7.0s | *pending* | *pending* | 7.89% / 1.0 FA | [17.65% / 0.6 FA](#1fa-szcore) |

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
- **NEDC TAES**: 24.15% sensitivity, 137.5 FA/24h
- **SzCORE**: 52.35% sensitivity, 8.5 FA/24h
- **Gap**: 16x difference in false alarms, 2.2x difference in sensitivity

### 2. Aggressive Tuning (0.95/15/7.0)
- **NEDC TAES**: 7.89% sensitivity, 1.0 FA/24h (native)
- **SzCORE**: 17.65% sensitivity, 0.6 FA/24h
- **Finding**: Can achieve <1 FA/24h with SzCORE, validating paper claims

### 3. Scoring Method Impact
- SzCORE's lenient parameters (30s/60s tolerance, event merging) create massive gap
- Even Temple's OVERLAP (pending) will likely show ~45% sensitivity based on NEDC docs
- Competition metrics (SzCORE) vs Clinical metrics (NEDC) serve different purposes

## Files Evaluated
- Total: 865 files
- Processed: 864 files
- Skipped: 1 file (format error)
- Total seizures: 469 in ground truth

## Next Steps
1. Extract NEDC OVERLAP scores from existing Temple binary results
2. Run SzCORE on 10 FA and 2.5 FA operating points
3. Create visualization comparing all scoring methods
4. Document clinical implications of each metric

## Notes
- All results from held-out eval set (no training data leakage)
- Native TAES implementation validated against Temple binaries
- SzCORE results use official `timescoring` package
- Thresholds tuned on dev set, validated on eval set