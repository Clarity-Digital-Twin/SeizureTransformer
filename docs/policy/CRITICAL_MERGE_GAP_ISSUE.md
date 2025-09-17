# 🚨 CRITICAL: merge_gap_sec Parameter Issue

**Status**: RESOLVED (2025-09-15) — Fully removed from evaluation; CI-enforced
**Severity**: CRITICAL - Violates NEDC/Picone evaluation standards
**Date Discovered**: September 14, 2025
**Impact**: 4X difference in false alarm rates (historical)

Update (2025-09-15)
- Removed `merge_gap_sec` from all evaluation CLIs/APIs and codepaths.
- Added CI guards to fail if artifacts contain merge-related fields or disclaimers.
- Documentation and SSOT updated to CLEAN, no-merge numbers (e.g., OVERLAP SEIZ FA = 26.89).
- A standalone helper `merge_nearby_events(...)` remains for notebook experiments only.

## Executive Summary

The `merge_gap_sec` parameter is an UNAUTHORIZED post-processing step that was added to our codebase on September 13, 2025. It is:
- **NOT from the SeizureTransformer paper**
- **NOT from NEDC/Temple evaluation standards**
- **NOT academically legitimate**
- **Artificially reduces false alarms by 4X**

## The Problem

### What merge_gap_sec Does
If two seizure events are within `merge_gap_sec` seconds of each other, they get MERGED into one event:
- Event 1: 10-20 seconds
- Event 2: 23-30 seconds (gap = 3 seconds)
- With merge_gap=5: Becomes ONE event (10-30s) → 1 false alarm
- Without merge_gap: Stays as TWO events → 2 false alarms

### Impact on Metrics
```
WITH merge_gap=5.0:
- NEDC TAES: 60.83 FA/24h
- NEDC OVERLAP: 25.01 FA/24h

WITHOUT merge_gap (correct):
- NEDC TAES: 136.73 FA/24h
- NEDC OVERLAP: 26.89 FA/24h (SEIZ)
```

**This is a 4X artificial improvement!**

## Where It Existed in Code (historical)

### Files Affected:
1. `evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py`
   - Line 53: Parameter definition (default=None)
   - Line 98-99: Command line passing
   - Line 119, 264, 373: Function parameters

2. `evaluation/nedc_eeg_eval/nedc_scoring/convert_predictions.py`
   - Accepts merge_gap_sec parameter
   - Passes to post_processing

3. `evaluation/nedc_eeg_eval/nedc_scoring/post_processing.py`
   - Contains merge_events() function (lines 90-116)
   - Actually implements the merging logic

4. `evaluation/nedc_eeg_eval/nedc_scoring/sweep_operating_point.py`
   - Used in parameter sweeps

5. `src/seizure_evaluation/szcore/cli.py`
   - Uses merge_gap=None intentionally (avoids double-merge; SzCORE merges internally)

## Why This Violates Standards

### NEDC/Picone Requirements:
1. **Time-Aligned Event Scoring (TAES)** requires accurate start/stop times
2. Each event should be scored SEPARATELY
3. Temporal localization is CRITICAL for evaluation
4. Merging events destroys temporal alignment information

### Quote from Picone et al. 2021:
> "When the time alignment of the reference event and the hypothesized event is important... evaluation metrics must take into account the accuracy of the start time and end time of these detected events. We refer to this as the temporal localization problem."

**Merging events DESTROYS temporal localization!**

## Git History

```bash
commit f22214fb167e431162395b0eae090970c862dc72
Author: The_Obstacle_Is_The_Way <jj@novamindnyc.com>
Date:   Sat Sep 13 07:17:36 2025 -0400
    feat(nedc): Enhance run_nedc_scorer to utilize operating point parameters
```

Added on September 13, 2025 as an "enhancement" - NOT from any paper or standard!

## Results Contamination

### Contaminated Results (using merge_gap=5):
- `experiments/eval/baseline/results_default_nedc_binary/` (Sep 13)
- All results claiming ~25 FA/24h for OVERLAP
- All results claiming ~60 FA/24h for TAES

### Clean Results (no merge_gap):
- `experiments/eval/FINAL_CLEAN_RUN/` (Sep 15)
- Shows TRUE performance: 26.89 FA/24h (OVERLAP, SEIZ)

## REQUIRED ACTIONS

### Immediate:
1. ⚠️ **DEPRECATE merge_gap_sec parameter**
2. ⚠️ **Default to None (no merging) for all evaluations**
3. ⚠️ **Re-run ALL evaluations without merge_gap**
4. ⚠️ **Update all documentation with correct numbers**

### Code Changes Needed:
```python
# evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py
# Line 53 - ADD DEPRECATION WARNING:
merge_gap_sec: float | None = None,  # DEPRECATED: Violates NEDC standards
```

### Documentation Updates:
- Update EVALUATION_RESULTS.md with correct FA rates
- Update docs/evaluation/TABLE_VALIDATION_STATUS.md
- Add warnings to all sweep scripts

## Correct Paper Parameters

Per Wu et al. 2025 SeizureTransformer paper:
- **Threshold**: 0.8
- **Morphological kernel**: 5 samples
- **Minimum duration**: 2.0 seconds
- **Merge gap**: NOT MENTIONED (should be None)

## Impact Assessment

### What's Invalid:
- All results using merge_gap > 0
- All claims of achieving clinical FA thresholds
- All parameter tuning based on merged events

### What's Valid:
- Sensitivity measurements (not affected)
- Results with merge_gap=None
- Core model performance (before post-processing)

## Recommendation

1. **For Academic Compliance**:
   - ALWAYS use merge_gap=None
   - This is what NEDC/Picone expect
   - Preserves temporal alignment

2. **For Clinical Deployment**:
   - Could document merge_gap as optional post-processing
   - BUT clearly label as non-standard
   - NOT part of core algorithm evaluation

## Severity: CRITICAL

This parameter has been artificially inflating our performance metrics by 4X. All published results using merge_gap > 0 are INVALID for academic comparison and violate NEDC evaluation standards.

**Verified with paper defaults (no merge):**
- NEDC OVERLAP: 26.89 FA/24h (SEIZ)
- NEDC TAES: 136.73 FA/24h

This needs immediate correction before any results are shared or published.

