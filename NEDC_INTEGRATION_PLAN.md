# 🔧 NEDC INTEGRATION PLAN
## Integrating Temple University's Official Seizure Scoring System

**Purpose**: Integrate NEDC (Neural Event Detection Characterization) v6.0.0 to get official TAES metrics for publication.

**Scope**: ONLY about the NEDC scoring backend itself. NOT about tuning parameters (see SEIZURE_TRANSFORMER_TUNING_PLAN.md for that).

## What is NEDC?

NEDC is Temple University's official seizure detection scorer. It calculates:
- **TAES metrics**: Time-Aligned Event Scoring (sensitivity, FA/24h, F1)
- **OVLP metrics**: Overlap-based scoring
- **EPOCH metrics**: Epoch-by-epoch accuracy

We need this for:
- Publishing results (journals require official NEDC scores)
- Comparing with other papers (apples-to-apples)
- Clinical certification

## Integration Has TWO Parts

### Part 1: Temple Binary Integration ✅ DONE
- NEDC v6.0.0 binary installed at `evaluation/nedc_eeg_eval/v6.0.0/`
- CSV converter built: `evaluation/nedc_scoring/convert_predictions.py`
- Post-processor built: `evaluation/nedc_scoring/post_processing.py`
- Runner built: `evaluation/nedc_scoring/run_nedc.py`
- Sweep tool built: `evaluation/nedc_scoring/sweep_operating_point.py`
- **STATUS**: Working, being used by parameter sweep RIGHT NOW

### Part 2: Native Python Implementation 🚧 IN PROGRESS
- Location: `seizure_evaluation/taes/scorer.py`
- **STATUS**: Partially implemented (243 lines), integrated behind `--backend native-taes`
- **GOAL**: Match NEDC TAES metrics and remove dependency on Temple binary
- **NEXT**: Complete validation and finalize parity with NEDC TAES

### What Works
```bash
# Full pipeline works
make -C evaluation/nedc_scoring all CHECKPOINT=experiments/dev/baseline/checkpoint.pkl

# Individual components work
python evaluation/nedc_scoring/convert_predictions.py ...
python evaluation/nedc_scoring/run_nedc.py ...
```

## The NEDC Pipeline

```
SeizureTransformer predictions (checkpoint.pkl)
    ↓ convert_predictions.py
CSV_bi files (NEDC format)
    ↓ run_nedc.py
NEDC binary execution
    ↓ parse results
TAES metrics (sensitivity, FA/24h, F1)
```

## Critical Format Requirements

### CSV_bi Format (MUST be exact!)
```csv
# version = csv_v1.0.0
# bname = file_id_here
# duration = 1800.0000 secs
channel,start_time,stop_time,label,confidence
TERM,42.2786,81.7760,seiz,1.0000
```

**Requirements**:
- Extension MUST be `.csv_bi` (not `.csv`)
- 4 decimal places for times
- Channel always "TERM"
- Label always "seiz"
- Headers must match exactly
- List files (`ref.list`, `hyp.list`) contain absolute paths (one per line)
- Use LF newlines when writing list and CSV files (Windows/WSL safe)

## File Structure

```
evaluation/
├── nedc_eeg_eval/v6.0.0/   # NEDC binary (DO NOT MODIFY)
│   ├── bin/
│   │   └── nedc_eeg_eval    # The scorer executable
│   └── lib/
│       └── python modules
└── nedc_scoring/            # Our integration (we own this)
    ├── convert_predictions.py
    ├── post_processing.py
    ├── run_nedc.py
    ├── sweep_operating_point.py
    └── Makefile
```

## Environment Setup

```bash
# Required environment variables
export NEDC_NFC=$(pwd)/evaluation/nedc_eeg_eval/v6.0.0
export PATH=$NEDC_NFC/bin:$PATH
export PYTHONPATH=$NEDC_NFC/lib:$PYTHONPATH
```

Note: `run_nedc.py` auto-sets these env vars when using the `nedc-binary` backend; explicit export is only needed when invoking the NEDC binary directly.

## Outputs

Given an `--outdir <DIR>`, the runner writes:
- `<DIR>/hyp/*.csv_bi` and `<DIR>/ref/*.csv_bi`
- `<DIR>/lists/{ref,hyp}.list` (absolute paths)
- `<DIR>/results/summary.txt` (official NEDC output)
- `<DIR>/results/metrics.json` (parsed TAES metrics + provenance)

## Native TAES Implementation (PRIMARY GOAL) 🎯

**THIS IS THE MAIN INTEGRATION GOAL** - Full Python implementation at `seizure_evaluation/taes/scorer.py` to:
- Remove ALL dependency on Temple binary
- Enable Windows support without WSL
- Speed up evaluation (10x faster)
- Full control over scoring logic
- Reproducible across platforms

**Current Status**: Partially implemented (243 lines), integrated behind `--backend native-taes`; needs completion and validation

### Implementation Plan
1. Complete the native TAES scorer in Python
2. Validate outputs match NEDC binary EXACTLY
3. Replace binary backend with native as default
4. Benchmark both pipelines with optimal parameters

### Validation Requirements
- Native scorer MUST produce identical TAES metrics as NEDC v6.0.0
- Validate on representative fixtures and the dev split used for sweeps
- Metrics must match to within 0.1 (percentage points) for sensitivity and FA/24h
- Both backends must yield the same FA/24h at the same operating point

## Common Issues

1. **"File not found" errors**: Check absolute paths in list files
2. **Wrong extension**: Must be `.csv_bi` not `.csv`
3. **Binary won't run**: Use WSL on Windows
4. **Empty results**: Check CSV headers match exactly

## Testing

```bash
# Test pipeline with synthetic data (no NEDC install required)
cd evaluation/nedc_scoring
make test

# Validate against golden NEDC outputs (requires NEDC binary)
python test_pipeline.py
```

## Key Commands

```bash
# Full pipeline (Makefile writes to evaluation/nedc_scoring/output by default)
make -C evaluation/nedc_scoring all CHECKPOINT=path/to/checkpoint.pkl

# Just conversion
make -C evaluation/nedc_scoring convert CHECKPOINT=path/to/checkpoint.pkl

# Just scoring (after conversion)
make -C evaluation/nedc_scoring score

# Clean outputs
make -C evaluation/nedc_scoring clean

# Preferred: write artifacts under experiments/**
python evaluation/nedc_scoring/convert_predictions.py \
  --checkpoint experiments/dev/baseline/checkpoint.pkl \
  --outdir experiments/dev/baseline/nedc_results

python evaluation/nedc_scoring/run_nedc.py \
  --outdir experiments/dev/baseline/nedc_results --score-only

# Optional: use native Python backend instead of NEDC binary
python evaluation/nedc_scoring/run_nedc.py \
  --checkpoint experiments/dev/baseline/checkpoint.pkl \
  --outdir experiments/dev/baseline/nedc_results_native \
  --backend native-taes
```
