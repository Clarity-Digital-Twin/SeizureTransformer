# Critical Citation Fixes Required for arXiv Paper

## The Problem
We've been claiming "≤10 FA/24h with ≥50% sensitivity" as THE clinical standard, citing Beniczky 2018. This is INCORRECT.

## What the Literature Actually Says

### 1. Beniczky & Ryvlin (2018) - Epilepsia
- **Does NOT specify** "10 FA/24h with ≥50% sensitivity"
- Only states false alarms/24h should be reported as a metric
- Defines 5 phases of validation but no numeric thresholds
- Current citation is INCORRECT for this claim

### 2. Roy et al. (2021) - eBioMedicine [NEW REFERENCE NEEDED]
**This is what we should cite for clinical thresholds:**
- **75% sensitivity** is the clinical goal for automated systems (page 524)
- **1 FA/24h** is human-level performance (page 836)
- States: "This sensitivity goal for an automated system is 75%"
- Their best systems achieved 426-1029 FA/24h at 75% sensitivity

### 3. FDA Requirements (from web search)
- Sensitivity: lower bound of 95% CI > 70%
- False alarm rate: < 2 FA/day
- More stringent than what we've been claiming

## Required Changes to Our Paper

### 1. Remove all instances of "10 FA/24h with ≥50% sensitivity" as THE clinical standard

### 2. Replace with one of these options:

**Option A: Use Roy et al. 2021 thresholds**
```markdown
The clinical deployment of seizure detection systems requires high sensitivity,
typically 75% or greater, with minimal false alarms (Roy et al., 2021).
Human-level performance achieves approximately 1 FA/24h.
```

**Option B: Keep 10 FA/24h as OUR target (not a standard)**
```markdown
We evaluate SeizureTransformer at multiple operating points, including a
clinically-motivated target of ≤10 FA/24h, which represents a practical
compromise between sensitivity and false alarm burden.
```

**Option C: Cite actual FDA requirements**
```markdown
FDA requirements for seizure detection devices specify sensitivity >70%
with <2 false alarms per day (48 FA/24h).
```

## Files That Need Editing

### High Priority (Main Paper):
1. `02_background.md` - Line 15: "typically less than 10 false alarms per 24 hours with at least 50% sensitivity (Beniczky et al., 2024)"
2. `05_discussion.md` - Line 13: "≤10 FA/24h with ≥50% sensitivity"
3. `01_introduction.md` - Line 13: "standard FDA thresholds of ≤10 FA/24h with ≥50% sensitivity"
4. `00_abstract.md` - Line 7: "below the ≥50% requirement"
5. `04_results.md` - Lines 26, 38: "falls below 50% sensitivity requirement"
6. `06_conclusion.md` - Line 3: "≥50% sensitivity required for practical utility"

### References Section:
7. `09_references.md` - Add Roy et al. 2021 as new reference
8. Update Beniczky citation to remove false threshold claim

## New Reference to Add

```bibtex
[16] Roy S, Kiral I, Mirmomeni M, et al. Evaluation of artificial intelligence
systems for assisting neurologists with fast and accurate annotations of scalp
electroencephalography data. eBioMedicine. 2021;66:103275.
doi:10.1016/j.ebiom.2021.103275
```

## Suggested Reframing

Instead of claiming we can't meet "THE standard", we should:

1. **Acknowledge multiple perspectives** on clinical thresholds
2. **Cite Roy et al. 2021** for 75% sensitivity goal
3. **Present 10 FA/24h** as a reasonable clinical target we chose
4. **Show that even at this relaxed threshold**, SeizureTransformer falls short (33.90% sensitivity)
5. **Note that human-level is 1 FA/24h** (even more stringent)

## Example Revision

**OLD (INCORRECT):**
"The clinical deployment of seizure detection systems requires meeting stringent performance thresholds, typically less than 10 false alarms per 24 hours with at least 50% sensitivity (Beniczky et al., 2018)."

**NEW (CORRECT):**
"The clinical deployment of seizure detection systems requires high sensitivity with minimal false alarms. Clinical goals typically target 75% sensitivity (Roy et al., 2021), while human reviewers achieve approximately 1 FA/24h. We evaluate SeizureTransformer at a practical threshold of ≤10 FA/24h, finding it achieves only 33.90% sensitivity—well below clinical requirements."

## Action Items

1. ✅ Convert Roy et al. 2021 PDF to markdown
2. ⬜ Add Roy et al. 2021 to references (reference [16])
3. ⬜ Fix all "10 FA/24h with ≥50% sensitivity" claims
4. ⬜ Update Beniczky citation to only claim what it actually says
5. ⬜ Reframe discussion around actual clinical standards (75% sensitivity)
6. ⬜ Note that our 33.90% at 10 FA/24h falls far short of 75% goal