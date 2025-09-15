# Background Section Brainstorming

## Purpose
Provide academic context for our evaluation, covering:
1. TUSZ dataset and its careful design
2. NEDC scorer and its relationship to TUSZ
3. Scoring methodology spectrum (TAES → OVERLAP → SzCORE)
4. SeizureTransformer model overview
5. Brief related work on evaluation challenges

## Key Themes to Thread Through
- **Matched ecosystems**: TUSZ + NEDC designed together by Temple
- **Scoring spectrum**: Different philosophies for different purposes
- **The evaluation gap**: Models trained on datasets but never properly evaluated on them
- **Clinical vs research priorities**: Why scoring choices matter

## Section-by-Section Outline

### Opening: The Dataset Foundation (2-3 paragraphs)
**TUSZ as gold standard**
- Largest public seizure dataset: 3,050 hours, 642 patients, 3,964 seizures
- **Critical feature**: Patient-disjoint train/dev/eval splits (486/53/43 patients)
- Eval set: 865 files, 127.7 hours, 469 seizures - truly held-out
- Created by Temple University Hospital with board-certified neurologist annotations
- Conservative annotation philosophy: clear electrographic seizures only, temporal precision

**Why patient-disjoint matters**
- Prevents data leakage between splits
- Enables valid generalization assessment
- Standard practice in ML but often violated in medical AI
- TUSZ got this right from the beginning (Shah et al. 2018)

### The Scoring Ecosystem (2-3 paragraphs)
**NEDC v6.0.0: The matched scorer**
- Created by same Temple team that made TUSZ
- Designed to match TUSZ's annotation philosophy
- Released August 2025 on TUH listserv
- Implements multiple scoring modes: OVERLAP, TAES, IEC, AAM, LEVY
- OVERLAP mode is clinical standard for TUSZ evaluation

**The scoring spectrum**
- TAES (Picone 2021): Most strict, partial credit based on temporal overlap %
  - Example: 60s seizure with 45s detected = 0.75 TP credit
  - Designed for research precision and algorithm development
- OVERLAP: Binary any-overlap scoring
  - Any temporal overlap = full TP
  - Standard practice, balances clinical and research needs
- SzCORE (Ebenezer 2024): Most permissive
  - Adds 30s pre-ictal, 60s post-ictal tolerances
  - Merges events <90s apart
  - Designed for clinical deployment where early warning matters

**Critical insight**: These aren't right/wrong but different valid perspectives
- Research: Need temporal precision (TAES)
- Clinical standard: Any detection valuable (OVERLAP)
- Deployment: Early warning + reduced alarms (SzCORE)

### SeizureTransformer: The State-of-the-Art (1-2 paragraphs)
**Architecture and training**
- Wu et al. 2025: Combines U-Net (biomedical segmentation) + Transformer (long-range dependencies)
- Trained on TUSZ v1.5.2 train subset (~910h) + Siena dataset (128h)
- 41M parameters, processes 60s windows at 256 Hz
- Won EpilepsyBench 2025 Challenge

**The evaluation situation**
- Claimed: 37% sensitivity @ 1 FA/24h on Dianalund (Danish dataset)
- Never evaluated on TUSZ eval set despite training on TUSZ
- EpilepsyBench marks TUSZ with 🚂 (train emoji), no metrics shown
- Authors openly shared pretrained weights (169MB) - commendable transparency

### The Evaluation Gap in the Field (1-2 paragraphs)
**Common pattern**
1. Train model on Dataset X
2. Evaluate on Dataset Y (different)
3. Claim generalization
4. Never test on X's held-out eval set
5. Use favorable scoring method

**Why this matters**
- Clinical deployment requires honest metrics on relevant data
- Cross-dataset performance ≠ within-dataset performance
- Scoring methodology can change results by 3-10×
- Patients deserve accurate performance claims

### Brief Related Work Pointers (1 paragraph)
- Evaluation metrics in seizure detection (Ward 2019, Picone 2021)
- Clinical deployment requirements: <10 FA/24h, >50% sensitivity (Beniczky 2024)
- Cross-dataset generalization challenges (Gemein 2020)
- Reproducibility crisis in medical AI (Haibe-Kains 2020)

## Key Data Points to Include

### TUSZ Numbers
- Total: 3,050 hours, 642 unique patients
- Train: 4,667 files, 910.3h, 486 patients, 2,420 seizures
- Dev: 1,832 files, 435.5h, 53 patients, 1,075 seizures
- **Eval: 865 files, 127.7h, 43 patients, 469 seizures**
- Version used by SeizureTransformer: v1.5.2 (subset)
- Our evaluation: v2.0.3 (full eval set)

### NEDC Details
- Version: v6.0.0 (August 2025)
- Scoring modes: OVERLAP (standard), TAES (strict), others
- Distribution: Temple University Hospital listserv
- Our validation: Perfect parity between NEDC and our Python implementation

### SzCORE Specifications
- Pre-ictal tolerance: 30 seconds
- Post-ictal tolerance: 60 seconds
- Event merging: <90 seconds apart
- Purpose: Clinical deployment, alarm reduction

### SeizureTransformer Specs
- Input: 19 channels, 256 Hz, 60s windows
- Post-processing: θ=0.8 threshold, k=5 morph kernel, d=2.0s min duration
- Training data: TUSZ train + Siena (total ~1,038 hours)
- Pretrained weights: 169MB, publicly available

## Professional Tone Guidance

### DO Emphasize
- Temple created both TUSZ and NEDC - matched ecosystem
- Different scoring methods serve different valid purposes
- SeizureTransformer represents genuine architectural advance
- The field needs standardized evaluation practices

### AVOID
- Attacking EpilepsyBench (valuable initiative)
- Dismissing SzCORE (clinically motivated)
- Criticizing Wu et al. personally (focus on systemic issues)
- Claiming one scoring method is "correct"

### Cutting but Fair Language
- "Despite patient-disjoint eval set, models trained on TUSZ are rarely evaluated on it"
- "The same predictions yield 3.1× different false alarm rates purely from scoring choice"
- "NEDC, designed specifically for TUSZ, reveals different performance than generic scorers"
- "The field lacks transparency about evaluation methodology"

## Flow and Transitions

**From Intro → Background**
"To understand these performance disparities, we must first examine the evaluation ecosystem..."

**Internal flow**
- Dataset → Scorer (matched design)
- Scorer types → Spectrum of philosophies
- Model overview → Never evaluated properly
- Systemic pattern → Need for change

**To Methods**
"Given this context, we now describe our evaluation methodology..."

## Citations to Include
- Shah et al. 2018 (TUSZ dataset)
- Picone et al. 2021 (NEDC, TAES vs OVERLAP)
- Ebenezer et al. 2024 (SzCORE)
- Wu et al. 2025 (SeizureTransformer)
- EpilepsyBench 2025 (challenge)
- Beniczky 2024 (clinical requirements)
- Brief mentions: Ward 2019, Gemein 2020, Haibe-Kains 2020

## Key Quotes to Potentially Use
- "OVLP is considered a very permissive way of scoring" - Picone 2021
- "30-second pre-ictal tolerance allows for early warning" - SzCORE
- "Patient-disjoint splits ensure valid generalization" - Shah 2018
- "Achieved state-of-the-art performance" - Wu 2025

## The Core Message
The infrastructure exists for proper evaluation (TUSZ eval set + NEDC scorer), but the field doesn't use it. Different scoring philosophies serve different purposes, but without transparency about which is used, performance claims lack context. Our work fills this evaluation gap.

## Paragraph Count Target
- 7-9 paragraphs total
- ~150-200 words per paragraph
- Total: ~1,200-1,500 words

## Remember
- This sets up Methods section (what we did)
- Provides context for Results (why numbers vary)
- Seeds Discussion points (implications)
- Keep it academic but accessible
- Let the facts speak - no need for hyperbole