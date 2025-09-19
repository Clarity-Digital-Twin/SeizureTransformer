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
if [[ ! -d "CURRENT_DRAFT" ]]; then
    echo "ERROR: Must run from arxiv_submission directory"
    exit 1
fi

# Create ARXIV_FINAL_VERSION directory if it doesn't exist
mkdir -p ARXIV_FINAL_VERSION

# Step 2: Assemble individual markdown files into single document
echo "[1/5] Assembling individual markdown sections..."
cd CURRENT_DRAFT
./assemble.sh
cd ..

# Step 3: Copy assembled markdown to ARXIV_FINAL_VERSION with clear name
echo "[2/6] Creating final markdown from SSOT..."
cp CURRENT_DRAFT/CURRENT_WORKING_DRAFT_ASSEMBLED.md ARXIV_FINAL_VERSION/FINAL_PAPER_FROM_SSOT.md
cp CURRENT_DRAFT/CURRENT_WORKING_DRAFT_ASSEMBLED.md ARXIV_FINAL_VERSION/FINAL_PAPER_CLEAN.md

# Step 4: Stage figures into nested path to match TeX includes
echo "[3/6] Staging figures for path compatibility..."
mkdir -p ARXIV_FINAL_VERSION/figures/output/arxiv
# Map lower-case sources to expected upper-case names
if compgen -G "figures/output/arxiv/fig1_performance_gap.pdf" > /dev/null; then
    cp -f figures/output/arxiv/fig1_performance_gap.pdf ARXIV_FINAL_VERSION/figures/output/arxiv/FIGURE_1_performance_gap.pdf || true
fi
if compgen -G "figures/output/arxiv/fig2_scoring_impact.pdf" > /dev/null; then
    cp -f figures/output/arxiv/fig2_scoring_impact.pdf ARXIV_FINAL_VERSION/figures/output/arxiv/FIGURE_2_scoring_impact.pdf || true
fi
if compgen -G "figures/output/arxiv/fig3_parameter_heatmap.pdf" > /dev/null; then
    cp -f figures/output/arxiv/fig3_parameter_heatmap.pdf ARXIV_FINAL_VERSION/figures/output/arxiv/FIGURE_3_parameter_heatmap.pdf || true
fi
if compgen -G "figures/output/arxiv/fig4_operating_curves.pdf" > /dev/null; then
    cp -f figures/output/arxiv/fig4_operating_curves.pdf ARXIV_FINAL_VERSION/figures/output/arxiv/FIGURE_4_operating_curves.pdf || true
fi
# Also keep convenience copies at root
cp -f ARXIV_FINAL_VERSION/figures/output/arxiv/FIGURE_*.pdf ARXIV_FINAL_VERSION/ 2>/dev/null || true

# Step 5: Convert markdown to LaTeX in ARXIV_FINAL_VERSION (with header)
echo "[4/6] Converting markdown to LaTeX..."
pandoc ARXIV_FINAL_VERSION/FINAL_PAPER_FROM_SSOT.md \
    -o ARXIV_FINAL_VERSION/FINAL_PAPER.tex \
    --standalone \
    -H arxiv_header.tex

# Step 6: Convert markdown to PDF in ARXIV_FINAL_VERSION with CAP styling
echo "[5/6] Generating PDF (CAP styling)..."
pandoc ARXIV_FINAL_VERSION/FINAL_PAPER_FROM_SSOT.md \
    -o ARXIV_FINAL_VERSION/SEIZURE_TRANSFORMER_ARXIV.pdf \
    --pdf-engine=xelatex \
    -V geometry:margin=1in \
    -V fontsize=11pt \
    -V documentclass=article \
    -V colorlinks=true \
    -H arxiv_header.tex \
    --resource-path=.:CURRENT_DRAFT:ARXIV_FINAL_VERSION:ARXIV_FINAL_VERSION/figures/output/arxiv

# Optional: sync locked copy (commented out to avoid overwriting)
# cp -f ARXIV_FINAL_VERSION/SEIZURE_TRANSFORMER_ARXIV.pdf ARXIV_FINAL_VERSION/SEIZURE_TRANSFORMER_ARXIV_LOCKED.pdf

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
echo "1. Individual markdown files in CURRENT_DRAFT/*.md (SSOT)"
echo "2. Assembled via CURRENT_DRAFT/assemble.sh"
echo "3. All outputs go to ARXIV_FINAL_VERSION/"
echo "4. No manual editing - all changes go to markdown SSOT"
echo ""
echo "ARXIV_FINAL_VERSION is the single source of truth for submission!"
