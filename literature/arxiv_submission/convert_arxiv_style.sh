#!/bin/bash
# Convert to arXiv-style PDF mimicking classic papers like "Attention Is All You Need"
# Clean, professional formatting without excessive LaTeX customization

echo "Converting to arXiv-style PDF (classic paper format)..."

# Generate PDF with minimal pandoc flags for clean output
# Following the style of classic ML papers on arXiv
pandoc full_paper_clean.md \
  -o jung_seizuretransformer_2025_arxiv.pdf \
  --pdf-engine=pdflatex \
  --standalone \
  -V documentclass=article \
  -V geometry:margin=1in \
  -V fontsize=10pt \
  -V linestretch=1.0 \
  -V linkcolor=black \
  -V urlcolor=black \
  -V citecolor=black \
  --highlight-style=kate

if [ $? -eq 0 ]; then
    echo "✓ Created jung_seizuretransformer_2025_arxiv.pdf"
else
    echo "Trying with xelatex for better compatibility..."
    pandoc full_paper_clean.md \
      -o jung_seizuretransformer_2025_arxiv.pdf \
      --pdf-engine=xelatex \
      --standalone \
      -V documentclass=article \
      -V geometry:margin=1in \
      -V fontsize=10pt
    echo "✓ Created jung_seizuretransformer_2025_arxiv.pdf (xelatex)"
fi

# Also generate clean LaTeX source for arXiv submission
pandoc full_paper_clean.md \
  -o jung_seizuretransformer_2025_arxiv.tex \
  --standalone \
  -V documentclass=article \
  -V geometry:margin=1in \
  -V fontsize=10pt \
  -V linestretch=1.0

echo "✓ Created jung_seizuretransformer_2025_arxiv.tex"
echo ""
echo "Files generated:"
echo "  • jung_seizuretransformer_2025_arxiv.pdf - Clean PDF like classic papers"
echo "  • jung_seizuretransformer_2025_arxiv.tex - LaTeX source for arXiv"
echo ""
echo "Note: This mimics the clean style of papers like 'Attention Is All You Need'"
echo "      Simple formatting, no TOC, minimal LaTeX customization"