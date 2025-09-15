# ALL REAL SCORES - NO MERGE GAP (HONEST NUMBERS)

Authoritative table: `FINAL_COMPREHENSIVE_RESULTS_TABLE.md` (4 scoring methods × 3 operating points). This file mirrors those numbers in a compact view.

## DEFAULT (thr=0.8, kernel=5, min_dur=2.0)

| Scoring Method | Sensitivity | FA/24h |
|----------------|-------------|--------|
| NEDC Binary TAES | 65.21% | 136.73 |
| NEDC Binary OVERLAP | 45.63% | 26.89 |
| Native Python OVERLAP | 45.63% | 26.89 |
| SzCORE | 52.35% | 8.59 |

## 10 FA TARGET (thr=0.88, kernel=5, min_dur=3.0)

| Scoring Method | Sensitivity | FA/24h | Meets Target? |
|----------------|-------------|--------|---------------|
| NEDC Binary TAES | 60.45% | 83.88 | ❌ NO |
| NEDC Binary OVERLAP | 33.90% | 10.27 | ❌ NO (≈10.3) |
| Native Python OVERLAP | 33.90% | 10.27 | ❌ NO (≈10.3) |
| SzCORE | 40.59% | 3.36 | ✅ YES |

## 2.5 FA TARGET (thr=0.95, kernel=5, min_dur=5.0)

| Scoring Method | Sensitivity | FA/24h | Meets Target? |
|----------------|-------------|--------|---------------|
| NEDC Binary TAES | 18.12% | 10.64 | ❌ NO |
| NEDC Binary OVERLAP | 14.50% | 2.05 | ✅ YES |
| Native Python OVERLAP | 14.50% | 2.05 | ✅ YES |
| SzCORE | 19.71% | 0.75 | ✅ YES |

## SUMMARY:
- **NEDC (Clinical Standard)**: 10 FA is near-achievable at ~34% sens; 2.5 FA is achievable at ~14.5% sens (low). TAES does not meet FA targets at corresponding settings.
- **SzCORE (EpilepsyBench)**: Meets both targets with higher sensitivity than OVERLAP at those settings (more permissive by design).
- **Reality**: Clinical viability (≤10 FA and ≥50% sens) is not achieved at any setting.
