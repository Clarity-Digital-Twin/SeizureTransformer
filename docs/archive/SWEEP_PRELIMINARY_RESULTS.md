# Preliminary Parameter Sweep Results

## Status (23:15 EDT)
- **10 FA/24h sweep**: 47/140 completed (33%)
- **2.5 FA/24h sweep**: 47/120 completed (39%)
- **1.0 FA/24h sweep**: 45/150 completed (30%)

## Key Findings So Far

### Paper Defaults (threshold=0.8, kernel=5, min_duration=2.0)
| Metric | Sensitivity | FA/24h | Notes |
|--------|------------|--------|-------|
| **NEDC OVERLAP** | 45.63% | 100.06 | Way too high FA |
| **NEDC TAES** | 24.71% | 134.01 | Also too high |

### Found: Clinical 10 FA/24h Target ✅
**threshold=0.90, kernel=5, min_duration=4.0**
| Metric | Sensitivity | FA/24h | Notes |
|--------|------------|--------|-------|
| **NEDC TAES** | 12.67% | **4.75** | Meets target! |
| **NEDC OVERLAP** | 28.78% | 28.21 | Still high |

### Observations

1. **Threshold Impact**: Moving from 0.8 → 0.9 dramatically reduces FA
   - TAES FA drops from 134 → 4.75 FA/24h (28x reduction!)
   - But sensitivity drops from 24.71% → 12.67%

2. **Min Duration Impact**: Increasing from 2s → 4s helps reduce FA
   - Filters out more brief false positives

3. **OVERLAP vs TAES**:
   - OVERLAP always has higher sensitivity but also higher FA
   - TAES is more conservative (as expected from time-aligned scoring)

## Docker Migration Success! 🎉

Successfully moved **80GB of data** out of codebase:
- `data/tusz/` - 62GB TUSZ dataset
- `data/siena/` - 18GB Siena dataset
- Symlinks created: `wu_2025/data/tusz → ../../data/tusz`
- Docker builds now possible!

## Next Steps

1. Wait for sweeps to complete (~1 hour remaining)
2. Find optimal parameters for each FA target:
   - 10 FA/24h - Clinical screening
   - 2.5 FA/24h - ICU monitoring
   - 1.0 FA/24h - Long-term monitoring
3. Update BENCHMARK_RESULTS.md with final recommendations

## Estimated Completion
Full results expected around **1:00 AM EDT**
