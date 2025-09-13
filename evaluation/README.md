# Evaluation Tools Directory

This directory contains **tools and infrastructure** for SeizureTransformer evaluation.

**⚠️ Note**: Experimental **results** are stored in `../experiments/` directory.

## Directory Structure

```
evaluation/
├── tusz/                   # TUSZ dataset evaluation scripts
│   └── run_tusz_eval.py    # Main evaluation script (generates checkpoints)
├── nedc_scoring/           # NEDC pipeline tools
│   ├── convert_predictions.py
│   ├── run_nedc.py
│   ├── sweep_operating_point.py
│   └── post_processing.py
└── nedc_eeg_eval/v6.0.0/   # Official NEDC binaries and libraries
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

### Score with NEDC
```bash
# Run NEDC pipeline
cd evaluation/nedc_scoring
make all CHECKPOINT=../../experiments/eval/my_experiment/checkpoint.pkl
```

### Sweep Operating Points
```bash
# Parameter optimization (dev split only)
python evaluation/nedc_scoring/sweep_operating_point.py \
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
