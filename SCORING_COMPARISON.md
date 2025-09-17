# Scoring Methods Comparison: NEDC vs SzCORE

## Executive Summary

This document clarifies the critical terminology confusion between different scoring methods used in seizure detection evaluation, specifically comparing NEDC (Temple's standard) and SzCORE (EpilepsyBench's standard).

**Key Finding**: Both NEDC and SzCORE offer multiple scoring modes, but they use different terminology and have different philosophies. Understanding these differences is crucial for interpreting results.

**Critical Insight**: "Event-based" doesn't mean the same thing across frameworks! Both OVLP and TAES are event-based, but one is permissive (any-overlap) and one is strict (fractional overlap).

---

## 1. NEDC Scoring Methods (Temple University)

NEDC v6.0.0 provides FIVE distinct scoring algorithms, as documented in Picone et al. 2021 [1]:

### 1.1 NEDC Scoring Modes

1. **EPOCH** (Epoch-Based Sampling)
   - Samples annotations at fixed intervals (e.g., 1 second)
   - Counts errors at each sample point
   - Similar to "sample-based" in ML terminology
   - Most granular scoring method

2. **OVLP** (Any-Overlap)
   - Binary event-level scoring
   - ANY temporal overlap = full true positive
   - Most permissive event-based scoring
   - Commonly reported for TUSZ

3. **TAES** (Time-Aligned Event Scoring)
   - Weights events by percentage of temporal overlap
   - If 50% of seizure detected = 0.5 TP credit
   - Strictest event-based scoring
   - Emphasizes temporal precision

4. **DPALIGN** (Dynamic Programming Alignment)
   - Uses edit distance minimization
   - Can work with or without time alignment
   - Common in speech recognition

5. **IRA** (Inter-Rater Agreement)
   - Uses EPOCH scoring to calculate Cohen's Kappa
   - Measures agreement like human annotators

### 1.2 Key NEDC Characteristics
- Developed specifically for TUSZ dataset
- Matches Temple's conservative annotation philosophy
- NO pre/post-ictal tolerances
- NO automatic event merging
- Reports FA/min then converts to FA/24h

---

## 2. SzCORE Scoring Methods (EpilepsyBench)

SzCORE, documented in Dan et al. 2024 [2], provides TWO complementary scoring modes:

### 2.1 SzCORE Scoring Modes

1. **Sample-Based Scoring**
   - Compares labels at fixed frequency (10 Hz default)
   - Sample-by-sample comparison
   - Equivalent to NEDC's EPOCH scoring
   - For ML algorithm development

2. **Event-Based Scoring** (ANY-OVERLAP with tolerances)
   - Binary event scoring like NEDC OVLP
   - BUT adds clinical tolerances:
     - 30 seconds pre-ictal tolerance
     - 60 seconds post-ictal tolerance
   - Merges events <90 seconds apart
   - Splits events >5 minutes
   - This is what we call "SzCORE" in our paper

### 2.2 Key SzCORE Characteristics
- Designed for cross-dataset comparison
- Prioritizes clinical utility over precision
- Built-in tolerances for early warning value
- Reduces alarm fatigue via merging
- Reports FA/24h as primary metric

---

## 3. Critical Comparisons

### 3.1 Terminology Mapping (THE KEY TO UNDERSTANDING)

| Concept | NEDC Term | SzCORE Term | What It Actually Does |
|---------|-----------|-------------|----------------------|
| **Time-sampled scoring** | EPOCH | Sample-based | Compares labels at 1s intervals; long seizures dominate |
| **Event: any overlap** | OVLP | (Not pure) | Event is TP if ANY overlap exists; NEDC has no tolerances |
| **Event: any overlap + tolerances** | (Not offered) | Event-based | Like OVLP but +30s pre/-60s post tolerances + merge <90s |
| **Event: fractional overlap** | TAES | (Not offered) | Partial credit based on % overlap; strictest scoring |

**CRITICAL**: All three event methods (OVLP, SzCORE Event, TAES) are "event-based" but differ dramatically:
- **OVLP**: Binary (hit or miss), no tolerances
- **SzCORE Event**: Binary WITH clinical tolerances/merging
- **TAES**: Fractional credit, penalizes misalignment

### 3.2 Key Differences

**NEDC OVLP vs SzCORE Event-Based**:
- Both use any-overlap principle
- NEDC: No tolerances, pure overlap
- SzCORE: +30s pre, +60s post tolerances, merge <90s
- Result: SzCORE typically 3-4x lower FA rates

**NEDC EPOCH vs SzCORE Sample-Based**:
- Conceptually identical
- Different sampling rates (NEDC: 1 Hz typical, SzCORE: 10 Hz default)
- Both give per-sample accuracy metrics

---

## 4. SeizureTransformer's Table III Mystery Solved

The paper's Table III shows:
- **Sample-based**: F1=0.5803, Sens=47.10%
- **Event-based**: F1=0.6752, Sens=71.10%

**What they actually used**: SzCORE (reference [20])
- Sample-based = SzCORE's sample-based scoring (like NEDC EPOCH)
- Event-based = SzCORE's event-based scoring (OVLP + tolerances)

**Critical observations**:
1. The 71.1% sensitivity uses SzCORE's permissive tolerances
2. They DON'T report FA/24h (the critical metric)
3. Threshold not specified (probably not 0.8)
4. NOT comparable to NEDC OVLP due to tolerances

---

## 5. Why This Matters for Our Paper

### 5.1 Our Evaluation Choices

We provide BOTH:
1. **NEDC scoring** (OVLP, TAES, EPOCH) - Temple's clinical standard for TUSZ
2. **SzCORE scoring** - EpilepsyBench standard for cross-dataset comparison

This allows readers to see:
- How scoring choice affects metrics (3.1x FA difference)
- Why claims vary so dramatically
- What performance looks like under clinical standards

### 5.2 Fair Comparisons

When we say "27x gap" we compare:
- Dianalund: 1 FA/24h with SzCORE (with tolerances)
- TUSZ: 26.89 FA/24h with NEDC OVLP (no tolerances)

A more "apples-to-apples" comparison:
- Dianalund: 1 FA/24h with SzCORE
- TUSZ: 8.59 FA/24h with SzCORE
- Still an 8.6x gap, but more comparable

### 5.3 The Missing Information

SeizureTransformer paper DOESN'T provide:
- FA/24h for their TUSZ evaluation
- Threshold used for Table III results
- Whether post-processing parameters changed
- Comparison with NEDC (TUSZ's standard)

Our work fills these critical gaps.

---

## 6. Recommendations for Clear Reporting

### 6.1 Always Specify

1. **Exact scorer**: "NEDC OVLP" not just "overlap"
2. **Version**: "NEDC v6.0.0", "SzCORE timescoring v0.0.6"
3. **Parameters**: Tolerances, merge gaps, sampling rates
4. **Metrics**: Both sensitivity AND FA/24h

### 6.2 Avoid Ambiguity

DON'T say: "We used event-based scoring"
DO say: "We used NEDC OVLP (any-overlap without tolerances)"

DON'T say: "We achieved 71% sensitivity"
DO say: "We achieved 71% sensitivity at X FA/24h using SzCORE event-based (30s/60s tolerances)"

---

## 7. What We Actually Used in Our Paper

### Our Reported Results (theta=0.8, k=5, d=2.0s):
- **NEDC OVLP**: 45.63% sensitivity, 26.89 FA/24h
- **NEDC TAES**: 65.21% sensitivity, 136.73 FA/24h
- **SzCORE Event-based**: 52.35% sensitivity, 8.59 FA/24h
- **Native OVLP**: 45.63% sensitivity, 26.89 FA/24h (validates NEDC implementation)

### What We Did NOT Compute:
- **NEDC EPOCH**: Sample-based scoring (would be interesting comparison)
- **SzCORE Sample-based**: Would likely be similar to NEDC EPOCH at 1Hz

### Why This Educational Approach Matters:
Most papers pick ONE scorer and report those numbers. We show ALL major scorers on the SAME predictions, revealing:
1. The 3.1x difference between NEDC OVLP and SzCORE Event (26.89 vs 8.59 FA/24h)
2. The 5.1x difference between NEDC OVLP and TAES (26.89 vs 136.73 FA/24h)
3. The 15.9x difference between SzCORE and TAES (8.59 vs 136.73 FA/24h)

**This proves scoring choice alone can make a model look amazing or terrible!**

## 8. Summary Table: Expected Performance Ranges

| Scoring Method | What It Is | Our Results (θ=0.8) | Strictness |
|----------------|------------|---------------------|------------|
| **NEDC TAES** | Event, fractional overlap | 65.21% / 136.73 FA/24h | Strictest |
| **NEDC OVLP** | Event, any-overlap | 45.63% / 26.89 FA/24h | Moderate |
| **SzCORE Event** | Event, any-overlap + tolerances | 52.35% / 8.59 FA/24h | Most Permissive |
| **NEDC EPOCH** | Time-sampled (1s) | Not computed | N/A |
| **SzCORE Sample** | Time-sampled (1s) | Not computed | N/A |

*Note: All results from identical SeizureTransformer predictions*

---

## References

[1] Shah V, Golmohammadi M, Obeid I, Picone J. "Objective Evaluation Metrics for Automatic Classification of EEG Events." In: Signal Processing in Medicine and Biology. Springer; 2021. p. 235-282.

[2] Dan J, et al. "SzCORE: A Seizure Community Open-source Research Evaluation framework for the validation of EEG-based automated seizure detection algorithms." Epilepsia. 2024.

[3] Wu K, et al. "SeizureTransformer: Scaling U-Net with Transformer for Simultaneous Time-Step Level Seizure Detection from Long EEG Recordings." 2025.

---

## 9. Quick Mental Model (For Fast Understanding)

### The Hierarchy of Strictness (Most to Least Strict):
1. **NEDC TAES** - Fractional overlap credit, penalizes misalignment heavily
2. **NEDC OVLP** - Binary any-overlap, no tolerances
3. **SzCORE Event** - Binary any-overlap WITH 30s/60s tolerances + merging

### Time vs Event Distinction:
- **Time-based** (EPOCH/Sample): Every second counts equally
- **Event-based** (OVLP/TAES/SzCORE): Each seizure counts once

### The Key Insight:
**"Event-based" is NOT one thing!** It includes:
- Permissive binary (OVLP)
- Permissive binary with tolerances (SzCORE Event)
- Strict fractional (TAES)

## 10. Future Work Suggested by This Analysis

Given our findings, future papers should:
1. **Always report multiple scorers** on the same predictions
2. **Include both NEDC and SzCORE** when evaluating on TUSZ
3. **Compute sample-based scores** for completeness
4. **Show the full spectrum** from strictest (TAES) to most permissive (SzCORE Event)

This educational approach reveals how dramatically scoring affects perceived performance and helps readers understand what the numbers really mean.

## 11. Comprehensive Results Matrix

### 11.1 What We Have Computed (✅) vs What We Need (❌)

| Parameter Set | Scorer | Type | Sensitivity | FA/24h | Status |
|--------------|--------|------|-------------|---------|---------|
| **DEFAULT (θ=0.8, k=5, d=2.0)** |
| | NEDC TAES | Event (fractional) | 65.21% | 136.73 | ✅ |
| | NEDC OVLP | Event (any-overlap) | 45.63% | 26.89 | ✅ |
| | NEDC EPOCH | Sample (1s) | ? | ? | ❌ NEED |
| | Native OVLP | Event (any-overlap) | 45.63% | 26.89 | ✅ |
| | SzCORE Event | Event (overlap+tol) | 52.35% | 8.59 | ✅ |
| | SzCORE Sample | Sample (1s) | ? | ? | ❌ NEED |
| **10 FA TARGET (θ=0.88, k=5, d=3.0)** |
| | NEDC TAES | Event (fractional) | 60.45% | 83.88 | ✅ |
| | NEDC OVLP | Event (any-overlap) | 33.90% | 10.27 | ✅ |
| | NEDC EPOCH | Sample (1s) | ? | ? | ❌ NEED |
| | Native OVLP | Event (any-overlap) | 33.90% | 10.27 | ✅ |
| | SzCORE Event | Event (overlap+tol) | 40.59% | 3.36 | ✅ |
| | SzCORE Sample | Sample (1s) | ? | ? | ❌ NEED |
| **2.5 FA TARGET (θ=0.95, k=5, d=5.0)** |
| | NEDC TAES | Event (fractional) | 18.12% | 10.64 | ✅ |
| | NEDC OVLP | Event (any-overlap) | 14.50% | 2.05 | ✅ |
| | NEDC EPOCH | Sample (1s) | ? | ? | ❌ NEED |
| | Native OVLP | Event (any-overlap) | 14.50% | 2.05 | ✅ |
| | SzCORE Event | Event (overlap+tol) | 19.71% | 0.75 | ✅ |
| | SzCORE Sample | Sample (1s) | ? | ? | ❌ NEED |

### 11.2 Missing Scores To Compute

We need to compute **6 missing scores**:
1. NEDC EPOCH at DEFAULT (θ=0.8, k=5, d=2.0)
2. NEDC EPOCH at 10FA (θ=0.88, k=5, d=3.0)
3. NEDC EPOCH at 2.5FA (θ=0.95, k=5, d=5.0)
4. SzCORE Sample at DEFAULT (θ=0.8, k=5, d=2.0)
5. SzCORE Sample at 10FA (θ=0.88, k=5, d=3.0)
6. SzCORE Sample at 2.5FA (θ=0.95, k=5, d=5.0)

## Appendix: Quick Reference

### NEDC Command (Produces 5 scores)
```bash
$NEDC_NFC/bin/nedc_eeg_eval ref.list hyp.list -o output
# Outputs: TAES, OVLP, EPOCH, DPALIGN, IRA
```

### SzCORE Python (Our implementation)
```python
from timescoring.scoring import EventScoring  # Event-based with tolerances
# Note: We did NOT implement SampleScoring in our evaluation
```

### Our Evaluation Pipeline
```bash
# We computed:
python run_nedc.py  # NEDC OVLP, TAES (via binary)
python run_szcore.py  # SzCORE Event-based only
# We did NOT compute: NEDC EPOCH or SzCORE Sample-based
```

---

*Last updated: 2025-01-16*
*This document provides definitive clarity on seizure detection scoring terminology and what we actually computed in our paper.*