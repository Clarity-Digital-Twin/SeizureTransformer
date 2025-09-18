# Final Scoring Clarification for Manuscript

## What We Report (All Event-Based)

We report THREE event-based scoring methods, from strictest to most permissive:

1. **NEDC TAES** (Time-Aligned Event Scoring)
   - Event-based with **fractional/partial credit**
   - Strictest method
   - Default: 65.21% sensitivity @ 136.73 FA/24h

2. **NEDC OVERLAP** (Any-Overlap)
   - Event-based with **binary scoring** (no partial credit)
   - Temple's standard for TUSZ
   - Default: 45.63% sensitivity @ 26.89 FA/24h

3. **SzCORE Event** (Any-Overlap + Clinical Tolerances)
   - Event-based with **binary scoring + tolerances**
   - Adds -30s pre-ictal, +60s post-ictal windows
   - Most permissive (EpilepsyBench standard)
   - Default: 52.35% sensitivity @ 8.59 FA/24h

## What We DON'T Report

- **SzCORE Sample-based (Epoch)**: 1 Hz sample comparison (≈ NEDC EPOCH)
- **NEDC EPOCH**: Per-second duration-weighted scoring
- These are not reported because they're not clinically interpretable

## Why the 15.9× Spread?

The 15.9× difference in FA rates (136.73/8.59) between NEDC TAES and SzCORE Event reflects:

1. **TAES's fractional credit**: Penalizes partial overlaps
2. **SzCORE's clinical tolerances**: Forgives timing misalignments
3. Both applied to **identical predictions**

## Figure Labels Are Correct

- Figure 1: "SzCORE Event" ✓
- Figure 2: "SzCORE Event" ✓
- Figure 3: "SzCORE Event" ✓
- Figure 4: References NEDC OVERLAP (for parameter analysis) ✓

## Manuscript Text Is Accurate

The Methods section correctly states:
> "SzCORE Any-Overlap extends binary scoring with clinical tolerances..."

This accurately describes the SzCORE Event mode we report.

## Key Takeaway

We compare THREE different EVENT-BASED philosophies:
- **TAES**: How much temporal alignment? (fractional)
- **OVERLAP**: Did events overlap at all? (binary)
- **SzCORE Event**: Did events overlap within clinical tolerances? (binary + forgiving)

This comparison demonstrates how evaluation philosophy, not model improvements, drives reported performance.