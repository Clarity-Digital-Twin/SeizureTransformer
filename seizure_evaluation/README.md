# Seizure Evaluation Module (Native OVERLAP)

Native Python implementation of the NEDC OVERLAP (OVLP) scorer for ownership and portability.

Important
- Canonical scoring path for TUSZ uses Temple’s official binaries via our wrappers in `evaluation/nedc_eeg_eval/nedc_scoring/`.
- This module exists for parity/tests only. It should not be used for official reporting.

## Layout

```
seizure_evaluation/
├── ovlp/
│   └── overlap_scorer.py   # Native OVERLAP scorer (primary)
└── taes/                   # Back-compat shim (deprecated)
    └── overlap_scorer.py   # Imports from ovlp and warns
```

## Usage (for tests and parity)

```python
from seizure_evaluation.ovlp.overlap_scorer import OverlapScorer
scorer = OverlapScorer()
metrics = scorer.score_from_files(ref_csv_bi, hyp_csv_bi)
```

## Validation targets
- Sensitivity (SEIZ): ±0.1% vs NEDC OVERLAP
- Total FA/24h (SEIZ + BCKG): ±0.1 vs NEDC OVERLAP

## Notes
- Path `seizure_evaluation.taes` remains temporarily for compatibility and will be removed after consumers migrate to `seizure_evaluation.ovlp`.
