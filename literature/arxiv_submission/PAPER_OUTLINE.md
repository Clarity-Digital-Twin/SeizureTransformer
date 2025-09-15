# SeizureTransformer on TUSZ: A 100× False Alarm Reality Check
## Revealing the Impact of Dataset-Matched Clinical Scoring Standards

### Core Narrative Arc
**The Hook**: State-of-the-art model claims 1 FA/24h, but first clinical evaluation reveals 100× higher false alarms
**The Investigation**: Systematic evaluation using Temple's NEDC v6.0.0 clinical standard
**The Discovery**: Scoring methodology alone accounts for 12× difference in reported performance
**The Contribution**: First reproducible NEDC evaluation pipeline + comprehensive operating points for clinical deployment

---

## Paper Structure

### Title Options
1. "SeizureTransformer Meets Clinical Reality: A 100× False Alarm Gap on TUSZ"
2. "When Benchmarks Hide Reality: SeizureTransformer's 100-fold False Alarm Gap"
3. "The Scoring Paradox: How SeizureTransformer Achieves 1 or 100 FA/24h on the Same Data"

### Abstract (250 words)
- **Problem**: SeizureTransformer won EpilepsyBench 2025 with 1 FA/24h, but no clinical evaluation exists
- **Method**: First evaluation using Temple's NEDC v6.0.0 on TUSZ v2.0.3 (865 files, 469 seizures)
- **Finding**: 100.06 FA/24h with NEDC vs 8.46 FA/24h with SzCORE (same predictions!)
- **Impact**: Scoring methodology alone creates 12× performance difference
- **Contribution**: Open-source evaluation pipeline + operating points for clinical deployment

### 1. Introduction
#### 1.1 The Clinical Deployment Gap
- FDA requirements: <10 FA/24h for viable clinical tools
- Current state: Models report stellar benchmarks but fail in hospitals
- The problem: Inconsistent evaluation standards across datasets

#### 1.2 The SeizureTransformer Success Story
- Won EpilepsyBench 2025 Challenge
- Claims 37% sensitivity @ 1 FA/24h on Dianalund
- Trained on TUSZ but never evaluated on it properly

#### 1.3 Our Investigation
- First to use Temple's NEDC v6.0.0 (clinical gold standard)
- Systematic comparison of scoring methodologies
- Reproducible pipeline for community

### 2. Background
#### 2.1 The TUSZ Dataset and NEDC Scoring
- Temple University Hospital EEG Seizure Corpus
- 3,050 hours training, 127.6 hours held-out eval
- NEDC: Designed specifically for TUSZ annotations

#### 2.2 The EpilepsyBench Challenge and SzCORE
- Cross-dataset benchmarking initiative
- SzCORE: "Any-Overlap" with 30s pre/60s post tolerances
- Designed for clinical early warning, not temporal precision

#### 2.3 The Scoring Spectrum
```
Most Permissive                                     Most Strict
SzCORE ← NEDC OVERLAP ← NEDC TAES
(Clinical)    (Research)     (Aspirational)
```

### 3. Methods
#### 3.1 Evaluation Pipeline
- Model: Wu et al.'s pretrained SeizureTransformer
- Dataset: TUSZ v2.0.3 eval split (patient-disjoint)
- Scorers: NEDC v6.0.0 binaries + Python reimplementation

#### 3.2 Parameter Tuning Protocol
- Dev set: TUSZ dev (1,013 files)
- Target: NEDC OVERLAP (balanced, widely used)
- Grid search: threshold × kernel_size × min_duration

#### 3.3 Multi-Scorer Validation
- Same predictions → 4 scoring methods
- NEDC TAES, NEDC OVERLAP, Python OVERLAP, SzCORE
- Reveals scoring impact independent of model

### 4. Results
#### 4.1 The 100× Gap
| Config | NEDC OVERLAP | SzCORE | Gap |
|--------|-------------|---------|-----|
| Paper defaults | 100.06 FA/24h | 8.46 FA/24h | 12× |
| vs Dianalund claim | 100.06 FA/24h | 1 FA/24h | 100× |

#### 4.2 Operating Points for Clinical Deployment
- 10 FA/24h target: Cannot achieve with NEDC (best: 39.50 FA)
- 2.5 FA/24h target: Cannot achieve with NEDC (best: 8.09 FA)
- 1 FA/24h target: Would require <5% sensitivity

#### 4.3 The Scoring Impact
- NEDC TAES: 24.15% sens @ 144.28 FA/24h
- NEDC OVERLAP: 45.63% sens @ 100.06 FA/24h
- SzCORE: 52.35% sens @ 8.46 FA/24h
- **Same predictions, 17× FA difference!**

### 5. Discussion
#### 5.1 Why This Matters
- Hospitals use NEDC for TUSZ-trained models
- EpilepsyBench uses SzCORE for all datasets
- Apples-to-oranges comparisons mislead the field

#### 5.2 Neither Scoring is "Wrong"
- NEDC: Optimized for research precision
- SzCORE: Optimized for clinical utility
- Both valid, but must match use case

#### 5.3 The Reproducibility Crisis
- Models trained on TUSZ but not evaluated on it
- Cherry-picking favorable scoring methods
- Need standardized, dataset-matched evaluation

### 6. Related Work
- Picone et al. 2021: Proposed TAES for better metrics
- Shah et al. 2018: TUSZ dataset paper
- EpilepsyBench 2024: Cross-dataset initiative

### 7. Conclusions
#### Key Takeaways
1. **100× gap** between claimed and clinical performance
2. **Scoring alone** creates 12× performance difference
3. **Dataset-matched** evaluation essential for validity

#### Recommendations
1. Always report multiple scoring methods
2. Use dataset-specific clinical scorers
3. Publish operating points for deployment

### 8. Reproducibility
- Code: github.com/Clarity-Digital-Twin/SeizureTransformer
- Weights: From Wu et al. repository
- Data: TUSZ v2.0.3 (requires DUA)
- Docker: Fully containerized pipeline

---

## Key Figures

### Figure 1: The Performance Spectrum
Visual showing same predictions scored 4 ways

### Figure 2: Operating Points
ROC-like curve but for FA/24h vs Sensitivity

### Figure 3: Scoring Method Comparison
Side-by-side: how each method counts detections

### Table 1: Comprehensive Results
All 12 data points (4 scorers × 3 operating points)

### Table 2: Cannot Meet Clinical Targets
Show attempts to reach 10, 2.5, 1 FA/24h

---

## Supplementary Materials
1. Full parameter sweep results
2. Per-file performance analysis
3. Error analysis (1 failed file)
4. Implementation details
5. NEDC/Python parity validation

---

## Key Messages to Emphasize

### The Positive Spin
- Not attacking SeizureTransformer (it's good!)
- Not attacking SzCORE (valid for clinical use!)
- Contributing reproducible evaluation infrastructure

### The Critical Points
1. **Benchmarks can be misleading** without context
2. **Scoring methodology** matters as much as model architecture
3. **Clinical deployment** requires dataset-matched evaluation

### The Call to Action
1. Standardize evaluation per dataset
2. Report multiple scoring methods
3. Publish deployment-ready parameters

---

## Potential Reviewer Concerns & Responses

**Q: "Is this just nitpicking about scoring?"**
A: No - 100× difference in false alarms determines clinical viability

**Q: "Why not train your own model?"**
A: Using author's weights ensures fair evaluation of their claims

**Q: "Is NEDC really the standard?"**
A: Yes - Temple created both TUSZ and NEDC as matched pairs

**Q: "Isn't SzCORE better for clinical use?"**
A: Context-dependent - but must be transparent about which is used

---

## Timeline & Checklist
- [ ] Write abstract (capture the hook)
- [ ] Create main figures (performance spectrum)
- [ ] Draft introduction (set the stage)
- [ ] Complete results section (the evidence)
- [ ] Polish discussion (the implications)
- [ ] Add reproducibility details
- [ ] Internal review
- [ ] arXiv submission