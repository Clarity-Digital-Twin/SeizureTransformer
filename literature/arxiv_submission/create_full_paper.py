#!/usr/bin/env python3
"""
Create full paper by concatenating markdown files and fixing figure paths
Author: John H. Jung, MD, MS
Date: September 2025
"""

import os
from pathlib import Path

def create_full_paper():
    """Concatenate all markdown files and prepare for PDF conversion."""

    # Define the order of files
    files = [
        "00_abstract.md",
        "01_introduction.md",
        "02_background.md",
        "03_methods_evaluation.md",
        "04_results.md",
        "05_discussion.md",
        "06_conclusion.md",
        "07_reproducibility.md",
        "08_acknowledgments.md",
        "09_references.md",
        "10_appendix.md"
    ]

    base_dir = Path("docs_with_figures")
    output_file = Path("full_paper.md")

    full_content = []

    for i, filename in enumerate(files):
        filepath = base_dir / filename

        if not filepath.exists():
            print(f"Warning: {filepath} not found, skipping...")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix figure paths (change ../figures/ to figures/)
        content = content.replace("../figures/", "figures/")

        # Add page break between major sections (except after abstract)
        if i > 0 and i < len(files) - 1:
            content = "\n\\newpage\n\n" + content

        full_content.append(content)

    # Join all content with double newlines
    final_content = "\n\n".join(full_content)

    # Write the combined file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"✓ Created {output_file}")
    print(f"  Total sections: {len(files)}")
    print(f"  Total size: {len(final_content):,} characters")

    # Create conversion script
    create_conversion_script()

def create_conversion_script():
    """Create bash script for PDF conversion."""

    script_content = '''#!/bin/bash
# Convert full paper to PDF using pandoc

echo "Converting to PDF..."

# Basic PDF generation
pandoc full_paper.md \\
  -o jung_seizuretransformer_2025.pdf \\
  --pdf-engine=xelatex \\
  --number-sections \\
  --toc \\
  --toc-depth=2 \\
  -V geometry:margin=1in \\
  -V fontsize=11pt \\
  -V documentclass=article \\
  -V colorlinks=true \\
  -V linkcolor=blue \\
  -V urlcolor=blue \\
  -V citecolor=blue

echo "✓ Created jung_seizuretransformer_2025.pdf"

# Also create LaTeX for arXiv submission
pandoc full_paper.md \\
  -s \\
  -o jung_seizuretransformer_2025.tex \\
  --number-sections \\
  --toc \\
  -V geometry:margin=1in \\
  -V fontsize=11pt \\
  -V documentclass=article

echo "✓ Created jung_seizuretransformer_2025.tex for arXiv"
'''

    with open('convert_to_pdf.sh', 'w') as f:
        f.write(script_content)

    # Make it executable
    os.chmod('convert_to_pdf.sh', 0o755)
    print("✓ Created convert_to_pdf.sh")
    print("\nTo generate PDF, run:")
    print("  ./convert_to_pdf.sh")
    print("\nOr manually with:")
    print("  pandoc full_paper.md -o paper.pdf")

if __name__ == "__main__":
    create_full_paper()