#!/bin/bash

# Convert full_paper_proper.md to PDF matching arXiv classic paper style
# Based on "Attention Is All You Need" formatting

echo "Converting full_paper_proper.md to arXiv-style PDF..."

# Use pdflatex for better compatibility with classic LaTeX style
pandoc full_paper_proper.md \
  -o jung_seizuretransformer_2025.pdf \
  --pdf-engine=pdflatex \
  --standalone \
  -V documentclass=article \
  -V geometry:"top=1.5in,bottom=1.5in,left=1.5in,right=1.5in" \
  -V fontsize=10pt \
  -V fontfamily=times \
  -V linestretch=1.15 \
  -V linkcolor=black \
  -V urlcolor=black \
  -V citecolor=black \
  -V secnumdepth=2 \
  -V indent=true \
  -V subparagraph=yes \
  --highlight-style=kate

if [ $? -eq 0 ]; then
    echo "✓ Created jung_seizuretransformer_2025.pdf"
    echo ""
    echo "Key formatting:"
    echo "  • 1.5 inch margins (professional width)"
    echo "  • Times font family"
    echo "  • 10pt font size"
    echo "  • Black hyperlinks (arXiv standard)"
    echo "  • Proper section numbering"
else
    echo "Error during PDF conversion"
fi