# OVERLAP Fix Cleanup Summary

## What Was Wrong

1. **We were parsing Temple's OVERLAP section** (45.63% sensitivity) but using the wrong algorithm
2. **Our TAESScorer used greedy 1-to-1 matching** which is incorrect for OVERLAP scoring
3. **Senior reviewer caught this**: We don't need fractional TAES, we need OVERLAP scoring

## What We Fixed

### 1. Created Correct OVERLAP Scorer
- ✅ `seizure_evaluation/taes/overlap_scorer.py` - NEW, implements exact Temple OVERLAP logic
- Any ref with ANY overlap = hit (not 1-to-1 constrained)
- Any hyp with ANY overlap = not a false alarm

### 2. Updated Pipeline
- ✅ `evaluation/nedc_scoring/run_nedc.py` now imports `OverlapScorer` instead of `TAESScorer`
- ✅ Changed metric accumulation from TP/FP/FN to hits/misses/false_alarms

### 3. Verified with Edge Cases
- ✅ Created `tests/test_overlap_edge_cases.py` proving the difference:
  - Case A: 1 hyp spans 2 refs → OVERLAP: 100% sens, Greedy: 50% sens ✓
  - Case B: 2 hyps overlap 1 ref → OVERLAP: 0 FA, Greedy: 864 FA/24h ✓

## Files Status

### Active/Correct Files
- `seizure_evaluation/taes/overlap_scorer.py` - CORRECT OVERLAP implementation
- `evaluation/nedc_scoring/run_nedc.py` - FIXED to use OverlapScorer

### Legacy/Redundant Files (Still Exist but Not Used)
- `seizure_evaluation/taes/scorer.py` - OLD greedy 1-to-1 matcher (NO LONGER IMPORTED)
  - Could be deleted OR kept for reference/other use cases
  - Currently NOT imported anywhere in the pipeline

### Incorrect Documentation (Should be Updated)
- `TEMPLE_PARITY_FIX_PLAN.md` - Was updated by senior to correct approach
- `MATHEMATICAL_COMPARISON_TEMPLE_VS_NATIVE.md` - Talks about fractional TAES (wrong focus)

## What's Clean Now

✅ **No redundant parallel implementations in use**
- Pipeline uses ONLY the OverlapScorer
- Old TAESScorer is orphaned (not imported)
- No references to "fractional TAES" in active code

## Next Steps

1. **Test full pipeline** with new OverlapScorer on dev/eval sets
2. **Verify parity** with Temple OVERLAP section (should now match exactly)
3. **Optional cleanup**:
   - Delete or archive `scorer.py` if confirmed unused
   - Update mathematical comparison doc to focus on OVERLAP vs greedy

## Key Learning

The senior reviewer was absolutely right: We were comparing apples to oranges:
- Temple OVERLAP: Any-overlap counting
- Our old TAESScorer: Greedy 1-to-1 matching
- The fix: Use exact OVERLAP logic, not fractional TAES

The codebase is now clean with no parallel/redundant implementations actively used.