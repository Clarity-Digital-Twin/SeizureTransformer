# 📊 FINAL COMPREHENSIVE SCORES - COMPLETE TRUTH

**CRITICAL**: Dev vs Eval splits have different FA rates!
- **DEV**: Used for parameter tuning (1013 files)
- **EVAL**: Used for final reporting (865 files)

---

## 1️⃣ DEFAULT CONFIGURATION (Paper: thr=0.8, kernel=5, min_dur=2.0, gap=0)

### ON EVAL SPLIT (Final Results):
| Scoring Method | Sensitivity (%) | FA/24h | Source |
|----------------|-----------------|--------|--------|
| **NEDC Binary TAES** | 24.15% | 27.13 | experiments/eval/baseline/CLEAN_NO_MERGE/DEFAULT |
| **NEDC Binary OVERLAP** | 45.63% | 100.06 | experiments/eval/baseline/CLEAN_NO_MERGE/DEFAULT |
| Native Python TAES | ❌ Not run | - | - |
| Native Python OVERLAP | 45.63% | 100.06 | experiments/eval/baseline/paper_default_nedc |

### ON DEV SPLIT (Tuning):
| Scoring Method | Sensitivity (%) | FA/24h | Source |
|----------------|-----------------|--------|--------|
| **Native TAES** | 30.51% | 107.29 | experiments/dev/baseline/sweeps CSV |

**⚠️ ISSUE**: Why is eval FA so much lower? Need to investigate!

---

## 2️⃣ 10 FA/24h TARGET (thr=0.95, kernel=5, min_dur=2.0, gap=None)

### FROM DEV SWEEP:
| Scoring Method | Sensitivity (%) | FA/24h | Status |
|----------------|-----------------|--------|--------|
| Native TAES | 13.67% | 9.97 | ✅ From sweep CSV |
| NEDC Binary TAES | 8.64% | 6.40 | CLEAN_NO_MERGE/10FA |
| NEDC Binary OVERLAP | 23.45% | 39.50 | CLEAN_NO_MERGE/10FA |
| Native OVERLAP | ❌ | - | Need to run |

---

## 3️⃣ 2.5 FA/24h TARGET (thr=0.95, kernel=11, min_dur=8.0, gap=None)

### FROM DEV SWEEP:
| Scoring Method | Sensitivity (%) | FA/24h | Status |
|----------------|-----------------|--------|--------|
| Native TAES | 8.19% | 2.48 | ✅ From sweep CSV |
| NEDC Binary TAES | 4.07% | 1.51 | CLEAN_NO_MERGE/2.5FA |
| NEDC Binary OVERLAP | 11.51% | 8.09 | CLEAN_NO_MERGE/2.5FA |
| Native OVERLAP | ❌ | - | Need to run |

---

## 4️⃣ 1 FA/24h TARGET

**Cannot achieve** - Best we got was 2.48 FA/24h (same as 2.5 FA target)

---

## ACTION ITEMS

1. ✅ We have DEFAULT scores (but confusing FA discrepancy)
2. ❌ Need to run tuned configs with all 4 scoring methods
3. ❌ Need to resolve why eval FA is so much lower than dev
4. ❌ No SzCORE scores at all (different scoring system)

---

## THE REAL NUMBERS WE SHOULD REPORT

**For the README (EVAL split, paper defaults):**
- NEDC TAES: 24.15% @ 27.13 FA/24h (SEIZ label)
- NEDC OVERLAP: 45.63% @ 100.06 FA/24h (SEIZ label)

**Something is WRONG - these FA rates are 10x lower than expected!**
