#!/usr/bin/env python3
"""
Preprocess markdown file for clean LaTeX/PDF conversion
Fixes common issues that break pandoc conversions
"""

import re
import sys

def preprocess_markdown(input_file, output_file):
    """Clean and prepare markdown for conversion"""

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix figure references - remove broken paths
    content = re.sub(
        r'!\[([^\]]+)\]\([^)]*\){[^}]*}',
        r'![\1](figures/placeholder.png)',
        content
    )

    # Simplify figure syntax for pandoc
    content = re.sub(
        r'!\[Figure (\d+): ([^\]]+)\]\([^)]+\)',
        r'**Figure \1:** \2',
        content
    )

    # Fix table formatting - convert complex tables to simple format
    # This handles the specific table in the paper
    table_pattern = r'\| Operating Point.*?\n\|.*?\n((?:\|.*?\n)+)'
    def fix_table(match):
        lines = match.group(0).split('\n')
        # Keep header and separator
        result = lines[0] + '\n' + lines[1] + '\n'
        # Process data rows
        for line in lines[2:]:
            if line.strip():
                result += line + '\n'
        return result

    content = re.sub(table_pattern, fix_table, content, flags=re.DOTALL)

    # Ensure proper spacing around sections
    content = re.sub(r'\n(#{1,3} )', r'\n\n\1', content)

    # Fix math symbols that might break LaTeX
    content = content.replace('~=', '≈')
    content = content.replace('>=', '≥')
    content = content.replace('<=', '≤')

    # Ensure YAML frontmatter is properly formatted
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            # Clean up YAML
            yaml = parts[1]
            # Fix email format
            yaml = yaml.replace('email: "JJ@novamindnyc.com"', 'email: "jj@novamindnyc.com"')
            content = '---' + yaml + '---' + parts[2]

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Preprocessed {input_file} -> {output_file}")
    return output_file

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "paper_clean.md"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "paper_preprocessed.md"
    preprocess_markdown(input_file, output_file)