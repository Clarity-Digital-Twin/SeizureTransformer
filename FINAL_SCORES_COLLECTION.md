# ⚠️ SUPERSEDED – See FINAL_COMPREHENSIVE_RESULTS_TABLE.md

Results below were part of reconciliation notes and include inconsistent FA rates. For canonical numbers and tables, use:
- `docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md`
- `docs/evaluation/PARAMETER_TUNING_METHODOLOGY.md`

# FINAL SCORES COLLECTION - SYSTEMATIC RECORDING

## 1. DEFAULT CONFIGURATION (Paper: thr=0.8, kernel=5, min_dur=2.0, gap=0)

### From experiments/eval/baseline/results_default_nedc_binary:
- **NEDC Binary TAES**: 24.15% sensitivity, 27.13 FA/24h (SEIZ label)
- **NEDC Binary OVERLAP**: 45.63% sensitivity, 100.06 FA/24h (SEIZ label)

### From experiments/dev/baseline/sweeps CSV (thr0.80_k5_min2.0_gap0.0):
- **Native TAES (from sweep)**: 30.51% sensitivity, 107.29 FA/24h

### CONFUSION - Why different FA rates?
- eval baseline: 14.80 FA/24h
- dev sweep: 107.29 FA/24h
- Something is WRONG here!

---

## 2. 10 FA/24h TARGET (thr=0.95, kernel=5, min_dur=2.0, gap=None)

### From experiments/dev/baseline/sweeps CSV:
- **NEDC Binary TAES**: 8.64% sensitivity, 6.40 FA/24h
- **NEDC Binary OVERLAP**: 23.45% sensitivity, 39.50 FA/24h
- **Native OVERLAP**: TBD

---

## 3. 2.5 FA/24h TARGET (thr=0.95, kernel=11, min_dur=8.0, gap=None)

### From experiments/dev/baseline/sweeps CSV:
- **NEDC Binary TAES**: 4.07% sensitivity, 1.51 FA/24h
- **NEDC Binary OVERLAP**: 11.51% sensitivity, 8.09 FA/24h
- **Native OVERLAP**: TBD

---

## CRITICAL ISSUE

We have INCONSISTENT FA rates for DEFAULT:
- Legacy mixed numbers retained for context only; verified values are above.

Need to identify which is correct!
