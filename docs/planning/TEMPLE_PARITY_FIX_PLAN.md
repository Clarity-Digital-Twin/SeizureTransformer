# TEMPLE NEDC OVERLAP PARITY FIX PLAN (Corrected)

## The Problem (What’s actually mismatched)

Our pipeline reports Temple’s OVERLAP metrics (any-overlap event scoring). The native “TAESScorer” currently uses a greedy 1-to-1 matching between hyp and ref events and then derives TP/FP/FN. That is not equivalent to Temple’s OVERLAP algorithm, which counts:
- Hits = number of reference events overlapped by at least one hypothesis event (no 1–1 constraint)
- Misses = number of reference events with no overlap
- False Alarms = number of hypothesis events that overlap no reference event

This discrepancy creates two edge-case mismatches versus Temple OVERLAP:
- One hyp overlaps multiple refs → Temple counts multiple hits (one per ref). Greedy 1–1 counts only 1 TP → sensitivity too low.
- Multiple hyps overlap one ref → Temple counts 1 hit, 0 FA. Greedy 1–1 matches one hyp, and (incorrectly) counts the others as FP → FA too high.

We do NOT need fractional TAES (DP alignment) to achieve parity with the OVERLAP section that we use. We need exact any-overlap counting.

## The Fix (Exact OVERLAP logic)

Replace the greedy matcher with any-overlap counting for OVERLAP mode:

Pseudo-code (per file, per label):
```
ref_overlapped = [False] * len(ref_events)
hyp_overlapped = [False] * len(hyp_events)

for r, ref in enumerate(ref_events):
  for h, hyp in enumerate(hyp_events):
    if overlap(ref, hyp) > 0:
      ref_overlapped[r] = True     # each ref can be ‘hit’ by any number of hyps
      hyp_overlapped[h] = True     # any overlapping hyp is NOT a false alarm

hits = sum(ref_overlapped)
misses = len(ref_events) - hits
false_alarms = len(hyp_events) - sum(hyp_overlapped)

sensitivity_percent = 100 * hits / len(ref_events) if len(ref_events) > 0 else 0
fa_per_24h = false_alarms * 86400.0 / total_duration_sec
```

This matches Temple’s `nedc_eeg_eval_ovlp.py` definitions and avoids 1–1 assignment entirely.

## Implementation Steps

1) Add explicit OVERLAP mode to native scorer
- Option A: Add a new `OverlapScorer` in `seizure_evaluation/taes/overlap_scorer.py` implementing the above.
- Option B: Extend `TAESScorer` with a `mode="overlap"` path that uses any-overlap counting instead of greedy matching.

2) Wire native backend to use OVERLAP mode
- In `evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py` where we create `TAESScorer(overlap_threshold=0.0)`, either:
  - switch to `OverlapScorer()`, or
  - pass `mode="overlap"` so it uses the any-overlap path.

3) Tests for exact parity on edge cases
- Case A: One hyp spans two refs → expect 2 hits, 0 FA.
- Case B: Two hyps overlap one ref → expect 1 hit, 0 FA (both hyps non-FA).
- Case C: No overlaps → 0 hits, FA = #hyps.

4) End-to-end verification
- Re-run `run_nedc.py` with `--backend native-taes` on dev/eval baselines and compare to Temple OVERLAP section. Require ≤0.01 tolerance for both sensitivity and FA/24h.

## Scope Boundaries (What this plan is NOT)

- Not implementing DP ALIGNMENT or fractional TAES. Those are separate scoring methods in NEDC and are not what our pipeline currently gates on.
- Not changing which section the pipeline parses (it already targets OVERLAP correctly). If we later choose DP ALIGNMENT for tuning/reporting, we’ll add a separate plan to mirror that method.

## Success Criteria

- Exact parity with Temple OVERLAP for sensitivity and FA/24h on dev and eval baselines (≤0.01 tolerance).
- Edge cases above match Temple semantics.
- `metrics.json` continues to store results under `overlap` (and duplicate to `taes` only for backward compatibility, if needed).

## Notes on F1

- Temple’s OVERLAP reports per-label F1 and a summary; our current native path calculates dataset-level F1 from aggregated TP/FP/FN. If F1 must match exactly, implement per-label accumulation and Temple’s summary formatting. Sens/FA parity is the primary goal.

## Optional Future Work

- Add a native DP ALIGNMENT/“true TAES” implementation if we decide to gate on that section.
- Add a flag in `run_nedc.py` to choose which section’s semantics the native backend should emulate (`--scoring {overlap, dpalign}`), keeping parsing/outputs consistent.

---

This corrected plan targets EXACT parity with the Temple OVERLAP section, which is what our pipeline currently reports. No fractional TAES required.
