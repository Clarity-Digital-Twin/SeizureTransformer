#!/usr/bin/env python3
"""Analyze all scoring sections in Temple NEDC output."""

import re
from pathlib import Path

summary_file = Path("experiments/eval/baseline/nedc_results_frozen_temple/results/summary.txt")

with open(summary_file) as f:
    content = f.read()

# Find all sections
sections = re.findall(r"NEDC (\w+[^:]*) SCORING SUMMARY", content)
print("Temple NEDC Scoring Sections Found:")
for i, section in enumerate(sections, 1):
    print(f"{i}. {section}")

print("\n" + "="*60)

# Extract metrics from each section
for section_name in sections:
    print(f"\n{section_name} Section:")

    # Find the section
    pattern = f"NEDC {re.escape(section_name)} SCORING SUMMARY.*?(?=NEDC|$)"
    section_match = re.search(pattern, content, re.DOTALL)

    if section_match:
        section_text = section_match.group(0)

        # Extract key metrics
        sens_match = re.search(r"Sensitivity.*?:\s+([\d.]+)", section_text)
        fa_match = re.search(r"Total False Alarm Rate:\s+([\d.]+)", section_text)
        f1_match = re.search(r"F1 Score.*?:\s+([\d.]+)", section_text)

        # Also look for Targets/Hits/FA counts
        targets_match = re.search(r"Targets:\s+([\d.]+)", section_text)
        hits_match = re.search(r"Hits:\s+([\d.]+)", section_text)
        fa_count_match = re.search(r"False Alarms:\s+([\d.]+)", section_text)

        if sens_match:
            print(f"  Sensitivity: {sens_match.group(1)}%")
        if fa_match:
            print(f"  FA/24h: {fa_match.group(1)}")
        if f1_match:
            print(f"  F1 Score: {f1_match.group(1)}")
        if targets_match and hits_match:
            print(f"  Targets: {targets_match.group(1)}, Hits: {hits_match.group(1)}")
        if fa_count_match:
            print(f"  False Alarms (count): {fa_count_match.group(1)}")

print("\n" + "="*60)
print("ISSUE FOUND:")
print("Our metrics.json extracts from DP ALIGNMENT section (27.72% sens, wrong FA)")
print("But we named it 'taes' in the JSON!")
print("The actual TAES section has different metrics with fractional counts.")
print("\nDP Alignment appears to be the right one for our use case.")