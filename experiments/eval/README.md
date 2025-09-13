# Eval Split Experiments

This directory contains final evaluation runs on the TUSZ eval split.

**⚠️ CRITICAL**: Each parameter set should only be run ONCE on eval split to avoid data leakage.

## Current Results

### Baseline (Existing)
- **Location**: `experiments/eval/baseline/` (migrated)
- **Parameters**: threshold=0.8, kernel=5, min_duration=2.0s
- **Results**: TAES Sensitivity=24.15%, FA/24h=137.5
- **Status**: ✅ Complete

### Tuned Parameters
- **Status**: ⏳ Awaiting dev split optimization
- **Source**: Best parameters from dev experiments
- **Target**: Clinically viable FA rate (<10/24h)

## Experiment Log

| Experiment | Date | Parameters | TAES Sens | TAES FA/24h | F1 | Notes |
|------------|------|------------|-----------|-------------|----|---------| 
| baseline   | 2025-01-13 | thr=0.8,k=5,min=2.0 | 24.15% | 137.5 | 31.19% | Default params |
| tuned_v1   | TBD | from dev sweep | TBD | TBD | TBD | Optimized for FA≤10 |

## Migration Plan

1. **Move existing results**: `evaluation/tusz/` → `experiments/eval/baseline/`
2. **Standardize format**: All eval experiments use same structure
3. **One-shot rule**: Each parameter set evaluated exactly once on eval split

## Submission Tracking

- **Baseline results**: Available for paper/benchmark submission
- **Tuned results**: Pending dev optimization completion
- **Final submission**: Will use best clinically viable parameters
