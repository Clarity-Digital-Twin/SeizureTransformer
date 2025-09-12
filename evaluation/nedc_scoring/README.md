# NEDC Scoring Integration

This directory contains our integration scripts for using NEDC evaluation tools with SeizureTransformer.

## Directory Structure

```
evaluation/
├── nedc_eeg_eval/         # Official NEDC software from Temple (v6.0.0)
│   └── v6.0.0/           # Unmodified NEDC tools
├── nedc_scoring/          # Our integration scripts
│   ├── convert_to_csv.py # Convert SeizureTransformer output to NEDC format
│   ├── run_scoring.py     # Run NEDC evaluation
│   └── parse_results.py   # Parse NEDC output for metrics
└── tusz/                  # TUSZ-specific evaluation
```

## Workflow

1. **Run SeizureTransformer** → Get predictions
2. **Convert to NEDC format** → CSV files with events
3. **Run NEDC scoring** → Official TAES metrics
4. **Parse results** → Extract key metrics

## Usage

```bash
# After running TUSZ evaluation
python evaluation/nedc_scoring/convert_to_csv.py

# Run official NEDC scoring
python evaluation/nedc_scoring/run_scoring.py

# Results will show:
# - TAES Sensitivity
# - False Alarms/24h
# - Other NEDC metrics
```

## Why Two Directories?

- `nedc_eeg_eval/` = Temple's official software (untouched)
- `nedc_scoring/` = Our code to use their software

This separation keeps Temple's code pristine while our integration scripts handle the SeizureTransformer-specific parts.