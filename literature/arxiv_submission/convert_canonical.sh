#!/bin/bash

# Canonical ArXiv PDF Conversion Script
# Converts markdown to professional PDF using pandoc with LaTeX
# Author: SeizureTransformer Team
# Date: 2025-09-16

set -e  # Exit on error

echo "=========================================="
echo "ArXiv Paper Conversion Pipeline"
echo "=========================================="

# Configuration
INPUT_FILE="paper_clean.md"
OUTPUT_PDF="seizuretransformer_arxiv_2025.pdf"
TEMPLATE="arxiv_article.tex"
LOG_FILE="conversion.log"

# Check dependencies
echo "Checking dependencies..."
command -v pandoc >/dev/null 2>&1 || { echo "Error: pandoc is required but not installed."; exit 1; }
command -v pdflatex >/dev/null 2>&1 || command -v xelatex >/dev/null 2>&1 || { echo "Error: LaTeX is required but not installed."; exit 1; }

# Check input files
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file $INPUT_FILE not found!"
    exit 1
fi

if [ ! -f "$TEMPLATE" ]; then
    echo "Warning: Template file $TEMPLATE not found. Using default settings."
    TEMPLATE_ARG=""
else
    TEMPLATE_ARG="--template=$TEMPLATE"
fi

echo "Converting $INPUT_FILE to PDF..."

# Primary conversion with xelatex (better Unicode support)
if command -v xelatex >/dev/null 2>&1; then
    echo "Using xelatex engine..."
    pandoc "$INPUT_FILE" \
        -o "$OUTPUT_PDF" \
        --pdf-engine=xelatex \
        $TEMPLATE_ARG \
        --standalone \
        -V documentclass=article \
        -V fontsize=10pt \
        -V geometry:"top=1in,bottom=1in,left=1in,right=1in" \
        -V mainfont="Times New Roman" \
        -V linkcolor=black \
        -V urlcolor=black \
        -V citecolor=black \
        --number-sections \
        --highlight-style=tango \
        --verbose \
        2>&1 | tee "$LOG_FILE"

# Fallback to pdflatex if xelatex not available
elif command -v pdflatex >/dev/null 2>&1; then
    echo "Using pdflatex engine..."
    pandoc "$INPUT_FILE" \
        -o "$OUTPUT_PDF" \
        --pdf-engine=pdflatex \
        $TEMPLATE_ARG \
        --standalone \
        -V documentclass=article \
        -V fontsize=10pt \
        -V geometry:"top=1in,bottom=1in,left=1in,right=1in" \
        -V fontfamily=times \
        -V linkcolor=black \
        -V urlcolor=black \
        -V citecolor=black \
        --number-sections \
        --highlight-style=tango \
        --verbose \
        2>&1 | tee "$LOG_FILE"
else
    echo "Error: No LaTeX engine found!"
    exit 1
fi

# Check if conversion succeeded
if [ -f "$OUTPUT_PDF" ]; then
    echo ""
    echo "=========================================="
    echo "✓ SUCCESS: PDF created at $OUTPUT_PDF"
    echo "=========================================="

    # Get file info
    FILE_SIZE=$(du -h "$OUTPUT_PDF" | cut -f1)
    PAGE_COUNT=$(pdfinfo "$OUTPUT_PDF" 2>/dev/null | grep "Pages:" | awk '{print $2}' || echo "unknown")

    echo "File size: $FILE_SIZE"
    echo "Page count: $PAGE_COUNT"
    echo ""
    echo "Next steps:"
    echo "1. Review the PDF for formatting issues"
    echo "2. Check figures are properly displayed"
    echo "3. Verify references and citations"
    echo "4. Ensure no text overflow"

    # Create a backup
    BACKUP_NAME="backup_$(date +%Y%m%d_%H%M%S)_$OUTPUT_PDF"
    cp "$OUTPUT_PDF" "$BACKUP_NAME"
    echo ""
    echo "Backup saved as: $BACKUP_NAME"

else
    echo ""
    echo "=========================================="
    echo "✗ ERROR: PDF conversion failed!"
    echo "=========================================="
    echo "Check $LOG_FILE for details"
    echo ""
    echo "Common issues:"
    echo "- Missing LaTeX packages"
    echo "- Malformed markdown"
    echo "- Invalid figure paths"
    echo "- LaTeX syntax errors in math mode"
    exit 1
fi

echo ""
echo "Conversion log saved to: $LOG_FILE"