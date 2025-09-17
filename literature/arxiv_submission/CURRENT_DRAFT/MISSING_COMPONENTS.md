# Missing Components and Precise Edits for CURRENT_WORKING_DRAFT.md

Purpose: enumerate gaps, specify exact edit locations, and provide ready‑to‑paste text blocks to finalize the paper. File references below use repository‑relative paths with starting line numbers.

## High‑Priority Fixes (structural)

- Replace legacy CLI/module paths with new entry points and src/ layout
  - Update reproduction commands and “Key scripts” list.
  - Current references to `evaluation/tusz/run_tusz_eval.py` and `evaluation/szcore_scoring/run_szcore.py` must change.
  - Impacted anchors in draft:
    - Reproducibility and Resources: `literature/arxiv_submission/current_draft/CURRENT_WORKING_DRAFT.md:228`
    - Exact Reproduction Procedure: `.../CURRENT_WORKING_DRAFT.md:245` (commands at 257, 282)
    - Key scripts list: `.../CURRENT_WORKING_DRAFT.md:469` (items at 476–478)

- Clarify SzCORE scoring details (variants and what we used)
  - Add a dedicated subsection under “Scoring Methodologies”.
  - Anchor: `.../CURRENT_WORKING_DRAFT.md:85` (Scoring Methodologies header)

- Integrate cross‑dataset comparison validity (summary from ADDITIONAL_INTEGRATIONS/COMPARISON_VALIDITY.md)
  - Add a short subsection in Discussion, and a pointer in Introduction.
  - Discussion anchor: first paragraph under Discussion `.../CURRENT_WORKING_DRAFT.md` around line 308.

## SzCORE Clarification (ready‑to‑paste)

Insert immediately after the SzCORE paragraph in Scoring Methodologies (after line ~107):

"""
### SzCORE Variants and Our Choice

The SzCORE toolkit supports event‑level evaluation with clinically motivated tolerances (−30 s pre‑ictal, +60 s post‑ictal) and merging of predictions separated by <90 s into single events. In some configurations, the underlying timescoring library can also report partial‑credit (time‑aligned) metrics akin to TAES. In this work we report SzCORE’s event‑level any‑overlap with tolerance windows (the common default in EpilepsyBench). We do not report time‑aligned partial‑credit SzCORE metrics to avoid conflating strict temporal scoring with SzCORE’s clinical‑tolerance philosophy. This distinction is called out to prevent misinterpretation when comparing across methods.
"""

Optional footnote to add at first SzCORE mention in Abstract/Intro: “We use SzCORE’s event‑level any‑overlap with tolerance windows unless noted.”

## Reproducibility Commands (replace block)

Replace the command block under “Exact Reproduction Procedure” to use the new CLIs. Edit at:
- `literature/arxiv_submission/current_draft/CURRENT_WORKING_DRAFT.md:257` and `:282`.

Use this updated text:

"""
### 2. Generate Model Predictions
```bash
tusz-eval \
  --data_dir /path/to/tusz_v2.0.3/edf/eval \
  --out_dir experiments/eval/repro \
  --device cuda
```

### 3. Apply NEDC Clinical Scoring
```bash
# Paper default (theta=0.8, k=5, d=2.0s)
nedc-run \
  --checkpoint experiments/eval/repro/checkpoint.pkl \
  --outdir results/nedc_default \
  --backend nedc-binary \
  --threshold 0.80 --kernel 5 --min_duration_sec 2.0

# Clinical 10 FA/24h target
nedc-run \
  --checkpoint experiments/eval/repro/checkpoint.pkl \
  --outdir results/nedc_10fa \
  --backend nedc-binary \
  --threshold 0.88 --kernel 5 --min_duration_sec 3.0
```

### 4. Apply SzCORE Comparison
```bash
szcore-run \
  --checkpoint experiments/eval/repro/checkpoint.pkl \
  --outdir results/szcore_default \
  --threshold 0.80 --kernel 5 --min_duration_sec 2.0
```
"""

Add a one‑line note under the NEDC section: “`nedc-run` is a dev‑only wrapper that expects the vendored `evaluation/nedc_eeg_eval/` tree available in a repo checkout or editable install.”

## “Key scripts” List (replace items)

Edit at `.../CURRENT_WORKING_DRAFT.md:476–478` to:

"""
- `tusz-eval` (CLI): Generate predictions; entry point `seizure_evaluation.tusz.cli:main`
- `nedc-run` (CLI): NEDC orchestration; wrapper defers to vendored NEDC tools
- `szcore-run` (CLI): SzCORE Event evaluation; entry point `seizure_evaluation.szcore.cli:main`
- `scripts/visualize_results.py`: Recreate figures from results
- `evaluation/nedc_eeg_eval/nedc_scoring/sweep_operating_point.py`: Parameter grid search (vendored tools)
"""

## Discussion: Cross‑Dataset Validity (concise insertion)

Add a new subsection in Discussion (after the “Systemic Issues” paragraph):

"""
### Cross‑Dataset Validity (Dianalund vs TUSZ)

Using identical SzCORE scoring, SeizureTransformer achieves 1 FA/24h on Dianalund (37% sensitivity) versus 8.59 FA/24h on TUSZ (52.35% sensitivity), an 8.6× degradation that indicates limited generalization across datasets even under permissive clinical tolerances. This isolates dataset shift from scoring effects. For completeness, we also report TUSZ results under NEDC OVERLAP (26.89 FA/24h) and TAES (136.73 FA/24h), quantifying how evaluation philosophy further expands apparent performance gaps.
"""

Optionally cite “ADDITIONAL_INTEGRATIONS/COMPARISON_VALIDITY.md” as supplemental discussion.

## Methods: Preprocessing Specifics (clarification)

Augment Model/Inference pipeline with the following sentence (after the notch filters sentence):

"""
We adopt a 1 Hz notch (Q=30) in addition to 60 Hz, reflecting our released evaluation code; this is not explicitly specified in the original paper and is disclosed here for reproducibility.
"""

## Methods: Post‑processing policy note

Add at the end of Post‑processing paragraph:

"""
For NEDC‑aligned evaluations we disable any gap‑merge heuristics (merge_gap), as NEDC tools treat each prediction segment independently; SzCORE merging is applied only in the SzCORE pipeline by design.
"""

## Reproducibility: Environment clarifications (optional lines)

Under Environment Setup, add a note on versions:

"""
We pin NEDC v6.0.0 and TUSZ v2.0.3; reproducibility requires these exact versions. Our packaging follows a `src/` layout; install via `uv pip install -e .`.
"""

## Figures/Tables cross‑checks (editorial)

- Ensure captions explicitly state “Same predictions evaluated under different scoring methodologies” (Fig. 3) to avoid implying model differences.
- Table 1 header: add “Same predictions; different scoring” in a footnote.

## Open Decisions / TODOs

- Confirm whether to add SzCORE time‑aligned (partial‑credit) metrics. If included, clearly separate from SzCORE event‑level results to avoid conflation with TAES.
- Optionally add a “Scorer taxonomy” box summarizing: TAES (partial credit), OVERLAP (any‑overlap), SzCORE (any‑overlap with tolerance windows + merges).
- Add CLI smoke tests to the repo and reference them briefly under Reproducibility.

## Integration Checklist

1) Insert SzCORE Variants subsection under Scoring Methodologies.
2) Replace reproduction commands with `tusz-eval`, `nedc-run`, `szcore-run`.
3) Update “Key scripts” list to CLIs.
4) Add Discussion “Cross‑Dataset Validity” paragraph (linking to ADDITIONAL_INTEGRATIONS/COMPARISON_VALIDITY.md).
5) Add preprocessing and post‑processing clarifications in Methods.
6) Re‑scan for any remaining legacy path references (`evaluation/tusz/run_tusz_eval.py`, `evaluation/szcore_scoring/*`).
