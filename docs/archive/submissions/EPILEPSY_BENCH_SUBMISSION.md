# Epilepsy Bench / SzCORE Submission (Archived Draft)

Archived until we finalize clinical tuning points and refresh all numbers from SINGLE_SOURCE_OF_TRUTH.md (no merge). When reviving, clearly specify the metric (TAES vs OVERLAP) and ensure defaults match docs/evaluation/EVALUATION_RESULTS_TABLE.md.

## Model Information

**Model Name**: SeizureTransformer  
**Version**: 1.0 (Wu et al., 2025)  
**Architecture**: U-Net encoder + Transformer decoder  
**Training Data**: Proprietary multi-center dataset (not TUSZ)  
**Evaluation**: TUSZ v2.0.3 eval split (zero-shot)  

## Submission Details

### Dataset Evaluated
- **Dataset**: Temple University Hospital EEG Seizure Corpus (TUSZ)
- **Version**: 2.0.3
- **Split**: eval (held-out test set)
- **Files**: 865/865 (all processed; one header repaired on a copy)
- **Duration**: 127.6 hours
- **Seizure Events**: 469

### Evaluation Protocol
- **Scorer**: NEDC EEG Eval v6.0.0 (official Temple University release)
- **Scoring Method**: TAES (Time-Aligned Event Scoring)
- **Post-processing**:
  - Probability threshold: 0.8
  - Morphological operations: kernel size 5
  - Minimum event duration: 2.0 seconds
- **Sampling Rate**: 256 Hz (model native)

## Results

### TAES Metrics (Event-based)
| Metric | Value |
|--------|-------|
| Sensitivity (Recall) | 24.71% |
| Precision (PPV) | 59.57% |
| F1 Score | 0.3493 |
| False Alarms per 24h | 60.83 |

### Sample-based Metrics
| Metric | Value |
|--------|-------|
| AUROC | 0.9021 |
| Sensitivity @ 0.8 threshold | 24.71% |
| Specificity @ 0.8 threshold | 93.09% |

## Reproducibility

### Code Repository
- **URL**: https://github.com/Clarity-Digital-Twin/SeizureTransformer
- **Commit**: [TO BE ADDED AFTER PUBLIC]
- **License**: MIT

### Model Weights
- **Location**: `wu_2025/src/wu_2025/model.pth`
- **Size**: 168 MB
- **SHA256**: [TO BE COMPUTED]

### Environment
```yaml
python: 3.10.12
pytorch: 2.0.1+cu117
cuda: 12.4
numpy: 1.24.3
mne: 1.7.1
pyedflib: 0.1.38
```

### Running the Evaluation
```bash
# 1. Clone repository
git clone https://github.com/Clarity-Digital-Twin/SeizureTransformer
cd SeizureTransformer

# 2. Setup environment
uv venv
source .venv/bin/activate
uv pip install ./wu_2025
uv pip install -e . --extra dev

# 3. Run TUSZ evaluation
python evaluation/tusz/run_tusz_eval.py \
    --data_dir /path/to/TUSZ/v2.0.3/eval \
    --output_dir evaluation/tusz \
    --device cuda

# 4-5. Convert + run NEDC scoring
python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py \
  --checkpoint experiments/eval/baseline/checkpoint.pkl \
  --outdir experiments/eval/baseline/nedc_results
```

## Key Findings

1. **High AUROC (0.9021)** indicates good discrimination ability at the sample level
2. **Low event-based sensitivity (24.15%)** suggests difficulty with seizure boundaries
3. **High false alarm rate (60.83/day)** far exceeds clinical acceptability (< 10/day)
4. **Threshold optimization needed**: Current 0.8 threshold may be suboptimal for TUSZ

## Notes for Benchmark

- This is a **zero-shot evaluation** (model not trained on TUSZ)
- Results represent **out-of-domain generalization** performance
- The paper's reported "1 FA/day" is from Dianalund dataset, not TUSZ
- We provide full NEDC output files for verification

## Contact

**Submitter**: Clarity Digital Twin Team  
**Email**: [REDACTED]  
**Repository Issues**: https://github.com/Clarity-Digital-Twin/SeizureTransformer/issues

## Declaration

We confirm that:
- [ ] Model was not trained on TUSZ eval split
- [ ] Evaluation uses official NEDC v6.0.0 scorer
- [ ] Results are reproducible with provided code
- [ ] No manual tuning on eval set was performed
