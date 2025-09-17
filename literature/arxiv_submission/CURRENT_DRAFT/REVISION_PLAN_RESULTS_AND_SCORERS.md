# Revision Plan — Results & Scorers (Native OVERLAP reporting)

Purpose: capture decisions and exact surgical edits to finalize the paper's Results, Methods, and supporting docs after deciding to not report Native OVERLAP as a separate scorer.

## Decision

- Do not report "Native OVERLAP" as a separate line in tables/figures/text.
- Keep a concise parity note: our native any-overlap implementation matches NEDC OVERLAP to 4 decimals across all metrics; we retain it for validation only.
- Public reporting focuses on three scorers: NEDC TAES, NEDC OVERLAP, SzCORE (event-level with clinical tolerances).

## Affected Content (where to edit)

Primary draft (split files):
- 02_introduction.md
  - Replace phrases like "four scoring methodologies" with "three scoring methodologies (NEDC TAES, NEDC OVERLAP, SzCORE)."
- 04_methods.md
  - Under "Scoring Methodologies": add a one-line parity note (native OVERLAP = NEDC OVERLAP; not reported separately).
  - Optionally retain Appendix C.3 for validation details; Methods should only carry the brief note.
- 05_results.md
  - Remove Native OVERLAP rows/mentions from the default results table and operating-points bullets.
  - First paragraph(s) that enumerate scorers must say "three" instead of "four."
- 11_appendix.md
  - Table A1: remove "Native OVERLAP" row.
  - Keep "C.3 Native OVERLAP Validation" subsection as the place where we show parity existed; adjust wording to clarify it's validation only.

Supporting docs:
- literature/arxiv_submission/current_draft/RESULTS.md
  - Remove Native OVERLAP table rows/bullets; add a top "Reporting policy" note.
- literature/arxiv_submission/current_draft/COMPLETE_RESULTS_COLLATED.md
  - Remove Native OVERLAP rows or add a prominent note that it will be omitted in publication; parity note remains.
- literature/arxiv_submission/current_draft/ADDITIONAL_INTEGRATIONS/RESULTS_ROOT.md
  - "What We Publish": change "report all four scorers" -> "report three scorers; Native OVERLAP parity validated, not reported."
- literature/arxiv_submission/current_draft/ADDITIONAL_INTEGRATIONS/SCORING_COMPARISON.md
  - Update framing to three reported scorers; mention native parity once for clarity.

Figures/captions:
- Any caption that says "same predictions under four scoring methodologies" -> "three scoring methodologies."
- Ensure figure legends/lines match three scorers (no duplicated line for Native OVERLAP).

## Exact Insert (Methods — parity note)

Insert under 04_methods.md, after the SzCORE paragraph in "Scoring Methodologies":

> We additionally implemented a native any-overlap scorer for validation and confirmed perfect parity with NEDC OVERLAP (identical metrics to four decimals). To reduce redundancy, we do not report Native OVERLAP separately.

## Results Tables — what to remove

- Default configuration table: remove "Native OVERLAP" row.
- Operating-point bullets (10 FA/24h; 2.5 FA/24h; ~1 FA/24h): remove Native OVERLAP bullets.
- Keep the parity statement as a sentence near the table ("Validation: native OVERLAP equals NEDC OVERLAP; omitted from tables").

## Text that must change "four" -> "three"

- Introduction: paragraph describing "four scoring methodologies" -> "three scoring methodologies."
- Results introduction sentence listing scorers.
- Any figure captions or section headers referencing four scorers.

## Numbers — unchanged

- NEDC TAES, NEDC OVERLAP, SzCORE values remain exactly as currently stated (defaults, 10 FA/24h, 2.5 FA/24h, and ~1 FA/24h comparison).
- AUROC remains 0.9019.

## Checks & Verification

- Assemble draft: `bash assemble.sh` and verify minimal diffs limited to intended sections.
- Search hygiene:
  - `rg -n "Native OVERLAP|Native\s+OVERLAP|native any-overlap" literature/arxiv_submission/current_draft` — should only remain in Methods parity sentence and Appendix C.3 title/body.
  - `rg -n "four scoring" literature/arxiv_submission/current_draft` — should be 0 after edits.
- Visual scan tables/figures to ensure only three scorers appear.

## Optional (future additions; not blocking)

- Add EPOCH/sample-based scores from NEDC summaries for defaults and clinical operating points.
- Add TUSZ parameters achieving ~71.1% event-based sensitivity (Table III match) and report FA/24h.

## Execution Order

1) Edit RESULTS.md and COMPLETE_RESULTS_COLLATED.md: remove Native OVERLAP rows; add reporting-policy note.
2) Update split draft sections (02/04/05/11) as above; reassemble and review diff.
3) Update ADDITIONAL_INTEGRATIONS docs (RESULTS_ROOT.md, SCORING_COMPARISON.md) to "three scorers."
4) Sweep captions and Intro for "four" -> "three".
5) Run search hygiene checks and final assemble.

## Quick Reference — Files

- literature/arxiv_submission/current_draft/04_methods.md
- literature/arxiv_submission/current_draft/05_results.md
- literature/arxiv_submission/current_draft/02_introduction.md
- literature/arxiv_submission/current_draft/11_appendix.md
- literature/arxiv_submission/current_draft/RESULTS.md
- literature/arxiv_submission/current_draft/COMPLETE_RESULTS_COLLATED.md
- literature/arxiv_submission/current_draft/ADDITIONAL_INTEGRATIONS/{RESULTS_ROOT.md,SCORING_COMPARISON.md}

