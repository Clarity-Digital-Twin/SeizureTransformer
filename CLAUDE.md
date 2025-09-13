# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Critical Repository Structure

This is a private fork of SeizureTransformer for clinical evaluation. The codebase has a strict separation:

- **`wu_2025/`** - NEVER MODIFY. Original upstream code containing the pretrained model (`model.pth`, 168MB)
- **`evaluation/`** - Active development area for TUSZ dataset evaluation and NEDC scoring
- **`scripts/`, `tests/`, `docs/`** - Safe to modify for development

## Build and Environment Commands

```bash
# Environment setup (using uv for speed)
uv venv
source .venv/bin/activate
uv pip install ./wu_2025
uv pip install -e . --extra dev

# Linting and type checking
ruff check evaluation/ scripts/ tests/
ruff format evaluation/ scripts/ tests/
mypy evaluation/ scripts/ tests/

# Testing
pytest tests/                     # All tests
python tests/test_inference.py    # Quick inference check
python evaluation/nedc_scoring/test_pipeline.py  # NEDC pipeline validation

# Run model inference
python -m wu_2025 input.edf output.tsv
```

## Architecture Overview

### SeizureTransformer Model Pipeline
```
EDF Input (19 channels, unipolar) 
    ↓ Z-score normalization
    ↓ Resample to 256 Hz
    ↓ Bandpass 0.5-120 Hz
    ↓ Notch filter at 60 Hz
    ↓ 60-second windows (15,360 samples)
SeizureTransformer (Transformer architecture)
    ↓ Per-sample probabilities [0,1]
    ↓ Threshold at 0.8
    ↓ Morphological operations (kernel=5)
    ↓ Remove events < 2 seconds
Seizure Events (start_sec, end_sec)
```

### NEDC Evaluation Pipeline (Temple University Standard)
```
evaluation/tusz/run_tusz_eval.py
    ↓ Generates checkpoint.pkl with predictions
evaluation/nedc_scoring/convert_predictions.py  
    ↓ Converts to NEDC CSV_bi format (NOT .csv!)
evaluation/nedc_scoring/run_nedc.py
    ↓ Runs NEDC v6.0.0 binary for TAES metrics
Results: Sensitivity, False Alarms/24h, F1 Score
```

## Key Technical Specifications

### Model Requirements
- **Input**: 19 channels, unipolar montage, continuous EDF
- **Sampling**: 256 Hz (model expectation)
- **Window**: 60 seconds for inference (no overlap)
- **Output**: Per-sample seizure probability at 256 Hz

### Post-Processing Parameters (Paper Specifications)
- Threshold: 0.8
- Morphological kernel size: 5 samples
- Minimum event duration: 2.0 seconds
- All timing conversions: samples / 256 = seconds

### NEDC CSV_bi Format (Critical)
```csv
# version = csv_v1.0.0
# bname = file_id
# duration = 1800.0000 secs
channel,start_time,stop_time,label,confidence
TERM,42.2786,81.7760,seiz,1.0000
```
- Extension MUST be `.csv_bi` not `.csv`
- Times use 4 decimal places
- Channel is always "TERM"

## Current Evaluation Status

The TUSZ evaluation pipeline (`evaluation/tusz/run_tusz_eval.py`) processes 865 EDF files from the Temple University Hospital EEG dataset. Results are stored in `checkpoint.pkl` containing predictions and ground truth events for NEDC scoring.

## Important Files and Their Purposes

- `SEIZURE_TRANSFORMER_TUNING_PLAN.md` - How to tune post-processing parameters on dev set
- `NEDC_INTEGRATION_PLAN.md` - How to integrate NEDC scoring backend
- `docs/IDEAL_REFERENCE_SEIZURE_TRANSFORMER_DATAFLOW.md` - Architecture documentation
- `evaluation/nedc_eeg_eval/v6.0.0/` - NEDC binaries (do not modify)
- `wu_2025/src/wu_2025/model.pth` - Pretrained weights (do not modify)

## Git Remote Structure

- `origin` - Private repo (Clarity-Digital-Twin/SeizureTransformer)
- `upstream` - Original repo (keruiwu/SeizureTransformer) 
- `fork` - Public fork for clean PRs

## Common Tasks

### Run Full NEDC Evaluation
```bash
# After TUSZ evaluation completes
cd evaluation/nedc_scoring
make test      # Validate pipeline with synthetic data
make all       # Run full NEDC scoring pipeline
```

### Debug Failed TUSZ Files
```bash
# Check evaluation log
tail -f evaluation/tusz/eval_log.txt

# Inspect checkpoint for errors
python -c "import pickle; c = pickle.load(open('evaluation/tusz/checkpoint.pkl', 'rb')); 
print([k for k,v in c['results'].items() if v.get('error')])"
```

### Environment Variables for NEDC
```bash
export NEDC_NFC=$(pwd)/evaluation/nedc_eeg_eval/v6.0.0
export PATH=$NEDC_NFC/bin:$PATH
export PYTHONPATH=$NEDC_NFC/lib:$PYTHONPATH
```
