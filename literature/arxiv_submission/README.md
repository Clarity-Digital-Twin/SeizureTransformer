# arXiv Submission Materials

## Story: SeizureTransformer's 100× False Alarm Reality Check

This directory contains materials for our arXiv preprint revealing the 100-fold gap between SeizureTransformer's benchmark claims and clinical reality when evaluated with proper scoring standards.

## Key Files

### Core Documents
- `PAPER_OUTLINE.md` - Complete paper structure with all sections planned
- `DRAFT_ABSTRACT.md` - Three versions of abstract (250 words each)
- `CONTRIBUTIONS_AND_NOVELTY.md` - Clear statement of contributions
- `FIGURES_PLAN.md` - Detailed figure specifications with code
- `REFERENCES.md` - Complete bibliography with citation strategy

### Single Source of Truth (SSOT)
- `CORE_1_SCORING_METHODOLOGIES.md`
- `CORE_2_SEIZURETRANSFORMER_MODEL.md`
- `CORE_3_EPILEPSYBENCH_SZSCORE.md`
- `CORE_4_NEDC_SOFTWARE.md`
- `CORE_5_TUSZ_DATASET.md`

All other docs and outlines must align to the facts and numbers in these five core documents (e.g., 865 files, 469 seizures, 127.7 hours; NEDC OVERLAP 100.06 FA/24h; SzCORE 8.46 FA/24h; ≈12× difference OVERLAP vs SzCORE; ≈16× TAES vs SzCORE).

### Siena dataset policy
- Siena Scalp EEG Database is used in training by Wu et al. and has no official train/dev/eval splits in its public release.
- Any results we report on Siena with the authors’ pretrained weights are in‑sample diagnostics only and are not comparable to held‑out TUSZ eval results.
- See `SIENA_EVALUATION_NOTES.md` for details and evaluation guidance.

### Narrative Elements
- **The Hook**: 1 FA/24h claimed → 100 FA/24h reality (100× gap)
- **The Discovery**: Scoring alone causes 12× difference
- **The Contribution**: First NEDC evaluation + reproducible pipeline

## Quick Facts for Paper

### Performance Numbers
- **100.06 FA/24h** - NEDC OVERLAP (clinical standard)
- **8.46 FA/24h** - SzCORE (EpilepsyBench standard)
- **12×** - Impact of scoring methodology alone
- **100×** - Gap to Dianalund benchmark claim

### Dataset
- **865 files** - TUSZ v2.0.3 eval set
- **469 seizures** - Ground truth events
- **127.7 hours** - Total recording time
- **100%** - Files successfully processed (865/865; one header repaired on a temporary copy)

### Operating Points
| Target | Best Achieved | Sensitivity |
|--------|--------------|-------------|
| 10 FA/24h | 39.50 FA/24h | 23.45% |
| 2.5 FA/24h | 8.09 FA/24h | 11.51% |
| 1 FA/24h | Not viable | <5% |

## Writing Strategy

### Tone
- **Constructive** not destructive
- **Educational** about scoring differences
- **Respectful** to all parties (Wu, Temple, EpilepsyBench)

### Key Messages
1. Benchmarks without context mislead the field
2. Scoring methodology matters as much as model architecture
3. Clinical deployment requires dataset-matched evaluation

### Target Venues
1. **arXiv** - Immediate dissemination
2. **NeurIPS 2025** - Datasets & Benchmarks track
3. **IEEE TBME** - Clinical validation focus
4. **Frontiers in Digital Health** - Open access, clinical audience

## Figures to Generate

Run these scripts to create publication-ready figures:

```python
# Generate all figures
python literature/arxiv_submission/generate_figures.py

# Individual figures
python literature/arxiv_submission/fig1_performance_spectrum.py
python literature/arxiv_submission/fig2_scoring_comparison.py
python literature/arxiv_submission/fig3_clinical_reality.py
```

## Next Steps

1. [ ] Generate actual figures from data
2. [ ] Write introduction section (2-3 pages)
3. [ ] Complete methods section with technical details
4. [ ] Polish results with statistical tests
5. [ ] Draft discussion connecting to broader implications
6. [ ] Internal review with team
7. [ ] Submit to arXiv

## LaTeX Template

Use NeurIPS 2025 style for consistency:
```bash
wget https://media.neurips.cc/Conferences/NeurIPS2025/Styles/neurips_2025.sty
```

## Data Statement

All evaluation data, code, and results available at:
- Repository: https://github.com/Clarity-Digital-Twin/SeizureTransformer
- Data: TUSZ v2.0.3 (requires DUA from Temple)
- Weights: From Wu et al. repository
- Docker: `seizure-transformer:latest`
