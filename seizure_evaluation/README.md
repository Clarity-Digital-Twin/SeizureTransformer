# Seizure Evaluation Module

Native Python implementation of NEDC scoring algorithms for full ownership and portability.

## Goal
Replace the external NEDC v6.0.0 binary dependency with our own clean, tested, typed implementation.

## Architecture

```
seizure_evaluation/
├── taes/
│   ├── overlap_scorer.py  ✅ OVERLAP scoring (PRIMARY)
│   └── scorer.py          🛈 Legacy greedy scorer (not used)
├── epoch/                 # Epoch-based scoring (future)
│   └── scorer.py          ⏳ TODO
├── dpalign/               # Dynamic Programming Alignment (future)
│   └── scorer.py          ⏳ TODO
└── ira/                   # Inter-Rater Agreement (future)
    └── scorer.py          ⏳ TODO
```

## Implementation Status

### Phase 4.1: OVERLAP (CRITICAL PATH) ✅
- Exact any-overlap semantics implemented (SEIZ + BCKG totals)
- Matches Temple OVERLAP for SEIZ sensitivity and TOTAL FA/24h
- Integrated with `run_nedc.py --backend native-taes`

### Phase 4.2: Other Scorers (OPTIONAL)
- OVLP: Used for segment-level evaluation
- EPOCH: 10-second window scoring
- DPALIGN: Advanced event alignment
- IRA: Multi-annotator agreement

## Usage

```python
# Direct usage (OVERLAP)
from seizure_evaluation.taes.overlap_scorer import OverlapScorer
scorer = OverlapScorer()
metrics = scorer.score_from_files(ref_csv_bi, hyp_csv_bi)

# Via run_nedc.py
python evaluation/nedc_scoring/run_nedc.py \
  --backend native-taes \
  --outdir results/
```

## Validation

Must match NEDC OVERLAP within tolerance:
- SEIZ Sensitivity: ±0.1%
- Total FA/24h (SEIZ + BCKG): ±0.1
- F1 Score: informational (aggregation differences)

## Why This Matters

1. **Portability**: Pure Python, no binary dependencies
2. **Maintainability**: Clean, documented, typed code
3. **Extensibility**: Can add custom metrics
4. **Speed**: Potential for optimization (NumPy, parallel)
5. **Ownership**: We control the entire pipeline
