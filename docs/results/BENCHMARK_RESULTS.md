# SeizureTransformer Benchmark Results

## Paper Default (threshold=0.8, kernel=5, min_duration=2.0, merge_gap=None)

| Metric | Sensitivity | FA/24h | F1 Score | Notes |
|--------|------------|--------|----------|-------|
| NEDC OVERLAP | 45.63% | 100.06 | 0.519 | Temple's binary event scorer |
| SzCORE | 52.35% | 8.46 | - | EpilepsyBench (90s internal merge) |

## Key Findings

1. **Without merge_gap manipulation**: The model shows ~100 FA/24h at paper defaults
2. **SzCORE difference**: SzCORE's internal 90s merge window reduces FA by ~12x vs NEDC
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
- SzCORE uses timescoring package with EpilepsyBench defaults

