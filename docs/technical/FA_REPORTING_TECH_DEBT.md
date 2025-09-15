# Technical Debt: FA/24h Reporting Consistency (TAES vs OVERLAP)

Owner: Evaluation/Scoring
Priority: High (clarity and credibility)
Status: Pending (documented; implementation planned)

Problem
- We mixed different FA/24h definitions when summarizing results:
  - TAES: per‑label (SEIZ) “False Alarm Rate per 24 hours”.
  - OVERLAP: OVERALL “Total False Alarm Rate per 24 hours” (SEIZ + BCKG).
- This makes OVERLAP look worse on FA while it’s just a semantic mismatch, not a scoring paradox.

Current State
- FINAL_COMPLETE_RESULTS.md includes a note explaining the mismatch and points to SCORING_FA_DEFINITIONS.md.
- Verified “no merge_gap” numbers are correct and sourced directly from NEDC outputs.
- Native OVERLAP parity with NEDC OVERLAP is confirmed.

Decision Needed (choose one reporting policy)
- Option A (recommended): Show both FA columns for each scorer
  - FA/24h (SEIZ) and FA/24h (TOTAL). Most transparent and prevents confusion.
- Option B: Report SEIZ‑only FA for both TAES and OVERLAP
  - Apples‑to‑apples; hides TOTAL information unless expanded.
- Option C: Report TOTAL FA for both (if available)
  - TAES TOTAL isn’t explicitly printed; would require deriving or omitting.

Plan (once a policy is chosen)
1) Parser + Metrics schema
- Implement robust extraction in a single module (e.g., evaluation/nedc_eeg_eval/nedc_scoring/parse_nedc_summary.py):
  - TAES: FA/24h (SEIZ)
  - OVERLAP: FA/24h (SEIZ), FA/24h (TOTAL)
- Update run_nedc.py to emit metrics.json with explicit fields:
  - taes.seiz.sensitivity_percent
  - taes.seiz.fa_per_24h
  - overlap.seiz.sensitivity_percent
  - overlap.seiz.fa_per_24h
  - overlap.total_fa_per_24h
  - background false alarms if needed

2) CLI/reporting switch
- Add a flag to run_nedc.py: --fa_reporting {seiz,total,both} (default=both)
- Tables use the chosen mode consistently.

3) Update docs + tables
- FINAL_COMPLETE_RESULTS.md: display both columns or correct single definition per policy.
- SCORING_FA_DEFINITIONS.md: reflect the final policy and examples.

4) Tests
- Add unit tests for parser against fixtures covering both TAES and OVERLAP.
- Add an integration test asserting the metrics.json schema and values for both SEIZ and TOTAL.

5) Guardrails (related hygiene)
- Enforce merge_gap=None in scoring paths (raise if != 0). Add a clear error message pointing to MERGE_GAP_POLICY.md.
- Add a CI check or test that fails if merge_gap != 0 is observed in params.json or output markers.

Acceptance Criteria
- One documented policy for FA reporting; implemented consistently across code and docs.
- run_nedc.py writes a metrics.json containing SEIZ and (if applicable) TOTAL FA values.
- FINAL tables use the selected policy; ambiguity removed.
- Tests cover both TAES and OVERLAP extraction and the new metrics schema.
- merge_gap usage is blocked by code in evaluation/nedc_eeg_eval/nedc_scoring to prevent regressions.

Notes
- If the team wants strict comparability with Temple publication conventions, SEIZ‑only may be preferred; otherwise, “both” provides maximum transparency.
