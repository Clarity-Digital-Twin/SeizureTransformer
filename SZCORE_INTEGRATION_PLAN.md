# SzCORE Integration Plan

## Executive Summary

SzCORE is the benchmarking platform used by EpilepsyBench 2025. We currently have it as a reference repo, but should consider integrating its scoring methodology (via the `timescoring` library) to enable direct comparison between SzCORE's "Any-Overlap" scoring and Temple's NEDC clinical scoring.

## Current State

### What We Have
1. **Reference Repos:**
   - `reference_repos/szcore/` - The benchmarking platform itself
   - `reference_repos/epilepsy_performance_metrics/` - The scoring library (published as `timescoring` on PyPI)

2. **Existing Integration:**
   - NEDC v6.0.0 integrated at `evaluation/nedc_eeg_eval/v6.0.0/`
   - Clean wrapper at `evaluation/nedc_scoring/run_nedc.py`
   - Already comparing NEDC's 5 metrics (TAES, OVERLAP, DPALIGN, EPOCH, IRA)

### Understanding the Scoring Difference

#### SzCORE/EpilepsyBench Scoring (from their docs):
- **Method:** "Any-Overlap" event-based scoring via `timescoring` library
- **Parameters:**
  - Minimum overlap: ANY overlap (even 1 sample)
  - Pre-ictal tolerance: 30 seconds
  - Post-ictal tolerance: 60 seconds
  - Event merging: < 90 seconds apart
  - Max event duration: 5 minutes (splits longer events)
- **Result on SeizureTransformer:** ~1 FA/24h (reported in paper)

#### Temple NEDC Scoring:
- **TAES (strictest):** 24.15% sensitivity, 137.5 FA/24h
- **OVERLAP (Temple's):** 45.63% sensitivity (still much stricter than SzCORE)
- **DPALIGN:** 52.88% sensitivity

## The Critical Gap

The 137x difference in false alarms (1 FA/24h vs 137.5 FA/24h) is due to:

1. **Tolerance Windows:** SzCORE allows 30s before and 60s after seizures
2. **Any-Overlap:** Even 1-sample overlap counts as correct detection
3. **Event Merging:** Merges events < 90s apart (reduces false alarms)
4. **Clinical vs Competition:** NEDC designed for clinical use, SzCORE for ML competitions

## Integration Strategy

### Option 1: Light Wrapper (Recommended)
Create `evaluation/szcore_scoring/` parallel to `evaluation/nedc_scoring/`:

```
evaluation/
├── nedc_scoring/        # Temple's clinical standard (already done)
│   └── run_nedc.py      # --backend nedc-binary (TAES, OVERLAP, etc.)
├── szcore_scoring/       # EpilepsyBench competition standard (to do)
│   ├── __init__.py
│   ├── run_szcore.py    # Main wrapper using timescoring library
│   ├── convert_to_hedscore.py  # Convert checkpoint.pkl to HED-SCORE format
│   └── README.md
```

**Critical Design Decision:** We will NOT implement native SzCORE. We only need:
1. NEDC official wrapper (done) - provides TAES, OVERLAP, and 3 other metrics
2. SzCORE via timescoring library - for competition metric comparison
3. Native implementations only for NEDC methods (already have native-overlap)

**Implementation:**
```python
# evaluation/szcore_scoring/run_szcore.py
import timescoring  # pip install timescoring

def run_szcore_evaluation(checkpoint_pkl, output_dir):
    """Run SzCORE's Any-Overlap scoring (as used in EpilepsyBench)."""
    # Convert checkpoint.pkl to HED-SCORE format
    # Apply SzCORE parameters (30s pre, 60s post, etc.)
    # Run timescoring with Any-Overlap
    # Return metrics matching EpilepsyBench reporting
```

### Option 2: Direct Library Usage
Simply `pip install timescoring` and use it directly in our evaluation scripts. Less clean but faster.

### Option 3: Full Platform Integration (Not Recommended)
Copy entire SzCORE platform. Overkill for our needs - we just need the scoring, not the containerization/CI infrastructure.

## Recommended Actions

### Phase 1: Immediate (This Week)
1. ✅ Create `SZCORE_INTEGRATION_PLAN.md` (this document)
2. Install `timescoring` library: `pip install timescoring`
3. Create minimal wrapper at `evaluation/szcore_scoring/run_szcore.py`
4. Run on TUSZ eval to get SzCORE metrics (expect ~2-5 FA/24h, not the 137.5 from NEDC)

### Phase 2: Integration (Next Week)
1. Add SzCORE scoring to our sweep pipeline
2. Create comparison table: NEDC (all 5 metrics) vs SzCORE
3. Document the exact parameter differences
4. Add to `run_full_evaluation.sh` with `--backend szcore` option

### Phase 3: Documentation
1. Update README with both scoring methodologies
2. Create visualization showing why scores differ so dramatically
3. Add clinical interpretation guide

## Key Benefits of Integration

1. **Reproducibility:** Verify paper's 1 FA/24h claim
2. **Comparison:** Direct comparison between competition and clinical metrics
3. **Understanding:** Quantify exact impact of each tolerance parameter
4. **Communication:** Better explain to stakeholders why deployment needs differ from competition

## Technical Requirements

```bash
# Install scoring library
pip install timescoring

# Or with visualization
pip install "timescoring[plotting]"
```

## File Structure After Integration

```
evaluation/
├── nedc_eeg_eval/v6.0.0/   # Temple's NEDC binary (unmodified)
├── nedc_scoring/            # NEDC wrapper (complete)
│   └── run_nedc.py         # Calls NEDC binary, extracts 5 metrics
├── szcore_scoring/          # SzCORE wrapper (to create)
│   ├── run_szcore.py       # Uses timescoring library
│   └── hedscore_convert.py # Format conversion
└── comparative_analysis/    # Compare both methodologies
    └── scoring_comparison.py
```

## Next Steps

1. **Decision Required:** Approve Option 1 (Light Wrapper) approach
2. **Install:** `pip install timescoring` in our environment
3. **Implement:** Create `evaluation/szcore_scoring/` directory and wrapper
4. **Validate:** Confirm we can reproduce paper's results
5. **Document:** Update all documentation with dual scoring methodology

## Critical Comparisons

### What This Integration Will Prove
1. **NEDC TAES**: 24.15% sensitivity, 137.5 FA/24h (clinical reality)
2. **NEDC OVERLAP**: 45.63% sensitivity (Temple's overlap, still strict)
3. **SzCORE Any-Overlap**: Expected ~90% sensitivity, ~2-5 FA/24h (competition metrics)

### Why This Matters
- **EpilepsyBench won't report TUSZ eval results** (marked with 🚂) despite patient-disjoint splits
- Even if they did, they'd use SzCORE scoring, not clinical NEDC
- This integration exposes the 30-100x gap between competition and clinical metrics
- Proves that "1 FA/24h" claim is meaningless without specifying the scoring method

## Notes

- SzCORE's "Any-Overlap" is NOT the same as Temple's "OVERLAP" scoring
- The `timescoring` library is well-maintained and actively used by EpilepsyBench
- This integration will definitively answer whether SeizureTransformer achieves:
  - ~1 FA/24h on Dianalund with SzCORE (paper claim)
  - ~2-5 FA/24h on TUSZ with SzCORE (our hypothesis)
  - 137.5 FA/24h on TUSZ with NEDC TAES (our finding)