#!/usr/bin/env python3
"""
Properly concatenate all docs_with_figures files into a single markdown document.
"""

import os

def concatenate_docs():
    """Concatenate all markdown files from docs_with_figures in order."""

    base_dir = "literature/arxiv_submission/docs_with_figures"

    # Files in the correct order
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

    content_parts = []

    for filename in files:
        filepath = os.path.join(base_dir, filename)
        print(f"Reading {filepath}...")

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

            # Skip YAML frontmatter if present (between --- lines at start)
            if content.startswith('---'):
                # Find the closing ---
                lines = content.split('\n')
                end_idx = -1
                for i in range(1, len(lines)):
                    if lines[i].strip() == '---':
                        end_idx = i
                        break
                if end_idx > 0:
                    content = '\n'.join(lines[end_idx+1:])

            # Add content with separator
            content_parts.append(content.strip())

    # Join all parts with double newline
    full_content = '\n\n'.join(content_parts)

    # Write the full paper
    output_file = "literature/arxiv_submission/full_paper_concatenated.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"\nWrote concatenated paper to {output_file}")

    # Print statistics
    lines = full_content.count('\n') + 1
    chars = len(full_content)
    print(f"Total lines: {lines}")
    print(f"Total characters: {chars}")

if __name__ == "__main__":
    concatenate_docs()