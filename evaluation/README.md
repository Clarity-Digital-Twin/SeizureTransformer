# Evaluation Directory Structure

## Organization
```
evaluation/
├── tusz/             # TUSZ-specific evaluation (paper replication)
├── nedc_eeg_eval/    # Official NEDC software from Temple (v6.0.0)
├── nedc_scoring/     # Our scripts to integrate with NEDC
└── siena/            # Siena evaluation (future)
```

## Running Evaluations

### TUSZ Evaluation (Paper Replication)
```bash
make run-eval-tusz
```
- Reproduces paper's AUROC of 0.876
- Uses paper's threshold of 0.8
- Outputs event-based metrics

### NEDC Official Scoring
```bash
make run-eval-nedc
```
- Uses Temple/NEDC's official TAES scoring
- Provides standardized metrics for comparison
- Includes FA/24h and sensitivity metrics

## Data Requirements
- TUSZ eval set at: `/data/tusz_1_5_2/edf/eval/`
- Model weights at: `wu_2025/src/wu_2025/model.pth`