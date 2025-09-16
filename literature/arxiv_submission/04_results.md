# Results

## Evaluation Setup

We evaluated SeizureTransformer on TUSZ v2.0.3's held-out evaluation set containing 865 EEG files (127.7 hours of recordings). Using the authors' pretrained weights, we generated predictions and evaluated them using four scoring methodologies: NEDC OVERLAP (Temple's official any-overlap mode), NEDC TAES (time-aligned), Native OVERLAP (our Python implementation), and SzCORE (EpilepsyBench standard).

## Primary Results

### Default Configuration (θ=0.80, k=5, d=2.0)

At the paper's default parameters, we observed dramatic variation across scoring methods. The same predictions yielded:

- **NEDC OVERLAP**: 45.63% sensitivity, 26.89 FA/24h
- **NEDC TAES**: 65.21% sensitivity, 136.73 FA/24h
- **Native OVERLAP**: 45.63% sensitivity, 26.89 FA/24h (perfect parity with NEDC)
- **SzCORE**: 52.35% sensitivity, 8.59 FA/24h

This represents a **3.1× difference** in false alarm rates between NEDC OVERLAP and SzCORE scoring on identical predictions. Compared to the paper's reported ~1 FA/24h on Dianalund, we observe a **27-fold gap** with NEDC OVERLAP and a **137-fold gap** with NEDC TAES.

### Clinical Deployment Targets

We optimized parameters on the development set to target clinical false alarm thresholds:

**10 FA/24h Target (θ=0.88, k=5, d=3.0)**:
- NEDC OVERLAP achieved 33.90% sensitivity at 10.27 FA/24h
- While meeting our FA constraint, this falls far below the 75% sensitivity goal for clinical systems (Roy et al., 2021)
- SzCORE achieved 40.59% sensitivity at only 3.36 FA/24h

**2.5 FA/24h Target (θ=0.95, k=5, d=5.0)**:
- NEDC OVERLAP achieved 14.50% sensitivity at 2.05 FA/24h
- Sensitivity too low for clinical viability
- SzCORE achieved 19.71% sensitivity at 0.75 FA/24h

## Key Findings

1. **Scoring Impact**: The ≈3.1× difference at default (NEDC OVERLAP vs SzCORE) stems entirely from scoring methodology, with TAES showing even larger divergence (5.1× vs OVERLAP).

2. **Clinical Viability**: SeizureTransformer cannot achieve clinical viability when evaluated with NEDC scoring on TUSZ. At 10 FA/24h, it reaches only 33.90% sensitivity, far below the 75% goal for clinical systems (Roy et al., 2021).

3. **Implementation Parity**: Our Native OVERLAP implementation achieved identical results to Temple's official NEDC binaries, validating our pipeline.

4. **AUROC Performance**: We measured AUROC of 0.9019.

## Data Integrity

All evaluations used:
- 865 files from TUSZ v2.0.3 eval set (127.7 hours)
- No data leakage (completely held-out test set)
- Identical post-processing across all scorers
- merge_gap disabled (no event merging) for NEDC compliance

Figure 1 illustrates the performance spectrum across scoring methods, while Figure 3 shows operating points relative to clinical deployment zones.
