#!/usr/bin/env bash
set -euo pipefail

# Build LaTeX and PDF from the renumbered, polished Markdown
# Requirements: pandoc, XeLaTeX (texlive-xetex)

ROOT_DIR="$(cd "$(dirname "$0")"/../.. && pwd)"
ARXIV_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ARXIV_DIR"

SRC_MD="PAPER_FINAL_FORMATTED_RENUMBERED.md"
OUT_PDF="SEIZURE_TRANSFORMER_ARXIV_FINAL.pdf"
OUT_TEX="SEIZURE_TRANSFORMER_ARXIV_FINAL.tex"

if [[ ! -f "$SRC_MD" ]]; then
  echo "Error: $SRC_MD not found. Run the renumber step first." >&2
  exit 1
fi

# Ensure pandoc sees repo root for figure paths (figures/output/arxiv/*)
RES_PATH=".:$ROOT_DIR"

common_args=(
  --from=markdown+yaml_metadata_block+smart+link_attributes
  --pdf-engine=xelatex
  --variable geometry:margin=1in
  --variable fontsize=11pt
  --variable documentclass=article
  -V colorlinks=true
  --toc
  --resource-path="${RES_PATH}"
)

echo "Generating LaTeX: $OUT_TEX"
pandoc "$SRC_MD" -t latex -o "$OUT_TEX" "${common_args[@]}"

echo "Generating PDF: $OUT_PDF"
pandoc "$SRC_MD" -o "$OUT_PDF" "${common_args[@]}"

echo "Done. Outputs:"
ls -la "$OUT_TEX" "$OUT_PDF"

