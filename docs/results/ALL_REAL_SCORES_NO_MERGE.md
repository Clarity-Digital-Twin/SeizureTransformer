# ALL REAL SCORES - NO MERGE GAP (HONEST NUMBERS)

Authoritative table: `FINAL_COMPREHENSIVE_RESULTS_TABLE.md` (4 scoring methods × 3 operating points). This file mirrors those numbers in a compact view.

## DEFAULT (thr=0.8, kernel=5, min_dur=2.0)

| Scoring Method | Sensitivity | FA/24h |
|----------------|-------------|--------|
| NEDC Binary TAES | 24.15% | 137.53 |
| NEDC Binary OVERLAP | 45.63% | 100.06 |
| Native Python OVERLAP | 45.63% | 100.06 |
| SzCORE | 52.35% | 8.46 |

## 10 FA TARGET (thr=0.95, kernel=5, min_dur=2.0)

| Scoring Method | Sensitivity | FA/24h | Meets Target? |
|----------------|-------------|--------|---------------|
| NEDC Binary TAES | 8.64% | 34.04 | ❌ NO |
| NEDC Binary OVERLAP | 23.45% | 39.50 | ❌ NO |
| Native Python OVERLAP | 23.45% | 39.50 | ❌ NO |
| SzCORE | 29.12% | 1.32 | ✅ YES |

## 2.5 FA TARGET (thr=0.95, kernel=11, min_dur=8.0)

| Scoring Method | Sensitivity | FA/24h | Meets Target? |
|----------------|-------------|--------|---------------|
| NEDC Binary TAES | 4.07% | 8.01 | ❌ NO |
| NEDC Binary OVERLAP | 11.51% | 8.09 | ❌ NO |
| Native Python OVERLAP | 11.51% | 8.09 | ❌ NO |
| SzCORE | 16.47% | 0.56 | ✅ YES |

## SUMMARY:
- **NEDC (Clinical Standard)**: CANNOT meet 10 or 2.5 FA targets
- **SzCORE (EpilepsyBench)**: CAN meet targets (but it's more lenient)
- **Reality**: Model needs ~40 FA/24h for reasonable sensitivity with NEDC
