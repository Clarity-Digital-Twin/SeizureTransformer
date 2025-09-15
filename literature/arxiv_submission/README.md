# arXiv Submission Materials

## Story: SeizureTransformer's 27–137× False Alarm Reality Check

This directory contains materials for our arXiv preprint revealing the 27–137× gap between SeizureTransformer's benchmark claims and clinical reality when evaluated with proper scoring standards.

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

All other docs and outlines must align to the facts and numbers in these five core documents (e.g., 865 files, 469 seizures, 127.7 hours; NEDC OVERLAP 26.89 FA/24h; SzCORE 8.59 FA/24h; ≈3.1× difference OVERLAP vs SzCORE at default; ≈16× TAES vs SzCORE).

### Siena dataset policy
- Siena Scalp EEG Database is used in training by Wu et al. and has no official train/dev/eval splits in its public release.
- Any results we report on Siena with the authors’ pretrained weights are in‑sample diagnostics only and are not comparable to held‑out TUSZ eval results.
- See `SIENA_EVALUATION_NOTES.md` for details and evaluation guidance.

### Narrative Elements
- **The Hook**: 1 FA/24h claimed → 26.89–136.73 FA/24h reality (27×–137× gap across scorers)
- **The Discovery**: Scoring and definition choice (SEIZ vs TOTAL) change FA/24h by multiples (≈3.1× default OVERLAP vs SzCORE; TAES much higher than OVERLAP)
- **The Contribution**: First NEDC evaluation + reproducible pipeline

## Quick Facts for Paper

### Performance Numbers
- **26.89 FA/24h (SEIZ)** - NEDC OVERLAP default (Temple)
- **136.73 FA/24h** - NEDC TAES default (Temple)
- **8.59 FA/24h** - SzCORE default (EpilepsyBench)
- **≈3.1×** - OVERLAP vs SzCORE FA at default (26.89 / 8.59)
- **27×–137×** - Gap to “1 FA/24h” claim depending on scorer

### Dataset
- **865 files** - TUSZ v2.0.3 eval set
- **469 seizures** - Ground truth events
- **127.7 hours** - Total recording time
- **100%** - Files successfully processed (865/865; one header repaired on a temporary copy)

### Operating Points
| Target | OVERLAP (FA/24h, Sens) | TAES (FA/24h, Sens) | SzCORE (FA/24h, Sens) |
|--------|-------------------------|---------------------|------------------------|
| Default | 26.89, 45.63% | 136.73, 65.21% | 8.59, 52.35% |
| 10 FA | 10.27, 33.90% | 83.88, 60.45% | 3.36, 40.59% |
| 2.5 FA | 2.05, 14.50% | 10.64, 18.12% | 0.75, 19.71% |

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
