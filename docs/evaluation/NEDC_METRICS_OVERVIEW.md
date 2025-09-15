# NEDC v6.0.0 Scoring Metrics Overview

## What NEDC Actually Provides

NEDC v6.0.0 automatically calculates **5 different scoring methods** when evaluating seizure detection:

### 1. TAES (Time-Aligned Event Scoring)
- **Our Results**: Pending re‑extraction at paper defaults (do not cite legacy values)
- **Description**: Strictest clinical standard with fractional scoring based on temporal alignment
- **Why we use it**: Most realistic for clinical deployment, penalizes timing errors

### 2. OVERLAP Scoring
- **Our Results**: 45.63% sensitivity, 26.89 FA/24h (SEIZ, paper defaults; merge_gap=None)
- **Description**: Counts detection if ANY overlap exists between prediction and ground truth
- **Important**: This is NOT the same as SzCORE's "Any-Overlap" - Temple's version is still strict about timing boundaries

### 3. DPALIGN (Dynamic Programming Alignment)
- **Our Results**: 52.88% sensitivity (248/469 seizures)
- **Description**: Uses dynamic programming to optimally align predicted events with reference events
- **Use case**: Understanding how well events match when optimally paired

### 4. EPOCH Scoring
- **Description**: Evaluates on fixed time windows (e.g., 1-second epochs)
- **Use case**: Comparing performance at specific time resolutions

### 5. IRA (Inter-Rater Agreement)
- **Description**: Measures agreement between reference and hypothesis like human annotators would
- **Use case**: Statistical agreement metrics similar to Cohen's kappa

## Key Insights from Our Evaluation

When we run NEDC on SeizureTransformer's TUSZ predictions:

```
Metric          | Sensitivity | False Alarms | Notes
----------------|-------------|--------------|-------
TAES            | TBD         | TBD          | Strictest (pending re‑extraction)
OVERLAP         | 45.63%      | 26.89 FA/24h | Temple's overlap (SEIZ FA)
DPALIGN         | —           | —            | See NEDC summary for details
```

## Critical Observation

The gap between NEDC OVERLAP and SzCORE Any‑Overlap (30s/60s tolerances with 90s merge) highlights the scoring methodology differences; SzCORE typically reports substantially lower FA for the same predictions.

## Future Integration Opportunities

Currently we only report TAES metrics in our README, but we could:
1. Add a comprehensive metrics table showing all 5 NEDC scores
2. Compare NEDC OVERLAP vs SzCORE Any-Overlap directly
3. Use EPOCH scoring for fixed-window analysis
4. Report IRA for statistical agreement metrics

## Implementation Status

- ✅ All 5 metrics are computed automatically by `evaluation/nedc_eeg_eval/v6.0.0/bin/nedc_eeg_eval`
- ✅ Results stored in `evaluation/nedc_eeg_eval/nedc_scoring/output/results/summary.txt`
- ✅ Our pipeline (`evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py`) runs the full suite
- ✅ We extract OVERLAP metrics explicitly and duplicate to `taes` for backward-compat; always state which metric is used

## Citation

```bibtex
@incollection{shah2021nedc,
  title = {Objective Evaluation Metrics for Automatic Classification of EEG Events},
  author = {Shah, V. and Golmohammadi, M. and Obeid, I. and Picone, J.},
  booktitle = {Signal Processing in Medicine and Biology},
  year = {2021}
}
```
