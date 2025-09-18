#!/usr/bin/env bash
# CLEAN CONVERSION CHAIN FOR ARXIV SUBMISSION
# ===========================================
# This script operationalizes the complete conversion chain from individual
# markdown files to final PDF, ensuring no drift or errors.

set -euo pipefail

echo "SEIZURE TRANSFORMER ARXIV PAPER CONVERSION CHAIN"
echo "================================================="
echo ""

# Step 1: Verify we're in the right directory
if [[ ! -d "current_draft" ]]; then
    echo "ERROR: Must run from arxiv_submission directory"
    exit 1
fi

# Step 2: Assemble individual markdown files into single document
echo "[1/4] Assembling individual markdown sections..."
cd current_draft
./assemble.sh
cd ..

# Step 3: Copy assembled markdown to main directory with clear name
echo "[2/4] Creating final markdown from SSOT..."
cp current_draft/CURRENT_WORKING_DRAFT_ASSEMBLED.md FINAL_PAPER_FROM_SSOT.md

# Step 4: Convert markdown to LaTeX
echo "[3/4] Converting markdown to LaTeX..."
pandoc FINAL_PAPER_FROM_SSOT.md \
    -o FINAL_PAPER.tex \
    --standalone \
    --pdf-engine=xelatex

# Step 5: Convert markdown to PDF (no TOC)
echo "[4/4] Generating PDF..."
pandoc FINAL_PAPER_FROM_SSOT.md \
    -o SEIZURE_TRANSFORMER_ARXIV.pdf \
    --pdf-engine=xelatex \
    -V geometry:margin=1in \
    -V fontsize=11pt \
    -V documentclass=article \
    -V colorlinks=true

echo ""
echo "CONVERSION COMPLETE!"
echo "===================="
echo "Final outputs:"
echo "  - FINAL_PAPER_FROM_SSOT.md (concatenated markdown)"
echo "  - FINAL_PAPER.tex (LaTeX file for arXiv)"
echo "  - SEIZURE_TRANSFORMER_ARXIV.pdf (PDF for review)"
echo ""
echo "THE CHAIN:"
echo "1. Individual markdown files in current_draft/*.md (SSOT)"
echo "2. Assembled via current_draft/assemble.sh"
echo "3. Converted using arxiv_template.tex"
echo "4. No manual LaTeX editing - all changes go to markdown SSOT"