# NEDC Scoring Integration

This directory contains our integration scripts for using NEDC evaluation tools with SeizureTransformer.

## Directory Structure

```
evaluation/
├── nedc_eeg_eval/                 # Official NEDC software from Temple (v6.0.0)
│   └── v6.0.0/                    # Unmodified NEDC tools
└── nedc_eeg_eval/nedc_scoring/    # Our integration scripts (this folder)
    ├── convert_predictions.py     # Convert checkpoint to NEDC CSV_bi format
    │                              # (also generates ref.list / hyp.list)
    ├── post_processing.py         # Threshold + morph ops + eventization
    └── run_nedc.py                # Run NEDC scorer and parse outputs
```

## Backends

- `nedc-binary` (default): Uses Temple’s official v6.0.0 scorer under `evaluation/nedc_eeg_eval/v6.0.0`.
- `native-overlap`: Uses our native Python OVERLAP scorer (`seizure_evaluation/ovlp`). Useful for portability checks.

Select with `--backend {nedc-binary,native-overlap}` in `run_nedc.py`.

## Workflow

1. **Run SeizureTransformer** → Get predictions
2. **Convert to NEDC format** → CSV files with events
3. **Run NEDC scoring** → Official TAES metrics
4. **Parse results** → Extract key metrics

## Usage

```bash
# 1) After running TUSZ evaluation (produces experiments/*/checkpoint.pkl)
python evaluation/nedc_eeg_eval/nedc_scoring/convert_predictions.py \
  --checkpoint experiments/eval/baseline/checkpoint.pkl \
  --outdir evaluation/nedc_eeg_eval/nedc_scoring/output

# 2) Environment for NEDC tools
export NEDC_NFC=$(pwd)/evaluation/nedc_eeg_eval/v6.0.0
export PATH=$NEDC_NFC/bin:$PATH
export PYTHONPATH=$NEDC_NFC/lib:$PYTHONPATH

# 3) Run official NEDC scoring (using wrapper or directly)
python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py
# OR directly:
$NEDC_NFC/bin/nedc_eeg_eval \
  evaluation/nedc_eeg_eval/nedc_scoring/output/lists/ref.list \
  evaluation/nedc_eeg_eval/nedc_scoring/output/lists/hyp.list \
  -o evaluation/nedc_eeg_eval/nedc_scoring/output/results

# Results include:
# - TAES Sensitivity / F1
# - False Alarms per 24h
# - Overlap and Epoch summaries
```

## Outputs

- Converted files: `output/hyp/*.csv_bi`, `output/ref/*.csv_bi`
- Pair lists for NEDC: `output/lists/{ref.list,hyp.list}`
- Results: `output/results/*` plus `metrics.json` and `operating_point.json`

## Why Two Directories?

- `nedc_eeg_eval/` = Temple's official software (untouched)
- `nedc_scoring/` = Our code to use their software

This separation keeps Temple's code pristine while our integration scripts handle the SeizureTransformer-specific parts.

## Deprecated

- `run_nedc_scoring.py` is a legacy stub. Use `run_nedc.py` instead.

## Conventions and tips

- Always invoke these scripts from the repository root to avoid creating nested
  `evaluation/...` directories due to relative paths. Example:
  `python evaluation/nedc_eeg_eval/nedc_scoring/test_pipeline.py` (run from repo root).
- Prefer `run_nedc.py --outdir <your/experiments/path>` for repeatable runs;
  avoid writing inside `v6.0.0/` which must remain pristine.

## Troubleshooting

- If you see nested paths (e.g., `evaluation/nedc_eeg_eval/nedc_scoring/evaluation/...`),
  they were created by running from the wrong CWD. Delete them safely and re-run from the repo root.
