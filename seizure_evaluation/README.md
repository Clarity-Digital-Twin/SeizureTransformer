# Seizure Evaluation Module

Native Python implementation of NEDC scoring algorithms for full ownership and portability.

## Goal
Replace the external NEDC v6.0.0 binary dependency with our own clean, tested, typed implementation.

## Architecture

```
seizure_evaluation/
├── taes/           # Time-Aligned Event Scoring (PRIMARY)
│   └── scorer.py   ✅ Implemented
├── ovlp/           # Overlap scoring
│   └── scorer.py   ⏳ TODO
├── epoch/          # Epoch-based scoring
│   └── scorer.py   ⏳ TODO
├── dpalign/        # Dynamic Programming Alignment
│   └── scorer.py   ⏳ TODO
└── ira/            # Inter-Rater Agreement
    └── scorer.py   ⏳ TODO
```

## Implementation Status

### Phase 4.1: TAES (CRITICAL PATH) ✅
- Core algorithm implemented
- Matches NEDC for sensitivity, FA/24h, F1
- Integrated with `run_nedc.py --backend native-taes`

### Phase 4.2: Other Scorers (OPTIONAL)
- OVLP: Used for segment-level evaluation
- EPOCH: 10-second window scoring
- DPALIGN: Advanced event alignment
- IRA: Multi-annotator agreement

## Usage

```python
# Direct usage
from seizure_evaluation.taes.scorer import TAESScorer
scorer = TAESScorer(overlap_threshold=0.5)
metrics = scorer.score_from_files(ref_csv_bi, hyp_csv_bi)

# Via run_nedc.py
python evaluation/nedc_scoring/run_nedc.py \
  --backend native-taes \
  --outdir results/
```

## Validation

Must match NEDC within tolerance:
- Sensitivity: ±0.1%
- FA/24h: ±0.1
- F1 Score: ±0.001

## Why This Matters

1. **Portability**: Pure Python, no binary dependencies
2. **Maintainability**: Clean, documented, typed code
3. **Extensibility**: Can add custom metrics
4. **Speed**: Potential for optimization (NumPy, parallel)
5. **Ownership**: We control the entire pipeline