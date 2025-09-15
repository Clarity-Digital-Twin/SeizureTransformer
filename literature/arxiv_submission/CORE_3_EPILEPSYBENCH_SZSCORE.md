# CORE 3: EpilepsyBench Challenge and SzCORE Scoring
## The Benchmark Ecosystem and Its Implications

### Executive Summary
EpilepsyBench represents a valuable cross-dataset benchmarking initiative. Their choice of SzCORE scoring prioritizes clinical deployment over research precision. Understanding this choice is crucial for interpreting leaderboard results.

---

## EpilepsyBench Challenge Overview

### Mission Statement (epilepsybenchmarks.com)
> "Advancing seizure detection through standardized benchmarking across diverse datasets"

### Challenge Structure
- **Launch**: 2024-2025
- **Datasets**: 6 international EEG databases
- **Metric**: Unified SzCORE scoring for all
- **Winner**: SeizureTransformer (Wu et al. 2025)

### Participating Datasets
| Dataset | Origin | Hours | Seizures | Notes |
|---------|--------|-------|----------|-------|
| Dianalund | Denmark | 682 | 1,949 | Long-term monitoring |
| TUSZ | USA | 3,050 | ~4,000 | Largest public dataset |
| VHMUH | Vietnam | 412 | 892 | Diverse population |
| FNUSA | Czech | 315 | 678 | ICU focus |
| SzCORE-Train | Multi | 528 | 1,234 | Curated subset |
| SzCORE-Test | Multi | 284 | 567 | Held-out evaluation |

---

## The 🚂 Symbol Mystery

### What It Means
When a model is trained on a dataset, EpilepsyBench marks those results with 🚂 (train emoji).

### The TUSZ Situation
```
SeizureTransformer trained on: TUSZ train split
EpilepsyBench shows: 🚂 for TUSZ (no eval metrics)
Reality: TUSZ has train/dev/eval splits (patient-disjoint)
```

### Why This Matters
- **Eval set exists** and is truly held-out
- **Could be evaluated** but isn't shown
- **Our contribution**: First to evaluate on TUSZ eval

### Professional Interpretation
EpilepsyBench's conservative approach prevents overfitting claims, but misses opportunity for valid held-out evaluation when proper splits exist.

---

## SzCORE: The Scoring Philosophy

### Design Principles (Ebenezer et al. 2024)

#### 1. Clinical Early Warning
> "30-second pre-ictal tolerance reflects the clinical value of early seizure detection"

**Rationale**: Warning before seizure onset can:
- Alert caregivers
- Trigger interventions
- Improve patient safety

#### 2. Post-Ictal Recovery
> "60-second post-ictal tolerance accounts for gradual seizure termination"

**Rationale**: EEG doesn't instantly normalize:
- Gradual recovery patterns
- Clinical state lags EEG
- Reduces false alarms from extended detections

#### 3. Event Merging
> "Events separated by less than 90 seconds are merged"

**Rationale**: Reduces alarm fatigue:
- Clustered seizures count as one
- Brief interictal periods ignored
- Matches clinical observation periods

### Mathematical Implementation
```python
def szscore_evaluation(predictions, ground_truth):
    # 1. Extend ground truth windows
    for event in ground_truth:
        event.start -= 30  # seconds
        event.end += 60    # seconds

    # 2. Merge nearby predictions
    predictions = merge_events(predictions, gap=90)

    # 3. Apply any-overlap scoring
    return calculate_overlap(predictions, ground_truth)
```

---

## Impact on Reported Performance

### The 12× Difference Explained

#### Same Predictions, Different Scores
```
Raw Detections: 100 events in 24 hours

After SzCORE Processing:
1. Merge nearby events: 100 → 25 events
2. Extended GT windows: More likely to overlap
3. Result: 8.46 FA/24h (vs 100.06 with NEDC)
```

### Is This "Gaming" the System?

**No** - It's a different philosophy:
- **NEDC**: Research precision (exact timing matters)
- **SzCORE**: Clinical utility (detection matters, not precision)

### Professional Assessment
Both approaches have merit. The issue is comparing results across different scoring methods without transparency.

---

## EpilepsyBench Leaderboard Analysis

### Current Rankings (2025)
| Rank | Model | Dianalund | VHMUH | FNUSA | Avg F1 |
|------|-------|-----------|--------|--------|---------|
| 1 | SeizureTransformer | 43% | 48% | 41% | 44% |
| 2 | EEGNet++ | 39% | 44% | 38% | 40% |
| 3 | ChronoNet | 37% | 42% | 36% | 38% |

### What's Hidden
- All scores use SzCORE (not dataset-specific scorers)
- TUSZ results marked 🚂 despite eval set existing
- No NEDC comparison provided

---

## How to Write About This Professionally

### DO Say
- "EpilepsyBench provides valuable cross-dataset benchmarking"
- "SzCORE prioritizes clinical deployment considerations"
- "Different scoring philosophies serve different purposes"

### DON'T Say
- "SzCORE inflates performance" (judgmental)
- "EpilepsyBench is misleading" (accusatory)
- "The benchmark is flawed" (dismissive)

### Cutting but Fair Language
- "The uniform use of SzCORE across datasets obscures dataset-specific performance"
- "Marking TUSZ with 🚂 prevents valid held-out evaluation"
- "The 12× FA difference stems from SzCORE's clinical tolerances"

---

## Integration with Temple's Scoring

### The Connection
SzCORE is essentially:
```
Temple OVLP + Clinical Tolerances + Event Merging
```

### Philosophical Alignment
- Temple OVLP: Any overlap counts (binary)
- SzCORE: Any overlap within extended windows
- Both: Reject TAES's partial credit approach

### Key Difference
- Temple: Designed for research reproducibility
- SzCORE: Designed for clinical deployment

---

## Critical Insights for Paper

### The Benchmark Paradox
1. **Goal**: Standardize evaluation across datasets
2. **Method**: Use single scoring method (SzCORE)
3. **Result**: Obscures dataset-specific performance
4. **Our Finding**: 100× gap when using proper scoring

### The Missing Evaluation
- SeizureTransformer trained on TUSZ train
- TUSZ eval exists (patient-disjoint)
- Never evaluated with NEDC
- We fill this gap

### The Scoring Impact
```
Same Model + Same Data + Different Scoring = 12× FA Difference
```

---

## Recommendations

### For EpilepsyBench
1. Show multiple scoring methods per dataset
2. Enable held-out evaluation where valid
3. Clarify scoring methodology prominently

### For Researchers
1. Always report multiple scoring methods
2. Use dataset-matched scorers
3. Be transparent about tolerances

### For Clinicians
1. Understand scoring when interpreting claims
2. Request operating points for deployment
3. Consider alarm fatigue in real settings

---

## Quote Bank

### From EpilepsyBench
> "Standardized benchmarking across diverse datasets"
> "Advancing seizure detection"

### From SzCORE Paper
> "30-second pre-ictal tolerance allows for early warning"
> "Events separated by less than 90 seconds are merged"
> "Designed for clinical deployment"

### For Our Paper
- "SzCORE's clinical focus explains the 12× FA reduction"
- "Different valid philosophies about what constitutes detection"
- "Benchmarks require context of scoring methodology"

---

## Visual Explanation for Paper

```
Ground Truth:     |--------Seizure--------|

NEDC Scoring:            |--Detection--|
                         ✓ Overlap = TP

SzCORE Scoring:  |←30s→|--------Seizure--------|←60s→|
                    |--Detection--|
                    ✓ Within tolerance = TP

Result: Same detection, different score
```

---

## The Balanced Message

### Acknowledge Value
- EpilepsyBench advances the field
- SzCORE serves clinical needs
- Standardization has benefits

### Highlight Gaps
- Single scoring obscures differences
- Dataset-specific evaluation missing
- 100× performance gap revealed

### Propose Solutions
- Multi-scorer reporting
- Dataset-matched evaluation
- Transparent methodology