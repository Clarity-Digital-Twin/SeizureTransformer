# Evaluation Tools Directory

This directory contains **tools and infrastructure** for SeizureTransformer evaluation.

**⚠️ Note**: Experimental **results** are stored in `../experiments/` directory.

## Directory Structure

```
evaluation/
├── nedc_eeg_eval/nedc_scoring/  # NEDC evaluation and parameter optimization
│   ├── convert_predictions.py    # Convert predictions to NEDC CSV_bi format
│   ├── post_processing.py        # Apply thresholds and morphological operations
│   ├── run_nedc.py               # Run NEDC scorer and extract metrics
│   ├── sweep_operating_point.py  # Grid search for optimal parameters
│   └── test_pipeline.py          # Validate pipeline with synthetic data
│
├── tusz/                   # TUSZ dataset evaluation scripts
│   └── run_tusz_eval.py    # Main evaluation script (generates checkpoints)
│
├── utils/                  # Shared evaluation utilities
│   ├── monitor_evaluation.sh    # Monitor running evaluations
│   └── enhance_evaluation_robustness.py # Add robustness improvements
│
└── nedc_eeg_eval/v6.0.0/   # Official NEDC binaries and libraries (do not modify)
```

## Tools vs Results Separation

### 🛠️ Tools (Stay in `evaluation/`)
- **Scripts**: Evaluation pipelines, converters, scorers
- **Binaries**: NEDC v6.0.0 official evaluation software
- **Infrastructure**: Reusable components across experiments

### 📊 Results (Go to `experiments/`)
- **Checkpoints**: Model predictions (*.pkl files)
- **Metrics**: NEDC scoring outputs, JSON summaries
- **Logs**: Execution logs, parameter records

## Running Evaluations

### Generate Predictions
```bash
# Create experiment checkpoint
python evaluation/tusz/run_tusz_eval.py \
  --data_dir /path/to/TUSZ/eval \
  --out_dir experiments/eval/my_experiment \
  --device auto
```

Tip: Run scripts from the repository root to avoid creating nested
`evaluation/...` paths due to relative paths. See
`evaluation/nedc_eeg_eval/nedc_scoring/README.md` for details.

### Score with NEDC
```bash
# Run NEDC pipeline
cd evaluation/nedc_eeg_eval/nedc_scoring
make all CHECKPOINT=../../experiments/eval/my_experiment/checkpoint.pkl

# Or directly, with explicit FA reporting policy
python run_nedc.py \
  --checkpoint ../../experiments/eval/my_experiment/checkpoint.pkl \
  --outdir ../../experiments/eval/my_experiment/nedc_results \
  --fa_reporting seiz  # choices: seiz | total | both (default: seiz)
```

### Sweep Operating Points
```bash
# Parameter optimization (dev split only)
python evaluation/nedc_eeg_eval/nedc_scoring/sweep_operating_point.py \
  --checkpoint experiments/dev/baseline/checkpoint.pkl \
  --target_fa_per_24h 10
```

## Migration Complete

✅ **Moved to experiments/eval/baseline/**:
- `checkpoint.pkl` (470MB baseline predictions)
- `results.json` (AUROC and sample-level metrics)  
- `eval_log.txt` (execution log)

✅ **Remaining in evaluation/tusz/**:
- `run_tusz_eval.py` (evaluation script - reusable tool)

This organization follows ML best practices:
- **Tools are version-controlled and shared**
- **Results are experiment-specific and tracked separately**
- **Clear separation between infrastructure and outputs**
