# Markdown to ArXiv LaTeX/PDF Conversion Best Practices (2025, Verified)

## Executive Summary

This guide documents a clean, reproducible path from Markdown to a high‑quality PDF suitable for arXiv, inspired by the “Attention Is All You Need” style. We target local conversion with Pandoc to PDF (XeLaTeX) and keep arXiv compatibility in mind. Key points: clean Markdown structure, safe LaTeX header settings, reliable fonts, and practical citation strategies.

## 1. Toolchain (What We Use and Why)

- Pandoc (≥ 3.1): Mature Markdown→LaTeX/PDF converter with built‑in citation processing via `--citeproc`.
- TeX engine: XeLaTeX locally for robust Unicode and font handling. If submitting TeX sources to arXiv, prefer pdfLaTeX/newtx for maximum compatibility; if uploading a final PDF, XeLaTeX is fine as long as fonts are embedded.
- TeX Live: arXiv updates annually; verify current version at https://info.arxiv.org/help/submit_tex.html. As of 2024–2025, expect TeX Live 2023/2024. Do not assume 2025 is the default.

Install (WSL/Debian/Ubuntu):
```bash
sudo apt-get update
sudo apt-get install -y pandoc texlive-xetex texlive-fonts-recommended texlive-latex-extra
```

## 2. Authoring Markdown (Structure That Converts Cleanly)

- Front matter: use YAML for title/authors/abstract.
  ```markdown
  ---
  title: "Your Paper Title"
  author:
    - Author One
    - Author Two
  abstract: |
    Your abstract text here (150–250 words).
  ---
  ```
- Headings: `#`, `##`, `###` only (max depth 3). Enable numbering with `--number-sections`.
- Math: `$...$` for inline; `$$...$$` for display. Escape LaTeX characters (`_`, `%`, `#`, `&`) when used as text.
- Figures: use relative paths and explicit widths.
  ```markdown
  ![Caption describing the figure.](figs/model.png){#fig:model width=80%}
  ```
- Tables: use GitHub‑style tables; keep them narrow for two‑column layouts.
- Code blocks: fenced triple backticks; avoid exotic languages to keep LaTeX dependencies minimal.

## 3. Citations and References (Two Practical Modes)

You can finish with either manual references or automatic bibliographies. Choose one and be consistent.

- Manual (what this repo currently uses via concatenation):
  - Write in‑text references as plain text like “[1]” and maintain a “References” section at the end (e.g., `09_references.md`).
  - No `[@...]` syntax needed; no `--citeproc` required.

- Automatic (Pandoc citeproc with BibTeX/CSL):
  - Use `[@key]` in the text, provide `--bibliography=references.bib --citeproc` and an optional style, e.g. `--csl=ieee.csl`.
  - Keep `references.bib` and `ieee.csl` in the repo. Note: `pandoc-citeproc` filter is deprecated; use `--citeproc`.

## 4. LaTeX Header and Template Choices (ArXiv‑Safe)

- Do not place `\documentclass{...}` inside files included with `-H`/header‑includes; Pandoc generates the class. Set class options via variables.
- Times‑like fonts:
  - XeLaTeX: `-V mainfont="TeX Gyre Termes"` (safe, TeXLive‑bundled).
  - pdfLaTeX: use `newtxtext,newtxmath` packages (Times‑like) instead of the legacy `times` package.
- Two‑column layout: pass `-V classoption=twocolumn`.
- Recommended header‑includes (no `\documentclass`):
  ```markdown
  ---
  header-includes:
    - \usepackage{graphicx}
    - \usepackage{booktabs}
    - \usepackage[font=small,labelfont=bf]{caption}
  ---
  ```

## 5. Conversion Commands (Copy‑Paste Ready)

- Single‑column (simple, robust):
  ```bash
  pandoc input.md \
    -o output.pdf \
    --pdf-engine=xelatex \
    -V documentclass=article \
    -V fontsize=11pt \
    -V geometry:margin=1in \
    -V mainfont="TeX Gyre Termes" \
    --number-sections \
    --standalone
  ```

- Two‑column (Attention‑like):
  ```bash
  pandoc input.md \
    -o output_twocol.pdf \
    --pdf-engine=xelatex \
    -V documentclass=article \
    -V classoption=twocolumn \
    -V fontsize=11pt \
    -V geometry:"top=1in,bottom=1in,left=1in,right=1in" \
    -V mainfont="TeX Gyre Termes" \
    -V linkcolor=black -V urlcolor=black -V citecolor=black \
    --number-sections \
    --standalone
  ```

- With citations (automatic mode only):
  ```bash
  pandoc input.md \
    -o output.pdf \
    --pdf-engine=xelatex \
    -V documentclass=article \
    -V fontsize=11pt \
    -V geometry:margin=1in \
    -V mainfont="TeX Gyre Termes" \
    --number-sections \
    --bibliography=references.bib \
    --csl=ieee.csl \
    --citeproc \
    --standalone
  ```

Notes:
- Avoid `--toc` unless you intend to include a table of contents (the Attention paper does not).
- Variables like `-V tables=true` or `-V graphics=true` are unnecessary.

## 6. Attention‑Paper Styling Tips (Practical)

- 11pt, Times‑like font, 1" margins, two columns where appropriate.
- Use full‑width figures in two‑column with LaTeX’s `figure*` environment. In Markdown, insert a raw block when needed:
  ```markdown
  ```{=latex}
  \begin{figure*}[t]
    \centering
    \includegraphics[width=0.9\textwidth]{figs/overview.pdf}
    \caption{Model overview.}
    \label{fig:overview}
  \end{figure*}
  ```
  ```
- Keep captions concise; bold label via `caption` package as shown above.

## 7. Common Issues and Fixes

- Figures too large or misplaced: set explicit widths (e.g., `{width=3.25in}`) and prefer vector graphics (PDF/SVG→PDF) for diagrams.
- Complex math: use raw LaTeX blocks (`{=latex}`) for `align`, matrices, or custom macros.
- Citations not rendering: use `--citeproc` (not the deprecated `pandoc-citeproc` filter) and ensure keys exist in `references.bib`.

## 8. QA Before Submission

- Fonts embedded:
  ```bash
  pdffonts output.pdf  # "emb" should be yes for all fonts
  ```
- File size (try to keep <10MB):
  ```bash
  gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/prepress \
     -dNOPAUSE -dQUIET -dBATCH -sOutputFile=compressed.pdf output.pdf
  ```
- PDF/A (optional; arXiv does not require it):
  ```bash
  gs -dPDFA -dBATCH -dNOPAUSE -sColorConversionStrategy=UseDeviceIndependentColor \
     -sDEVICE=pdfwrite -dPDFACompatibilityPolicy=2 \
     -sOutputFile=output_pdfa.pdf output.pdf
  ```
- arXiv compatibility: if uploading TeX sources, avoid shell‑escape and experimental packages; include all assets (images, .bbl if you use BibTeX). If uploading a final PDF, ensure fonts are embedded and metadata is correct.

## 9. Our Local Automation (This Repo)

- Current working script: `literature/arxiv_submission/CONVERSION/convert_final.sh`
  - Inputs `../CURRENT_DRAFT/full_paper_proper.md`, runs `preprocess_markdown.py`, and produces `seizuretransformer_arxiv_final.pdf`.
  - Uses XeLaTeX locally with Times‑like font (you may switch to `TeX Gyre Termes` for safer portability).
- Current paper source: `CURRENT_DRAFT/full_paper_proper.md` (contains the concatenated content and an embedded references section via `09_references.md`).

## 10. References and Resources

- Pandoc Manual: https://pandoc.org/MANUAL.html
- arXiv TeX help: https://info.arxiv.org/help/submit_tex.html
- CSL styles (IEEE etc.): https://github.com/citation-style-language/styles
- “Attention Is All You Need”: https://arxiv.org/abs/1706.03762

## 11. Summary

- Author clean Markdown with shallow heading depth, explicit figure widths, and simple math.
- Convert locally with Pandoc→XeLaTeX; use Times‑like fonts that are part of TeX Live (e.g., TeX Gyre Termes) for reliability.
- Choose one citation mode: manual references (current repo) or `--citeproc` with a `.bib`.
- For arXiv, either upload the final PDF (ensure embedded fonts) or TeX sources (prefer pdfLaTeX/newtx and include all assets).

This revision corrects font, header, citation, and arXiv details so your conversions are accurate and predictable.
