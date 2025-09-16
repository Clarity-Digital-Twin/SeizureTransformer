#!/usr/bin/env python3
"""
Preprocess markdown for clean Pandoc → XeLaTeX conversion without destroying content.
- Keep YAML title/author; remove date from YAML.
- Remove any duplicate manual title/author/date block in the body.
- Make 'Abstract' unnumbered.
"""
import re
import sys
from pathlib import Path

def split_yaml(text: str):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n(.*)$', text, flags=re.S)
    if not m:
        return None, None, text
    return m.group(1), None, m.group(2)

def rebuild(yaml: str, body: str) -> str:
    yaml = yaml.rstrip('\n') + '\n'
    return f"---\n{yaml}---\n{body}"

def strip_manual_title_block_with_yaml(yaml: str, body: str) -> str:
    # if we can read title from YAML, remove a matching manual block in body
    mt = re.search(r'^\s*title:\s*"?(.+?)"?\s*$', yaml, flags=re.M)
    title = mt.group(1) if mt else None
    if not title:
        return body
    bl = body.lstrip('\n')
    lines = bl.splitlines(True)
    i = 0
    # Match H1 with the same title
    if i < len(lines) and re.match(r'^#\s+' + re.escape(title) + r'\s*$', lines[i]):
        i += 1
        # Skip up to 5 short lines (author, affiliation, date)
        k = 0
        while i < len(lines) and k < 5 and lines[i].strip() and len(lines[i].strip()) <= 60:
            i += 1; k += 1
        # Remove an immediate horizontal rule
        if i < len(lines) and lines[i].strip() == '---':
            i += 1
        body = ''.join(lines[i:]).lstrip('\n')
    return body

def make_abstract_unnumbered(text: str) -> str:
    # Convert '## Abstract' to unnumbered heading for Pandoc
    text = re.sub(r'^(##\s+Abstract)\s*$', r"\1 {.unnumbered}", text, flags=re.M)
    return text

def clean_yaml_remove_date(yaml: str) -> str:
    yaml = __import__('re').sub(r'(?m)^\s*date\s*:\s*.*(?:\n|$)', '', yaml)
    return yaml



def preprocess_markdown(input_file: str, output_file: str) -> None:
    content = Path(input_file).read_text(encoding='utf-8')
    # Normalize line endings to \n
    content = content.replace('\r\n','\n')
    # Parse YAML
    yaml, _, body = split_yaml(content)
    if yaml is not None:
        yaml = clean_yaml_remove_date(yaml)
        # Remove manual duplicate title block in body (if present)
        body = strip_manual_title_block_with_yaml(yaml, body)
        # Extra guard: drop a leading author/affiliation block ending with an HR
        body = re.sub(r'^(?:\*\*.*\*\*\s*\n(?:.*\n){0,6}?---\s*\n)', '', body)
        content = rebuild(yaml, body)
    # Make Abstract unnumbered
    content = make_abstract_unnumbered(content)
    # Normalize spacing
    content = re.sub(r'\n{3,}', '\n\n', content)
    Path(output_file).write_text(content, encoding='utf-8')
    print(f"Preprocessed {input_file} -> {output_file}")

if __name__ == '__main__':
    inp = sys.argv[1] if len(sys.argv) > 1 else 'paper.md'
    out = sys.argv[2] if len(sys.argv) > 2 else 'paper_preprocessed.md'
    preprocess_markdown(inp, out)