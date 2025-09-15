# FINAL SCORES COLLECTION - SYSTEMATIC RECORDING

## 1. DEFAULT CONFIGURATION (Paper: thr=0.8, kernel=5, min_dur=2.0, gap=0)

### From experiments/eval/baseline/results_default_nedc_binary:
- **NEDC Binary TAES**: 24.71% sensitivity, 14.80 FA/24h (SEIZ label)
- **NEDC Binary OVERLAP**: 45.63% sensitivity, 13.92 FA/24h (SEIZ label)

### From experiments/dev/baseline/sweeps CSV (thr0.80_k5_min2.0_gap0.0):
- **Native TAES (from sweep)**: 30.51% sensitivity, 107.29 FA/24h

### CONFUSION - Why different FA rates?
- eval baseline: 14.80 FA/24h
- dev sweep: 107.29 FA/24h
- Something is WRONG here!

---

## 2. 10 FA/24h TARGET (thr=0.95, kernel=5, min_dur=2.0, gap=5.0)

### From experiments/dev/baseline/sweeps CSV:
- **Native TAES**: 13.67% sensitivity, 9.97 FA/24h
- **NEDC Binary TAES**: TBD
- **NEDC Binary OVERLAP**: TBD
- **Native OVERLAP**: TBD

---

## 3. 2.5 FA/24h TARGET (thr=0.95, kernel=11, min_dur=8.0, gap=10.0)

### From experiments/dev/baseline/sweeps CSV:
- **Native TAES**: 8.19% sensitivity, 2.48 FA/24h
- **NEDC Binary TAES**: TBD
- **NEDC Binary OVERLAP**: TBD
- **Native OVERLAP**: TBD

---

## CRITICAL ISSUE

We have INCONSISTENT FA rates for DEFAULT:
- Some results show ~14 FA/24h
- Others show ~107 FA/24h
- Paper claims 134 FA/24h

Need to identify which is correct!