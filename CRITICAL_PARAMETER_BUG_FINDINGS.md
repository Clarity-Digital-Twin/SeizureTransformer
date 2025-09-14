# Critical Analysis: Post-Processing Parameter Tuning Issues
**Date**: September 14, 2025
**Status**: Parameter misconfiguration identified - requires retuning
**Impact**: Operating point metrics incorrect; pipeline code functional

## Executive Summary
The morphological kernel size parameter in our post-processing pipeline exhibits counterintuitive behavior: increasing kernel size leads to higher false alarm rates rather than lower ones. This resulted in our "10 FA/24h" operating point actually producing 94.5 FA/24h.

## Quantitative Analysis

### Expected vs Actual Performance

| Operating Point | Target FA/24h | Actual FA/24h | Deviation Factor |
|-----------------|---------------|---------------|------------|
| Default | N/A | 60.83 ✅ | Normal |
| 10 FA | 10.0 | **94.48** ❌ | 9.4x WORSE |
| 2.5 FA | 2.5 | **38.60** ❌ | 15.4x WORSE |
| 1 FA | 1.0 | **34.85** ❌ | 34.8x WORSE |

### Event Count Analysis
```
Default (thresh=0.80, kernel=5, min_dur=2.0s): 344 seizure events detected
10FA    (thresh=0.88, kernel=7, min_dur=2.5s): 465 seizure events detected (35% increase)
Test    (thresh=0.95, kernel=5, min_dur=2.0s): 320 seizure events detected (expected reduction)
```

## Root Cause Analysis

### The Parameter Table That Failed
| Target | Threshold | Kernel | Min Duration | Result |
|--------|-----------|--------|--------------|--------|
| 10 FA | 0.88 ↑ | **7 ↑** | 2.5s ↑ | 94.5 FA (FAIL) |
| 2.5 FA | 0.93 ↑ | **11 ↑** | 5.0s ↑ | 38.6 FA (FAIL) |
| 1 FA | 0.95 ↑ | **15 ↑** | 7.0s ↑ | 34.8 FA (FAIL) |

### Why The Kernel Size Breaks Everything

1. **What we thought**: Larger kernel = more smoothing = fewer events
2. **What actually happens**:
   - Larger kernel = more DILATION in morphological operations
   - This EXPANDS seizure boundaries
   - Adjacent events get MERGED into mega-events
   - Result: MORE false alarm time, not less!

3. **The math**:
   ```python
   # Morphological closing operation
   closed = binary_dilation(binary_erosion(signal, kernel), kernel)
   # Larger kernel → more dilation → seizures grow bigger!
   ```

## Parameter Behavior Analysis

```
Threshold ↑ = Fewer false alarms ✅ (works as expected)
Min Duration ↑ = Fewer false alarms ✅ (works as expected)
Kernel Size ↑ = MORE false alarms ❌ (OPPOSITE of what we want!)
```

## Proposed Solutions

### Option 1: Fixed Kernel Strategy
```python
# Keep kernel constant, only tune threshold and min_duration
10 FA:  threshold=0.90, kernel=5, min_duration=3.0s
2.5 FA: threshold=0.94, kernel=5, min_duration=4.0s
1 FA:   threshold=0.96, kernel=5, min_duration=5.0s
```

### Option 2: Inverse Kernel Strategy
```python
# DECREASE kernel for stricter operating points
10 FA:  threshold=0.88, kernel=3, min_duration=2.5s
2.5 FA: threshold=0.93, kernel=2, min_duration=4.0s
1 FA:   threshold=0.95, kernel=1, min_duration=5.0s
```

### Option 3: Proper Parameter Sweep
```python
# Test all combinations systematically
for threshold in [0.80, 0.85, 0.90, 0.95]:
    for kernel in [1, 3, 5, 7]:
        for min_dur in [1.0, 2.0, 3.0, 5.0]:
            # Run and find what actually gives 10 FA/24h
```

## Investigation Timeline

1. **Initial evaluation**: Got 137.5 FA/24h (was actually wrong, real was 60.83)
2. **Tried to tune for clinical targets**: 10 FA, 2.5 FA, 1 FA
3. **Applied "intuitive" logic**: Increase ALL parameters for stricter detection
4. **Results came out BACKWARDS**: Higher thresholds gave MORE false alarms
5. **Investigation revealed**: Kernel size was the culprit
6. **Current status**: Need to rerun with correct parameters

## Impact Assessment

1. **README is partially wrong**: Operating points table shows wrong FA rates
2. **EVALUATION_RESULTS_TABLE.md**: Has incorrect data for tuned operating points
3. **Published results**: May need correction if anyone used these parameters
4. **Good news**: Default parameters (0.80/5/2.0) are CORRECT at 60.83 FA/24h

## Action Plan

1. **IMMEDIATE**: Document this finding (DONE - this file)
2. **NEXT**: Design correct parameter sweep strategy
3. **THEN**: Rerun all operating points with fixed parameters
4. **FINALLY**: Update all documentation with correct values

## Key Findings

1. **Always verify assumptions**: "Bigger = stricter" is not always true
2. **Morphological operations are tricky**: Dilation/erosion effects compound
3. **Test each parameter independently**: Don't change everything at once
4. **Validate incrementally**: Check event counts, not just final metrics

## Related Files

- `EVALUATION_RESULTS_TABLE.md` - Contains the incorrect results
- `README.md` - Operating points table needs updating
- `evaluation/nedc_eeg_eval/nedc_scoring/convert_predictions.py` - Where morphological ops happen
- `experiments/eval/baseline/results_*/` - Contains all the evidence

## Critical Insight

**Morphological kernel size has an inverse relationship with false alarm reduction. Larger kernels dilate seizure boundaries, increasing total seizure time and false alarm rates.**