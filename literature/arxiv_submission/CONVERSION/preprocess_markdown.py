#!/usr/bin/env python3
"""
Simplified preprocessor that removes duplicate title blocks.
"""
import re
import sys
from pathlib import Path

def preprocess_markdown(input_file: str, output_file: str) -> None:
    content = Path(input_file).read_text(encoding='utf-8')

    # Remove the duplicate title block that appears after the YAML
    # The pattern is: # Title\n**Author**\nAffiliation\nDate\n---\n
    pattern = r'^#\s+SeizureTransformer[^\n]+\n\n?\*\*[^\n]+\*\*\n[^\n]+\n[^\n]+\n\n?---\s*\n'
    content = re.sub(pattern, '', content, count=1, flags=re.MULTILINE)

    # Make Abstract unnumbered
    content = re.sub(r'^(##\s+Abstract)\s*$', r"\1 {.unnumbered}", content, flags=re.M)

    # Remove date from YAML if present
    content = re.sub(r'^(\s*date:\s*[^\n]*\n)', '', content, flags=re.M)

    Path(output_file).write_text(content, encoding='utf-8')
    print(f"Preprocessed {input_file} -> {output_file}")

if __name__ == '__main__':
    inp = sys.argv[1] if len(sys.argv) > 1 else 'paper.md'
    out = sys.argv[2] if len(sys.argv) > 2 else 'paper_preprocessed.md'
    preprocess_markdown(inp, out)