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

### Option 1: Copy Library for Perfect Parallelism (Recommended)
We will copy the `epilepsy_performance_metrics` library to maintain **exact parallelism** with our NEDC approach:

```
evaluation/
├── nedc_eeg_eval/v6.0.0/   # Official NEDC binary (copied, untouched)
├── timescoring/v1.0.0/      # Official timescoring library (copied, untouched)
│   ├── src/timescoring/     # Copy from reference_repos/epilepsy_performance_metrics/src/
│   ├── LICENSE              # Their original license
│   └── README.md            # Note that this is unmodified upstream code
├── nedc_scoring/            # Our NEDC wrapper (done)
│   └── run_nedc.py         # Calls ../nedc_eeg_eval/v6.0.0/
└── szcore_scoring/          # Our SzCORE wrapper (to do)
    ├── __init__.py
    ├── run_szcore.py       # Imports from ../timescoring/v1.0.0/
    ├── convert_to_hedscore.py  # checkpoint.pkl → HED-SCORE TSV
    └── README.md
```

**Why Copy Instead of Pip:**
- **Perfect parallelism**: Both NEDC and SzCORE have their official code in `evaluation/`
- **Version locked**: Exact version v1.0.0, won't break with updates
- **Self-contained**: No external dependencies
- **Clear provenance**: Obviously using unmodified official implementation

**Critical Design Decision:** We will NOT implement native SzCORE. We only need:
1. NEDC official wrapper (done) - provides TAES, OVERLAP, and 3 other metrics
2. SzCORE via copied `timescoring` library - for competition metric comparison
3. Native implementations only for NEDC methods (already have native-overlap)

**Concrete Implementation Plan:**
```python
# evaluation/szcore_scoring/run_szcore.py
"""
Wrapper for SzCORE's Any-Overlap scoring using timescoring library.
This reproduces EpilepsyBench 2025's evaluation methodology.
"""
import sys
import pickle
from pathlib import Path

# Import from our copied library
sys.path.insert(0, str(Path(__file__).parent.parent / 'timescoring' / 'v1.0.0' / 'src'))
from timescoring.annotations import Annotation
from timescoring.scoring import EventScoring

def run_szcore_evaluation(checkpoint_pkl, output_dir):
    """
    Run SzCORE's Any-Overlap scoring (as used in EpilepsyBench).

    Args:
        checkpoint_pkl: Path to checkpoint.pkl from TUSZ evaluation
        output_dir: Where to save SzCORE metrics

    Returns:
        Dict with sensitivity, precision, f1, fpRate matching EpilepsyBench
    """
    # Load predictions from checkpoint
    with open(checkpoint_pkl, 'rb') as f:
        checkpoint = pickle.load(f)

    # Define SzCORE parameters (from challenge description)
    params = EventScoring.Parameters(
        toleranceStart=30,        # 30s pre-ictal tolerance
        toleranceEnd=60,          # 60s post-ictal tolerance
        minOverlap=0,             # ANY overlap (even 1 sample)
        maxEventDuration=5*60,    # Split events > 5 minutes
        minDurationBetweenEvents=90  # Merge events < 90s apart
    )

    all_results = []
    for file_id, data in checkpoint['results'].items():
        # Convert to Annotation objects
        ref = Annotation(data['ground_truth'], fs=256, duration=data['duration'])
        hyp = Annotation(data['predictions'], fs=256, duration=data['duration'])

        # Score with SzCORE parameters
        scores = EventScoring(ref, hyp, params)
        all_results.append({
            'sensitivity': scores.sensitivity,
            'precision': scores.precision,
            'f1': scores.f1,
            'fpRate': scores.fpRate
        })

    # Average across all files (as per SzCORE methodology)
    return aggregate_metrics(all_results)
```

### Option 2: Direct Library Usage
Simply `pip install timescoring` and use it directly in our evaluation scripts. Less clean but faster.

### Option 3: Full Platform Integration (Not Recommended)
Copy entire SzCORE platform. Overkill for our needs - we just need the scoring, not the containerization/CI infrastructure.

## Implementation Approach Clarification

### What We're NOT Doing:
- ❌ Not implementing our own version of SzCORE scoring
- ❌ Not modifying the timescoring library code
- ❌ Not using pip install (to maintain parallelism with NEDC)

### What We ARE Doing:
- ✅ Copying `epilepsy_performance_metrics` to `evaluation/timescoring/v1.0.0/` (untouched)
- ✅ Creating a thin wrapper that imports from the copied library
- ✅ Converting our checkpoint.pkl format to what timescoring expects
- ✅ Perfect parallelism with our NEDC wrapper architecture

### Copy Instructions:
```bash
# Step 1: Copy the library preserving structure
cp -r reference_repos/epilepsy_performance_metrics/src evaluation/timescoring/v1.0.0/
cp reference_repos/epilepsy_performance_metrics/LICENSE evaluation/timescoring/v1.0.0/
cp reference_repos/epilepsy_performance_metrics/README.md evaluation/timescoring/v1.0.0/

# Step 2: Add a note that this is unmodified upstream code
echo "# Note: This is unmodified code from https://github.com/esl-epfl/epilepsy_performance_metrics" > evaluation/timescoring/v1.0.0/DO_NOT_MODIFY.md
```

### Why Copy Instead of Pip:
1. **Perfect parallelism**: Matches NEDC approach exactly
2. **Version control**: We know exactly what version we're using
3. **Reproducibility**: No external dependencies
4. **Clear structure**: Both official implementations live in `evaluation/`

## Recommended Actions

### Phase 1: Immediate (This Week)
1. ✅ Create `SZCORE_INTEGRATION_PLAN.md` (this document)
2. Copy `epilepsy_performance_metrics` to `evaluation/timescoring/v1.0.0/`
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
├── nedc_eeg_eval/v6.0.0/   # Temple's NEDC binary (unmodified, copied)
├── nedc_scoring/            # NEDC wrapper (complete)
│   ├── run_nedc.py         # Calls NEDC binary, extracts 5 metrics
│   ├── convert_predictions.py  # checkpoint.pkl → CSV_bi format
│   └── post_processing.py  # Thresholds and morphological ops
├── szcore_scoring/          # SzCORE wrapper (to create)
│   ├── __init__.py
│   ├── run_szcore.py       # Uses pip-installed timescoring
│   ├── convert_to_hedscore.py  # checkpoint.pkl → HED-SCORE TSV
│   └── README.md           # Usage documentation
└── comparative_analysis/    # Compare both methodologies (Phase 3)
    └── scoring_comparison.py

# Note: reference_repos/epilepsy_performance_metrics/ stays as reference only
# We use pip-installed version, not a local copy
```

## HED-SCORE Conversion Details

```python
# evaluation/szcore_scoring/convert_to_hedscore.py
"""Convert checkpoint.pkl predictions to HED-SCORE TSV format."""

def convert_to_hedscore(checkpoint_pkl, output_dir):
    """
    Convert predictions to HED-SCORE format required by timescoring.

    HED-SCORE TSV format:
    onset	duration	eventType	confidence	channels	dateTime	        recordingDuration
    296.0	40.0    	sz      	n/a     	n/a     	2016-11-06 13:43:04	3600.00
    """
    with open(checkpoint_pkl, 'rb') as f:
        checkpoint = pickle.load(f)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for file_id, data in checkpoint['results'].items():
        events = data['predictions']  # List of (start, end) tuples
        duration = data['duration']

        # Create TSV content
        lines = ['onset\tduration\teventType\tconfidence\tchannels\tdateTime\trecordingDuration']

        for start, end in events:
            onset = start / 256.0  # Convert samples to seconds
            event_duration = (end - start) / 256.0
            # Use dummy datetime (not evaluated)
            lines.append(f'{onset:.1f}\t{event_duration:.1f}\tsz\tn/a\tn/a\t2024-01-01 00:00:00\t{duration:.2f}')

        # Write TSV file
        output_file = output_dir / f'{file_id}.tsv'
        output_file.write_text('\n'.join(lines))
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