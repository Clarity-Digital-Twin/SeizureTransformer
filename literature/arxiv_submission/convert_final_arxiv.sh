#!/bin/bash
# Final arXiv conversion matching "Attention Is All You Need" formatting
# Professional academic paper style with proper spacing and margins

echo "Converting to final arXiv format (matching classic ML papers)..."

# Option 1: Use the custom LaTeX template (RECOMMENDED)
echo "Compiling custom LaTeX template..."
pdflatex -interaction=nonstopmode arxiv_template.tex > /dev/null 2>&1
pdflatex -interaction=nonstopmode arxiv_template.tex > /dev/null 2>&1  # Run twice for references

if [ $? -eq 0 ]; then
    mv arxiv_template.pdf jung_seizuretransformer_2025_final.pdf
    echo "✓ Created jung_seizuretransformer_2025_final.pdf (custom LaTeX template)"
fi

# Option 2: Pandoc with optimized settings for arXiv style
echo ""
echo "Also generating pandoc version with matched settings..."
pandoc full_paper_clean.md \
  -o jung_seizuretransformer_2025_pandoc.pdf \
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
  --highlight-style=kate 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Created jung_seizuretransformer_2025_pandoc.pdf (pandoc version)"
fi

echo ""
echo "Files generated:"
echo "  • jung_seizuretransformer_2025_final.pdf  - Best version (custom LaTeX)"
echo "  • jung_seizuretransformer_2025_pandoc.pdf - Alternative (pandoc)"
echo "  • arxiv_template.tex                      - LaTeX source for editing"
echo ""
echo "Key formatting matching 'Attention Is All You Need':"
echo "  ✓ Centered title with horizontal rules"
echo "  ✓ 1.5 inch margins (wider, more professional)"
echo "  ✓ Times font family"
echo "  ✓ 10pt font size"
echo "  ✓ Proper author/affiliation formatting"
echo "  ✓ Centered 'Abstract' heading"
echo "  ✓ Black hyperlinks (not colored)"
echo "  ✓ Clean section numbering"