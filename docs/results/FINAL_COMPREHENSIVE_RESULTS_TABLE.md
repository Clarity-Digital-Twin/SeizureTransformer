# FINAL COMPREHENSIVE RESULTS TABLE - NO MERGE GAP
**All results WITHOUT merge_gap parameter (honest, real numbers)**

## Understanding the Scoring Methods

Each scoring method serves different purposes in seizure detection evaluation:

1. **NEDC Temple TAES** - Most strict (Time-Aligned Event Scoring)
   - Proposed by Picone et al. (2021) as improved metric
   - Weights detections by percentage of overlap
   - Provides most rigorous temporal accuracy assessment

2. **NEDC Temple OVERLAP** - Common practice (Any-overlap scoring)
   - Widely used in TUSZ evaluations
   - Any temporal overlap counts as detection
   - **Our tuning target** - balanced for practical use

3. **Python OVERLAP** - Our implementation
   - Validates parity with Temple's NEDC binary
   - Identical results to NEDC OVERLAP

4. **SzCORE Event** (Any-Overlap + tolerances) - EpilepsyBench standard (most permissive)
   - Includes 30s pre-ictal and 60s post-ictal tolerances
   - Merges events <90s apart
   - Designed for clinical applications where early warning is valuable

---

## DEFAULT PARAMETERS
**Settings:** threshold=0.8, kernel_size=5, min_duration=2.0
**Source:** Paper defaults from Wu et al. 2025

| Scoring Method | Sensitivity (%) | False Alarms/24h |
|---|---:|---:|
| **NEDC Temple TAES** | 65.21 | 136.73 |
| **NEDC Temple OVERLAP** | 45.63 | 26.89 |
| **Python OVERLAP** | 45.63 | 26.89 |
| **SzCORE Event** | 52.35 | 8.59 |

---

## 10 FA/24h TARGET
**Settings:** threshold=0.88, kernel_size=5, min_duration=3.0
**Target:** ≤10 FA/24h

| Scoring Method | Sensitivity (%) | False Alarms/24h | Meets Target |
|---|---:|---:|:---:|
| **NEDC Temple TAES** | 60.45 | 83.88 | ❌ |
| **NEDC Temple OVERLAP** | 33.90 | 10.27 | ❌ (≈10.3) |
| **Python OVERLAP** | 33.90 | 10.27 | ❌ (≈10.3) |
| **SzCORE Event** | 40.59 | 3.36 | ✅ |

---

## 2.5 FA/24h TARGET
**Settings:** threshold=0.95, kernel_size=5, min_duration=5.0
**Target:** ≤2.5 FA/24h

| Scoring Method | Sensitivity (%) | False Alarms/24h | Meets Target |
|---|---:|---:|:---:|
| **NEDC Temple TAES** | 18.12 | 10.64 | ❌ |
| **NEDC Temple OVERLAP** | 14.50 | 2.05 | ✅ |
| **Python OVERLAP** | 14.50 | 2.05 | ✅ |
| **SzCORE Event** | 19.71 | 0.75 | ✅ |

---

## 1 FA/24h TARGET
**Status:** NOT TESTED (would require extreme parameters that likely yield <5% sensitivity)

---

## KEY FINDINGS

### Performance Under Different Standards
- **NEDC OVERLAP (Temple):**
  - Default (paper): 45.63% sens, 26.89 FA/24h (SEIZ)
  - 10 FA target: ≈10.27 FA/24h at 33.90% sens (near target but <50% sens)
  - 2.5 FA target: 2.05 FA/24h at 14.50% sens (meets FA target, very low sens)

- **NEDC TAES (Temple, time-aligned):**
  - Default: 65.21% sens, 136.73 FA/24h
  - 10 FA target setting: 60.45% sens, 83.88 FA/24h (does not meet FA target)
  - 2.5 FA target setting: 18.12% sens, 10.64 FA/24h (does not meet FA target)

- **SzCORE Event (EpilepsyBench):** Meets both FA targets with higher sensitivity than OVERLAP at the same settings (e.g., 3.36 FA @ 40.59% and 0.75 FA @ 19.71%).

### Important Context
- Different scoring methods serve different clinical and research needs
- SzCORE Event's permissiveness reflects real-world clinical priorities (early warning)
- NEDC's stricter scoring reflects research priorities (temporal precision)
- **Neither approach is "wrong" - they measure different aspects of performance**

Note on FA/24h: For NEDC and Python OVERLAP rows, FA/24h reported here is SEIZ-only (primary), consistent with our reporting policy; NEDC’s “Total False Alarm Rate” (SEIZ+BCKG) is also available in raw summaries. SzCORE Event FA/24h follows its event-based definition.

### Methodology Note
We tuned parameters using NEDC OVERLAP (the common practice for TUSZ) and evaluated across all metrics for transparency. This reveals how scoring methodology significantly impacts reported performance.

---

## Data Sources
- Evaluation split: TUSZ v2.0.3 eval (865 files)
- Model: SeizureTransformer (authors' pretrained weights)
- Location: `/experiments/eval/baseline/CLEAN_NO_MERGE/`
- Generated: September 15, 2025
 
<!-- moved to docs/results -->
