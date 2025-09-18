# SeizureTransformer Benchmark Results

## Paper Default (threshold=0.8, kernel=5, min_duration=2.0, merge_gap=None)

| Metric | Sensitivity | FA/24h | F1 Score | Notes |
|--------|------------|--------|----------|-------|
| NEDC OVERLAP | 45.63% | 26.89 | 0.518 | Temple's binary event scorer (SEIZ FA) |
| SzCORE Event | 52.35% | 8.59 | - | EpilepsyBench (90s internal merge) |

## Key Findings

1. **Without merge_gap manipulation**: The model shows 26.89 FA/24h (SEIZ) at paper defaults (OVERLAP)
2. **SzCORE difference**: SzCORE Event's tolerances/merge reduce FA by ≈3.1× vs OVERLAP at default
3. **Clinical viability**: At paper defaults, NOT clinically viable (need <10 FA/24h)

## Clinical Tuning Targets

| Target FA/24h | Threshold | Kernel | Min Duration | Sensitivity | Status |
|--------------|-----------|--------|--------------|-------------|---------|
| ~10 | TBD | TBD | TBD | TBD | In Progress |
| ~2.5 | TBD | TBD | TBD | TBD | Pending |
| ~1.0 | TBD | TBD | TBD | TBD | Pending |

## Important Notes

- All results use merge_gap=None (no artificial FA reduction)
- NEDC scores follow Temple University standards
- SzCORE Event uses timescoring package with EpilepsyBench defaults

