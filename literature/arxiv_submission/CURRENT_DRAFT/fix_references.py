#!/usr/bin/env python3
"""Fix reference ordering to match order of appearance in text"""

import re
from pathlib import Path
from collections import OrderedDict

# Define the sections to process in order
SECTIONS = [
    "01_abstract.md",
    "02_introduction.md",
    "03_background.md",
    "04_methods.md",
    "05_results.md",
    "06_discussion.md",
    "07_conclusion.md",
    "08_reproducibility.md"
]

def find_citation_order():
    """Find the order in which citations appear in the text"""
    seen = OrderedDict()
    citation_pattern = re.compile(r'\[(\d+)\]')

    for section_file in SECTIONS:
        if Path(section_file).exists():
            content = Path(section_file).read_text()
            matches = citation_pattern.findall(content)
            for ref_num in matches:
                if ref_num not in seen:
                    seen[ref_num] = len(seen) + 1

    return seen

def create_mapping(old_order):
    """Create mapping from old to new reference numbers"""
    mapping = {}
    for old_num, new_num in old_order.items():
        mapping[int(old_num)] = new_num
    return mapping

def update_content(content, mapping):
    """Update reference numbers in content"""
    # Sort by length descending to avoid replacing [1] when we mean [11]
    sorted_refs = sorted(mapping.items(), key=lambda x: -x[0])

    for old_ref, new_ref in sorted_refs:
        # Replace [old] with [new]
        old_pattern = f'[{old_ref}]'
        new_pattern = f'[{new_ref}]'
        content = content.replace(old_pattern, new_pattern)

    return content

def update_reference_list():
    """Update the reference list to match new numbering"""
    ref_file = "10_references_from_draft.md"
    if not Path(ref_file).exists():
        print(f"Warning: {ref_file} not found")
        return

    # Read current references
    content = Path(ref_file).read_text()
    lines = content.split('\n')

    # Extract references (lines starting with [N])
    references = {}
    other_lines = []
    ref_pattern = re.compile(r'^\[(\d+)\]')

    for line in lines:
        match = ref_pattern.match(line)
        if match:
            ref_num = int(match.group(1))
            references[ref_num] = line
        else:
            other_lines.append(line)

    # Get the mapping
    citation_order = find_citation_order()
    mapping = create_mapping(citation_order)

    # Create new reference list in correct order
    new_references = []
    for new_num in range(1, len(mapping) + 1):
        # Find which old reference should be at this position
        for old_num, mapped_new in mapping.items():
            if mapped_new == new_num:
                if old_num in references:
                    # Update the reference number in the text
                    old_ref = references[old_num]
                    new_ref = re.sub(r'^\[\d+\]', f'[{new_num}]', old_ref)
                    new_references.append(new_ref)
                break

    # Add any unused references at the end (refs 12, 13, etc)
    next_num = len(mapping) + 1
    for old_num in sorted(references.keys()):
        if old_num not in mapping:
            old_ref = references[old_num]
            new_ref = re.sub(r'^\[\d+\]', f'[{next_num}]', old_ref)
            new_references.append(new_ref)
            next_num += 1

    # Reconstruct the file
    result_lines = []
    if other_lines and other_lines[0].strip():  # Add header if exists
        result_lines.extend(other_lines[:1])
        result_lines.append('')

    result_lines.extend(new_references)

    # Write back
    Path(ref_file).write_text('\n'.join(result_lines))
    print(f"Updated {ref_file}")

def main():
    # Find citation order
    citation_order = find_citation_order()
    print("Citation order of appearance:")
    for old_num, new_num in citation_order.items():
        print(f"  [{old_num}] -> [{new_num}]")

    # Create mapping
    mapping = create_mapping(citation_order)

    # Update each section file
    for section_file in SECTIONS:
        if Path(section_file).exists():
            content = Path(section_file).read_text()
            new_content = update_content(content, mapping)
            Path(section_file).write_text(new_content)
            print(f"Updated {section_file}")

    # Update reference list
    update_reference_list()

    # Update assembled versions
    for assembled_file in ["CURRENT_WORKING_DRAFT_ASSEMBLED.md", "FULL_PAPER_PURE.md"]:
        if Path(assembled_file).exists():
            content = Path(assembled_file).read_text()
            new_content = update_content(content, mapping)
            Path(assembled_file).write_text(new_content)
            print(f"Updated {assembled_file}")

    print("\nDone! References are now in order of appearance.")

if __name__ == "__main__":
    main()