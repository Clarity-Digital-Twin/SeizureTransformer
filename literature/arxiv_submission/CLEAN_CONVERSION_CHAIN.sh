#!/usr/bin/env bash
# CLEAN CONVERSION CHAIN FOR ARXIV SUBMISSION
# ===========================================
# This script operationalizes the complete conversion chain from individual
# markdown files to final PDF, ensuring no drift or errors.
# All outputs go to ARXIV_FINAL_VERSION directory

set -euo pipefail

echo "SEIZURE TRANSFORMER ARXIV PAPER CONVERSION CHAIN"
echo "================================================="
echo ""

# Step 1: Verify we're in the right directory
if [[ ! -d "current_draft" ]]; then
    echo "ERROR: Must run from arxiv_submission directory"
    exit 1
fi

# Create ARXIV_FINAL_VERSION directory if it doesn't exist
mkdir -p ARXIV_FINAL_VERSION

# Step 2: Assemble individual markdown files into single document
echo "[1/5] Assembling individual markdown sections..."
cd current_draft
./assemble.sh
cd ..

# Step 3: Copy assembled markdown to ARXIV_FINAL_VERSION with clear name
echo "[2/5] Creating final markdown from SSOT..."
cp current_draft/CURRENT_WORKING_DRAFT_ASSEMBLED.md ARXIV_FINAL_VERSION/FINAL_PAPER_FROM_SSOT.md
cp current_draft/CURRENT_WORKING_DRAFT_ASSEMBLED.md ARXIV_FINAL_VERSION/FINAL_PAPER_CLEAN.md

# Step 4: Convert markdown to LaTeX in ARXIV_FINAL_VERSION
echo "[3/5] Converting markdown to LaTeX..."
pandoc ARXIV_FINAL_VERSION/FINAL_PAPER_FROM_SSOT.md \
    -o ARXIV_FINAL_VERSION/FINAL_PAPER.tex \
    --standalone \
    --pdf-engine=xelatex \
    -H <(echo "\\usepackage{caption}") \
    -H <(echo "\\captionsetup[figure]{font=small,labelfont=bf,skip=5pt}")

# Step 5: Convert markdown to PDF in ARXIV_FINAL_VERSION (no TOC, smart figure placement)
echo "[4/5] Generating PDF..."
pandoc ARXIV_FINAL_VERSION/FINAL_PAPER_FROM_SSOT.md \
    -o ARXIV_FINAL_VERSION/SEIZURE_TRANSFORMER_ARXIV.pdf \
    --pdf-engine=xelatex \
    -V geometry:margin=1in \
    -V fontsize=11pt \
    -V documentclass=article \
    -V colorlinks=true \
    -H <(echo "\\usepackage{caption}") \
    -H <(echo "\\captionsetup[figure]{font=small,labelfont=bf,skip=5pt}") \
    --resource-path=.:current_draft

# Step 6: Copy figures to ARXIV_FINAL_VERSION if they exist
echo "[5/5] Copying figures to ARXIV_FINAL_VERSION..."
if [[ -d "figures/output/arxiv" ]]; then
    cp figures/output/arxiv/FIGURE_*.pdf ARXIV_FINAL_VERSION/ 2>/dev/null || true
    echo "  ✓ Figures copied"
fi

echo ""
echo "CONVERSION COMPLETE!"
echo "===================="
echo "All outputs in ARXIV_FINAL_VERSION/:"
echo "  - FINAL_PAPER_FROM_SSOT.md (concatenated markdown)"
echo "  - FINAL_PAPER_CLEAN.md (clean version)"
echo "  - FINAL_PAPER.tex (LaTeX file for arXiv)"
echo "  - SEIZURE_TRANSFORMER_ARXIV.pdf (PDF for review)"
echo "  - FIGURE_*.pdf (all figures)"
echo ""
echo "THE CHAIN:"
echo "1. Individual markdown files in current_draft/*.md (SSOT)"
echo "2. Assembled via current_draft/assemble.sh"
echo "3. All outputs go to ARXIV_FINAL_VERSION/"
echo "4. No manual editing - all changes go to markdown SSOT"
echo ""
echo "ARXIV_FINAL_VERSION is the single source of truth for submission!"
