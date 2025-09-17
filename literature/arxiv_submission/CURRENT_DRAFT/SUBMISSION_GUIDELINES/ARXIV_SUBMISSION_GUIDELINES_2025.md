---
title: "arXiv Submission Guidelines & Checklist (2025)"
author: "SeizureTransformer — CURRENT_DRAFT"
date: "September 2025"
---

# Executive Summary

This document distills arXiv’s submission requirements and maps them to our current paper and toolchain. We target a clean, low‑friction submission with either: (A) a single‑column PDF upload, or (B) LaTeX source generated from Pandoc. We recommend staying single‑column for reliability.

# arXiv Requirements (Essentials)

- Accepted text formats (preference order): `(La)TeX / PDFLaTeX`, then `PDF`, then `HTML`.
- If your article was created with TeX/LaTeX, arXiv expects you to submit TeX source rather than only a compiled PDF.
- Accepted figure formats:
  - For pdfLaTeX/XeLaTeX: `.pdf`, `.png`, `.jpg` (no mixing with EPS/PS).
  - For classic LaTeX (DVI route): `.ps`/`.eps`.
- File names: only `a–z A–Z 0–9 _ + - . , =`. Case sensitive. Avoid spaces.
- No scanned documents. No PDF produced from TeX if you do not also include source.
- You may upload a `.zip`/`.tar.gz` with subfolders. Top‑level TeX files must contain a `\documentclass{...}` to be selectable as “Top‑Level TeX”.

# Our Current Status (This Repo)

- Manuscript source: `CURRENT_DRAFT/full_paper_proper.md` (single‑column) → PDF built via Pandoc + XeLaTeX.
- Figures: referenced as `../figures/*.png` with anchors and widths. PNG is acceptable for pdfLaTeX/XeLaTeX.
- References: numeric style `[1]…[14]` fully defined in the paper’s References list; no placeholders remain.
- Build script: `CONVERSION/convert_final.sh` (uses TeX Gyre fonts, single‑column by default). Two‑column build is available but conflicts with `longtable` (LaTeX limitation) — keep single‑column for arXiv.

# Submission Options

## Option A — PDF Upload (Fastest)

- Upload `CURRENT_DRAFT/seizuretransformer_arxiv_final.pdf`.
- Pros: Quick, robust rendering; no TeX packaging needed.
- Cons: arXiv prefers TeX sources when TeX was used; moderators may request source for TeX‑generated PDFs.

## Option B — TeX Source Upload (Recommended if asked)

- Generate `.tex` from our Markdown and include figures.
- Important path rule: the `.tex` should reference figures within the archive root (e.g., `figures/`), not parent paths like `../figures/`.
- Use single‑column (two‑column + longtable fails under LaTeX).

Suggested commands to export TeX (single‑column):

```
cd literature/arxiv_submission/CONVERSION
python3 preprocess_markdown.py ../CURRENT_DRAFT/full_paper_proper.md paper_preprocessed.md
pandoc paper_preprocessed.md \
  -s -o seizuretransformer_arxiv.tex \
  -V documentclass=article \
  -V fontsize=11pt \
  -V geometry:margin=1in \
  -V mainfont="TeX Gyre Termes"
```

Then: copy figures into `CONVERSION/figures/` and replace `../figures/` → `figures/` in the generated `.tex` (or adjust the Markdown and rebuild). Package `.tex` + `figures/` into a `.zip`/`.tar.gz` and upload.

# Metadata & File Hygiene

- Title/Abstract: Enter clean text into arXiv’s metadata form (no heavy markup). Our manuscript’s YAML matches the intended title and date.
- Authors/Affiliation: Provide complete names; affiliations can be included in the abstract page metadata.
- License: Choose appropriate license during submission.
- Categories: Choose the most appropriate (e.g., cs.LG / eess.SP / q-bio.NC) — verify at submission time.
- Filenames: Ensure no spaces and case‑exact matches for included figures (e.g., `fig1_performance_gap.png`).

# Known Constraints & Resolutions

- Two‑column + tables: `longtable` cannot appear in two‑column mode. For two‑column output, convert Markdown tables to raw LaTeX floats (`table*` + `tabular`) or keep single‑column.
- Fonts: TeX Gyre Termes/Cursor are bundled with TeX Live (safe on arXiv). Avoid non‑bundled system fonts.
- Graphics format: Keep PNG/PDF/JPG (no TIFF). Use vector PDFs where possible for diagrams.

# Pre‑Submission Checklist (This Paper)

- [x] Single‑column PDF compiles cleanly via Pandoc + XeLaTeX.
- [x] All citations in text are defined in References ([1]–[14]).
- [x] Figures referenced with relative paths; PNG format is acceptable.
- [x] No HTML or exotic Markdown extensions.
- [x] No external assets or shell‑escape required.

# Submission Steps (Walkthrough)

1. Build the final single‑column PDF with `convert_final.sh`.
2. On arXiv, Start New Submission → Upload PDF (Option A), or upload `.zip/.tar.gz` with `.tex` + `figures/` (Option B).
3. Click “Check Files”, confirm auto‑detected processor and (if TeX) top‑level `.tex` file.
4. Fix any filename/path warnings (case, missing files). Re‑upload if needed.
5. Enter metadata (title/abstract/authors/categories/license).
6. Preview PDF; verify figures and references.
7. Submit before daily cutoff (14:00 US Eastern).

# Alignment Summary

- Our single‑column PDF is aligned and ready for upload.
- If moderators request TeX source, export `.tex`, fix figure paths to `figures/`, and upload source archive instead.

