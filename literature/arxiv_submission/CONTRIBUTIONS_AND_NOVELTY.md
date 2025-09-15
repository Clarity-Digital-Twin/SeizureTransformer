# Contributions and Novelty Statement

## Primary Novel Contributions

### 1. First Clinical Evaluation of SeizureTransformer on TUSZ
- **Novelty**: Despite TUSZ being the training dataset, no prior work evaluated with clinical scoring
- **Impact**: Reveals true clinical performance vs benchmark claims
- **Significance**: 100× gap changes deployment viability assessment

### 2. Quantifying Scoring Method Impact
- **Novelty**: First systematic comparison of 4 scoring methods on identical predictions
- **Impact**: Shows 12× performance difference from scoring alone
- **Significance**: Explains discrepancies in literature without model changes

### 3. Reproducible NEDC v6.0.0 Integration
- **Novelty**: First open-source pipeline integrating Temple's clinical scorer
- **Impact**: Enables community to replicate clinical evaluations
- **Significance**: Bridges research-to-clinic evaluation gap

---

## Technical Contributions

### Software Engineering
1. **Dual-track Implementation**
   - Temple NEDC binaries (unmodified) for validity
   - Python reimplementation for production
   - <0.1% parity validation

2. **Containerized Pipeline**
   - Docker images for CPU/GPU deployment
   - Reproducible environment specification
   - Dataset-agnostic architecture

3. **Comprehensive Testing Suite**
   - 55 unit/integration tests
   - Synthetic data validation
   - Per-file error analysis

### Evaluation Methodology
1. **Systematic Parameter Tuning**
   - Grid search on dev set (1,013 files)
   - Target: NEDC OVERLAP (balanced)
   - 3 clinical operating points

2. **Multi-metric Reporting**
   - Sensitivity, FA/24h, F1, AUROC
   - Per-file and aggregate metrics
   - Error analysis and edge cases

---

## What This Paper is NOT

### Not an Attack Paper
- ✅ Respects SeizureTransformer's achievement
- ✅ Acknowledges SzCORE's clinical validity
- ✅ Recognizes different use cases for metrics

### Not a New Model Paper
- Using pretrained weights ensures fairness
- Focus on evaluation, not architecture
- Reproducibility over novelty

### Not a Dataset Paper
- Using existing TUSZ v2.0.3
- Following established protocols
- Adding evaluation layer only

---

## Key Insights Revealed

### 1. The Benchmark Illusion
**Finding**: Same model can claim 1 or 100 FA/24h
**Insight**: Benchmarks without context mislead the field
**Implication**: Need dataset-matched evaluation standards

### 2. The Clinical Gap
**Finding**: Cannot meet FDA targets with proper scoring
**Insight**: Lab success ≠ clinical viability
**Implication**: Must report clinical-relevant metrics

### 3. The Scoring Spectrum
**Finding**: 17× spread from strictest to most permissive
**Insight**: No "correct" scoring - depends on use case
**Implication**: Must report multiple methods transparently

---

## Community Impact

### For Researchers
- Template for rigorous evaluation
- Baseline for future comparisons
- Understanding of metric variations

### For Clinicians
- Reality check on AI readiness
- Operating points for deployment
- Understanding of performance claims

### For Developers
- Production-ready evaluation code
- Docker deployment patterns
- Testing methodology

---

## Reproducibility Checklist

### ✅ Data Availability
- TUSZ v2.0.3 publicly available (with DUA)
- Clear download instructions
- Version-specific paths

### ✅ Code Availability
- GitHub repository with all code
- Tagged release for paper version
- Documentation and examples

### ✅ Model Availability
- Using public pretrained weights
- Clear provenance (Wu's repository)
- No modifications to architecture

### ✅ Environment Specification
- Docker containers (CPU/GPU)
- Requirements files (pip/conda)
- System specifications documented

### ✅ Results Reproducibility
- Checkpoint files provided
- Random seeds fixed
- Detailed logs included

---

## Broader Impacts

### Positive Impacts
1. **Transparency**: Reveals true performance gaps
2. **Standardization**: Pushes for consistent evaluation
3. **Clinical Trust**: Honest reporting builds confidence
4. **Open Science**: Full reproducibility enables progress

### Potential Concerns
1. **Discouraging?**: Might seem like "nothing works"
   - **Response**: Better to know reality than false hope
2. **Too Critical?**: Might upset model authors
   - **Response**: Constructive, not destructive critique
3. **Confusing?**: Multiple metrics might overwhelm
   - **Response**: Education through clear explanation

---

## Why This Work Matters

### The 100× Gap Story
- Not just a number - determines clinical deployment
- Patients deserve honest performance assessment
- Investors need realistic expectations

### The Reproducibility Story
- Science requires verification
- Clinical AI needs rigorous standards
- Open tools enable progress

### The Standards Story
- Different use cases need different metrics
- Transparency about methods essential
- Community needs agreed standards

---

## Reviewer Response Preparation

### "Why didn't you train your own model?"
- Focus on evaluation methodology
- Using pretrained ensures fairness
- Training would confound contributions

### "Isn't this just engineering?"
- Engineering evaluation IS research
- Reproducibility crisis needs solutions
- Clinical deployment needs standards

### "Why does scoring method matter?"
- 12× difference determines viability
- Clinical vs research priorities differ
- Transparency enables informed decisions

### "What's the solution?"
- Report multiple metrics always
- Use dataset-matched scorers
- Publish operating points

---

## The Elevator Pitch

**One Sentence**:
"We show that SeizureTransformer's claimed 1 FA/24h becomes 100 FA/24h when evaluated with clinical standards on its training dataset."

**Three Sentences**:
"SeizureTransformer won EpilepsyBench with 1 FA/24h but was never evaluated on TUSZ with clinical scoring. We reveal 100 FA/24h using Temple's NEDC standard - a 100× gap. Scoring methodology alone creates 12× performance differences, highlighting need for standardized evaluation."

**One Paragraph**:
"State-of-the-art seizure detection models report impressive benchmark performance, but clinical deployment reveals massive gaps. We present the first evaluation of SeizureTransformer using Temple's NEDC v6.0.0 clinical standard on TUSZ, revealing 100 false alarms per 24 hours versus the 1 FA/24h achieved on other datasets. Our systematic comparison shows scoring methodology alone creates a 12-fold performance difference, with the same predictions yielding anywhere from 8 to 144 FA/24h depending on the scorer. This work provides reproducible evaluation infrastructure and comprehensive operating points, demonstrating the critical need for dataset-matched clinical evaluation standards in medical AI."