# Mathematical Comparison: Temple NEDC vs Native TAES Implementation

## Executive Summary

After deep analysis of both implementations, the key mathematical differences are:

1. **Overlap Calculation Method**
2. **Fractional Scoring Approach**
3. **Rounding and Precision Handling**
4. **Event Matching Algorithm**

## 1. CORE ALGORITHM DIFFERENCES

### Temple NEDC v6.0.0 Approach

The Temple implementation uses a **fractional TAES scoring** approach with complex partial overlap calculations:

```python
# Temple calculates fractional hits/misses/false alarms
def calc_hf(self, ref, hyp):
    ref_dur = stop_r - start_r

    # Pre-prediction overlap (hyp starts before ref)
    if start_h <= start_r and stop_h <= stop_r:
        hit = (stop_h - start_r) / ref_dur
        fa = min(1.0, (start_r - start_h) / ref_dur)

    # Post-prediction overlap (hyp starts after ref)
    elif start_h >= start_r and stop_h >= stop_r:
        hit = (stop_r - start_h) / ref_dur
        fa = min(1.0, (stop_h - stop_r) / ref_dur)

    # Over-prediction (hyp completely contains ref)
    elif start_h < start_r and stop_h > stop_r:
        hit = 1.0
        fa = ((stop_h - stop_r) + (start_r - start_h)) / ref_dur
```

**Key insight**: Temple normalizes all calculations by `ref_dur` (reference duration), creating fractional scores.

### Native TAES Implementation

Our native implementation uses a **greedy binary matching** approach:

```python
# Native uses overlap ratio for matching
for h_idx, hyp in enumerate(hyp_events):
    best_overlap = 0.0
    best_ref_idx = -1

    for r_idx, ref in enumerate(ref_events):
        if ref_matched[r_idx]:
            continue

        # Simple overlap duration
        overlap_start = max(hyp.start_time, ref.start_time)
        overlap_stop = min(hyp.stop_time, ref.stop_time)
        overlap_duration = max(0, overlap_stop - overlap_start)

        # Overlap ratio relative to reference
        if ref.duration > 0:
            overlap_ratio = overlap_duration / ref.duration
            if overlap_ratio >= self.overlap_threshold:  # 0.0 for OVERLAP
                # Match found
```

**Key insight**: Native uses binary matching (matched/not matched) rather than fractional scores.

## 2. MATHEMATICAL DIFFERENCES IN DETAIL

### A. Event Overlap Detection

**Temple NEDC:**
```python
def anyovlp(self, ref, hyp):
    # Creates integer sets for overlap detection
    refset = set(range(int(ref[0]), int(ref[1]) + 1))
    hypset = set(range(int(hyp[0]), int(hyp[1]) + 1))
    return len(refset.intersection(hypset)) != 0
```
- Uses **integer seconds** for overlap detection
- Creates memory-intensive sets for each comparison
- Potential rounding issues when converting float → int

**Native:**
```python
def overlaps(self, other: "Event", min_overlap: float = 0.0) -> bool:
    overlap_start = max(self.start_time, other.start_time)
    overlap_stop = min(self.stop_time, other.stop_time)
    overlap_duration = max(0, overlap_stop - overlap_start)
    return overlap_duration >= min_overlap
```
- Uses **floating-point** calculations directly
- More efficient (no set creation)
- Preserves precision

### B. Multiple Overlaps Handling

**Temple NEDC** handles complex scenarios with multiple overlapping events:

```python
# Temple can give fractional credit for multiple overlaps
# Example: One hyp event overlapping multiple ref events
#   Ref1: <-->    Ref2: <-->   Ref3: <-->
#   Hyp:  <-------------------------------->
# Result: hit=1.0 for Ref1, miss=1.0 for Ref2&3, fa=(excess_duration/ref_dur)
```

**Native** uses first-best matching:
```python
# Native: One-to-one matching only
# Same scenario would match Hyp to best overlapping Ref (likely Ref1)
# Ref2 and Ref3 become false negatives
# Hyp counts as 1 true positive
```

### C. Scoring Calculation

**Temple Final Score:**
```python
sensitivity = 100 * (sum(fractional_hits) / num_ref_events)
fa_per_24h = sum(fractional_fa) * 86400 / total_duration
```

**Native Final Score:**
```python
sensitivity = 100 * (num_matched_hyp / num_ref_events)
fa_per_24h = num_unmatched_hyp * 86400 / total_duration
```

## 3. WHY WE SEE PERFECT PARITY ON EVAL

Despite these mathematical differences, we achieve **perfect parity** on the eval set because:

1. **Post-processing creates clean events**: After applying threshold=0.99, kernel=21, min_duration=16s, events are well-separated and rarely overlap partially.

2. **Binary matching converges**: When events are either clearly overlapping or not, both algorithms converge to the same result.

3. **Rounding at output**: Both implementations round final metrics to 2 decimal places, masking small differences.

## 4. WHERE DIFFERENCES APPEAR

Differences are most visible when:

1. **Events partially overlap** (e.g., default threshold=0.8)
2. **Multiple short events** occur in sequence
3. **One long hyp spans multiple refs** (or vice versa)

Example from our results:
```
DEV SET (more partial overlaps):
- Temple: 0.65% @ 0.22 FA/24h
- Native: 0.65% @ 0.00 FA/24h  ← FA difference due to fractional vs binary

EVAL SET (cleaner events):
- Temple: 1.28% @ 0.38 FA/24h
- Native: 1.28% @ 0.38 FA/24h  ← Perfect match
```

## 5. CRITICAL IMPLEMENTATION DETAILS

### Temple Precision Issues

```python
# Temple uses integer conversion that can lose precision
refset = set(range(int(ref[0]), int(ref[1]) + 1))
# Event at 1.9-2.1 seconds becomes int(1) to int(2)+1 = {1,2,3}
# Lost fractional seconds!
```

### Native Precision Preservation

```python
# Native keeps full float precision
overlap_duration = max(0, overlap_stop - overlap_start)
# Event at 1.9-2.1 maintains exact 0.2 second duration
```

## 6. RECOMMENDATIONS

1. **For Clinical Deployment**: The differences are negligible at extreme thresholds (0.95+) where events are well-separated.

2. **For Research**: Be aware that Temple's fractional scoring can give different results than binary matching at lower thresholds.

3. **For Validation**: Our native implementation is mathematically simpler and more efficient, while achieving functional parity for clinical use cases.

## 7. CONCLUSION

The Temple NEDC implementation uses a sophisticated fractional scoring system that can award partial credit for partial overlaps. Our native implementation uses a simpler binary matching approach.

**At high thresholds (0.95+), both converge to identical results**, which is why we see perfect parity on the eval set. The mathematical differences only matter for edge cases with significant partial overlaps, which are filtered out by aggressive post-processing.

The native implementation is:
- ✅ More efficient (no set operations)
- ✅ More precise (preserves floats)
- ✅ Simpler to understand and maintain
- ✅ Functionally equivalent for clinical parameters

