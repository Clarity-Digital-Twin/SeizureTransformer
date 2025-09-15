# Technical Debt: Native Scorer Implementation

## Current State (2025-01-14)

### What We Have
We have implemented a **native Python OVERLAP scorer**, NOT a native TAES scorer as originally intended.

**Location**: `seizure_evaluation/taes/overlap_scorer.py`
- Despite being in a folder named "taes", this is actually an `OverlapScorer` class
- Implements Temple NEDC's OVERLAP scoring method (any-overlap counting)
- Does NOT implement TAES (Time-Aligned Event Scoring with fractional temporal matching)

### Backend Aliases
In `evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py`:
- `--backend native-overlap`: Correctly named, runs native OVERLAP scorer
- `--backend native-taes`: **Misleading alias** - actually runs the same OVERLAP scorer
- `--backend nedc-binary`: Runs Temple's official binary (produces TAES, OVERLAP, DPALIGN, EPOCH)

### Scoring Method Differences

#### OVERLAP Scoring (What We Implemented)
- **Hit**: Any reference event with ANY overlap to ANY hypothesis event
- **Miss**: Reference event with NO overlap to any hypothesis
- **False Alarm**: Hypothesis event with NO overlap to any reference
- No 1-to-1 matching constraint
- Binary scoring: events either overlap or don't

#### TAES Scoring (What We Intended to Implement)
- Fractional temporal alignment scoring
- Considers degree of temporal overlap between events
- More stringent than OVERLAP
- Penalizes poor temporal alignment even when events overlap
- Used for strictest clinical evaluation

### Verification Status

Our native OVERLAP implementation achieves **parity with Temple NEDC OVERLAP** under the verified, non‑merged baseline:
- Default params (0.8/5/2.0, merge_gap=None): Both report 45.63% sensitivity, 26.89 FA/24h (SEIZ), F1≈0.518

Notes:
- Prior numbers showing ~25.01 FA/24h were contaminated by a non‑standard merge_gap and are invalid for academic comparison.
- Tuned rows (e.g., “2.5 FA”, “1 FA”) are pending a fresh sweep with merge_gap=None and are intentionally omitted here.

The native scorer correctly:
- Implements any-overlap counting logic
- Computes BCKG false alarms for Temple's "Total False Alarm Rate"
- Produces metrics matching Temple OVERLAP section within ±0.01%

### JSON Key Confusion

In `run_nedc.py` lines 338-340, we store OVERLAP metrics under both keys:
```python
metrics["overlap"] = { ... }  # Correct key
metrics["taes"] = metrics["overlap"].copy()  # Misleading for backward compatibility
```

This causes `metrics.json` to have a "taes" key that actually contains OVERLAP results.

### Table Labeling Issues

In `EVALUATION_RESULTS_TABLE.md`:
- Column labeled "NEDC TAES (Native)" should be "NEDC OVERLAP (Native)"
- These are just duplicates of Temple OVERLAP, not independent TAES measurements
- This has caused significant confusion in interpreting results

## Technical Debt Items

1. **Misleading Naming**
   - Folder `seizure_evaluation/taes/` contains OVERLAP scorer, not TAES
   - Backend alias `native-taes` runs OVERLAP scoring
   - JSON key `taes` contains OVERLAP metrics

2. **Missing Implementation**
   - We never implemented native TAES scoring with fractional temporal alignment
   - Cannot independently verify Temple TAES results without running their binary

3. **Documentation Gaps**
   - No clear documentation that our "native" implementation is OVERLAP-only
   - Evaluation results table incorrectly labels native scorer as TAES

## Resolution Plan

### Immediate Actions (Do Now)
1. ✅ Document this technical debt clearly (this file)
2. Update `EVALUATION_RESULTS_TABLE.md` to correctly label "Native" as OVERLAP
3. Add warnings in code comments about the misleading aliases

### Future Implementation (When Needed)
1. Implement actual native TAES scorer in `seizure_evaluation/taes/taes_scorer.py`
   - Study Temple NEDC v6.0.0 TAES implementation
   - Implement fractional temporal scoring algorithm
   - Validate against Temple binary TAES outputs
2. Rename current `overlap_scorer.py` more clearly
3. Update backend choices to distinguish:
   - `native-overlap`: Current OVERLAP implementation
   - `native-taes`: Future actual TAES implementation
4. Fix JSON keys to use accurate names

## Why This Is Acceptable For Now

1. **Temple OVERLAP is clinically relevant**: OVERLAP scoring is an official Temple metric used in publications
2. **Parity achieved**: Our native OVERLAP matches Temple's exactly (verified to ±0.01%)
3. **Temple binary available**: We can still get TAES scores via Temple's official binary
4. **Research focus**: For parameter tuning and research, OVERLAP is sufficient
5. **No data corruption**: Results are accurate, just mislabeled

## Summary

**We have a working, accurate native OVERLAP scorer that achieves parity with Temple NEDC.**

The confusion arose from:
- Wanting to implement TAES but building OVERLAP instead
- Poor naming choices (folder, aliases, JSON keys)
- Incomplete documentation

This is **acceptable technical debt** because:
- The implementation is correct for what it does (OVERLAP)
- We can still access TAES via Temple's binary
- OVERLAP is a valid, published clinical metric
- Future TAES implementation can be added without breaking changes

The priority is to fix documentation/labeling now, implement native TAES later if needed.

