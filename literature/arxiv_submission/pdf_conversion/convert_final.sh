#!/bin/bash

# Final conversion script with preprocessing
# Handles all known issues for clean PDF output

set -euo pipefail

echo "=========================================="
echo "ArXiv Paper Final Conversion Pipeline"
echo "=========================================="

# Usage: ./convert_final.sh [--twocol]
TWOCOL=0
if [[ "${1:-}" == "--twocol" ]]; then
  TWOCOL=1
  shift || true
fi

# Step 1: Preprocess markdown
echo "Step 1: Preprocessing markdown..."
python3 preprocess_markdown.py ../CURRENT_DRAFT/full_paper_proper.md paper_preprocessed.md

# Step 2: Convert to PDF with robust options (TeX Gyre Termes)
echo "Step 2: Converting to PDF..."

PANDOC_OPTS=(
  --pdf-engine=xelatex
  -V documentclass=article
  -V fontsize=11pt
  -V geometry:margin=1in
  -V mainfont="TeX Gyre Termes"
  -V monofont="TeX Gyre Cursor"
  -V linkcolor=black -V urlcolor=black -V citecolor=black
  --number-sections
  --standalone
  --listings
)

if [[ "$TWOCOL" -eq 1 ]]; then
  echo "  • Enabling two-column layout"
  PANDOC_OPTS+=( -V classoption=twocolumn )
fi

pandoc paper_preprocessed.md \
  -o seizuretransformer_arxiv_final.pdf \
  "${PANDOC_OPTS[@]}" \
  2>&1 | tee conversion_final.log

# Check result and copy to CURRENT_DRAFT
if [ -f "seizuretransformer_arxiv_final.pdf" ]; then
  echo ""
  echo "=========================================="
  echo "✓ SUCCESS: PDF created successfully!"
  echo "=========================================="
  echo "Output: $(pwd)/seizuretransformer_arxiv_final.pdf"

  # Get file info if pdfinfo is available
  if command -v pdfinfo >/dev/null 2>&1; then
    echo ""
    pdfinfo seizuretransformer_arxiv_final.pdf | grep -E "Pages:|File size:"
  fi

  # Copy to CURRENT_DRAFT for convenience
  cp -f seizuretransformer_arxiv_final.pdf ../CURRENT_DRAFT/seizuretransformer_arxiv_final.pdf || true
  echo "Copied to: ../CURRENT_DRAFT/seizuretransformer_arxiv_final.pdf"
else
  echo ""
  echo "✗ ERROR: Conversion failed"
  echo "Check conversion_final.log for details"
  exit 1
fi
