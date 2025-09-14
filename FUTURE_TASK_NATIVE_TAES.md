# Future Task: Implement Native TAES Scorer

## Background
We currently have a native Python implementation of Temple NEDC's OVERLAP scoring method, but we originally intended to implement TAES (Time-Aligned Event Scoring). This document outlines the future implementation task.

## What is TAES?
TAES (Time-Aligned Event Scoring) is Temple University's strictest seizure detection evaluation metric:
- Uses fractional temporal alignment scoring
- Penalizes poor temporal alignment even when events overlap
- More stringent than OVERLAP scoring
- Industry standard for clinical EEG evaluation

## Current State
- **Have**: Native OVERLAP scorer at `seizure_evaluation/taes/overlap_scorer.py`
- **Have**: Access to Temple TAES via their binary (`evaluation/nedc_eeg_eval/v6.0.0/bin/nedc_eeg_eval`)
- **Missing**: Native Python TAES implementation

## Implementation Requirements

### Algorithm Overview
1. **Temporal Alignment Calculation**
   - For each reference-hypothesis pair, calculate temporal overlap fraction
   - Score = intersection_duration / union_duration
   - Ranges from 0 (no overlap) to 1 (perfect alignment)

2. **Optimal Matching**
   - Use Hungarian algorithm or similar for 1-to-1 event matching
   - Maximize total alignment score across all matches
   - Unmatched events become misses (ref) or false alarms (hyp)

3. **Fractional Scoring**
   - Each matched pair contributes fractional TP based on alignment
   - TP_fractional = sum of all alignment scores
   - FN = unmatched reference events + (1 - alignment) for matched refs
   - FP = unmatched hypothesis events

### Implementation Plan

```python
# Proposed location: seizure_evaluation/taes/taes_scorer.py

class TAESScorer:
    """
    Native implementation of Temple NEDC TAES scoring.

    TAES uses fractional temporal alignment:
    - 1-to-1 optimal matching between ref and hyp events
    - Fractional credit based on temporal overlap
    - Stricter than OVERLAP scoring
    """

    def score_events(self, ref_events, hyp_events, total_duration_sec):
        # 1. Build cost matrix (negative alignment scores)
        # 2. Apply Hungarian algorithm for optimal matching
        # 3. Calculate fractional TP, FP, FN
        # 4. Return TAESMetrics
        pass
```

### Validation Requirements
1. Compare against Temple binary TAES output
2. Achieve <0.1% difference in metrics across test cases
3. Validate on:
   - Default parameters (0.8/5/2.0)
   - Aggressive parameters (0.95/15/7.0)
   - Edge cases (single events, no overlap, perfect overlap)

### Test Cases
```python
# test_taes_scorer.py

def test_perfect_alignment():
    """Events perfectly aligned should score 1.0"""

def test_partial_overlap():
    """50% overlap should score 0.5"""

def test_no_overlap():
    """No overlap should score 0.0"""

def test_multiple_events():
    """Verify optimal matching with multiple events"""

def test_parity_with_temple():
    """Compare with Temple binary output on real data"""
```

## Benefits of Implementation
1. **Independence**: No longer dependent on Temple binary
2. **Speed**: Native Python likely faster than subprocess calls
3. **Debugging**: Easier to debug and understand TAES behavior
4. **Customization**: Can add custom metrics or modifications
5. **Cross-platform**: Pure Python works everywhere

## Resources
- Temple NEDC source: `evaluation/nedc_eeg_eval/v6.0.0/src/`
- TAES paper: [Link to Temple's TAES publication]
- Hungarian algorithm: `scipy.optimize.linear_sum_assignment`

## Estimated Effort
- Core implementation: 2-3 days
- Validation and testing: 1-2 days
- Documentation: 0.5 days
- **Total: ~1 week**

## Priority
**LOW** - Current OVERLAP implementation is sufficient for research. Temple binary provides TAES when needed.

## Acceptance Criteria
- [ ] Implement TAESScorer class with fractional scoring
- [ ] Add comprehensive unit tests
- [ ] Validate <0.1% difference from Temple binary
- [ ] Update run_nedc.py to use native TAES (not alias to OVERLAP)
- [ ] Document algorithm and usage
- [ ] Update EVALUATION_RESULTS_TABLE.md with native TAES column

## Notes
- This is technical debt, not urgent
- OVERLAP scoring is clinically valid and published
- Temple binary TAES works fine for now
- Implement only if/when we need TAES independence