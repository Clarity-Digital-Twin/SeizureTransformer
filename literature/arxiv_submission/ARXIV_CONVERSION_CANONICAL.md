# Canonical ArXiv PDF Conversion Guide
## For SeizureTransformer Paper Submission

This document establishes the definitive process for converting our markdown paper to a professional PDF suitable for arXiv submission.

## 1. CHOSEN TOOL: Pandoc with LaTeX Backend

**Primary Tool**: Pandoc 2.x or 3.x with pdflatex/xelatex
**Rationale**:
- Most flexible markdown-to-PDF conversion
- Direct LaTeX control for academic formatting
- Handles citations, figures, and cross-references
- Industry standard for academic document conversion

## 2. MARKDOWN FORMATTING REQUIREMENTS

### Document Structure
```markdown
---
title: "SeizureTransformer on TUSZ: A 27-137x Performance Gap Between Claims and Reproducible Evaluation"
author:
  - name: "John H. Jung, MD, MS"
    affiliation: "Independent Researcher"
    email: "JJ@novamindnyc.com"
date: "September 2025"
abstract: |
  Your abstract text here...
---

# Introduction

Content...

## Subsection

Content...
```

### Figure References
```markdown
![Caption text](figures/fig1.png){width=100%}

# Or for LaTeX-specific control:
\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{figures/fig1.png}
\caption{Caption text}
\label{fig:performance-gap}
\end{figure}
```

### Citations
```markdown
[@Smith2024; @Jones2023]  # For BibTeX citations
Smith et al. (2024)       # For inline text citations
```

### Mathematics
```markdown
$\theta = 0.8$            # Inline math
$$F_1 = 2 \cdot \frac{precision \cdot recall}{precision + recall}$$  # Display math
```

## 3. CONVERSION PIPELINE

### Step 1: Prepare Clean Markdown
1. Remove HTML tags (convert to markdown equivalents)
2. Fix figure paths (relative to document root)
3. Ensure proper header hierarchy (# ## ### etc)
4. Add YAML frontmatter

### Step 2: Create LaTeX Template (optional but recommended)
```latex
% arxiv_template.tex
\documentclass[10pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{times}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{amsmath}
\usepackage{cite}

\hypersetup{
    colorlinks=true,
    linkcolor=black,
    citecolor=black,
    urlcolor=black
}

\title{$title$}
\author{$for(author)$$author.name$\\$author.affiliation$\\$author.email$$sep$\and$endfor$}
\date{$date$}

\begin{document}
\maketitle

\begin{abstract}
$abstract$
\end{abstract}

$body$

\end{document}
```

### Step 3: Conversion Command
```bash
pandoc input.md \
  -o output.pdf \
  --pdf-engine=xelatex \
  --template=arxiv_template.tex \
  --citeproc \
  --bibliography=refs.bib \
  --csl=ieee.csl \
  -V documentclass=article \
  -V fontsize=10pt \
  -V geometry:"margin=1in" \
  -V linkcolor=black \
  --number-sections \
  --toc=false
```

## 4. COMMON ISSUES AND SOLUTIONS

### Issue: Title/Author Not Appearing
**Solution**: Use YAML frontmatter, not markdown headers for metadata

### Issue: Figures Not Found
**Solution**: Use relative paths from document location, ensure files exist

### Issue: Text Overflow
**Solution**: Add explicit line breaks or adjust geometry margins

### Issue: References Not Formatting
**Solution**: Use --citeproc flag and provide .bib file

### Issue: Math Not Rendering
**Solution**: Use proper LaTeX math delimiters ($...$, $$...$$)

## 5. ITERATIVE REFINEMENT PROCESS

### Phase 1: Basic Conversion
1. Get basic text converting cleanly
2. Verify section structure
3. Check page breaks

### Phase 2: Formatting
1. Adjust margins and font sizes
2. Fix figure placement
3. Ensure consistent spacing

### Phase 3: Polish
1. Add page numbers
2. Format references properly
3. Ensure hyperlinks work but appear black

## 6. VALIDATION CHECKLIST

- [ ] Title and authors appear correctly on first page
- [ ] Abstract is properly formatted
- [ ] All sections have correct numbering
- [ ] Figures are visible and captioned
- [ ] References are properly formatted
- [ ] No text overflow beyond margins
- [ ] Page numbers present
- [ ] Hyperlinks work but appear black (arXiv standard)
- [ ] Math equations render correctly
- [ ] Tables (if any) are properly formatted

## 7. ARXIV-SPECIFIC REQUIREMENTS

1. **File Size**: Keep under 10MB (compress figures if needed)
2. **Format**: PDF/A if possible for archival
3. **Fonts**: Embed all fonts (xelatex does this automatically)
4. **Color**: Use black text, grayscale or color figures ok
5. **Links**: Should be black in print but functional

## 8. RECOMMENDED WORKFLOW

1. Start with clean markdown (no HTML)
2. Use conversion script (see next section)
3. Review PDF output
4. Fix issues in markdown source (not PDF)
5. Re-run conversion
6. Iterate until perfect

## 9. NOTES ON TOOL ALTERNATIVES

**Avoided Tools**:
- Direct LaTeX: Too complex for iterative editing
- Word/LibreOffice: Poor equation and figure handling
- Online converters: Lack control and reproducibility
- Markdown-pdf npm packages: Limited academic formatting

**Why Pandoc**:
- Actively maintained
- Extensive documentation
- Academic community standard
- Handles complex documents
- Scriptable and reproducible

## 10. VERSION TRACKING

Keep track of successful conversion parameters:
```
# Working as of 2024-09-16
pandoc version: 3.1.9
xelatex version: XeTeX 3.141592653-2.6-0.999995
Platform: Ubuntu 22.04 / WSL2
Status: Produces clean 2-column IEEE-style paper
```

## NEXT STEPS

1. Clean the current markdown file to remove HTML and fix paths
2. Run the canonical conversion script
3. Iterate based on output quality
4. Document any adjustments needed

Remember: The goal is a clean, professional PDF that looks like papers from top ML conferences (NeurIPS, ICML, ICLR) or journals (Nature, Science).