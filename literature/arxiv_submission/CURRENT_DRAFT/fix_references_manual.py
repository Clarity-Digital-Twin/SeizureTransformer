#!/usr/bin/env python3
"""Manually fix reference ordering based on what citations actually refer to"""

import re
from pathlib import Path

# Manual mapping based on what the text actually refers to
# After analyzing the text, here's what each citation refers to:
CORRECT_MAPPING = {
    # In text [1] refers to EpilepsyBench/SeizureTransformer - Was originally [5] or [1]
    # In text [2] refers to TUSZ/Shah - Was originally [3]
    # In text [3] refers to SzCORE - Was originally [4]
    # etc.

    # Current wrong -> Correct original
    1: 5,   # Text [1] (EpilepsyBench) should map to original [5]
    2: 3,   # Text [2] (TUSZ) should map to original [3]
    3: 4,   # Text [3] (SzCORE) should map to original [4]
    4: 10,  # Text [4] (Roy) should map to original [10]
    5: 9,   # Text [5] (Gemein) should map to original [9]
    6: 11,  # Text [6] (Siena/Detti) should map to original [11]
    7: 14,  # Text [7] (pyEDFlib) should map to original [14]
    8: 1,   # Text [8] (SeizureTransformer Wu) should map to original [1]
    9: 2,   # Text [9] (Shah TAES) should map to original [2]
    10: 6,  # Text [10] (NEDC) should map to original [6]
    11: 7,  # Text [11] (Beniczky) should map to original [7]
    12: 12, # Text [12] (WHO) should map to original [12]
    13: 13, # Text [13] (Perucca) should map to original [13]
}

# But wait - I need to analyze what the text CURRENTLY says
# Let me check what [1] actually refers to in the abstract

def analyze_current_citations():
    """Analyze what citations currently refer to"""
    abstract = Path("01_abstract.md").read_text()

    # Find what [1] refers to
    if "EpilepsyBench" in abstract and "[1]" in abstract:
        print("Text uses [1] for EpilepsyBench")
        # Original EpilepsyBench was [5]

    if "TUSZ" in abstract and "[2]" in abstract:
        print("Text uses [2] for TUSZ")
        # Original TUSZ was [3]

def main():
    # Read original references
    orig_refs = {}
    with open("10_references_original.md") as f:
        for line in f:
            match = re.match(r'^\[(\d+)\] (.+)', line)
            if match:
                num = int(match.group(1))
                content = match.group(2)
                orig_refs[num] = line.strip()

    print("Original references:")
    for i in range(1, 15):
        if i in orig_refs:
            print(f"  [{i}] {orig_refs[i][:60]}...")

    # The correct order based on what the text refers to:
    # Text [1] should be EpilepsyBench (original [5])
    # Text [2] should be TUSZ Shah (original [3])
    # Text [3] should be SzCORE (original [4])
    # Text [4] should be Roy (original [10])
    # Text [5] should be Gemein (original [9])
    # Text [6] should be Detti/Siena (original [11])
    # Text [7] should be WHO (original [12])
    # Text [8] should be SeizureTransformer Wu (original [1])
    # Text [9] should be Shah TAES (original [2])
    # Text [10] should be NEDC (original [6])
    # Text [11] should be pyEDFlib (original [14])
    # Text [12] should be Beniczky (original [7])
    # Text [13] should be Perucca (original [13])
    # Text [14] should be Haibe-Kains (original [8])

    new_order = [5, 3, 4, 10, 9, 11, 12, 1, 2, 6, 14, 7, 13, 8]

    # Create new reference list
    new_refs = ["# References", ""]
    for i, orig_num in enumerate(new_order, 1):
        if orig_num in orig_refs:
            # Replace the number
            new_ref = re.sub(r'^\[\d+\]', f'[{i}]', orig_refs[orig_num])
            new_refs.append(new_ref)
            print(f"[{i}] <- original [{orig_num}]")

    # Write new references
    Path("10_references_from_draft.md").write_text('\n'.join(new_refs))
    print("\nWrote corrected references to 10_references_from_draft.md")

if __name__ == "__main__":
    analyze_current_citations()
    main()