#!/bin/bash

# Convert full_paper_proper.md to PDF with nice formatting

echo "Converting full_paper_proper.md to PDF..."

pandoc full_paper_proper.md \
  -o jung_seizuretransformer_2025.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1.5in \
  -V fontsize=10pt \
  -V mainfont="Times New Roman" \
  -V monofont="Courier New" \
  -V urlcolor=black \
  -V linkcolor=black \
  -V citecolor=black \
  --highlight-style=tango

echo "PDF created: jung_seizuretransformer_2025.pdf"