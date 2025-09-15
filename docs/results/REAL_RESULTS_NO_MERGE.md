# 🔴 REAL RESULTS - NO MERGE_GAP (NO CHEATING)

For the full 4×3 results across all scoring methods and operating points, see `FINAL_COMPREHENSIVE_RESULTS_TABLE.md`.

**Date**: September 15, 2025, 3:30 AM  
**Dataset**: TUSZ v2.0.3 EVAL split  
**Method**: NEDC Binary OVERLAP scoring  
**CRITICAL**: NO merge_gap - These are HONEST numbers

---

## THE TRUTH

| Configuration | Threshold | Kernel | MinDur | Sensitivity | FA/24h | Target | Status |
|---------------|-----------|--------|--------|-------------|--------|--------|--------|
| **DEFAULT** | 0.8 | 5 | 2.0s | 45.63% | **26.89** | - | ❌ Too high |
| **10 FA** | 0.88 | 5 | 3.0s | 33.90% | **10.27** | 10 | ❌ Near |
| **2.5 FA** | 0.95 | 5 | 5.0s | 14.50% | **2.05** | 2.5 | ✅ Met |

---

## 🔴 HARSH REALITY

**Clinical viability (≤10 FA/24h and ≥50% sensitivity) is not achieved at any setting**

- Best "10 FA target" under OVERLAP: **10.27 FA/24h** at **33.90% sens** (below 50% sens)
- Best "2.5 FA target" under OVERLAP: **2.05 FA/24h** at **14.50% sens** (FA met; sens too low)
- TAES at corresponding settings remains far above FA targets (e.g., 83.88 and 10.64 FA/24h)

---

## Why Previous Results Were Wrong

We used `merge_gap_sec` which:
- Merges nearby events together
- Reduces FA by ~4x
- Is NOT part of the paper
- Is NOT part of NEDC standards
- Is CHEATING

With merge_gap enabled, FA/24h can drop by ~3–4× (non‑standard).  
Without merge_gap (policy), the honest numbers are those reported above.

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
