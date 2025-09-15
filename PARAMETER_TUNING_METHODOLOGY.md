# Parameter Tuning Methodology

## Overview
This document explains our parameter tuning methodology and rationale for the SeizureTransformer evaluation on TUSZ.

## Tuning Target: NEDC OVERLAP
We tuned post-processing parameters (threshold, kernel_size, min_duration) using **NEDC OVERLAP scoring** as our optimization target.

### Why NEDC OVERLAP?

1. **Clinical Standard for TUSZ**
   - NEDC OVERLAP is the de facto clinical evaluation standard for the Temple University Hospital EEG Seizure Corpus
   - Used by Temple University's official NEDC v6.0.0 scorer
   - Balances clinical utility with practical constraints

2. **Middle-Ground Stringency**
   - More strict than SzCORE (which has 30s pre-ictal, 60s post-ictal tolerances)
   - More lenient than NEDC TAES (which requires precise time alignment)
   - Represents realistic clinical expectations

3. **Scientifically Sound Approach**
   - Tuning with the most lenient scorer (SzCORE) would produce parameters that fail on stricter metrics
   - Tuning with the strictest scorer (TAES) would be overly conservative
   - NEDC OVERLAP provides balanced parameters that work reasonably across all metrics

## Understanding Different Scoring Methodologies

Each scoring method serves different purposes and has merit for specific use cases. We present them ordered by relative permissiveness to help understand their characteristics:

From **MOST PERMISSIVE** to **MOST STRICT**:

### 1. SzCORE Any-Overlap (Most Permissive)
- Any overlap = 100% detection
- 30 seconds pre-ictal tolerance (allows early detection)
- 60 seconds post-ictal tolerance (allows extended detection)
- Merges events <90 seconds apart
- **Purpose:** Designed for practical clinical applications where early warning is valuable
- **Result: ~10x lower FA rates than NEDC due to event merging and tolerances**

### 2. NEDC OVERLAP (Common Practice) ← **OUR TUNING TARGET**
- Any overlap within event boundaries = detection
- No pre/post-ictal tolerances
- Widely used in practice for TUSZ evaluation
- **Practical balance between accuracy and utility**
- Note: While considered "permissive" by some researchers, it remains the de facto standard

### 3. Native Python OVERLAP
- Our implementation matching NEDC OVERLAP
- Validates parity with Temple's binary
- Same results as NEDC OVERLAP

### 4. NEDC TAES (Most Strict)
- Time-Aligned Event Scoring
- Weights by percentage of overlap
- Penalizes temporal misalignment
- **Proposed by Picone et al. as improved metric**
- More rigorous but not yet widely adopted in practice

## Parameter Sets Obtained

Using NEDC OVERLAP as our tuning target, we identified:

### DEFAULT (Paper Parameters)
- threshold = 0.8
- kernel_size = 5
- min_duration = 2.0 seconds
- **Result:** 45.63% sensitivity @ 100.06 FA/24h

### 10 FA/24h Target
- threshold = 0.95
- kernel_size = 5
- min_duration = 2.0 seconds
- **Result:** 23.45% sensitivity @ 39.50 FA/24h (FAILS target)

### 2.5 FA/24h Target
- threshold = 0.95
- kernel_size = 11
- min_duration = 8.0 seconds
- **Result:** 11.51% sensitivity @ 8.09 FA/24h (FAILS target)

## Cross-Metric Evaluation

After tuning with NEDC OVERLAP, we evaluated the same parameters across all 4 scoring methods to demonstrate:

1. **Impact of scoring methodology** on reported performance
2. **Relative permissiveness** of different standards
3. **Clinical reality** - model cannot meet FA targets with standard NEDC scoring

## Key Finding

**SeizureTransformer cannot meet clinical false alarm targets (10 FA/24h, 2.5 FA/24h) when evaluated with the clinical standard NEDC scoring**, despite achieving excellent results with the more permissive SzCORE scoring used in EpilepsyBench.

## Conclusion

Our methodology of tuning with NEDC OVERLAP and then evaluating across all metrics provides:
- **Transparency** about scoring methodology impact
- **Clinical relevance** using the actual TUSZ standard
- **Scientific rigor** by showing performance across multiple metrics
- **Honest assessment** of real-world deployability

This approach reveals the critical gap between competition metrics (SzCORE) and clinical requirements (NEDC).