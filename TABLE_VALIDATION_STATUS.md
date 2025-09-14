# Evaluation Results Table Validation Status

## ✅ VERIFIED ROWS (Senior Spec Ready)

### Default (0.8/5/2.0) - 100% VERIFIED
- **NEDC TAES (Temple)**: 24.71% / 60.83 FA ✅
  - Source: `experiments/eval/baseline/results_default_nedc_binary/results/summary.txt`
  - TAES SCORING SUMMARY section, OVERALL RESULTS
- **NEDC OVERLAP (Temple)**: 45.63% / 25.01 FA ✅
  - Source: Same file, OVERLAP SCORING SUMMARY section
  - Uses "Total False Alarm Rate" (SEIZ + BCKG combined)
- **NEDC OVERLAP (Native)**: 45.63% / 25.01 FA ✅
  - Matches Temple OVERLAP exactly (parity achieved)
- **SzCORE**: 52.35% / 8.46 FA ✅
  - Source: `experiments/eval/baseline/szcore_results/szcore_summary.json`

### 2.5FA (0.93/11/5.0) - 100% VERIFIED
- **NEDC TAES (Temple)**: 4.13% / 38.60 FA ✅
- **NEDC OVERLAP (Temple)**: 11.51% / 2.45 FA ✅
- **NEDC OVERLAP (Native)**: 11.51% / 2.44 FA ✅ (0.01 diff is rounding)
- **SzCORE**: 27.94% / 1.32 FA ✅

### 1FA (0.95/15/7.0) - 100% VERIFIED
- **NEDC TAES (Temple)**: 0.41% / 34.85 FA ✅
- **NEDC OVERLAP (Temple)**: 1.28% / 0.38 FA ✅
- **NEDC OVERLAP (Native)**: 1.28% / 0.38 FA ✅
- **SzCORE**: 17.65% / 0.56 FA ✅

## ❌ NEEDS RERUN

### 10FA (0.88/7/2.5) - INVALID DATA
- **Temple/Native columns**: Currently show default params data (wrong!)
- **SzCORE**: 41.76% / 3.57 FA ✅ (this is correct)
- **ACTION REQUIRED**: Rerun with `--threshold 0.88 --kernel 7 --min_duration_sec 2.5`

## Important Notes

1. **FA/24h Definition**: Temple reports "Total False Alarm Rate" which includes both SEIZ and BCKG label false alarms. This is why OVERLAP shows ~25 FA/24h, not ~14 FA/24h (SEIZ-only).

2. **Native is OVERLAP**: Our "native" implementation is OVERLAP scoring, NOT TAES. See `TECHNICAL_DEBT_NATIVE_SCORER.md` for details.

3. **SzCORE Count**: The note about 340 vs 469 targets is due to different counting methods (SzCORE may merge events differently). Percentages are still comparable.

4. **No .txt Artifacts**: All `.txt` summary files are in `experiments/` which is gitignored. DO NOT stage or commit these.

## Validation Checklist

- [x] Default row metrics verified against source files
- [x] 2.5FA row metrics verified against source files
- [x] 1FA row metrics verified against source files
- [ ] 10FA row - NEEDS RERUN WITH CORRECT PARAMS
- [x] Native OVERLAP achieves parity with Temple OVERLAP
- [x] FA/24h uses Temple's "Total" definition consistently
- [x] Typo "compkrable" fixed to "comparable"
- [x] Added footnote about Native being OVERLAP not TAES
- [x] Added urgent rerun commands for 10FA

## Senior Spec Status

**95% READY** - Table is accurate except for 10FA row which is clearly marked as needing rerun. All other data is verified from primary sources and achieves the accuracy needed for publication/senior review.