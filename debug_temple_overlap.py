#!/usr/bin/env python3
"""Debug: What overlap method does Temple NEDC use?"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Let's examine the actual scoring algorithm more carefully
print("Temple NEDC TAES Algorithm Investigation")
print("="*60)
print("\nKnown facts about TAES scoring:")
print("1. TAES = Time-Aligned Event Scoring")
print("2. Temple results: 27.72% sensitivity, 12.41 FA/24h")
print("3. Our results with overlap=0.0: 23.45% sensitivity, 9.97 FA/24h")
print("4. Our results with overlap=0.5: 7.68% sensitivity, 23.89 FA/24h")

print("\nPossible issues:")
print("1. Overlap calculation method (ratio relative to what?)")
print("2. Event matching algorithm (greedy vs optimal)")
print("3. Minimum overlap duration (not ratio)")
print("4. Any-Any matching vs 1-to-1 matching")

# Let's examine our scorer's matching algorithm
from seizure_evaluation.taes.scorer import TAESScorer, Event

# Create test cases
print("\n" + "="*60)
print("Testing edge cases:")

# Test case 1: One reference spans multiple hypotheses
ref_events = [Event(0, 100)]  # One long event
hyp_events = [Event(10, 20), Event(30, 40), Event(50, 60)]  # Three short events

scorer = TAESScorer(overlap_threshold=0.0)

# Manually calculate what Temple might do
print("\nCase 1: One reference event spans multiple predictions")
print("Reference: [0-100]")
print("Hypothesis: [10-20], [30-40], [50-60]")

# Our scorer uses greedy 1-to-1 matching
# Temple might allow many-to-one matching?

# Test case 2: Check the actual matching in our implementation
print("\nLet's trace through the matching algorithm...")
print("Our algorithm: For each hypothesis, find best matching reference")
print("Temple might: Allow multiple hypotheses to match same reference?")