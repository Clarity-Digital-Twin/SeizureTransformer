# 🔴 REAL RESULTS - NO MERGE_GAP (NO CHEATING)

**Date**: September 15, 2025, 3:30 AM  
**Dataset**: TUSZ v2.0.3 EVAL split  
**Method**: NEDC Binary OVERLAP scoring  
**CRITICAL**: NO merge_gap - These are HONEST numbers

---

## THE TRUTH

| Configuration | Threshold | Kernel | MinDur | Sensitivity | FA/24h | Target | Status |
|---------------|-----------|--------|--------|-------------|--------|--------|--------|
| **DEFAULT** | 0.8 | 5 | 2.0s | 45.63% | **100.06** | - | ❌ Too high |
| **10 FA** | 0.95 | 5 | 2.0s | 23.45% | **39.50** | 10 | ❌ FAILED |
| **2.5 FA** | 0.95 | 11 | 8.0s | 11.51% | **8.09** | 2.5 | ❌ FAILED |

---

## 🔴 HARSH REALITY

**WE CANNOT ACHIEVE CLINICAL FA TARGETS WITHOUT CHEATING**

- Best we can do for "10 FA target": **39.50 FA/24h** (4x over target)
- Best we can do for "2.5 FA target": **8.09 FA/24h** (3x over target)
- To get <10 FA, we'd need even higher thresholds, killing sensitivity further

---

## Why Previous Results Were Wrong

We used `merge_gap_sec` which:
- Merges nearby events together
- Reduces FA by ~4x
- Is NOT part of the paper
- Is NOT part of NEDC standards
- Is CHEATING

With merge_gap=5.0, we got 9.97 FA (looked great!)  
Without merge_gap, we get 39.50 FA (reality!)

---

## What This Means

1. **SeizureTransformer on TUSZ cannot meet clinical FA targets** with standard NEDC scoring
2. **The 100x FA problem is real** - Default gives 100 FA/24h
3. **Even extreme tuning** (0.95 threshold) only reduces to ~40 FA/24h
4. **We need different approaches** - not just threshold tuning

---

## Next Steps

1. Update all documentation with REAL numbers
2. Remove merge_gap functionality completely
3. Acknowledge that model needs improvement for clinical use
4. Consider alternative approaches (patient-specific tuning, different architectures)

---

**Location**: `experiments/eval/baseline/CLEAN_NO_MERGE/`  
**Verified**: These are the TRUE numbers without any post-processing tricks