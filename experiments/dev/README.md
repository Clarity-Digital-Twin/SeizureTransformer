# Dev Split Experiments

This directory contains all hyperparameter tuning experiments on the TUSZ dev split.

## Current Experiments

### Baseline (Default Parameters)
- **Directory**: `baseline/`
- **Parameters**: threshold=0.8, kernel=5, min_duration=2.0s
- **Status**: ⏳ Pending
- **Purpose**: Establish dev split baseline before tuning

### Parameter Sweeps
- **Directory**: `sweep_*/`
- **Grid Search**: threshold × kernel × min_duration × merge_gap
- **Target**: FA/24h ≤ 10 with maximum sensitivity
- **Status**: ⏳ Pending

## Experiment Log

| Experiment | Date | FA/24h Target | Best Sensitivity | Best FA/24h | Parameters | Status |
|------------|------|---------------|------------------|-------------|------------|---------|
| baseline   | TBD  | N/A          | TBD              | TBD         | default    | pending |
| sweep_fa10 | TBD  | 10           | TBD              | TBD         | TBD        | pending |
| sweep_fa5  | TBD  | 5            | TBD              | TBD         | TBD        | pending |

## Next Steps

1. **Run dev baseline**: Establish baseline performance on dev split
2. **Parameter sweep**: Grid search for clinical targets (5-10 FA/24h)
3. **Select best**: Choose operating point for eval split
4. **Document decision**: Record rationale for parameter choice