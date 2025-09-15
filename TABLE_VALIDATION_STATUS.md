# Evaluation Results Table Validation Status

## ✅ Verified (No Merge Gap)

- Default (0.8/5/2.0):
  - NEDC OVERLAP (Temple): 45.63% sensitivity, 100.06 FA/24h, F1=0.519
  - NEDC OVERLAP (Native): 45.63% sensitivity, 100.06 FA/24h, F1=0.519 (parity)
  - SzCORE: 52.35% sensitivity, 8.46 FA/24h
  - NEDC TAES (Temple): Pending re‑extraction at paper defaults

## ⏳ Pending (Recompute with merge_gap=None)

- 10 FA target: Pending fresh sweep
- 2.5 FA target: Pending fresh sweep
- 1 FA target: Pending fresh sweep

## Important Notes

1. FA/24h is Temple’s “Total False Alarm Rate” (SEIZ + BCKG combined) for OVERLAP.
2. Native is OVERLAP: our “native” implementation scores OVERLAP, not TAES. See TECHNICAL_DEBT_NATIVE_SCORER.md.
3. Prior figures such as 60.83 (TAES) and 25.01 (OVERLAP) were affected by a non‑standard merge_gap and must not be used.

## Validation Checklist

- [x] Default NEDC OVERLAP verified from primary artifacts
- [x] Native OVERLAP parity with Temple OVERLAP
- [x] SzCORE summary verified via timescoring output
- [ ] TAES default metrics re‑extracted
- [ ] Clinical targets recomputed (10 / 2.5 / 1 FA)
