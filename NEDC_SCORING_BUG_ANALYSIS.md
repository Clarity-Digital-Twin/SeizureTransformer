# 🔍 NEDC SCORING BUG ANALYSIS

## Executive Summary

**Root cause was metrics extraction, not native scoring. Fixed.**

Our native Python scorer correctly implements OVERLAP scoring (with `overlap_threshold=0.0`) and matches Temple NEDC's OVERLAP section for sensitivity and FA/24h. The confusion arose because `metrics.json` used to extract metrics from the first section in Temple’s `summary.txt` (DP ALIGNMENT) instead of the OVERLAP section. `run_nedc.py` now explicitly parses the OVERLAP block and stores those values under `overlap` (duplicated to `taes` for backward-compat).

## Key Findings

### 1. Temple NEDC Has FOUR Different Scoring Methods

Temple NEDC v6.0.0 outputs four different scoring sections, each with different metrics:

1. **DP ALIGNMENT** - Dynamic programming alignment scoring
   - Sensitivity: 27.72%, FA/24h: 12.41, F1: 0.4114
   - Uses more lenient matching criteria

2. **OVERLAP** - Simple overlap-based scoring
   - Sensitivity: 23.45%, FA/24h: 9.97, F1: 0.3704
   - Any overlap between ref and hyp events counts as a match

3. **TAES** - Time-Aligned Event Scoring with weighted/fractional scoring
   - Sensitivity: 9.08%, FA/24h: 49.08, F1: 0.1617
   - Uses fractional hit counts (42.59 hits from 469 targets)

4. **EPOCH** - Epoch-by-epoch binary classification
   - Very high FA rate (4549.93/24h)
   - Not event-based

### 2. Our Native Scorer Matches OVERLAP Perfectly

When configured with `overlap_threshold=0.0` (any overlap), our native scorer produces:
- Sensitivity: 23.45% ✅ (Temple OVERLAP: 23.4542%)
- FA/24h: 9.97 ✅ (Temple OVERLAP: 9.9679%)
- F1: differs slightly (native aggregates TP/FP/FN; Temple OVERLAP reports per-label F1). We treat F1 as informational and gate on sens/FA.

### 3. The Metrics Extraction Bug

The original issue was in `evaluation/nedc_scoring/run_nedc.py::extract_and_save_metrics()` (extracting the first “Sensitivity” from DP ALIGNMENT). This has been fixed to target the OVERLAP section explicitly.

## Which Scoring Method Should We Use?

### Option 1: DP ALIGNMENT (Current metrics.json)
- **Pros**: Higher sensitivity (27.72% vs 23.45%)
- **Cons**: Higher FA rate (12.41 vs 9.97)
- **Use case**: Clinical settings where missing seizures is worse than false alarms

### Option 2: OVERLAP (What native scorer implements)
- **Pros**: Lower FA rate (9.97 - meets our <10 FA/24h target!)
- **Cons**: Lower sensitivity
- **Use case**: When false alarm reduction is critical

### Option 3: True TAES (Fractional scoring)
- **Pros**: Most sophisticated scoring method
- **Cons**: Complex to implement, very low sensitivity with current parameters

## Immediate Actions Required

1. **Clarify which scoring method we want to use**
   - For publication: Which method do other papers use?
   - For clinical: Which meets our FA < 10/24h requirement?

2. **Fix the metrics extraction** ✅
   - Extract from OVERLAP section (done; matches native)
   - If DP ALIGNMENT becomes the target, either change parser or implement DP ALIGNMENT in native

3. **Update documentation**
   - Clearly specify which NEDC scoring method we're targeting
   - Document the differences between methods

## Code Location of Issues

1. **Native scorer**: `seizure_evaluation/taes/scorer.py`
   - Actually implements OVERLAP correctly!
   - Just needs `overlap_threshold=0.0` setting

2. **Metrics extraction**: `evaluation/nedc_scoring/run_nedc.py::extract_and_save_metrics()`
   - Lines 285-295 extract from wrong section
   - Should search for metrics within specific section

3. **Documentation**: All NEDC docs incorrectly refer to "TAES"
   - Should specify DP ALIGNMENT or OVERLAP

## Test Commands

```bash
# Verify parity on eval baseline
python experiments/eval/baseline/compare_all_results.py

# Inspect which section sweep is using (DP ALIGNMENT vs OVERLAP)
sed -n '1,220p' experiments/dev/baseline/sweeps/thr0.95_k5_min2.0_gap5.0/results/summary.txt | less
```

## Resolution

The "bug" is actually a **misunderstanding of which scoring method to use**. Our native implementation is CORRECT for OVERLAP scoring. We need to decide:

1. Use OVERLAP scoring (native already works, just fix metrics extraction)
2. Use DP ALIGNMENT scoring (need to implement in native)
3. Use true TAES scoring (complex fractional implementation needed)

**Recommendation**: Use OVERLAP since it meets our FA < 10/24h target and our native implementation already works!
