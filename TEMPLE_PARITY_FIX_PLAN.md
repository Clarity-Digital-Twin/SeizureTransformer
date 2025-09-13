# TEMPLE NEDC FULL PARITY FIX PLAN

## THE PROBLEM

Our Native TAES implementation uses **binary matching** (event matches or doesn't), while Temple NEDC uses **fractional TAES scoring** (partial credit for partial overlaps).

This causes differences when:
- Events partially overlap
- One hyp spans multiple refs
- Multiple hyps overlap one ref

## THE EXACT FIX NEEDED

### 1. WHAT WE HAVE NOW (WRONG)

```python
# seizure_evaluation/taes/scorer.py - CURRENT BROKEN APPROACH
class TAESScorer:
    def score_events(self, ref_events, hyp_events, total_duration_sec):
        # WRONG: Binary matching - each event is 1 or 0
        for h_idx, hyp in enumerate(hyp_events):
            for r_idx, ref in enumerate(ref_events):
                if overlap_exists:
                    ref_matched[r_idx] = True  # BINARY!
                    hyp_matched[h_idx] = True  # BINARY!

        # WRONG: Counts matched events
        true_positives = sum(hyp_matched)  # Integer count
        false_positives = len(hyp_events) - true_positives
```

### 2. WHAT TEMPLE DOES (CORRECT)

```python
# Temple's fractional TAES algorithm
class NedcTAES:
    def compute(self, ref, hyp):
        # CORRECT: Fractional scoring
        hit = 0.0  # Can be 0.0 to N (fractional)
        mis = 0.0  # Can be 0.0 to N (fractional)
        fal = 0.0  # Can be 0.0 to N (fractional)

        for each ref_event:
            for each overlapping hyp_event:
                # Calculate fractional hit/miss/fa
                ref_dur = ref.stop - ref.start
                overlap_dur = min(ref.stop, hyp.stop) - max(ref.start, hyp.start)

                # Fractional hit based on overlap percentage
                p_hit = overlap_dur / ref_dur

                # Fractional FA for parts outside ref
                pre_ref = max(0, ref.start - hyp.start)
                post_ref = max(0, hyp.stop - ref.stop)
                p_fa = (pre_ref + post_ref) / ref_dur

                # Fractional miss for uncovered ref
                p_miss = 1.0 - p_hit

                hit += p_hit
                mis += p_miss
                fal += p_fa
```

### 3. THE EXACT FIX TO IMPLEMENT

Create new file: `seizure_evaluation/taes/fractional_scorer.py`

```python
class FractionalTAESScorer:
    """
    EXACT Temple NEDC v6.0.0 fractional TAES implementation.
    This MUST match Temple's algorithm exactly for full parity.
    """

    def score_events(self, ref_events, hyp_events, total_duration_sec):
        # Initialize fractional counters
        total_hits = 0.0
        total_misses = 0.0
        total_false_alarms = 0.0

        # Track which events have been processed
        ref_used = [False] * len(ref_events)
        hyp_used = [False] * len(hyp_events)

        # Process each reference event
        for r_idx, ref in enumerate(ref_events):
            ref_dur = ref.stop_time - ref.start_time

            # Find all overlapping hypothesis events
            overlapping_hyps = []
            for h_idx, hyp in enumerate(hyp_events):
                overlap_start = max(ref.start_time, hyp.start_time)
                overlap_stop = min(ref.stop_time, hyp.stop_time)
                if overlap_stop > overlap_start:
                    overlapping_hyps.append((h_idx, hyp))

            if overlapping_hyps:
                # Distribute fractional scores
                for h_idx, hyp in overlapping_hyps:
                    if not hyp_used[h_idx]:
                        # Calculate fractional components
                        overlap_start = max(ref.start_time, hyp.start_time)
                        overlap_stop = min(ref.stop_time, hyp.stop_time)
                        overlap_dur = overlap_stop - overlap_start

                        # Fractional hit (portion of ref covered)
                        fractional_hit = overlap_dur / ref_dur

                        # Fractional FA (portions of hyp outside ref)
                        pre_ref = max(0, ref.start_time - hyp.start_time)
                        post_ref = max(0, hyp.stop_time - ref.stop_time)
                        fractional_fa = (pre_ref + post_ref) / ref_dur

                        # Cap FA at 1.0 per Temple's implementation
                        fractional_fa = min(1.0, fractional_fa)

                        total_hits += fractional_hit
                        total_false_alarms += fractional_fa

                        hyp_used[h_idx] = True
                        ref_used[r_idx] = True
                        break  # Use first overlapping hyp (Temple's greedy approach)

                # Fractional miss for uncovered portion
                if ref_used[r_idx]:
                    total_misses += (1.0 - fractional_hit)
            else:
                # No overlapping hyp - full miss
                total_misses += 1.0

        # Count remaining unused hyps as full false alarms
        for h_idx, used in enumerate(hyp_used):
            if not used:
                total_false_alarms += 1.0

        # Calculate final metrics matching Temple's formulas
        num_ref_events = len(ref_events)
        sensitivity = 100.0 * total_hits / num_ref_events if num_ref_events > 0 else 0.0
        fa_per_24h = total_false_alarms * 86400.0 / total_duration_sec

        return {
            "sensitivity_percent": round(sensitivity, 4),  # Match Temple's 4 decimals
            "fa_per_24h": round(fa_per_24h, 4),
            "fractional_hits": total_hits,
            "fractional_misses": total_misses,
            "fractional_fa": total_false_alarms
        }
```

## IMPLEMENTATION STEPS

### Step 1: Create Fractional Scorer
1. Create `seizure_evaluation/taes/fractional_scorer.py` with above code
2. Port EXACT logic from Temple's `calc_hf()` and `compute_partial()` methods
3. Handle all 4 overlap cases Temple handles:
   - Pre-prediction (hyp starts before ref)
   - Post-prediction (hyp ends after ref)
   - Over-prediction (hyp contains ref)
   - Under-prediction (ref contains hyp)

### Step 2: Update Pipeline
1. Modify `evaluation/nedc_scoring/native_taes_scoring.py` to use `FractionalTAESScorer`
2. Change import from `TAESScorer` to `FractionalTAESScorer`
3. Keep all other pipeline code identical

### Step 3: Test Edge Cases
1. Run `test_mathematical_differences.py` with new scorer
2. Verify Edge Case 1 now gives ~50% sensitivity (not 100%)
3. Verify Edge Case 2 distributes credit across all refs
4. All edge cases should now match Temple's behavior

### Step 4: Validate Full Parity
1. Run on dev set - should match Temple exactly
2. Run on eval set - should still match (already does)
3. Document any remaining differences

## SUCCESS CRITERIA

✅ Dev set results MUST match Temple exactly:
- Default: 23.53% @ 19.45 FA/24h (both Temple and Native)
- 2.5fa: 7.44% @ 2.26 FA/24h (both Temple and Native)
- 1fa: 0.65% @ 0.22 FA/24h (both Temple and Native)

✅ Eval set results MUST remain matched:
- Already perfect parity, should stay that way

✅ Edge cases MUST behave like Temple:
- Partial overlaps give fractional credit
- Multiple overlaps handled with fractional distribution

## WHY THIS FIX IS CORRECT

1. **Temple is the gold standard** - NEDC v6.0.0 is what the research community uses
2. **Fractional scoring is more accurate** - Gives partial credit for partial detections
3. **Required for reproducibility** - Papers using NEDC expect this exact algorithm
4. **Clinical deployment** - FDA/regulatory approval based on Temple's metrics

## DO NOT DO THESE THINGS

❌ Do NOT create a "better" algorithm - we want EXACT Temple parity
❌ Do NOT optimize or simplify - match Temple's logic exactly, even if inefficient
❌ Do NOT change precision/rounding - use Temple's exact approach
❌ Do NOT fix Temple's bugs - if Temple has a bug, we replicate it for parity

## FINAL VALIDATION

After implementation, this command MUST show identical results:

```bash
# Both should give EXACT same metrics
python evaluation/nedc_scoring/run_nedc.py      # Temple binary
python evaluation/nedc_scoring/native_taes.py    # Our fractional implementation
```

If ANY difference exists, the implementation is WRONG and must be fixed.

---

**THIS PLAN MUST BE APPROVED BEFORE IMPLEMENTATION**

The goal is 100% mathematical parity with Temple NEDC v6.0.0, not a "better" algorithm.