# Core Document Synthesis
## How the 5 Elements Tell Our Complete Story

### The Interconnected Narrative

```
TUSZ Dataset (CORE 5)
    ↓ creates
Annotations with specific philosophy
    ↓ matched by
NEDC v6.0.0 Software (CORE 4)
    ↓ implements
Scoring Methodologies (CORE 1)
    ↓ contrasts with
SzCORE/EpilepsyBench (CORE 3)
    ↓ evaluates
SeizureTransformer Model (CORE 2)
    ↓ reveals
100× Performance Gap
```

---

## The Story in Three Acts

### Act 1: The Setup
**CORE 5 (TUSZ) + CORE 4 (NEDC)**

Temple creates both dataset and scorer as matched pair:
- TUSZ: Conservative annotations, precise timing
- NEDC: No tolerance windows, exact evaluation
- **Key Point**: Designed to work together

### Act 2: The Divergence
**CORE 3 (EpilepsyBench) + CORE 1 (Scoring Methods)**

EpilepsyBench chooses different path:
- SzCORE: Clinical tolerances (30s/60s)
- Uniform scoring across all datasets
- **Key Point**: 12× more permissive than NEDC

### Act 3: The Revelation
**CORE 2 (SeizureTransformer) + Our Evaluation**

First proper evaluation reveals truth:
- Model claims 1 FA/24h (Dianalund + SzCORE)
- Reality: 100 FA/24h (TUSZ + NEDC)
- **Key Point**: 100× gap from scoring and dataset

---

## Cross-Document Connections

### Connection 1: TUSZ ↔ NEDC
```
From CORE 5: "Annotations follow Temple's clinical guidelines"
From CORE 4: "NEDC scoring matches those same guidelines"
Synthesis: This matched design is why NEDC is required for TUSZ
```

### Connection 2: NEDC ↔ SzCORE
```
From CORE 1: "OVLP is any-overlap binary scoring"
From CORE 3: "SzCORE = OVLP + tolerances + merging"
Synthesis: SzCORE adds ~90 seconds of wiggle room
```

### Connection 3: SeizureTransformer ↔ Evaluation Gap
```
From CORE 2: "Trained on TUSZ, never evaluated on it"
From CORE 5: "Eval set exists but marked with 🚂"
Synthesis: Valid evaluation possible but never done
```

### Connection 4: Scoring Impact
```
From CORE 1: "Same predictions → ≈16× FA spread"
From CORE 3: "SzCORE designed for clinical utility"
From CORE 4: "NEDC designed for research precision"
Synthesis: Different philosophies, massive impact
```

---

## The Professional Framing

### What We're NOT Saying
❌ SeizureTransformer is bad (it's good!)
❌ SzCORE is wrong (valid for clinical use)
❌ EpilepsyBench is flawed (valuable initiative)
❌ NEDC is the only way (context-dependent)

### What We ARE Saying
✅ Scoring methodology creates 12× difference
✅ Dataset-matched evaluation essential
✅ Benchmarks need transparency
✅ Clinical claims require proper validation

---

## Key Numbers Across Documents

### The Performance Cascade
```
Claimed (Dianalund + SzCORE):        1 FA/24h
Our Finding (TUSZ + SzCORE):         8.46 FA/24h
Our Finding (TUSZ + NEDC):           100.06 FA/24h
Our Finding (TUSZ + NEDC TAES):      137.53 FA/24h (Total False Alarm Rate)
```

### The Gaps
- **100×**: Dianalund claim vs TUSZ reality
- **12×**: SzCORE vs NEDC on same data
- **≈16×**: Most permissive vs most strict

---

## Writing Strategy Using Cores

### Introduction (Use CORES 2, 3, 5)
- SeizureTransformer wins EpilepsyBench
- TUSZ is training dataset
- Eval never done properly

### Methods (Use CORES 4, 5, 1)
- NEDC as gold standard
- TUSZ eval set details
- Scoring methodology comparison

### Results (Use ALL CORES)
- 100× gap revealed
- Scoring impact quantified
- Operating points provided

### Discussion (Use CORES 1, 3, 4)
- Why scoring matters
- Clinical vs research priorities
- Need for standards

---

## The Cutting Edge (Professional but Direct)

### From Core Documents
1. "Despite patient-disjoint eval set, never properly evaluated" (CORE 5)
2. "The 12× difference stems entirely from scoring methodology" (CORE 1)
3. "Marking TUSZ with 🚂 prevents valid held-out evaluation" (CORE 3)
4. "NEDC reveals the true clinical performance" (CORE 4)
5. "The 1 FA/24h achievement was on Dianalund, not training dataset" (CORE 2)

### Synthesized Message
"State-of-the-art model trained on TUSZ wins competitions elsewhere but was never evaluated on TUSZ's held-out set with clinical scoring. When we perform this missing evaluation, we discover a 100-fold gap between benchmark claims and clinical reality, with scoring methodology alone accounting for a 12-fold difference."

---

## Action Items from Cores

### Immediate Paper Needs
1. Generate Figure 1: Performance spectrum (from CORE 1)
2. Create Table 1: Comprehensive results (from CORES 1+4)
3. Write methods section on NEDC integration (from CORE 4)
4. Draft introduction hook (from CORE 2+3)

### Evidence to Emphasize
- First NEDC v6.0.0 evaluation (CORE 4)
- Patient-disjoint validation (CORE 5)
- 12× scoring impact (CORE 1)
- Clinical deployment gaps (CORE 3)

---

## The One-Paragraph Summary

Drawing from all 5 cores: "SeizureTransformer, winner of the 2025 EpilepsyBench Challenge with 1 FA/24h on Dianalund, was trained on TUSZ but never evaluated on its held-out test set with Temple's NEDC clinical scorer. We perform this missing evaluation, revealing 100.06 FA/24h with NEDC versus 8.46 FA/24h with EpilepsyBench's SzCORE—a 12-fold difference from scoring alone. This gap stems from fundamental differences in evaluation philosophy: NEDC, designed specifically for TUSZ by the same team that created the dataset, enforces strict temporal precision, while SzCORE adds 30-second pre-ictal and 60-second post-ictal tolerances plus event merging for clinical deployment scenarios. Our work demonstrates that meaningful clinical AI evaluation requires dataset-matched scoring standards, transparent methodology reporting, and honest assessment using held-out test sets."

---

## Quality Checklist

### Facts Verified Across Cores
✅ 100.06 FA/24h with NEDC (CORES 1, 4)
✅ 8.46 FA/24h with SzCORE (CORES 1, 3)
✅ 865 files in eval set (CORE 5)
✅ NEDC v6.0.0 released Aug 2025 (CORE 4)
✅ 30s/60s tolerances in SzCORE (CORES 1, 3)

### Professional Tone Maintained
✅ Respectful to all parties
✅ Focus on systemic issues
✅ Constructive recommendations
✅ Evidence-based claims
