# CORE 1: Scoring Methodologies for Seizure Detection
## The Foundation of Performance Measurement

### Executive Summary
Different scoring methods serve different purposes. There is no "wrong" method - only methods mismatched to their intended use case. Understanding these differences is crucial for interpreting performance claims.

---

## The Scoring Spectrum

```
Most Strict                                                Most Permissive
    TAES ← OVLP ← NEDC OVERLAP ← SzCORE Any-Overlap
(Research)    (Clinical Standard)      (Early Warning)
```

---

## 1. TAES (Time-Aligned Event Scoring)

### Definition (Picone 2021)
> "TAES weights the decision based on the percentage of overlap between reference and hypothesis events."

### Mathematics
```
Score = (overlap_duration / max(ref_duration, hyp_duration)) × 100%
```

### Characteristics
- **Purpose**: Research precision, temporal accuracy assessment
- **Weighting**: Partial credit based on overlap percentage
- **Use Case**: Algorithm development, fine-tuning temporal precision

### Professional Assessment
**Strengths**: Most rigorous metric for temporal accuracy. Provides nuanced performance measurement.
**Limitations**: Perhaps too strict for clinical deployment where any detection might be valuable.
**Context**: Proposed by Picone et al. as improvement over binary scoring, but not widely adopted yet.

---

## 2. OVLP/OVERLAP (Binary Any-Overlap Scoring)

### Definition (Picone 2021)
> "OVLP is considered a very permissive way of scoring since any amount of overlap between a reference and hypothesis event constitutes a true positive."

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
**Context**: De facto standard in seizure detection literature. What most papers report.

---

## 3. NEDC OVERLAP (Temple's Implementation)

### Definition
Temple University's specific implementation of OVLP scoring within NEDC framework.

### Characteristics
- **Purpose**: Clinical evaluation standard for TUSZ
- **Implementation**: Part of NEDC v6.0.0 software suite
- **Validation**: Matched to TUSZ annotation methodology

### Professional Assessment
**Strengths**: Designed by same team that created TUSZ. Gold standard for this dataset.
**Context**: When papers say "evaluated on TUSZ", this is what should be used.
**Note**: Produces identical results to generic OVLP but within NEDC's comprehensive framework.

---

## 4. SzCORE Any-Overlap (with Tolerances)

### Definition (Ebenezer 2024)
> "Any-overlap scoring with 30-second pre-ictal tolerance, 60-second post-ictal tolerance, and merging of events separated by less than 90 seconds."

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

## 5. Other Scoring Methods in NEDC v6.0.0

### IEC (Inter-Event Correlation)
- Correlation-based scoring
- Less commonly used

### AAM (Affiliation Marker)
- Assignment-based scoring
- Research applications

### Note on NEDC Suite
NEDC v6.0.0 ships with all 5 scoring modalities, but OVLP and TAES are most relevant for our analysis.

---

## Critical Insights

### The 12× Difference
Same predictions on TUSZ yield:
- NEDC TAES: 144.28 FA/24h
- NEDC OVERLAP: 100.06 FA/24h
- SzCORE: 8.46 FA/24h

**This 17× spread is from scoring alone, not model performance.**

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
"We achieve 45.63% sensitivity @ 100.06 FA/24h (NEDC OVERLAP)
and 52.35% sensitivity @ 8.46 FA/24h (SzCORE)"
```

### Context Matters
- Training dataset → Use its standard scorer
- Clinical deployment → Consider tolerances
- Research comparison → Use same scorer

### The Golden Rule
**Transparency above all. Let readers judge based on full information.**

---

## Quote Bank for Paper

### On OVLP Being Permissive
> "OVLP is considered a very permissive way of scoring" - Picone 2021

### On TAES Motivation
> "TAES was proposed as an alternative to address limitations" - Picone 2021

### On Clinical Tolerances
> "30-second pre-ictal tolerance allows for early warning systems" - SzCORE

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
- "The 12× difference in reported false alarms stems entirely from scoring methodology"
- "Without transparent reporting of scoring methods, performance claims lack context"
- "Clinical viability conclusions depend critically on evaluation standard chosen"