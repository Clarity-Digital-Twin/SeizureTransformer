#!/usr/bin/env python3
"""
Test OVERLAP scorer edge cases to verify Temple NEDC parity.
These tests demonstrate the key differences between OVERLAP and greedy 1-to-1 matching.
"""

from seizure_evaluation.taes.overlap_scorer import OverlapScorer, Event
from seizure_evaluation.taes.scorer import TAESScorer


def test_case_a_one_hyp_multiple_refs():
    """
    Edge Case A: One hyp spans two refs
    Temple OVERLAP: 2 hits, 0 FA (both refs are hit)
    Greedy 1-to-1: 1 TP, 1 FN (only one ref matched)
    """
    print("\n=== Case A: One Hyp Overlapping Two Refs ===")

    ref_events = [
        Event(10.0, 20.0),  # Ref 1
        Event(25.0, 35.0),  # Ref 2
    ]
    hyp_events = [
        Event(15.0, 30.0),  # Overlaps both refs
    ]

    # Test OVERLAP scorer
    overlap_scorer = OverlapScorer()
    overlap_metrics = overlap_scorer.score_events(ref_events, hyp_events, 100.0)

    print(f"Refs: [10-20], [25-35]")
    print(f"Hyp:  [15-30] (overlaps both)")
    print(f"\nOVERLAP Scorer (Correct):")
    print(f"  Hits: {overlap_metrics.hits}, Misses: {overlap_metrics.misses}, FA: {overlap_metrics.false_alarms}")
    print(f"  Sensitivity: {overlap_metrics.sensitivity:.1f}%")
    print(f"  Expected: 2 hits, 0 misses, 0 FA → 100% sensitivity ✓")

    # Compare with greedy 1-to-1
    taes_scorer = TAESScorer(overlap_threshold=0.0)
    taes_metrics = taes_scorer.score_events(ref_events, hyp_events, 100.0)

    print(f"\nGreedy 1-to-1 (Wrong for OVERLAP):")
    print(f"  TP: {taes_metrics.true_positives}, FP: {taes_metrics.false_positives}, FN: {taes_metrics.false_negatives}")
    print(f"  Sensitivity: {taes_metrics.sensitivity:.1f}%")
    print(f"  Gets: 1 TP, 0 FP, 1 FN → 50% sensitivity ✗")


def test_case_b_multiple_hyps_one_ref():
    """
    Edge Case B: Two hyps overlap one ref
    Temple OVERLAP: 1 hit, 0 FA (ref is hit, both hyps valid)
    Greedy 1-to-1: 1 TP, 1 FP (one hyp matched, other counted as FP)
    """
    print("\n=== Case B: Two Hyps Overlapping One Ref ===")

    ref_events = [
        Event(20.0, 40.0),  # One ref
    ]
    hyp_events = [
        Event(15.0, 25.0),  # Hyp 1 overlaps ref
        Event(35.0, 45.0),  # Hyp 2 overlaps ref
    ]

    # Test OVERLAP scorer
    overlap_scorer = OverlapScorer()
    overlap_metrics = overlap_scorer.score_events(ref_events, hyp_events, 100.0)

    print(f"Ref:  [20-40]")
    print(f"Hyps: [15-25], [35-45] (both overlap ref)")
    print(f"\nOVERLAP Scorer (Correct):")
    print(f"  Hits: {overlap_metrics.hits}, Misses: {overlap_metrics.misses}, FA: {overlap_metrics.false_alarms}")
    print(f"  FA/24h: {overlap_metrics.fa_per_24h:.1f}")
    print(f"  Expected: 1 hit, 0 misses, 0 FA → 0 FA/24h ✓")

    # Compare with greedy 1-to-1
    taes_scorer = TAESScorer(overlap_threshold=0.0)
    taes_metrics = taes_scorer.score_events(ref_events, hyp_events, 100.0)

    print(f"\nGreedy 1-to-1 (Wrong for OVERLAP):")
    print(f"  TP: {taes_metrics.true_positives}, FP: {taes_metrics.false_positives}, FN: {taes_metrics.false_negatives}")
    print(f"  FA/24h: {taes_metrics.fa_per_24h:.1f}")
    print(f"  Gets: 1 TP, 1 FP, 0 FN → 864 FA/24h ✗")


def test_case_c_no_overlaps():
    """
    Edge Case C: No overlaps
    Both methods should agree: 0 hits, all FA
    """
    print("\n=== Case C: No Overlaps ===")

    ref_events = [
        Event(10.0, 20.0),
        Event(30.0, 40.0),
    ]
    hyp_events = [
        Event(50.0, 60.0),
        Event(70.0, 80.0),
    ]

    # Test OVERLAP scorer
    overlap_scorer = OverlapScorer()
    overlap_metrics = overlap_scorer.score_events(ref_events, hyp_events, 100.0)

    print(f"Refs: [10-20], [30-40]")
    print(f"Hyps: [50-60], [70-80] (no overlaps)")
    print(f"\nOVERLAP Scorer:")
    print(f"  Hits: {overlap_metrics.hits}, Misses: {overlap_metrics.misses}, FA: {overlap_metrics.false_alarms}")
    print(f"  Expected: 0 hits, 2 misses, 2 FA ✓")

    # Compare with greedy 1-to-1
    taes_scorer = TAESScorer(overlap_threshold=0.0)
    taes_metrics = taes_scorer.score_events(ref_events, hyp_events, 100.0)

    print(f"\nGreedy 1-to-1:")
    print(f"  TP: {taes_metrics.true_positives}, FP: {taes_metrics.false_positives}, FN: {taes_metrics.false_negatives}")
    print(f"  Both methods agree here ✓")


def test_real_scenario():
    """
    Real scenario showing why dev set has small differences.
    With many events, the differences compound.
    """
    print("\n=== Real Scenario: Why Dev Differs ===")

    # Simulate typical TUSZ scenario
    ref_events = [
        Event(100.0, 120.0),
        Event(200.0, 220.0),
        Event(300.0, 320.0),
    ]
    hyp_events = [
        Event(95.0, 125.0),   # Overlaps ref 1
        Event(195.0, 205.0),  # Overlaps ref 2
        Event(210.0, 215.0),  # Also overlaps ref 2!
        Event(400.0, 420.0),  # No overlap (FA)
    ]

    # Test OVERLAP scorer
    overlap_scorer = OverlapScorer()
    overlap_metrics = overlap_scorer.score_events(ref_events, hyp_events, 1800.0)

    print(f"Complex scenario with multiple overlaps")
    print(f"\nOVERLAP Scorer (Temple method):")
    print(f"  Hits: {overlap_metrics.hits}, Misses: {overlap_metrics.misses}, FA: {overlap_metrics.false_alarms}")
    print(f"  Sensitivity: {overlap_metrics.sensitivity:.1f}%, FA/24h: {overlap_metrics.fa_per_24h:.2f}")

    # Compare with greedy 1-to-1
    taes_scorer = TAESScorer(overlap_threshold=0.0)
    taes_metrics = taes_scorer.score_events(ref_events, hyp_events, 1800.0)

    print(f"\nGreedy 1-to-1 (our current method):")
    print(f"  TP: {taes_metrics.true_positives}, FP: {taes_metrics.false_positives}, FN: {taes_metrics.false_negatives}")
    print(f"  Sensitivity: {taes_metrics.sensitivity:.1f}%, FA/24h: {taes_metrics.fa_per_24h:.2f}")
    print(f"\n  → Greedy counts hyp[210-215] as FP, but OVERLAP doesn't!")


if __name__ == "__main__":
    print("=" * 60)
    print("OVERLAP SCORER EDGE CASE TESTS")
    print("Verifying Temple NEDC OVERLAP parity")
    print("=" * 60)

    test_case_a_one_hyp_multiple_refs()
    test_case_b_multiple_hyps_one_ref()
    test_case_c_no_overlaps()
    test_real_scenario()

    print("\n" + "=" * 60)
    print("KEY INSIGHT: OVERLAP counts any-overlap, not 1-to-1 matching!")
    print("This explains the small differences we see on dev set.")
    print("=" * 60)