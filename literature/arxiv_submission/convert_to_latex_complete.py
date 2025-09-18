#!/usr/bin/env python3
"""Convert complete markdown paper to LaTeX with all sections and references"""

import re
import sys

def clean_latex_text(text):
    """Clean and convert markdown to LaTeX format"""
    # Replace special characters
    text = text.replace('~=', r'$\approx$')
    text = re.sub(r'~(\d)', r'$\\sim$\\1', text)
    text = re.sub(r'(\d+)-(\d+)×', r'\\1--\\2$\\times$', text)
    text = re.sub(r'(\d+)×', r'\\1$\\times$', text)
    text = re.sub(r'(\d+)x\s', r'\\1$\\times$ ', text)

    # Fix percentages and underscores
    text = re.sub(r'(\d+)%', r'\\1\\%', text)
    text = text.replace('_', r'\_')

    # FA/24h notation
    text = re.sub(r'(\d+\.?\d*)\s*FA/24h', r'\\1~FA/24h', text)

    # Math symbols
    text = text.replace('>=', r'$\geq$')
    text = text.replace('<=', r'$\leq$')
    text = text.replace('±', r'$\pm$')

    # Greek letters
    text = text.replace('theta=', r'$\theta$=')
    text = text.replace('theta ', r'$\theta$ ')
    text = text.replace('k=', r'$k$=')
    text = text.replace('d=', r'$d$=')

    # Bold and italic
    text = re.sub(r'\*\*([^*]+)\*\*', r'\\textbf{\\1}', text)
    text = re.sub(r'\*([^*]+)\*', r'\\textit{\\1}', text)

    # URLs
    text = re.sub(r'https?://[^\s)]+', lambda m: r'\url{' + m.group() + '}', text)

    # Fix [train] emoji reference
    text = text.replace('[train]', '(train emoji)')

    return text

# Read the full markdown
with open('current_draft/FULL_PAPER_PURE.md', 'r') as f:
    lines = f.readlines()

# Extract content sections
abstract = []
intro = []
background = []
methods = []
results = []
discussion = []
conclusion = []
repro = []
ack = []
appendix = []

current_section = None
for i, line in enumerate(lines):
    if '## Abstract' in line:
        current_section = 'abstract'
    elif '# Introduction' in line and i > 20:
        current_section = 'intro'
    elif '# Background' in line:
        current_section = 'background'
    elif '# Methods' in line and i < 100:
        current_section = 'methods'
    elif '# Results' in line and i < 150:
        current_section = 'results'
    elif '# Discussion' in line:
        current_section = 'discussion'
    elif '# Conclusion' in line and i > 200:
        current_section = 'conclusion'
    elif '# Reproducibility' in line and i > 220:
        current_section = 'repro'
    elif '# Acknowledgments' in line:
        current_section = 'ack'
    elif '# Appendix' in line:
        current_section = 'appendix'
    elif current_section:
        if current_section == 'abstract':
            abstract.append(line)
        elif current_section == 'intro':
            intro.append(line)
        elif current_section == 'background':
            background.append(line)
        elif current_section == 'methods':
            methods.append(line)
        elif current_section == 'results':
            results.append(line)
        elif current_section == 'discussion':
            discussion.append(line)
        elif current_section == 'conclusion':
            conclusion.append(line)
        elif current_section == 'repro':
            repro.append(line)
        elif current_section == 'ack':
            ack.append(line)
        elif current_section == 'appendix':
            appendix.append(line)

# Process sections
abstract_text = clean_latex_text(''.join(abstract[1:]))  # Skip empty line
intro_text = clean_latex_text(''.join(intro[1:]))
background_text = clean_latex_text(''.join(background[1:]))
methods_text = clean_latex_text(''.join(methods[1:]))
results_text = clean_latex_text(''.join(results[1:]))
discussion_text = clean_latex_text(''.join(discussion[1:]))
conclusion_text = clean_latex_text(''.join(conclusion[1:]))
repro_text = clean_latex_text(''.join(repro[1:]))
ack_text = clean_latex_text(''.join(ack[1:]))

# Extract specific tables
def process_table(text, start_marker, end_marker=None):
    """Extract and format LaTeX tables"""
    lines = text.split('\n')
    in_table = False
    table_lines = []

    for line in lines:
        if start_marker in line:
            in_table = True
        elif end_marker and end_marker in line:
            break
        elif in_table and '|' in line:
            # Process table row
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if cells:
                table_lines.append(' & '.join(cells) + r' \\')

    return '\n'.join(table_lines)

print("Conversion complete - sections extracted")
print(f"Abstract: {len(abstract_text)} chars")
print(f"Introduction: {len(intro_text)} chars")
print(f"Background: {len(background_text)} chars")
print(f"Methods: {len(methods_text)} chars")
print(f"Results: {len(results_text)} chars")
print(f"Discussion: {len(discussion_text)} chars")
print(f"Conclusion: {len(conclusion_text)} chars")
print(f"Reproducibility: {len(repro_text)} chars")
print(f"Acknowledgments: {len(ack_text)} chars")

# Save extracted sections for manual assembly
with open('latex/sections_extracted.txt', 'w') as f:
    f.write("ABSTRACT:\n" + abstract_text + "\n\n")
    f.write("INTRODUCTION:\n" + intro_text + "\n\n")
    f.write("BACKGROUND:\n" + background_text + "\n\n")
    f.write("METHODS:\n" + methods_text + "\n\n")
    f.write("RESULTS:\n" + results_text + "\n\n")
    f.write("DISCUSSION:\n" + discussion_text + "\n\n")
    f.write("CONCLUSION:\n" + conclusion_text + "\n\n")
    f.write("REPRODUCIBILITY:\n" + repro_text + "\n\n")
    f.write("ACKNOWLEDGMENTS:\n" + ack_text + "\n\n")

print("\nSections saved to latex/sections_extracted.txt")