# Methodology Comparison: Are We Making a Fair Comparison?

## Executive Summary

**The Critical Question**: SeizureTransformer achieved 1 FA/24h at 37% sensitivity on Dianalund using theta=0.8. We measured 26.89 FA/24h at 45.63% sensitivity on TUSZ using the same theta=0.8. Is our 27-137x performance gap claim methodologically sound?

**Short Answer**: YES, our comparison is fair and methodologically sound. Here's why:

1. **Same parameters were used**: The authors explicitly state they used theta=0.8 (80% threshold) on Dianalund
2. **FA/24h was THE target**: The authors acknowledge sacrificing sensitivity for low FA rate as the primary ranking criterion
3. **We tested equivalent thresholds**: At theta=0.98 on TUSZ, we achieve 0.86 FA/24h but only 8.10% sensitivity
4. **The comparison reveals dataset/scoring differences**, not parameter tuning differences

## The Authors' Explicit Statement

From the SeizureTransformer paper (Page 4):

> "It is noteworthy that we set the picking threshold to be 80% in the competition, which leads to a **relative low sensitivity but comes with the best precision and False Positive rate**."

They achieved on Dianalund (EpilepsyBench Challenge):
- **Threshold**: 0.8 (80%)
- **Sensitivity**: 37%
- **FA/24h**: 1
- **F1-score**: 0.43

## Our TUSZ Evaluation at Same Parameters

At the SAME theta=0.8, k=5, d=2.0s on TUSZ eval:
- **NEDC OVERLAP**: 45.63% sensitivity, 26.89 FA/24h
- **NEDC TAES**: 65.21% sensitivity, 136.73 FA/24h
- **SzCORE**: 52.35% sensitivity, 8.59 FA/24h

## What If We Matched the 1 FA/24h Target on TUSZ?

We DID test this. From our Appendix Table B1:

At theta=0.98, k=9, d=6.0s (extreme parameters):
- **NEDC OVERLAP**: 8.10% sensitivity, 0.86 FA/24h
- **This is clinically useless** (8% sensitivity vs 37% on Dianalund)

## Why This Comparison IS Fair

### 1. Parameters Are Held Constant
- Both evaluations use theta=0.8 as the primary comparison point
- This isolates the effect of dataset + scoring methodology
- The authors chose 0.8 specifically to optimize for FA/24h on Dianalund

### 2. The Authors Prioritized FA/24h
From the paper:
- "false positive per day were used as the **primary ranking criterion** to align with real-world requirements"
- They explicitly sacrificed sensitivity to achieve 1 FA/24h
- This was their deliberate choice for the competition

### 3. Alternative Comparisons Support Our Claim

**If we compared at matched FA rates** (both ~1 FA/24h):
- Dianalund: 37% sensitivity at 1 FA/24h (theta=0.8)
- TUSZ: 8.10% sensitivity at 0.86 FA/24h (theta=0.98)
- **This shows a 4.5x sensitivity gap at matched FA rates**

**If we compared with SzCORE** (EpilepsyBench's scorer):
- The same theta=0.8 gives 8.59 FA/24h on TUSZ with SzCORE
- Still an 8.6x gap from the 1 FA/24h Dianalund claim
- Even with SzCORE's permissive scoring, the gap persists

### 4. The Root Cause Analysis

The 27-137x gap stems from THREE compounding factors:

1. **Dataset differences** (TUSZ vs Dianalund)
   - Different patient populations
   - Different recording conditions
   - Different annotation standards

2. **Scoring methodology** (NEDC vs SzCORE)
   - SzCORE adds 30s pre-ictal + 60s post-ictal tolerances
   - SzCORE merges events <90s apart
   - We show 3.1x difference from scoring alone

3. **NOT from parameter selection**
   - We used identical parameters (theta=0.8) for fair comparison
   - Even extreme tuning can't close the gap

## Methodological Integrity Check

✅ **What we did RIGHT**:
- Used exact same parameters (theta=0.8, k=5, d=2.0s) as primary comparison
- Tested multiple scoring methods to show methodology impact
- Explored full parameter space to find what WOULD achieve 1 FA/24h
- Documented that even at 1 FA/24h on TUSZ, sensitivity is only 8.10%

✅ **Our claims are conservative**:
- We report 27x gap using NEDC OVERLAP (most common for TUSZ)
- We could claim 137x using NEDC TAES (stricter scoring)
- We acknowledge SzCORE reduces this to 8.6x (still substantial)

❌ **What would be UNFAIR**:
- Comparing different thresholds without disclosure
- Cherry-picking the worst scorer for maximum gap
- Not testing what parameters achieve 1 FA/24h on TUSZ
- Hiding that different datasets have different optimal parameters

## The Academic Integrity Statement

Our paper states:
> "At the paper's default parameters (threshold=0.8, kernel=5, duration=2.0s), we observe 45.63% sensitivity at 26.89 FA/24h with NEDC OVERLAP—a 27-fold increase from the Dianalund benchmark claim."

This is **methodologically sound** because:
1. We compare at identical parameters
2. We explicitly state the parameters used
3. We show results across multiple scorers
4. We provide the full trade-off curve

## Conclusion

**The comparison is fair.** The 27-137x gap is real and stems from:
- Different datasets (TUSZ vs Dianalund)
- Different scoring methods (NEDC vs SzCORE)
- NOT from parameter selection bias

The authors optimized for 1 FA/24h at the cost of sensitivity. When we apply the same model with the same parameters to TUSZ, the false alarm rate increases 27-fold with NEDC OVERLAP. Even when we tune to achieve 1 FA/24h on TUSZ (theta=0.98), sensitivity drops to 8.10%—far below clinical viability.

**The key insight**: A model can appear clinically ready on one dataset+scorer combination while being completely undeployable on another. This isn't a flaw in SeizureTransformer—it's a fundamental challenge in seizure detection that our evaluation exposes.

## Critical Addition: What Scoring Tool Did They Use for Table III?

**The Mystery of Table III (TUSZ Results)**:
The paper shows two different scoring scales for TUSZ evaluation:
- **Sample-based**: F1=0.5803, Sensitivity=0.4710 (47.1%), Precision=0.7556
- **Event-based**: F1=0.6752, Sensitivity=0.7110 (71.1%), Precision=0.6427
- **NO FALSE ALARM RATES reported**
- **NO THRESHOLD specified**

**What the paper says**: "using the same evaluation metrics (F1-score, sensitivity, and precision) implemented by the challenge organizers [20]. The testing tools provide both sample-level and event-level evaluation."

**Reference [20] is**: J. Dan et al., "SzCORE: Seizure community open-source research evaluation framework..." (2024)

**Critical Finding**: They used SzCORE for BOTH evaluations! SzCORE provides:
1. **Sample-based scoring**: Per-sample evaluation (like pixel-wise accuracy)
2. **Event-based scoring**: Per-event evaluation with ANY-OVERLAP (what we call SzCORE in our paper)

**Key Insights**:
- The 71.1% event-based sensitivity is likely WITH SzCORE's permissive tolerances (30s pre, 60s post)
- They don't report FA/24h for TUSZ, hiding the critical deployment metric
- The threshold used is NOT specified (likely different from 0.8)
- This is NOT NEDC scoring - it's SzCORE applied to TUSZ

**Why This Matters**:
- Their "best" TUSZ result (71.1% sensitivity) uses SzCORE's permissive scoring
- Without FA rates, we can't know if this is clinically viable
- Our evaluation fills this gap by showing FA rates with multiple scorers

## References in Repository

- Original paper analysis: `/literature/markdown/seizure_transformer/SeizureTransformer.md`
- Our results table: `/docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md`
- Parameter sweep data: Appendix Table B1 in paper
- SzCORE implementation: `szcore-run` CLI → `src/seizure_evaluation/szcore/cli.py`
- NEDC integration: `/evaluation/nedc_eeg_eval/nedc_scoring/`

---

*Last updated: 2025-01-16*
*This document provides the definitive answer to methodology questions about our SeizureTransformer evaluation.*
