# Results

## Evaluation Setup

We evaluated SeizureTransformer on TUSZ v2.0.3's held-out evaluation set containing 865 EEG files (127.7 hours of recordings). Using the authors' pretrained weights, we generated predictions and evaluated them using three scoring methodologies: NEDC OVERLAP (Temple's official any-overlap mode), NEDC TAES (time-aligned), and SzCORE Event (EpilepsyBench standard).

## Primary Results

### Default Configuration (theta=0.80, k=5, d=2.0)

At the paper's default parameters, we observed dramatic variation across scoring methods. The same predictions yielded:

- **NEDC OVERLAP**: 45.63% sensitivity, 26.89 FA/24h
- **NEDC TAES**: 65.21% sensitivity, 136.73 FA/24h
- **SzCORE Event**: 52.35% sensitivity, 8.59 FA/24h

This represents a **3.1x difference** in false alarm rates between NEDC OVERLAP and SzCORE Event scoring on identical predictions. Compared to the paper's reported ~1 FA/24h on Dianalund, we observe a **27-fold gap** with NEDC OVERLAP and a **137-fold gap** with NEDC TAES.

| Scoring Method | Sensitivity (%) | FA/24h  | Multiplier vs Claimed | F1 Score |
|:---------------|----------------:|--------:|----------------------:|---------:|
| **Dianalund (Claimed)** | 37.00 | 1.00 | 1x | 0.43* |
| SzCORE Event | 52.35 | 8.59 | 9x | 0.485 |
| NEDC OVERLAP | 45.63 | 26.89 | **27x** | 0.396 |
| NEDC TAES | 60.45 | 136.73 | **137x** | 0.237 |

Table 1: Performance at default parameters (theta=0.80, k=5, d=2.0). *F1 from competition leaderboard.

### Clinical Deployment Targets

We optimized parameters on the development set to target clinical false alarm thresholds:

**10 FA/24h Target (theta=0.88, k=5, d=3.0)**:
- NEDC OVERLAP achieved 33.90% sensitivity at 10.27 FA/24h
- While meeting our FA constraint, this falls far below the 75% sensitivity goal for clinical systems [10]
- SzCORE Event achieved 40.59% sensitivity at only 3.36 FA/24h

**2.5 FA/24h Target (theta=0.95, k=5, d=5.0)**:
- NEDC OVERLAP achieved 14.50% sensitivity at 2.05 FA/24h
- Sensitivity too low for clinical viability
- SzCORE Event achieved 19.71% sensitivity at 0.75 FA/24h

![Figure 2: Operating characteristic curves across scoring methodologies. The same model predictions yield dramatically different sensitivity-false alarm tradeoffs depending on scoring choice. The clinical target zone (green) represents the desired operating region for deployment (>=75% sensitivity, <=10 FA/24h). The paper's default operating point (black circle) falls far outside clinical viability for all scoring methods on TUSZ.](../figures/output/arxiv/fig2_operating_curves.png){#fig:operating-curves width=100%}

## Key Findings

1. **Scoring Impact**: The ~=3.1x difference at default (NEDC OVERLAP vs SzCORE Event) stems entirely from scoring methodology, with TAES showing even larger divergence (5.1x vs OVERLAP).

2. **Clinical Viability**: SeizureTransformer cannot achieve clinical viability when evaluated with NEDC scoring on TUSZ. At 10 FA/24h, it reaches only 33.90% sensitivity, far below the 75% goal for clinical systems [10].

3. **AUROC Performance**: We measured AUROC of 0.9019.

## Data Integrity

All evaluations used:
- 865 files from TUSZ v2.0.3 eval set (127.7 hours)
- No data leakage (completely held-out test set)
- Identical post-processing across all scorers
- merge_gap disabled (no event merging) for NEDC compliance

See Appendix Tables A1-A2 for full metrics; accompanying plots are reproducible via `scripts/visualize_results.py` and included in the repository.

