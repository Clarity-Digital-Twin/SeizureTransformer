# Discussion Section - Brainstorming Document

## Key Points to Cover

### 1. Main Finding Interpretation
- 27-137× performance gap between claimed and actual
- Not unique to SeizureTransformer - systemic issue
- Different datasets, different realities

### 2. Scoring Method Impact Analysis
- 3.1× difference (OVERLAP vs SzCORE) at default
- 5.1× difference (TAES vs OVERLAP)
- 15.9× difference (TAES vs SzCORE)
- Each serves different clinical purposes
- No "right" answer - transparency is key

### 3. Clinical Deployment Reality
- Cannot meet FDA requirements (≤10 FA/24h, ≥50% sensitivity)
- 33.90% sensitivity at 10.27 FA/24h is best achievable
- Gap between research success and clinical viability

### 4. Why These Gaps Exist
- Training vs evaluation dataset differences
- Benchmark optimization vs clinical requirements
- Scoring philosophy differences
- Lack of standardization

### 5. Broader Implications
- Field needs standardized evaluation
- Dataset-matched scoring essential
- Multiple metrics should be reported
- Clinical requirements differ from research metrics

### 6. Constructive Recommendations
- Always evaluate on training dataset's held-out set
- Report multiple scoring methods
- Use dataset-matched evaluation tools
- Provide operating points for different use cases

### 7. Acknowledge Achievements
- SeizureTransformer is architectural advance
- Cross-dataset performance is meaningful
- AUROC of 0.9019 shows model capability
- Problem is evaluation standards, not model quality

### 8. Address Potential Criticisms
- Not attacking the model or authors
- Not saying SzCORE is wrong
- Not dismissing benchmark achievements
- Highlighting need for transparency

## Paragraph Flow

### P1: Main Finding Context
- Start with 27-137× gap
- Frame as systemic issue, not individual failure
- Acknowledge SeizureTransformer's contributions

### P2: Scoring Method Analysis
- Deep dive into 3.1× difference
- Explain why different scorers exist
- Clinical vs research priorities

### P3: Clinical Deployment Gap
- Cannot meet FDA thresholds
- Best achievable: 33.90% @ 10.27 FA/24h
- Reality check for field

### P4: Root Causes
- Dataset differences (TUSZ vs Dianalund)
- Benchmark gaming vs clinical needs
- Evaluation methodology gaps

### P5: Broader Pattern
- Not unique to SeizureTransformer
- Field-wide issue with evaluation
- Need for standardization

### P6: Path Forward
- Concrete recommendations
- Multi-metric reporting
- Dataset-matched evaluation
- Transparency above all

### P7: Limitations of Our Work
- Only evaluated one model
- TUSZ-specific findings
- Didn't retrain model
- Focus on evaluation only

### P8: Future Directions
- Community standards needed
- More models need evaluation
- Clinical validation studies
- Real-world deployment data

## Key Quotes from Core Documents

From CONTRIBUTIONS_AND_NOVELTY.md:
- "Same model can claim 1 or 26.89-136.73 FA/24h"
- "Lab success ≠ clinical viability"
- "No 'correct' scoring - depends on use case"

From WRITING_STRATEGY.md:
- "Attack the system, not the people"
- "SeizureTransformer advances architecture while revealing evaluation gaps"
- "Different scoring philosophies serve different purposes, but transparency is non-negotiable"

From CORE_1_SCORING_METHODOLOGIES.md:
- "OVLP is considered a very permissive way of scoring" - Picone 2021
- "3.1× difference from scorer alone"

## Tone Guidelines

- Professional and measured
- Critical but constructive
- Data-driven arguments
- Acknowledge genuine achievements
- Focus on systemic issues
- Provide actionable recommendations
- No personal attacks
- No conspiracy theories

## Data Points to Emphasize

- 26.89 FA/24h (NEDC OVERLAP) vs 1 FA/24h (claimed)
- 136.73 FA/24h (NEDC TAES) - strictest scoring
- 8.59 FA/24h (SzCORE) - most permissive
- 33.90% sensitivity at 10.27 FA/24h - best clinical operating point
- 0.9019 AUROC - shows model has signal
- 865 files, 127.7 hours, 469 seizures - substantial evaluation

## What NOT to Say

- Don't say "SeizureTransformer doesn't work"
- Don't attack Wu et al. personally
- Don't dismiss SzCORE as invalid
- Don't claim NEDC is the only truth
- Don't suggest malicious intent
- Don't use inflammatory language

## The Core Message

SeizureTransformer's 27-137× performance gap reveals not a failed model but a broken evaluation ecosystem. The field needs transparent, standardized, dataset-matched evaluation with multiple metrics reported. Different scoring methods serve different purposes - the key is transparency about which is being used and why. Clinical deployment requires meeting specific thresholds that current models cannot achieve when properly evaluated, but this gap can be closed through honest assessment and targeted improvement.