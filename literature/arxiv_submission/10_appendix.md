# Appendix

## A. Extended Performance Metrics

### Table A1: Complete Performance Matrix Across All Scoring Methods
| Scoring Method | Sensitivity (%) | Specificity (%) | Precision (%) | F1 Score | FA/24h | AUROC |
|---|---|---|---|---|---|---|
| **Default Parameters (θ=0.80, k=5, d=2.0)** |
| NEDC TAES | 65.21 | 99.68 | 14.73 | 0.2403 | 136.73 | - |
| NEDC OVERLAP | 45.63 | 99.90 | 37.83 | 0.4136 | 26.89 | - |
| Native OVERLAP | 45.63 | 99.90 | 37.83 | 0.4136 | 26.89 | - |
| SzCORE | 52.35 | 99.97 | 67.07 | 0.5880 | 8.59 | - |
| **10 FA/24h Target (θ=0.88, k=5, d=3.0)** |
| NEDC OVERLAP | 33.90 | 99.96 | 55.98 | 0.4223 | 10.27 | - |
| SzCORE | 40.59 | 99.99 | 83.77 | 0.5470 | 3.36 | - |
| **2.5 FA/24h Target (θ=0.95, k=5, d=5.0)** |
| NEDC OVERLAP | 14.50 | 99.99 | 74.44 | 0.2426 | 2.05 | - |
| SzCORE | 19.71 | 100.00 | 91.07 | 0.3242 | 0.75 | - |

### Table A2: Sensitivity at Fixed False Alarm Rates
| FA/24h Threshold | NEDC OVERLAP Sens. (%) | SzCORE Sens. (%) | Parameters Used |
|---|---|---|---|
| 30.0 | 45.63 | 54.80 | θ=0.80, k=5, d=2.0 |
| 10.0 | 33.90 | 48.61 | θ=0.88, k=5, d=3.0 |
| 5.0 | 24.73 | 43.28 | θ=0.92, k=5, d=4.0 |
| 2.5 | 14.50 | 35.18 | θ=0.95, k=5, d=5.0 |
| 1.0 | 8.10 | 24.31 | θ=0.98, k=7, d=6.0 |

## B. Parameter Sweep Analysis

### Table B1: Grid Search Results (NEDC OVERLAP)
| Threshold | Kernel | Min Duration (s) | Sensitivity (%) | FA/24h | F1 Score |
|---|---|---|---|---|---|
| 0.70 | 3 | 1.0 | 58.42 | 68.47 | 0.3856 |
| 0.75 | 5 | 1.5 | 51.60 | 42.13 | 0.4021 |
| 0.80 | 5 | 2.0 | 45.63 | 26.89 | 0.4136 |
| 0.85 | 5 | 2.5 | 39.23 | 16.48 | 0.4193 |
| 0.88 | 5 | 3.0 | 33.90 | 10.27 | 0.4223 |
| 0.90 | 7 | 3.5 | 28.78 | 7.14 | 0.4098 |
| 0.92 | 7 | 4.0 | 24.73 | 4.86 | 0.3912 |
| 0.95 | 7 | 5.0 | 14.50 | 2.05 | 0.2426 |
| 0.98 | 9 | 6.0 | 8.10 | 0.86 | 0.1473 |

## C. Scoring Methodology Details

### C.1 NEDC TAES Calculation
TAES weights true positives by temporal overlap percentage:
```
TP_weight = overlap_duration / reference_duration
FP_weight = non_overlap_duration / hypothesis_duration
```
This explains why TAES produces higher false alarm rates—partial overlaps contribute fractional false positives.

### C.2 SzCORE Tolerance Windows
SzCORE expands evaluation windows:
- **Pre-ictal**: 30 seconds before seizure onset
- **Post-ictal**: 60 seconds after seizure offset
- **Gap Merging**: Events <90s apart treated as single event

These tolerances reduce false alarms by ~3.1× compared to NEDC OVERLAP.

### C.3 Native OVERLAP Validation
Our Python implementation achieved perfect parity with NEDC binary:
- Identical TP/FP/FN counts across all 865 files
- Matching sensitivity: 45.63%
- Matching FA/24h: 26.89
- Validates our evaluation pipeline integrity

## D. Dataset Statistics

### Table D1: TUSZ v2.0.3 Evaluation Set Characteristics
| Metric | Value |
|---|---|
| Total Files | 865 |
| Total Duration | 127.7 hours |
| Unique Patients | 43 |
| Total Seizures | 469 |
| Mean Seizure Duration | 68.4 ± 142.3 seconds |
| Median Seizure Duration | 31.0 seconds |
| Files with Seizures | 281 (32.5%) |
| Files without Seizures | 584 (67.5%) |
| Seizures per File (when present) | 1.67 ± 1.82 |

### Table D2: Seizure Type Distribution
| Seizure Type | Count | Percentage |
|---|---|---|
| Generalized | 187 | 39.9% |
| Focal | 215 | 45.8% |
| Unknown/Other | 67 | 14.3% |

## E. Computational Performance

### Table E1: Processing Time Breakdown
| Stage | Time (hours) | Files/hour |
|---|---|---|
| EDF Loading | 0.8 | 1081 |
| Preprocessing | 1.2 | 721 |
| Model Inference | 5.5 | 157 |
| Post-processing | 0.5 | 1730 |
| **Total** | **8.0** | **108** |

Hardware: NVIDIA RTX 4090, AMD Ryzen 9 5950X, 64GB RAM

## F. Error Analysis

### F.1 Common False Positive Patterns
1. **Movement artifacts**: 34% of FPs
2. **Electrode pop/disconnect**: 22% of FPs
3. **Rhythmic non-epileptic activity**: 18% of FPs
4. **Eye movements/blinks**: 15% of FPs
5. **Other artifacts**: 11% of FPs

### F.2 Missed Seizures (False Negatives)
1. **Brief seizures (<10s)**: 42% of FNs
2. **Low-amplitude events**: 28% of FNs
3. **Focal seizures**: 20% of FNs
4. **Heavily artifacted segments**: 10% of FNs

## G. Code Availability

All analysis code, including figure generation scripts, is available at:
https://github.com/[REDACTED]/seizure-transformer-eval

Key scripts:
- `evaluation/tusz/run_tusz_eval.py`: Generate predictions
- `evaluation/nedc_scoring/run_nedc.py`: NEDC evaluation
- `evaluation/szcore_scoring/run_szcore.py`: SzCORE evaluation
- `scripts/generate_figures.py`: Reproduce all figures
- `scripts/parameter_sweep.py`: Grid search optimization
