# OPERATIONALIZED ARXIV SUBMISSION CHAIN

## THE GOLDEN RULE
**ALL CONTENT CHANGES GO TO INDIVIDUAL MARKDOWN FILES IN `current_draft/`**
Never edit LaTeX or concatenated files directly!

## THE CHAIN (SSOT → PDF)

### 1. SINGLE SOURCE OF TRUTH (SSOT)
```
current_draft/
  ├── 00_front_matter.md     # Title, author info
  ├── 01_abstract.md          # Abstract
  ├── 02_introduction.md      # Introduction
  ├── 03_background.md        # Background
  ├── 04_methods.md           # Methods
  ├── 05_results.md           # Results
  ├── 06_discussion.md        # Discussion
  ├── 07_conclusion.md        # Conclusion
  ├── 08_reproducibility.md   # Reproducibility statement
  ├── 09_acknowledgments.md   # Acknowledgments
  ├── 10_references_from_draft.md  # References (in order of appearance)
  └── 11_appendix.md          # Appendices
```

### 2. ASSEMBLY PROCESS
```bash
cd current_draft
./assemble.sh
# Creates: CURRENT_WORKING_DRAFT_ASSEMBLED.md
```

### 3. CONVERSION TO PDF
```bash
# Run from arxiv_submission directory:
./CLEAN_CONVERSION_CHAIN.sh
```

This creates:
- `FINAL_PAPER_FROM_SSOT.md` - Final concatenated markdown
- `FINAL_PAPER.tex` - LaTeX for arXiv submission
- `SEIZURE_TRANSFORMER_ARXIV.pdf` - PDF for review

## WORKFLOW FOR MAKING CHANGES

### Content Changes (text, data, references)
1. Edit the appropriate file in `current_draft/`
2. Run `./CLEAN_CONVERSION_CHAIN.sh`
3. Review PDF

### Formatting Changes (spacing, fonts, margins)
1. Edit pandoc command in `CLEAN_CONVERSION_CHAIN.sh`
2. Run `./CLEAN_CONVERSION_CHAIN.sh`
3. Review PDF

### NEVER DO THIS
- ❌ Edit FINAL_PAPER.tex directly
- ❌ Edit FINAL_PAPER_FROM_SSOT.md directly
- ❌ Edit concatenated markdown files
- ❌ Create multiple versions of the same file

## KEY SPECIFICATIONS

### Current Settings
- **Font size**: 11pt
- **Margins**: 1 inch all sides
- **Document class**: article
- **PDF engine**: xelatex
- **References**: Order of appearance (not alphabetical)
- **No TOC**: Disabled for arXiv submission

### Files to Submit to arXiv
1. `FINAL_PAPER.tex` - Main LaTeX file
2. `figures/output/arxiv/*.pdf` - Figure files (when available)

## VALIDATION CHECKLIST

Before submission, verify:
- [ ] References appear in order of first citation
- [ ] No "Neureka" errors (should be "Neural Engineering Data Consortium")
- [ ] All 14 references are included
- [ ] PDF has no table of contents
- [ ] References section appears at the end
- [ ] Abstract matches SSOT in `01_abstract.md`
- [ ] Introduction matches SSOT in `02_introduction.md`

## TROUBLESHOOTING

### Missing References in PDF
Check that `10_references_from_draft.md` is listed in `current_draft/SECTION_ORDER`

### Wrong Reference Order
Run the reference fix script in `current_draft/`

### Formatting Issues
Modify pandoc variables in `CLEAN_CONVERSION_CHAIN.sh`

### Content Drift
Always edit `current_draft/*.md` files, never the concatenated versions

## ARCHIVED FILES

Old attempts moved to `_old_attempts/` for reference but should not be used.