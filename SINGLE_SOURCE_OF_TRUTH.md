# SINGLE SOURCE OF TRUTH - SeizureTransformer Evaluation
**Last Verified**: September 14, 2025, 20:54
**DO NOT TRUST ANY OTHER NUMBERS**

## ✅ WHAT ACTUALLY WORKS

### Temple NEDC Binary (v6.0.0) - VERIFIED WORKING
Test run: `experiments/eval/baseline/test_final_fix/`
- Command: `python3 evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py --backend nedc-binary`
- Status: **100% WORKING**

## 🚨 CRITICAL DISCOVERY: merge_gap_sec CHANGES EVERYTHING!

### WITH merge_gap_sec=5.0 (Sep 13 results):
**Parameters**: t=0.8, k=5, m=2.0, **merge_gap=5.0**
- **NEDC TAES**: 24.71% / 60.83 FA/24h
- **NEDC OVERLAP**: 45.63% / 25.01 FA/24h

### WITHOUT merge_gap_sec (Sep 14 results):
**Parameters**: t=0.8, k=5, m=2.0, **merge_gap=None**
- **NEDC TAES**: ? % / 137.53 FA/24h
- **NEDC OVERLAP**: 45.63% / 100.06 FA/24h

**IMPACT**: The merge_gap parameter reduces FA by ~4X!

## ❌ WHAT'S BROKEN

### Native OVERLAP Scorer
- Error: `ModuleNotFoundError: No module named 'seizure_evaluation'`
- Status: **BROKEN** - import path issue

### SzCORE Scorer
- Error: `ModuleNotFoundError: No module named 'evaluation'`
- Status: **BROKEN** - import path issue
- Note: Code exists at `evaluation/szcore_scoring/run_szcore.py` but can't run

## 🚫 FALSE CLAIMS TO IGNORE

These numbers were WRONG and should be ignored:
- "60.83 FA/24h for TAES" - WRONG manual calculation
- "25.01 FA/24h for OVERLAP" - WRONG manual calculation
- "Native OVERLAP is working" - FALSE, it's broken
- "SzCORE is fully implemented" - FALSE, it's broken

## 📊 PARAMETERS TO TEST

We need to test these 42 combinations (7 thresholds × 6 min_durations):
- Thresholds: [0.80, 0.85, 0.90, 0.92, 0.94, 0.96, 0.98]
- Min durations: [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
- Kernel: FIXED at 5 (don't change!)

## 🎯 TARGET OPERATING POINTS

Need to find parameters that achieve:
1. **10 ± 1 FA/24h** - Record exact FA (e.g., 10.2)
2. **2.5 ± 0.5 FA/24h** - Record exact FA (e.g., 2.3)
3. **1.0 ± 0.2 FA/24h** - Record exact FA (e.g., 0.9)

## NEXT STEPS

1. Fix import paths for Native OVERLAP and SzCORE
2. Run systematic parameter sweep with Temple NEDC only
3. Update all documentation with correct numbers

**TRUST ONLY ACTUAL TEST OUTPUTS, NOT MANUAL CALCULATIONS**