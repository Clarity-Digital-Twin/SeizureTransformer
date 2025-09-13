# Scripts Directory

High-level orchestration and experiment management scripts.

## Scripts

### `experiment_tracker.py`
Manages experiment configuration and tracking across dev/eval splits.
```bash
# Create experiment config
python scripts/experiment_tracker.py create-config \
    --split dev --description "baseline" \
    --threshold 0.6 --kernel 11

# Compare experiments
python scripts/experiment_tracker.py compare --split dev
```

### `visualize_results.py`
Generate plots and visualizations from experiment results.
```bash
python scripts/visualize_results.py \
    --checkpoint experiments/eval/baseline/checkpoint.pkl \
    --output experiments/eval/baseline/plots/
```

## Organization

- **Experiment Management**: `experiment_tracker.py`, `visualize_results.py`
- **Dataset-specific tools**: Moved to `evaluation/<dataset>/`
- **Evaluation utilities**: Moved to `evaluation/utils/`

This keeps high-level orchestration separate from evaluation implementation details.