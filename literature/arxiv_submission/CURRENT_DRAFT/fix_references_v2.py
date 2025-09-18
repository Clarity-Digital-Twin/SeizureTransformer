#!/usr/bin/env python3
"""Fix reference ordering to match order of appearance in text - Version 2"""

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

# Original references mapping
ORIGINAL_REFS = {
    1: "Wu K, Zhao Z, Yener B. SeizureTransformer",
    2: "Shah V, Golmohammadi M, Obeid I, Picone J. Objective Evaluation Metrics",
    3: "Shah V, von Weltin E, Lopez S, McHugh JR",
    4: "Dan J, Pale U, Amirshahi A",
    5: "EpilepsyBench Consortium",
    6: "NEDC. Neural Engineering Data Consortium",
    7: "Beniczky S, Ryvlin P",
    8: "Haibe-Kains B, Adam GA",
    9: "Gemein LAW, Schirrmeister RT",
    10: "Roy S, Kiral I, Mirmomeni M",
    11: "Detti P. Siena Scalp EEG Database",
    12: "World Health Organization. Epilepsy",
    13: "Perucca E, Perucca P",
    14: "Holger, Kern S, Papadopoulos"
}

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

def main():
    # Find citation order (what citations appear in what order)
    citation_order = find_citation_order()
    print("Order of first appearance:")
    for old_num, new_num in citation_order.items():
        old_num_int = int(old_num)
        print(f"  [{old_num}] ({ORIGINAL_REFS.get(old_num_int, 'Unknown')[:30]}...) -> [{new_num}]")

    # Create mapping
    mapping = {int(old): new for old, new in citation_order.items()}

    # Read original references file
    original_refs_path = Path("10_references_original.md")
    if not original_refs_path.exists():
        print("Error: 10_references_original.md not found")
        return

    ref_content = original_refs_path.read_text()
    lines = ref_content.split('\n')

    # Parse references
    references = {}
    header_lines = []
    for line in lines:
        match = re.match(r'^\[(\d+)\]', line)
        if match:
            ref_num = int(match.group(1))
            references[ref_num] = line
        elif line.strip() and not line.startswith('['):
            header_lines.append(line)

    # Update each section file - replace citations
    for section_file in SECTIONS:
        if Path(section_file).exists():
            content = Path(section_file).read_text()

            # Sort mappings by old number descending to avoid [1] matching in [11]
            sorted_mapping = sorted(mapping.items(), key=lambda x: -x[0])

            for old_ref, new_ref in sorted_mapping:
                # Use word boundaries to ensure we don't replace partial matches
                old_pattern = f'[{old_ref}]'
                new_pattern = f'[{new_ref}]'
                content = content.replace(old_pattern, new_pattern)

            Path(section_file).write_text(content)
            print(f"Updated citations in {section_file}")

    # Create new reference list in correct order
    new_refs = []
    for new_num in range(1, len(mapping) + 1):
        # Find which old reference should be at this position
        for old_num, mapped_new in mapping.items():
            if mapped_new == new_num:
                if old_num in references:
                    # Update the reference number in the text
                    old_ref = references[old_num]
                    new_ref = re.sub(r'^\[\d+\]', f'[{new_num}]', old_ref)
                    new_refs.append(new_ref)
                break

    # Add any unused references at the end (refs 12, 13, 14 if not cited)
    next_num = len(mapping) + 1
    for old_num in sorted(references.keys()):
        if old_num not in mapping:
            old_ref = references[old_num]
            new_ref = re.sub(r'^\[\d+\]', f'[{next_num}]', old_ref)
            new_refs.append(new_ref)
            print(f"  Unused reference [{old_num}] moved to [{next_num}]")
            next_num += 1

    # Write new reference file
    output_lines = []
    if header_lines:
        output_lines.extend(header_lines)
        output_lines.append('')
    output_lines.extend(new_refs)

    Path("10_references_from_draft.md").write_text('\n'.join(output_lines))
    print(f"Updated 10_references_from_draft.md")

    # Update assembled versions
    for assembled_file in ["CURRENT_WORKING_DRAFT_ASSEMBLED.md", "FULL_PAPER_PURE.md"]:
        if Path(assembled_file).exists():
            content = Path(assembled_file).read_text()

            # Replace citations
            sorted_mapping = sorted(mapping.items(), key=lambda x: -x[0])
            for old_ref, new_ref in sorted_mapping:
                old_pattern = f'[{old_ref}]'
                new_pattern = f'[{new_ref}]'
                content = content.replace(old_pattern, new_pattern)

            # Replace reference section
            ref_pattern = r'# References\n\n.*?(?=# |\Z)'
            new_ref_section = '# References\n\n' + '\n'.join(new_refs) + '\n\n'
            content = re.sub(ref_pattern, new_ref_section, content, flags=re.DOTALL)

            Path(assembled_file).write_text(content)
            print(f"Updated {assembled_file}")

    print("\nDone! References are now in order of appearance.")

if __name__ == "__main__":
    main()