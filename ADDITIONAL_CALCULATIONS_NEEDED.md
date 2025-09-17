# Additional Calculations to Strengthen Our Case

## Executive Summary

While our current results prove the 27-137x performance gap, several additional calculations would make our argument ironclad.

---

## Priority 1: Find Exact 1 FA/24h Operating Point with SzCORE

**Why This Matters**: Direct apples-to-apples comparison with Dianalund's 1 FA/24h claim

**Current Data**:
- θ=0.95 gives 0.75 FA/24h (19.71% sensitivity)
- θ=0.88 gives 3.36 FA/24h (40.59% sensitivity)

**What We Need**:
- Find θ between 0.88-0.95 that gives exactly 1.0 FA/24h
- Estimate: θ ≈ 0.93-0.94
- Expected sensitivity: ~25-30%

**Impact**: Shows that even with SzCORE's permissive scoring, achieving 1 FA/24h on TUSZ requires significant sensitivity sacrifice compared to Dianalund's 37%.

---

## Priority 2: Match Their Table III Claims (71.1% Sensitivity)

**Why This Matters**: They claim 71.1% event-based sensitivity on TUSZ but don't report FA/24h

**What We Need**:
- Test parameter sweeps to find what gives 71.1% SzCORE sensitivity
- Report the corresponding FA/24h (likely very high)
- Show they cherry-picked sensitivity without showing FA rate

**Expected Finding**:
- Probably requires θ ≈ 0.5-0.6
- FA/24h likely >100

---

## Priority 3: Complete NEDC EPOCH Scoring

**Why This Matters**: Sample-based scoring is standard for ML evaluation

**What We Need**:
1. NEDC EPOCH at DEFAULT (θ=0.8, k=5, d=2.0)
2. NEDC EPOCH at 10FA (θ=0.88, k=5, d=3.0)
3. NEDC EPOCH at 2.5FA (θ=0.95, k=5, d=5.0)

**Implementation Note**:
- NEDC binary already computes this
- Just need to extract from existing summaries

---

## Priority 4: Add SzCORE Sample-Based Scoring

**Why This Matters**: Completes the scoring matrix and shows consistency

**What We Need**:
1. SzCORE Sample at DEFAULT (θ=0.8, k=5, d=2.0)
2. SzCORE Sample at 10FA (θ=0.88, k=5, d=3.0)
3. SzCORE Sample at 2.5FA (θ=0.95, k=5, d=5.0)

**Implementation Note**:
- Requires adding SampleScoring to our szcore_scoring module
- Should match NEDC EPOCH closely at 1Hz sampling

---

## Priority 5: Find NEDC OVLP 1 FA/24h Operating Point

**Why This Matters**: Shows what it takes to achieve benchmark with TUSZ's standard scorer

**Current Data**:
- θ=0.95 gives 2.05 FA/24h (14.50% sensitivity)
- Need higher threshold

**What We Need**:
- Find θ that gives exactly 1.0 FA/24h with NEDC OVLP
- Estimate: θ ≈ 0.97-0.98
- Expected sensitivity: <10%

---

## Quick Wins (Can Extract from Existing Data)

### From existing NEDC summaries:
1. EPOCH scores (already computed, just not extracted)
2. Total FA rates (SEIZ + BCKG combined)
3. IRA scores for inter-rater agreement perspective

### From existing checkpoints:
1. Per-file performance breakdown
2. Seizure duration distribution impact
3. Files with highest FA contribution

---

## Implementation Plan

### Phase 1: Extract from existing (1 hour)
- [ ] Extract NEDC EPOCH from existing summaries
- [ ] Document total FA rates (SEIZ+BCKG)
- [ ] Analyze per-file performance

### Phase 2: Quick parameter search (2 hours)
- [ ] Binary search for SzCORE 1 FA/24h threshold
- [ ] Binary search for NEDC OVLP 1 FA/24h threshold
- [ ] Document sensitivities at these points

### Phase 3: Table III investigation (3 hours)
- [ ] Parameter sweep to find 71.1% sensitivity
- [ ] Document corresponding FA/24h
- [ ] Compare to paper's omission

### Phase 4: Complete scoring matrix (4 hours)
- [ ] Implement SzCORE SampleScoring
- [ ] Run at all operating points
- [ ] Complete Section 11 of SCORING_COMPARISON.md

---

## Expected Impact on Paper

These calculations will allow us to state:

1. **"Using identical SzCORE scoring, achieving Dianalund's 1 FA/24h benchmark on TUSZ requires θ≈0.94 with only ~25% sensitivity vs their 37%"**

2. **"The paper's 71.1% sensitivity claim on TUSZ comes at [X] FA/24h - information conspicuously absent from their Table III"**

3. **"Under TUSZ's standard NEDC OVLP scoring, achieving 1 FA/24h requires θ≈0.98 with <10% sensitivity"**

4. **"Sample-based scoring (NEDC EPOCH) shows [X]% accuracy, confirming poor temporal alignment"**

These concrete numbers make our critique unassailable.

---

*Last updated: 2025-01-16*
*Priority: Complete Priority 1-2 for immediate paper impact*