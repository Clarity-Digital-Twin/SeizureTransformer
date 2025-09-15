# Results

Purpose: present key numbers clearly and concisely.

Use SSOT: `core_documents/CORE_SYNTHESIS.md`, `core_documents/FIGURES_PLAN.md`, `docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md` (source values).

- Default params: report sensitivity and FA/24h for all four scoring methods
- Operating points: 10 FA/24h target, 2.5 FA/24h target — what is achievable
- Scoring impact: ≈3.1× difference at default (OVERLAP vs SzCORE); TAES >> OVERLAP
- NEDC/Python parity: identical numbers for OVERLAP
- Figures: references to Fig. 1 (performance spectrum), Fig. 3 (clinical zones)

Key numbers (TUSZ v2.0.3 eval, 865 files)

- Default (t=0.80, k=5, m=2.0):
  - NEDC OVERLAP: 45.63% sensitivity, 26.89 FA/24h (SEIZ)
  - NEDC TAES: 65.21% sensitivity, 136.73 FA/24h
  - Native OVERLAP: 45.63% sensitivity, 26.89 FA/24h (parity)
  - SzCORE: 52.35% sensitivity, 8.59 FA/24h

- 10 FA target (t=0.88, k=5, m=3.0):
  - OVERLAP: 33.90% sensitivity, 10.27 FA/24h (near 10; <50% sens)
  - TAES: 60.45% sensitivity, 83.88 FA/24h (does not meet FA target)
  - SzCORE: 40.59% sensitivity, 3.36 FA/24h

- 2.5 FA target (t=0.95, k=5, m=5.0):
  - OVERLAP: 14.50% sensitivity, 2.05 FA/24h (meets FA; very low sens)
  - TAES: 18.12% sensitivity, 10.64 FA/24h (does not meet FA target)
  - SzCORE: 19.71% sensitivity, 0.75 FA/24h

Results provenance
- Predictions produced by authors’ pretrained weights (trained on TUSZ train + Siena), with our inference pipeline matching OSS preprocessing.
- Tuning performed only on TUSZ dev (1,832 files); no eval contamination.
- Final metrics computed on TUSZ eval (865 files) using four scorers on identical predictions.
