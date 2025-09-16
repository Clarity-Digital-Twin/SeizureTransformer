# CORE 1: Scoring Methodologies for Seizure Detection
## The Foundation of Performance Measurement

### Executive Summary
Different scoring methods serve different purposes. There is no "wrong" method - only methods mismatched to their intended use case. Understanding these differences is crucial for interpreting performance claims.

---

## The Scoring Spectrum

```
Most strict                                        Most permissive
    TAES  →  OVERLAP (OVLP / NEDC OVERLAP)  →  SzCORE Any-Overlap
      (temporal precision)         (any-overlap)             (tolerances + merge)
```

Source:
- Picone et al. (Objective Evaluation Metrics) describe OVLP vs TAES and their relative stringency
  (literature/markdown/picone-evaluation/picone-2021-objective-evaluation-metrics.md).
- Our NEDC v6.0.0 summary shows separate OVERLAP and TAES sections
  (evaluation/nedc_eeg_eval/nedc_scoring/output/results/summary.txt).

---

## 1. TAES (Time-Aligned Event Scoring)

### Definition (Picone 2021)
"Time-Aligned Event Scoring (TAES) accounts for the temporal alignment of the hypothesis to the
reference annotation" and computes partial credit per event based on overlap. See:
- literature/markdown/picone-evaluation/picone-2021-objective-evaluation-metrics.md (search: "Time-Aligned Event Scoring (TAES)")

### How TAES tallies errors (per Picone 2021)
- TP contribution: detected overlap duration divided by reference duration
- FN contribution: missed portion of reference divided by reference duration
- FP contribution: inserted (incorrect) duration divided by inserted duration; capped at 1 per event
- Multiple reference events covered by one long hypothesis: all but first are counted as FNs

Repo source passages:
- TAES overview and motivation: lines ~166–185 and ~209 in
  literature/markdown/picone-evaluation/picone-2021-objective-evaluation-metrics.md

### Characteristics
- **Purpose**: Research precision, temporal accuracy assessment
- **Weighting**: Partial credit based on overlap percentage
- **Use Case**: Algorithm development, fine-tuning temporal precision

### Professional Assessment
**Strengths**: Most rigorous metric for temporal accuracy. Provides nuanced performance measurement.
**Limitations**: Perhaps too strict for clinical deployment where any detection might be valuable.
**Context**: Proposed by Picone et al. as improvement over binary scoring, but not widely adopted yet.

---

## 2. OVLP / OVERLAP (Binary Any-Overlap Scoring)

### Definition (Picone 2021)
"OVLP is considered a very permissive way of scoring since any amount of overlap between a reference and
hypothesis event constitutes a true positive."

Repo source passage:
- literature/markdown/picone-evaluation/picone-2021-objective-evaluation-metrics.md (search: "Any-Overlap Method (OVLP)" and
  the sentence containing "very permissive").

### Mathematics
```
If (ref_start < hyp_end) AND (hyp_start < ref_end):
    Score = 1.0 (True Positive)
Else:
    Score = 0.0 (False Negative or False Positive)
```

### Characteristics
- **Purpose**: Clinical standard for TUSZ evaluation
- **Weighting**: Binary - any overlap counts fully
- **Use Case**: Widely used in literature, balanced approach

### Professional Assessment
**Strengths**: Simple, interpretable, widely understood. Standard practice for TUSZ.
**Limitations**: Doesn't reward temporal precision. Brief overlaps count same as perfect alignment.
**Context**: De facto standard in seizure detection literature; widely used for TUSZ. Our native implementation
matches Temple’s OVERLAP results exactly (see below).

---

## 3. NEDC OVERLAP (Temple’s Implementation of OVLP)

### Definition
Temple University’s official implementation of OVLP within the NEDC framework.

### Characteristics
- **Purpose**: Clinical evaluation standard for TUSZ
- **Implementation**: Part of NEDC v6.0.0 software suite
- **Validation**: Matched to TUSZ annotation methodology

### Professional Assessment
**Strengths**: Designed by same team that created TUSZ. Gold standard for this dataset.
**Context**: When papers say "evaluated on TUSZ", this is what should be used.
**Parity note**: Produces identical results to our native OVLP implementation in this repo.

Repo sources:
- NEDC outputs include a dedicated OVERLAP section: evaluation/nedc_eeg_eval/nedc_scoring/output/results/summary.txt
  (search: "NEDC OVERLAP SCORING SUMMARY").
- Our native scorer uses `OverlapScorer` and writes a compatible summary: evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py
  (search: "native-overlap", "OverlapScorer").
- Identical numbers for NEDC OVERLAP and Python OVERLAP are documented in
  docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md.

---

## 4. SzCORE Any-Overlap (with Tolerances)

### Definition (SzCORE 2024)
Any-overlap scoring with 30-second pre-ictal tolerance, 60-second post-ictal tolerance, and merging of events
separated by less than 90 seconds.

Repo source passages:
- literature/markdown/SzCORE/SzCORE.md (lines ~544–559: pre-ictal/post-ictal tolerances and 90s merge rule).

### Mathematics
```
Extended_ref = [ref_start - 30s, ref_end + 60s]
If events < 90s apart: merge into single event
Then apply any-overlap scoring
```

### Characteristics
- **Purpose**: Clinical early warning systems
- **Tolerances**: -30s/+60s around ground truth
- **Merging**: Events <90s apart become one
- **Use Case**: EpilepsyBench standard, clinical deployment

### Professional Assessment
**Strengths**: Clinically motivated - early warning valuable. Reduces alarm fatigue via merging.
**Limitations**: Very permissive - might mask poor temporal precision.
**Context**: Designed for real-world deployment where early detection saves lives.

---

## 5. Other NEDC v6.0.0 Summaries Present in Our Runs

- DP ALIGNMENT (sequence alignment–based summary)
- EPOCH (sample/epoch-based confusion matrix and rates)
- INTER-RATER AGREEMENT (Kappa)

Repo source:
- evaluation/nedc_eeg_eval/nedc_scoring/output/results/summary.txt contains sections:
  "NEDC DP ALIGNMENT SCORING SUMMARY", "NEDC EPOCH SCORING SUMMARY",
  "NEDC OVERLAP SCORING SUMMARY", "NEDC TAES SCORING SUMMARY",
  and "NEDC INTER-RATER AGREEMENT SUMMARY".

---

## Critical Insights

### The Scoring Impact (documented in-repo)
Same predictions on TUSZ (paper defaults) yield:
- NEDC OVERLAP: 26.89 FA/24h (SEIZ-only)
- Python OVERLAP: 26.89 FA/24h (parity)
- SzCORE: 8.59 FA/24h

Ratios for context:
- OVERLAP vs SzCORE: 26.89 / 8.59 ≈ 3.1×
- TAES is stricter than OVERLAP and yields higher FA/24h; see canonical table for exact values.

Repo source:
- docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md (canonical 4×3 results; no merge_gap).

### Why This Matters
1. **Clinical Deployment**: 10 FA/24h threshold determines viability
2. **Literature Comparison**: Papers using different scoring aren't comparable
3. **Benchmark Gaming**: Cherry-picking favorable scoring inflates performance

### Professional Framing
- **Not "Cheating"**: Different valid perspectives on what constitutes detection
- **Not "Wrong"**: Each serves legitimate use case
- **Key Issue**: Lack of transparency about which method used

---

## Recommendations for Fair Reporting

### Best Practice
Always report multiple scoring methods:
```
"We achieve 45.63% sensitivity @ 26.89 FA/24h (NEDC OVERLAP SEIZ)
and 52.35% sensitivity @ 8.59 FA/24h (SzCORE)"
```

Repo source for the above numbers:
- docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md (Default operating point section).

### Context Matters
- Training dataset → Use its standard scorer
- Clinical deployment → Consider tolerances
- Research comparison → Use same scorer

### The Golden Rule
**Transparency above all. Let readers judge based on full information.**

---

## Quote Bank for Paper

### On OVLP Being Permissive
> "OVLP is considered a very permissive way of scoring..." — Picone 2021
  (literature/markdown/picone-evaluation/picone-2021-objective-evaluation-metrics.md; search: "Any-Overlap Method (OVLP)").

### On TAES Motivation
> "[We] introduce... Time-Aligned Event Scoring (TAES), that accounts for the temporal alignment of the hypothesis to the reference annotation." — Picone 2021
  (literature/markdown/picone-evaluation/picone-2021-objective-evaluation-metrics.md; search: "Time-Aligned Event Scoring (TAES)").

### On Clinical Tolerances
> "We advise a 30 seconds pre-ictal tolerance... a 60 seconds post-ictal tolerance... [and] merging events separated by less than 90 seconds" — SzCORE 2024
  (literature/markdown/SzCORE/SzCORE.md lines ~544–559).

### On Standardization Need
> "The lack of standardized evaluation metrics hampers progress" - Ward 2019

---

## How to Write About This Professionally

### DO Say
- "Different scoring methods serve different clinical and research priorities"
- "SzCORE's tolerances reflect real-world deployment needs"
- "NEDC provides dataset-matched evaluation for TUSZ"

### DON'T Say
- "SzCORE is too permissive" (judgmental)
- "TAES is unnecessarily strict" (dismissive)
- "Papers using SzCORE are inflating numbers" (accusatory)

### Cutting but Fair Language
- "The ~3.1× difference in reported false alarms (OVERLAP vs SzCORE) stems from scoring methodology"
- "Without transparent reporting of scoring methods, performance claims lack context"
- "Clinical viability conclusions depend critically on evaluation standard chosen"

---

## Pointers to Code and Outputs in This Repo
- NEDC integration and native OVERLAP scorer:
  - evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py (search: "native-overlap", "OverlapScorer")
  - evaluation/nedc_eeg_eval/nedc_scoring/convert_predictions.py (CSV_bi conversion)
- Example NEDC summary with all sections (DP ALIGNMENT, EPOCH, OVERLAP, TAES, IRA):
  - evaluation/nedc_eeg_eval/nedc_scoring/output/results/summary.txt
- Canonical, merge_gap-free results (4 scorers × 3 operating points):
  - docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md
