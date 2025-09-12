# NEDC Scoring Integration

This directory contains our integration scripts for using NEDC evaluation tools with SeizureTransformer.

## Directory Structure

```
evaluation/
├── nedc_eeg_eval/         # Official NEDC software from Temple (v6.0.0)
│   └── v6.0.0/           # Unmodified NEDC tools
├── nedc_scoring/          # Our integration scripts
│   ├── convert_predictions.py  # Convert checkpoint to NEDC CSV_bi format
│   ├── create_lists.py         # Generate ref.list / hyp.list (abs paths)
│   ├── post_processing.py      # Threshold + morph ops + eventization
│   └── run_nedc.py             # Run NEDC scorer and parse outputs
└── tusz/                  # TUSZ-specific evaluation
```

## Workflow

1. **Run SeizureTransformer** → Get predictions
2. **Convert to NEDC format** → CSV files with events
3. **Run NEDC scoring** → Official TAES metrics
4. **Parse results** → Extract key metrics

## Usage

```bash
# 1) After running TUSZ evaluation (produces evaluation/tusz/checkpoint.pkl)
python evaluation/nedc_scoring/convert_predictions.py \
  --checkpoint evaluation/tusz/checkpoint.pkl \
  --outdir evaluation/nedc_scoring/output

# 2) Environment for NEDC tools
export NEDC_NFC=$(pwd)/evaluation/nedc_eeg_eval/v6.0.0
export PATH=$NEDC_NFC/bin:$PATH
export PYTHONPATH=$NEDC_NFC/lib:$PYTHONPATH

# 3) Run official NEDC scoring (using wrapper or directly)
python evaluation/nedc_scoring/run_nedc.py
# OR directly:
$NEDC_NFC/bin/nedc_eeg_eval \
  evaluation/nedc_scoring/output/lists/ref.list \
  evaluation/nedc_scoring/output/lists/hyp.list \
  -o evaluation/nedc_scoring/output/results

# Results include:
# - TAES Sensitivity / F1
# - False Alarms per 24h
# - Overlap and Epoch summaries
```

## Why Two Directories?

- `nedc_eeg_eval/` = Temple's official software (untouched)
- `nedc_scoring/` = Our code to use their software

This separation keeps Temple's code pristine while our integration scripts handle the SeizureTransformer-specific parts.
