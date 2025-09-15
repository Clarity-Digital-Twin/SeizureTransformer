# MERGE_GAP Policy, Risks, and Safe Removal Plan

Owner: Evaluation/Scoring
Priority: Critical (standards compliance, reproducibility)
Status: Phase 1 (hard-block) and Phase 2 (removal) completed; CI guards in place

## Summary
- The `merge_gap`/`merge_gap_sec` flag merges nearby predicted events in post‑processing. This lowers false alarms by collapsing short gaps, but it is non‑standard and not part of Temple/NEDC evaluation.
- For academic/clinical reporting and cross‑scorer parity, `merge_gap` must remain disabled. All canonical results are computed with `merge_gap=None`.
- This document enumerates where the flag still appears, why it is risky, and a phased plan to deprecate and remove it safely with guardrails and verification.

## Why Remove It
- Standards: NEDC TAES/OVERLAP do not include a pre‑scoring merge of predicted events. Enabling it invalidates comparisons.
- Reproducibility: It changes FA/24h dramatically (~3–4× reduction observed), masking trade‑offs.
- Double‑merge risk: SzCORE already merges events internally (90 s). Merging in post‑processing risks double‑merging and optimistic FA.

## Where It Existed (now removed)
- Post‑processing (implementation):
  - `evaluation/nedc_eeg_eval/nedc_scoring/post_processing.py` → formerly accepted `merge_gap_sec`; now removed. Utility `merge_nearby_events(...)` retained (not used by evaluation).
- NEDC conversion/runner (CLI/API):
  - `convert_predictions.py` and `run_nedc.py` previously exposed `--merge_gap_sec`; flag and plumbing removed.
  - `sweep_operating_point.py` previously accepted `--merge_gaps`; option and plumbing removed.
- Other tools:
  - `scripts/experiment_tracker.py` previously accepted/recorded `merge_gap_sec`; field removed.
  - `evaluation/szcore_scoring/run_szcore.py` explicitly sets `merge_gap_sec=None` (correct)
  - `evaluation/szcore_scoring/convert_to_hedscore.py` uses `merge_gap_sec=None` (to avoid double‑merge); no change required
  - Tests: references to merge_gap removed from evaluation tests; `merge_nearby_events` still unit‑tested
  - CI: sweep no longer passes merge_gap arguments; added compliance checks guarding against reintroduction

## Policy
- Academic and clinical metrics must be computed with `merge_gap=None`.
- The repo must not accept non‑None `merge_gap` in any evaluation path. If provided, explicitly fail with a clear error that points to this policy.
- Keep `merge_nearby_events(...)` as a utility for research notebooks, but it must not be reachable from scoring codepaths.

## Deprecation and Removal Plan

Phase 0 — Policy freeze (already in place)
- Defaults documented as `merge_gap=None` in RESULTS_ROOT and status docs.
- Warnings + disclaimers land when non‑standard values are provided.

Phase 1 — Hard‑block usage (no behavior change when compliant)
- NEDC pipeline:
  - In `convert_predictions.py`: if `merge_gap_sec not in (None, 0, 0.0)`, raise `ValueError` with a link to this doc. Keep the CLI flag for now but make it unusable (explicit error).
  - In `run_nedc.py`: same validation before calling conversion. Keep writing `operating_point.json` with `merge_gap_sec: 0.0`.
  - In `sweep_operating_point.py`: remove non‑zero values from `--merge_gaps` help and validation; if any non‑zero is supplied, exit with error.
- Experiments:
  - In `scripts/experiment_tracker.py`: accept but ignore `merge_gap_sec` (force `None` in the produced config) and print a one‑line warning. Plan to remove the field in Phase 2.
- Tests/CI:
  - Update tests that expect a warning file to instead expect a hard error on non‑zero `merge_gap_sec`.
  - Add a CI guard that fails if `merge_gap_sec` appears in any CLI arguments or JSON manifests with a non‑zero value.
  - Optional: add a unit test that asserts neither conversion nor scoring produce `NONSTANDARD_POSTPROCESSING.txt` under compliant settings.

Phase 2 — Remove flags and parameters (breaking surface changes)
(Completed)
- Post‑processing:
  - Remove `merge_gap_sec` from `apply_seizure_transformer_postprocessing` signature and implementation. Keep `merge_nearby_events` as a separate, documented helper not used by evaluation.
- NEDC pipeline:
  - `--merge_gap_sec` removed from `convert_predictions.py` and `run_nedc.py` CLIs and code (disclaimers removed).
  - `--merge_gaps` removed from `sweep_operating_point.py`; naming simplified.
- Experiments:
  - Remove `merge_gap_sec` from `scripts/experiment_tracker.py` (CLI and JSON). For backwards compatibility, if the field exists in a historic config JSON, ignore it with a one‑line notice.
- Tests:
  - Remove tests asserting merge behavior via the main post‑processing; keep unit tests for `merge_nearby_events` under a utils test module.
- Docs:
  - Update any references to `merge_gap` to clarify it is no longer available in evaluation codepaths.

Phase 3 — Cleanup and enforcement
- Remove any dead code paths, manifest keys, and log messages related to merge_gap.
- Add a simple lint/CI check to grep for `merge_gap_sec` in source and fail if found outside of this policy doc or the `merge_nearby_events` utility/test.

## File‑by‑File Tasks (Phase 1 → Phase 2)

- `evaluation/nedc_eeg_eval/nedc_scoring/post_processing.py`
  - Phase 1: Add a guard at the top of `apply_seizure_transformer_postprocessing`: if `merge_gap_sec not in (None, 0, 0.0)`: raise `ValueError("merge_gap_sec is deprecated and disallowed. See docs/technical/MERGE_GAP_POLICY.md")`.
  - Phase 2: Remove `merge_gap_sec` from the signature and the optional merge step. Keep `merge_nearby_events(...)` exported with a docstring noting it is not used for evaluation.

- `evaluation/nedc_eeg_eval/nedc_scoring/convert_predictions.py`
  - Phase 1: Validate input; if non‑zero `merge_gap_sec`, raise. Keep `params.json` writing `merge_gap_sec: 0.0` for reproducibility.
  - Phase 2: Remove the CLI flag and param; stop writing the merge field in `params.json`.

- `evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py`
  - Phase 1: Validate and disallow non‑zero `merge_gap_sec` early; keep warning message for `None` vs `0` equivalence removed.
  - Phase 2: Remove the flag entirely, delete related disclaimer and operating‑point merge field.

- `evaluation/nedc_eeg_eval/nedc_scoring/sweep_operating_point.py`
  - Phase 1: Change `--merge_gaps` default to `0` and error on any non‑zero value; do not pass it through.
  - Phase 2: Remove the option and all plumbing (`merge_gap` from `Result` dataclass, CSV columns, recommended JSON).

- `evaluation/szcore_scoring/*`
  - Confirm all calls pass `merge_gap_sec=None`. No change required; keep comments explaining “avoid double‑merge; SzCORE merges internally (90s)”.

- `scripts/experiment_tracker.py`
  - Argument and field removed; historic configs ignored if present.

- Tests
  - Phase 1: Update `tests/test_convert_predictions.py` to expect a `ValueError` when a non‑zero merge gap is provided.
  - Phase 2: Remove tests referring to the parameter. Keep unit tests for `merge_nearby_events` under a neutral utils test (not part of evaluation pipeline tests).

- CI (`.github/workflows/nedc-conformance.yml`)
  - Removed sweep argument; added guard to fail if any artifact contains `merge_gap_sec` or writes `NONSTANDARD_POSTPROCESSING.txt`.

## Verification Plan (invariants and parity)
- NEDC parity:
  - Re‑run the default pipeline on TUSZ eval and confirm OVERLAP and TAES numbers exactly match the current canonical “no merge” results.
- SzCORE parity:
  - Re‑run SzCORE evaluation with `merge_gap_sec=None` to confirm no change.
- Config/manifest hygiene:
  - Verify `params.json` contains no `merge_gap_sec` (Phase 2). During Phase 1, it must be `0.0` when present.
- Guardrails:
  - Add a small test that scans produced result directories for `NONSTANDARD_POSTPROCESSING.txt` and fails the test suite if found.

## Rollback
- If a downstream consumer relied on merged events, restore the `merge_nearby_events(...)` helper in userland (not wired into evaluation). Provide a small example snippet in a notebook; do not re‑introduce the flag into evaluation CLIs.

## Acceptance Criteria
- It is impossible to run evaluation with a non‑None/positive `merge_gap`.
- No CLI or config surfaces expose `merge_gap` in the evaluation codepaths.
- Canonical results remain unchanged (parity with existing “no merge” SSOT).
- Documentation clearly states the policy and the rationale, and tests/CI enforce it.

---

For background and results context, see:
- `RESULTS_ROOT.md` (SSOT for publication results; all without merge_gap)
- `docs/status/SINGLE_SOURCE_OF_TRUTH.md`
- `docs/evaluation/NEDC_METRICS_OVERVIEW.md`
- `docs/technical/FA_REPORTING_TECH_DEBT.md` (FA reporting policy, references this document)
