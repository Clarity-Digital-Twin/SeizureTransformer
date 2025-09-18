# arXiv Paper Conversion Guide

## Final PDF Location
- **Final PDF**: `SEIZURE_TRANSFORMER_ARXIV_FINAL.pdf` (no TOC; references match citations)

## Source Files Required
1. **Markdown source**: `PAPER_FINAL_FORMATTED_RENUMBERED.md` (contains YAML header; citations renumbered by first appearance)
2. **Figures**: Located in `figures/output/arxiv/`
   - fig1_performance_gap.pdf
   - fig2_operating_curves.pdf
   - fig3_scoring_impact.pdf
   - fig4_parameter_heatmap.pdf

## Exact Conversion Command
```bash
pandoc PAPER_FINAL_FORMATTED_RENUMBERED.md \
  -o SEIZURE_TRANSFORMER_ARXIV_FINAL.pdf \
  --pdf-engine=xelatex \
  --variable geometry:margin=1in \
  --variable fontsize=11pt \
  --variable documentclass=article \
  -V colorlinks=true -V linkcolor=black -V citecolor=black -V urlcolor=blue
```

## Key Formatting Elements in PAPER_FINAL_FORMATTED.md

### YAML Header Structure
```yaml
---
title: |
  **SeizureTransformer: A Transformer-based Model for Generalized Seizure Detection**
author:
  - John H. Jung, MD, MS
  - Independent Researcher
  - jj@novamindnyc.com
abstract: |
  [Abstract content here]
---
```

### Figure Format (Prevents Double Numbering)
```markdown
![Caption text without "Figure N:" prefix](figures/output/arxiv/figN_name.pdf)
```

### Important Notes
- **Figure Order**: Must be fig1 → fig2 → fig3 → fig4 in the markdown
- **No "Figure N:" prefix** in captions
- **Use relative paths** from arxiv_submission directory
- **11pt font** with 1-inch margins for arXiv compliance
- **XeLaTeX engine** for better font rendering

## Regenerating After Edits

1. Edit `PAPER_FINAL_FORMATTED_RENUMBERED.md` as needed
2. Run the exact pandoc command above
3. Verify:
  - Reasonable page count (no TOC)
  - References count matches citations and order of appearance
  - Figures numbered 1–4 in correct order

## Files to Keep
- `PAPER_FINAL_FORMATTED.md` - Source markdown with YAML header
- `SEIZURE_TRANSFORMER_ARXIV_FINAL.pdf` - Final PDF for submission
- `figures/output/arxiv/*.pdf` - All 4 figure PDFs
- This guide (`ARXIV_CONVERSION_GUIDE.md`)

## Archived Content
- Old attempts: `_failed_attempts/` and `_archived_attempts/`
- Previous drafts: `old_drafts/`
