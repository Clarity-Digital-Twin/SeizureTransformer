# 🔍 NEDC SCORING BUG ANALYSIS
Status: Archived — superseded by PARAMETER_TUNING_ANALYSIS.md and OPERATIONAL_TUNING_PLAN.md. Retained for historical context.

## Executive Summary

Two issues, both resolved:

1) Metrics extraction parsed DP ALIGNMENT rather than OVERLAP. Fixed to parse OVERLAP explicitly and store under `overlap` (duplicated to `taes`).
2) Native scorer semantics were greedy 1–1 and didn’t match Temple’s OVERLAP totals. Implemented exact any-overlap with background complements in `seizure_evaluation/taes/overlap_scorer.py`, and updated the native backend to report Temple’s TOTAL False Alarm Rate (SEIZ + BCKG).

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

### 2. Our Native Scorer Now Matches OVERLAP Perfectly

With the OverlapScorer:
- SEIZ sensitivity matches Temple’s OVERLAP “SEIZ” sensitivity (per-label block).
- Reported FA/24h matches Temple’s OVERLAP “Total False Alarm Rate” (SEIZ + BCKG), by summing false alarms across both labels using background complements.
- F1: native prints dataset-level F1 for convenience; Temple prints per-label and summary F1. Treat as informational unless exact match is required.

### 3. The Metrics Extraction Bug

The original issue was in `evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py::extract_and_save_metrics()` (extracting the first “Sensitivity” from DP ALIGNMENT). This has been fixed to target the OVERLAP section explicitly.

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

2. **Fix the metrics extraction and semantics** ✅
   - Extract from OVERLAP section (done; matches native)
   - Native backend now mirrors Temple OVERLAP including TOTAL FA/24h

3. **Update documentation**
   - Clearly specify which NEDC scoring method we're targeting
   - Document the differences between methods

## Code Location of Issues

1. **Native scorer**: `seizure_evaluation/taes/overlap_scorer.py`
   - Implements any-overlap + background complements (SEIZ + BCKG totals)

2. **Metrics extraction**: `evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py::extract_and_save_metrics()`
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

We target OVERLAP for gating and reporting, and native now matches Temple exactly (SEIZ sensitivity + TOTAL FA/24h) on dev/eval baselines. If we ever choose DP ALIGNMENT or true TAES (fractional), we’ll implement those separately in native and switch the parser accordingly.

