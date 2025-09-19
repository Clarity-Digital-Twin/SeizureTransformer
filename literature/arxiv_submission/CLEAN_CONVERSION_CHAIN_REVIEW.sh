#!/usr/bin/env bash
# REVIEW-ONLY build: does NOT touch ARXIV_FINAL_VERSION
set -euo pipefail

echo "SEIZURE TRANSFORMER ARXIV REVIEW BUILD"
echo "======================================"

if [[ ! -d "CURRENT_DRAFT" ]]; then
  echo "ERROR: Must run from literature/arxiv_submission" >&2
  exit 1
fi

REVIEW_DIR="ARXIV_REVIEW_BUILD"
mkdir -p "$REVIEW_DIR"

echo "[1/5] Assemble markdown (SSOT)"
pushd CURRENT_DRAFT >/dev/null
./assemble.sh
popd >/dev/null

cp CURRENT_DRAFT/CURRENT_WORKING_DRAFT_ASSEMBLED.md "$REVIEW_DIR/REVIEW_FROM_SSOT.md"

echo "[2/5] Stage figures to match paths"
mkdir -p "$REVIEW_DIR/figures/output/arxiv"
if compgen -G "ARXIV_FINAL_VERSION/FIGURE_*.pdf" > /dev/null; then
  cp ARXIV_FINAL_VERSION/FIGURE_*.pdf "$REVIEW_DIR/figures/output/arxiv/"
elif compgen -G "figures/output/arxiv/FIGURE_*.pdf" > /dev/null; then
  cp figures/output/arxiv/FIGURE_*.pdf "$REVIEW_DIR/figures/output/arxiv/"
else
  echo "WARNING: No figures found (expected FIGURE_*.pdf)" >&2
fi

echo "[3/5] Create TeX with tighter captions"
pandoc "$REVIEW_DIR/REVIEW_FROM_SSOT.md" \
  -o "$REVIEW_DIR/FINAL_PAPER_REVIEW.tex" \
  --standalone \
  -H arxiv_header.tex

echo "[4/5] Create review PDF (XeLaTeX)"
pandoc "$REVIEW_DIR/REVIEW_FROM_SSOT.md" \
  -o "$REVIEW_DIR/SEIZURE_TRANSFORMER_REVIEW.pdf" \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=article \
  -V colorlinks=true \
  -H arxiv_header.tex \
  --resource-path=.:CURRENT_DRAFT:$REVIEW_DIR:$REVIEW_DIR/figures/output/arxiv:ARXIV_FINAL_VERSION

echo "[5/5] Done. Review outputs in $REVIEW_DIR/"
ls -la "$REVIEW_DIR" || true

