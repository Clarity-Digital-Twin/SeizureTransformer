#!/bin/bash

# Final conversion script with preprocessing
# Handles all known issues for clean PDF output

set -e

echo "=========================================="
echo "ArXiv Paper Final Conversion Pipeline"
echo "=========================================="

# Step 1: Preprocess markdown
echo "Step 1: Preprocessing markdown..."
python3 preprocess_markdown.py paper_clean.md paper_preprocessed.md

# Step 2: Convert to PDF with simpler options
echo "Step 2: Converting to PDF..."

# Use simpler pandoc options that work reliably
pandoc paper_preprocessed.md \
    -o seizuretransformer_arxiv_final.pdf \
    --pdf-engine=xelatex \
    -V documentclass=article \
    -V fontsize=11pt \
    -V geometry:margin=1in \
    -V mainfont="Liberation Serif" \
    -V monofont="Liberation Mono" \
    -V linkcolor=black \
    -V urlcolor=black \
    -V citecolor=black \
    --number-sections \
    --standalone \
    -V tables=true \
    -V graphics=true \
    2>&1 | tee conversion_final.log

# Check result
if [ -f "seizuretransformer_arxiv_final.pdf" ]; then
    echo ""
    echo "=========================================="
    echo "✓ SUCCESS: PDF created successfully!"
    echo "=========================================="
    echo "Output: seizuretransformer_arxiv_final.pdf"

    # Get file info if pdfinfo is available
    if command -v pdfinfo >/dev/null 2>&1; then
        echo ""
        pdfinfo seizuretransformer_arxiv_final.pdf | grep -E "Pages:|File size:"
    fi
else
    echo ""
    echo "✗ ERROR: Conversion failed"
    echo "Check conversion_final.log for details"
    exit 1
fi