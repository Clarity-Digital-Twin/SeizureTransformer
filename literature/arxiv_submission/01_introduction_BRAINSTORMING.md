# Introduction Brainstorming Document
## Building the Perfect Opening

### Core Narrative Threads (from all documents)

#### Thread 1: The Achievement vs Reality Gap
- **The Win**: SeizureTransformer wins 2025 EpilepsyBench with 1 FA/24h on Dianalund
- **The Training**: Trained on TUSZ (largest public dataset)
- **The Gap**: Never evaluated on TUSZ with clinical scoring
- **The Reality**: 27-fold gap when properly evaluated (26.89 vs 1 FA/24h)

#### Thread 2: The Scoring Paradox
- Same model, same predictions, different scorers
- 3.1× difference just from scoring choice (OVERLAP vs SzCORE)
- Not about right/wrong - about transparency and matching use cases
- TAES even stricter: 137× gap from original claim

#### Thread 3: The Systemic Issue
- Not attacking SeizureTransformer (it's good!)
- Not attacking SzCORE (valid for clinical use!)
- Revealing field-wide evaluation problems
- Need for dataset-matched standards

#### Thread 4: The Clinical Deployment Crisis
- FDA requirement: d10 FA/24h with e50% sensitivity
- SeizureTransformer at 10 FA target: only 33.90% sensitivity
- No current model meets clinical thresholds with proper scoring
- Patients waiting for deployable AI

### Powerful Opening Hooks (choose one)

#### Hook A: The Question
"How can the same seizure detection model achieve both 1 and 27 false alarms per 24 hours?"

#### Hook B: The Paradox
"SeizureTransformer claimed state-of-the-art performance with 1 FA/24h, yet when evaluated on its own training dataset, it produces 27 times more false alarms."

#### Hook C: The Reality Check
"The promise of AI in seizure detection faces a stark reality: models claiming near-perfect performance in benchmarks fail clinical standards by orders of magnitude."

#### Hook D: The Direct Statement
"We present the first clinical evaluation of SeizureTransformer on TUSZ, revealing a 27-fold gap between benchmark claims and deployment reality."

#### Hook E: The Clinical Context (RECOMMENDED)
"Epilepsy affects 50 million people worldwide, with 30% experiencing drug-resistant seizures requiring continuous monitoring. While AI promises to revolutionize seizure detection, a critical gap exists between benchmark achievements and clinical reality."

### Key Facts and Numbers to Weave In

#### Performance Numbers (verified from MASTER_RESULTS_SSOT)
- **Claimed**: ~1 FA/24h (Dianalund)
- **Our Finding**: 26.89 FA/24h (NEDC OVERLAP)
- **Our Finding**: 136.73 FA/24h (NEDC TAES)
- **Our Finding**: 8.59 FA/24h (SzCORE)
- **Gap Factors**: 27× (OVERLAP), 137× (TAES), 8.6× (SzCORE)

#### Dataset Facts
- TUSZ: 3,050 hours, 642 patients, 3,964 seizures
- Eval set: 865 files, 127.7 hours, 469 seizures
- Patient-disjoint splits (no leakage)
- Created by Temple with matched NEDC scorer

#### Scoring Impact
- 3.1× difference (OVERLAP vs SzCORE) at default
- Same predictions, different results
- NEDC: strict temporal precision
- SzCORE: 30s pre-ictal, 60s post-ictal tolerances

### Introduction Flow (Paragraph by Paragraph)

#### Paragraph 1: Clinical Context & Hook
- Start with epilepsy impact and monitoring needs
- Introduce promise of AI detection
- Set up the evaluation gap problem
- End with our contribution teaser

#### Paragraph 2: The Success Story
- SeizureTransformer's achievements
- EpilepsyBench 2025 victory
- Architectural innovation (U-Net + Transformer)
- Training on TUSZ dataset

#### Paragraph 3: The Evaluation Gap
- Despite TUSZ training, never evaluated on it
- TUSZ has held-out eval set (patient-disjoint)
- Temple created NEDC specifically for TUSZ
- This gap exists across the field

#### Paragraph 4: The Scoring Divergence
- Different communities use different scorers
- NEDC (Temple) vs SzCORE (EpilepsyBench)
- Each valid but serve different purposes
- Creates incomparable results

#### Paragraph 5: Our Investigation & Findings
- First to evaluate with NEDC v6.0.0
- Systematic comparison of 4 scoring methods
- Key finding: 27× gap (OVERLAP), 137× (TAES)
- Scoring alone creates 3.1× difference

#### Paragraph 6: Contributions
- Reproducible NEDC evaluation pipeline
- Comprehensive operating points
- Evidence for need of standards
- Open-source infrastructure

#### Paragraph 7: Paper Roadmap
- Methods: evaluation design
- Results: the gaps revealed
- Discussion: implications
- Path forward for field

### Professional Framing Language

#### Words to Use
- "reveals" (not "exposes")
- "gap" (not "failure")
- "evaluation standard" (not "scoring trick")
- "clinical reality" (not "true performance")
- "dataset-matched" (not "correct")

#### Key Phrases
- "First clinical evaluation reveals..."
- "When evaluated with Temple's standard..."
- "Scoring methodology alone accounts for..."
- "Meaningful clinical deployment requires..."

### Themes to Balance

#### Give Credit
- Acknowledge SeizureTransformer's innovation
- Respect SzCORE's clinical validity
- Appreciate EpilepsyBench initiative

#### Reveal Truth
- 27-137× gap is real and matters
- Scoring creates 3.1× difference
- Cannot meet clinical thresholds

#### Propose Solutions
- Transparent reporting
- Dataset-matched evaluation
- Multiple metrics always

### Draft Opening Sentences (mix and match)

1. "Epilepsy monitoring generates 50TB of EEG data annually in major hospitals, yet automated seizure detection remains tantalizingly out of reach for clinical deployment."

2. "SeizureTransformer's victory in the 2025 EpilepsyBench Challenge with 1 false alarm per 24 hours represents both the promise and peril of modern AI evaluation."

3. "The field of automated seizure detection faces a paradox: models excel in benchmarks but fail in hospitals."

4. "When the same seizure detection model can claim anywhere from 1 to 137 false alarms per 24 hours depending on how it's scored, the field has an evaluation crisis."

5. "We present the first clinical evaluation of SeizureTransformer using Temple University's NEDC v6.0.0 standard, revealing fundamental gaps between benchmark claims and deployment reality."

### The Story Arc

**Setup**: AI promises to help epilepsy patients
**Rising Action**: SeizureTransformer wins competitions
**Complication**: Never evaluated properly on TUSZ
**Investigation**: We perform missing evaluation
**Climax**: 27-137× gap discovered
**Resolution**: Need dataset-matched standards
**Future**: Path forward for field

### Critical Points to Make

1. **Not an attack**: This is about systemic issues, not individual failures
2. **Scoring matters**: 3.1× from methodology alone
3. **Clinical viability**: Current models can't meet FDA thresholds
4. **Reproducibility**: We provide open infrastructure
5. **Constructive**: We propose solutions

### Potential Reviewer Concerns to Address Early

- "Why didn't you train your own model?" ’ Using pretrained ensures fairness
- "Is NEDC really necessary?" ’ Temple created it specifically for TUSZ
- "Isn't SzCORE better?" ’ Different tools for different purposes

### The One-Paragraph Version

"Automated seizure detection promises to transform epilepsy care, with SeizureTransformer achieving state-of-the-art performance of 1 false alarm per 24 hours in the 2025 EpilepsyBench Challenge. However, this modeltrained on the Temple University Hospital Seizure (TUSZ) datasethas never been evaluated on TUSZ's held-out test set using Temple's clinical scoring standard. We present the first such evaluation using NEDC v6.0.0, revealing 26.89 false alarms per 24 hours with NEDC OVERLAP versus 8.59 with EpilepsyBench's SzCOREa 3.1-fold difference from scoring methodology alone. When using NEDC's strictest TAES scoring, the rate climbs to 136.73 FA/24h, representing a 137-fold gap from the original claim. Our systematic comparison demonstrates that meaningful clinical deployment requires dataset-matched evaluation standards, transparent methodology reporting, and honest assessment of performance gaps. We contribute reproducible evaluation infrastructure and comprehensive operating points to bridge the gap between benchmark achievements and clinical reality."

### Final Checklist for Introduction

- [ ] Hook that grabs attention
- [ ] Clinical context established
- [ ] SeizureTransformer achievements acknowledged
- [ ] Evaluation gap clearly stated
- [ ] Our contribution highlighted
- [ ] Professional, constructive tone
- [ ] Numbers are accurate (verify against MASTER_RESULTS_SSOT)
- [ ] Clear roadmap for paper
- [ ] Balanced (credit where due + hard truths)

### Writing Strategy

1. Start broad (epilepsy impact)
2. Narrow to AI detection promise
3. Focus on SeizureTransformer success
4. Reveal the evaluation gap
5. Present our investigation
6. State key findings clearly
7. List contributions
8. Roadmap the paper

### The Core Message

**In one sentence**: "State-of-the-art seizure detection models achieve impressive benchmark results but face a 27-137× false alarm gap when evaluated with clinical standards on their training datasets."

**The deeper point**: The field needs transparent, dataset-matched evaluation to bridge the gap between research achievements and clinical deployment.