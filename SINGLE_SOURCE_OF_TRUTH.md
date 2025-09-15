# SINGLE SOURCE OF TRUTH - SeizureTransformer Evaluation
**Last Updated**: September 14, 2025, 22:11
**Status**: All scorers working, merge_gap deprecated

## 🎯 VERIFIED RESULTS (Paper Defaults, No Merge Gap)

### Official Performance Numbers
**Parameters**: threshold=0.8, kernel=5, min_duration=2.0, **merge_gap=None**

| Scorer | Sensitivity | FA/24h | F1 Score | Notes |
|--------|------------|--------|----------|-------|
| **NEDC OVERLAP** | 45.63% | 100.06 | 0.519 | Temple's binary event scorer |
| **Native OVERLAP** | 45.63% | 100.06 | 0.519 | Exact parity with NEDC |
| **SzCORE** | 52.35% | 8.46 | - | 90s internal merge reduces FA |

## ✅ WHAT'S WORKING NOW

1. **NEDC Binary v6.0.0** - Temple's official scorer
2. **Native OVERLAP** - Python implementation (exact parity)
3. **SzCORE Wrapper** - timescoring package integration
4. **Import Paths** - All fixed after restructuring
5. **Type Checking** - mypy passes with proper hints

## 🚨 CRITICAL: merge_gap_sec Discovery (see docs/policy/MERGE_GAP_POLICY.md)

### The Problem
- merge_gap_sec=5 was artificially reducing FA by ~4x
- Not from paper, not NEDC standard
- Likely unintentional "reward hacking"

### The Fix
- Deprecated with warnings throughout codebase (see `docs/policy/MERGE_GAP_POLICY.md`)
- Default changed to None/0
- NONSTANDARD_POSTPROCESSING.txt created when used

### Impact on Results
| Config | OVERLAP Sensitivity | OVERLAP FA/24h |
|--------|-------------------|----------------|
| With merge_gap=5 | 41.90% | 25.01 |
| Without merge_gap | 45.63% | 100.06 |

## 📊 CLINICAL OPERATING POINTS

### Current Status
- Paper defaults verified: 100.06 FA/24h at threshold=0.8
- Parameter sweep running for clinical targets
- 84 combinations being tested (7 thresholds × 4 kernels × 3 min_durations)

### Targets
1. **~10 FA/24h** - In progress
2. **~2.5 FA/24h** - Pending
3. **~1.0 FA/24h** - Pending

## 🔧 TECHNICAL STATUS

### Code Quality
```bash
make check-all  # All pass
- Linting: ✅ ruff check passes
- Formatting: ✅ ruff format passes
- Type checking: ✅ mypy passes (no errors)
- Tests: ✅ 18/18 pass
```

### Key Files Updated
- `evaluation/nedc_eeg_eval/nedc_scoring/post_processing.py` - Deprecation warnings
- `evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py` - Default merge_gap=None
- `evaluation/szcore_scoring/run_szcore.py` - Fixed imports and types
- `Makefile` - Updated paths and removed merge_gap from sweep
- `tests/integration/test_nedc_conformance.py` - Fixed import paths

## ⚠️ IMPORTANT NOTES

1. **Always use merge_gap=None** for academic/clinical reporting
2. **NEDC OVERLAP** is our primary metric (matches Temple standards)
3. **SzCORE** has internal 90s merge (reduces FA by ~12x vs NEDC)
4. **AUROC 0.876** matches paper's reported value

## 📈 NEXT STEPS

1. Complete parameter sweep for clinical targets
2. Update BENCHMARK_RESULTS.md with tuned parameters
3. Document final operating points for deployment

**TRUST ONLY ACTUAL TEST OUTPUTS WITH merge_gap=None**
