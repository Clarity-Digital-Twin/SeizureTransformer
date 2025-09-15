# Writing Strategy: Professional, Cutting, and Honest
## How to Tell Hard Truths Without Being a Dick

### The Golden Rules

1. **Attack the System, Not the People**
   - ❌ "Wu et al. cherry-picked metrics"
   - ✅ "The field lacks standardized evaluation"

2. **Acknowledge Genuine Contributions**
   - ❌ "SeizureTransformer's claims are bogus"
   - ✅ "SeizureTransformer advances architecture while revealing evaluation gaps"

3. **Use Data to Cut Deep**
   - ❌ "The model doesn't work"
   - ✅ "100.06 FA/24h versus claimed 1 FA/24h represents a 100× gap"

---

## Framing Techniques

### The "Yes, And..." Approach
```
"SeizureTransformer represents a significant architectural advance,
AND when evaluated with clinical standards reveals fundamental
challenges in the field's evaluation methodology."
```

### The "Context Matters" Frame
```
"The model achieves 1 FA/24h with SzCORE's clinical tolerances,
which becomes 100 FA/24h with NEDC's research precision,
highlighting how context determines performance claims."
```

### The "Broader Pattern" Frame
```
"This 100× gap is not unique to SeizureTransformer but reflects
a systemic issue in how seizure detection models are evaluated."
```

---

## Language Choices

### Words to Use
- "Reveals" (not "exposes")
- "Gap" (not "failure")
- "Overlooked" (not "ignored")
- "Opportunity" (not "mistake")
- "Systemic" (not "widespread fraud")

### Power Phrases
- "First clinical evaluation reveals..."
- "When properly assessed..."
- "Dataset-matched evaluation shows..."
- "Transparent reporting would show..."
- "Clinical reality differs from..."

---

## Handling Sensitive Topics

### The 100× Gap
**Too Harsh**: "Claims are off by 100×"
**Too Soft**: "Some differences in metrics"
**Just Right**: "A 100-fold gap exists between benchmark performance and clinical evaluation"

### The 🚂 Issue
**Too Harsh**: "EpilepsyBench hides TUSZ results"
**Too Soft**: "Some datasets aren't shown"
**Just Right**: "Valid held-out evaluation is prevented by conservative marking policies"

### Scoring Differences
**Too Harsh**: "SzCORE inflates performance"
**Too Soft**: "Different scorers exist"
**Just Right**: "Scoring methodology alone creates 12× performance differences"

---

## The Introduction Hook

### Version 1: The Mystery
"How can a state-of-the-art model achieve both 1 and 100 false alarms per 24 hours?"

### Version 2: The Revelation
"We present the first clinical evaluation of SeizureTransformer, revealing a 100-fold gap between benchmark claims and deployment reality."

### Version 3: The Challenge
"Current seizure detection benchmarks may be hiding a uncomfortable truth: models that excel in competitions fail clinical standards by orders of magnitude."

---

## Addressing Potential Criticism

### "You're being unfair to SeizureTransformer"
**Response in paper**: "We evaluate using the authors' exact weights and recommended parameters, ensuring fair assessment of published claims."

### "You're attacking EpilepsyBench"
**Response in paper**: "EpilepsyBench provides valuable cross-dataset comparison; our work complements it with dataset-specific clinical evaluation."

### "SzCORE is valid for clinical use"
**Response in paper**: "Different scoring methods serve different purposes—our work quantifies these differences to enable informed decisions."

---

## The Results Presentation

### Lead with Impact
"SeizureTransformer achieves 45.63% sensitivity at 100.06 false alarms per 24 hours when evaluated on TUSZ with NEDC scoring."

### Follow with Context
"The same predictions yield 8.46 FA/24h with SzCORE's clinical tolerances, demonstrating a 12-fold impact from scoring methodology alone."

### Conclude with Implications
"These results indicate that models cannot meet clinical deployment thresholds when evaluated with dataset-matched standards."

---

## The Discussion Balance

### Paragraph 1: Acknowledge Achievements
"SeizureTransformer's architectural innovations and cross-dataset performance represent meaningful advances..."

### Paragraph 2: Present Hard Truths
"However, the 100-fold gap between benchmark and clinical performance reveals fundamental challenges..."

### Paragraph 3: Systemic Issues
"This gap reflects not individual failure but systemic issues in evaluation standards..."

### Paragraph 4: Constructive Path Forward
"Addressing these challenges requires transparent reporting, dataset-matched evaluation, and..."

---

## Specific Cutting Lines (With Context)

### On Performance Claims
"The 1 FA/24h achievement, while impressive on Dianalund, becomes 100 FA/24h on the model's training dataset."

### On Evaluation Gaps
"Despite TUSZ's carefully designed held-out set, no prior evaluation with clinical scoring exists."

### On Scoring Impact
"A 12-fold difference in reported performance stems entirely from the choice of scoring methodology."

### On Clinical Reality
"Current benchmarks may be optimizing for metrics that diverge from clinical needs."

---

## The Conclusion Tone

### What We Found (Direct)
"Our evaluation reveals a 100-fold gap between benchmark claims and clinical reality."

### Why It Matters (Urgent)
"This gap determines whether AI seizure detection can be deployed in hospitals."

### What To Do (Constructive)
"Standardized, dataset-matched evaluation with transparent reporting can bridge this gap."

---

## Review Checklist

Before submitting, ensure:

✅ Every criticism paired with acknowledgment
✅ Focus on systems, not individuals
✅ Data drives the narrative
✅ Constructive recommendations included
✅ Professional tone throughout
✅ No personal attacks
✅ No conspiracy theories
✅ No unsubstantiated claims

---

## The One-Liner Summaries

### For Abstract
"First clinical evaluation reveals 100× gap between benchmark and reality."

### For Introduction
"State-of-the-art models may be state-of-the-art at gaming benchmarks."

### For Discussion
"Different scoring philosophies serve different purposes, but transparency is non-negotiable."

### For Conclusion
"Clinical AI requires clinical evaluation—not benchmark optimization."

---

## Final Wisdom

**Be the paper you'd want to receive as a reviewer:**
- Rigorous but respectful
- Critical but constructive
- Direct but professional
- Honest but fair

**Remember**: We're revealing uncomfortable truths to improve the field, not to tear down colleagues. The goal is better seizure detection for patients, not academic point-scoring.