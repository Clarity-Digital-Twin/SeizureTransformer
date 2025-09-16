#!/bin/bash
# Convert full paper to PDF using pandoc

echo "Converting to PDF..."

# Basic PDF generation
pandoc full_paper.md \
  -o jung_seizuretransformer_2025.pdf \
  --pdf-engine=xelatex \
  --number-sections \
  --toc \
  --toc-depth=2 \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=article \
  -V colorlinks=true \
  -V linkcolor=blue \
  -V urlcolor=blue \
  -V citecolor=blue

echo "✓ Created jung_seizuretransformer_2025.pdf"

# Also create LaTeX for arXiv submission
pandoc full_paper.md \
  -s \
  -o jung_seizuretransformer_2025.tex \
  --number-sections \
  --toc \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=article

echo "✓ Created jung_seizuretransformer_2025.tex for arXiv"
