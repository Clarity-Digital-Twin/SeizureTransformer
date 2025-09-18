# ArXiv Submission Structure

## Final Outputs (Ready for Submission)
- `SEIZURE_TRANSFORMER_ARXIV.pdf` - Final PDF for ArXiv submission
- `FINAL_PAPER.tex` - LaTeX file for ArXiv (if they need source)
- `FINAL_PAPER_FROM_SSOT.md` - Assembled markdown (for reference)

## Source of Truth
- `current_draft/` - Individual markdown sections (edit these!)
  - `00_front_matter.md` through `11_appendix.md`
  - `assemble.sh` - Assembles sections into single document

## Figures Pipeline
- `figures/scripts/` - Python scripts to generate figures
  - `fig1_performance_gap.py`
  - `fig2_scoring_impact.py`
  - `fig3_parameter_heatmap.py`
  - `fig4_operating_curves.py`
  - `config.py` - Shared configuration

- `figures/output/arxiv/` - Generated figures
  - `FIGURE_1_performance_gap.{pdf,png}`
  - `FIGURE_2_scoring_impact.{pdf,png}`
  - `FIGURE_3_parameter_heatmap.{pdf,png}`
  - `FIGURE_4_operating_curves.{pdf,png}`

- `figures/data/` - Source data for figures

## Build Process
Run `./CLEAN_CONVERSION_CHAIN.sh` to:
1. Assemble markdown sections
2. Convert to LaTeX
3. Generate final PDF

## Important Notes
- **NEVER edit FINAL_PAPER.tex directly** - changes go in markdown
- **NEVER edit assembled files** - changes go in current_draft/*.md
- Figures are referenced as `FIGURE_X` in markdown
- All changes must flow through the conversion chain

## Archive Directories
- `ARCHIVED_OLD_VERSIONS/` - Previous iterations
- `ARXIV_FINAL_VERSION/` - Backup of submission version
- Various `ARCHIVED_*/` folders contain old/duplicate files