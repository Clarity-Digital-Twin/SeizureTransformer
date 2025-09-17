# Cleanup Refactoring Plan (Phase 2 → 3)

This document tracks all remaining cleanup after the src/ migration. Goal: remove shims, eliminate path hacks, and finalize a crisp structure that clearly separates vendored tools from first‑party code.

See also: `docs/VENDORED_SOURCES.md` for vendored provenance and policy.

Scope is limited to our code; do not edit vendored trees: `wu_2025/` and `evaluation/nedc_eeg_eval/`.

## Goals

- Remove backwards‑compatibility shims and any `sys.path` edits in shims.
- Align Makefile, docs, and examples to new CLI entry points and package paths.
- Resolve packaging edge cases (notably `nedc-run`).
- Keep `evaluation/` vendor‑only; keep all first‑party code under `src/seizure_evaluation/`.

## Current Structure (snapshot)

- First‑party package: `src/seizure_evaluation/{ovlp,tusz,szcore,utils}`
- Vendored: `wu_2025/`, `evaluation/nedc_eeg_eval/**`
- Shims (temporary): `evaluation/{tusz,utils,szcore_scoring}`
- Tooling: `pyproject.toml` (src layout), `Makefile`, tests under `tests/`

## Shim Inventory and Actions

All shims emit `DeprecationWarning` and insert `src` onto `sys.path` so they work without editable installs. Plan is to remove shims entirely after downstream migration and stop path edits.

1) `evaluation/tusz/run_tusz_eval.py`
   - Purpose: Redirect to `src/seizure_evaluation/tusz/cli.py:main`.
   - Current: `# ruff: noqa`, `sys.path` insert, re-exports, `main()` if __main__.
   - Action: Remove file after migration window. Update all docs to use `tusz-eval` or `python -m seizure_evaluation.tusz.cli`.

2) `evaluation/utils/edf_repair.py`
   - Purpose: Re-export from `seizure_evaluation.utils.edf_repair`.
   - Current: `# ruff: noqa`, `sys.path` insert.
   - Action: Remove file after migration. Replace imports in any internal scripts or docs.

3) `evaluation/utils/enhance_evaluation_robustness.py`
   - Purpose: Re-export from `seizure_evaluation.utils.enhance_evaluation_robustness`.
   - Current: `# ruff: noqa`, `sys.path` insert.
   - Action: Remove file after migration. Update imports in docs/scripts if present.

4) `evaluation/szcore_scoring/run_szcore.py`
   - Purpose: Redirect to `seizure_evaluation.szcore.cli:main`.
   - Current: `# ruff: noqa`, `sys.path` insert, re-exports, `main()` if __main__.
   - Action: Remove file after migration. Prefer `szcore-run` or `python -m seizure_evaluation.szcore.cli` in docs/Makefile.

5) `evaluation/szcore_scoring/convert_to_hedscore.py`
   - Purpose: Re-export from `seizure_evaluation.szcore.convert_to_hedscore`.
   - Current: `# ruff: noqa`, `sys.path` insert.
   - Action: Remove file after migration. Update references.

Notes:
- `evaluation/nedc_eeg_eval/nedc_scoring/*` stays vendor/tooling territory. We do not move these modules; they already import the native scorer via `seizure_evaluation.ovlp.overlap_scorer` and will continue to work post-shim removal.

## Packaging and CLI Cleanups

- `pyproject.toml`
  - OK: src layout is active; package is `src/seizure_evaluation`.
  - FIXED: `nedc-run` now points to `seizure_evaluation.nedc.cli:main` (wrapper that defers to vendored tools when present).

- Makefile
  - Lint/format/typecheck: Correctly target `src/ evaluation/ scripts/ tests/`.
  - Docker smoke tests now override entrypoint to run `tusz-eval --help` and `nedc-run --help` inside the container for CLI availability.
  - Benchmark/sweep: Prefer `szcore-run` and the NEDC scripts via the stable module path under `evaluation/nedc_eeg_eval/nedc_scoring` or via the wrapper.

## Docs and Examples to Update

- `README.md`: Update invocation examples to `tusz-eval` / `szcore-run` and new import paths (`seizure_evaluation.*`).
- `docs/` (including `RESTRUCTURE_PLAN.md`): Add a short deprecation banner and link to this cleanup plan.
- Any notebooks or analysis docs under `literature/` that import from legacy `evaluation.*` paths.

## Tests and Validation

- Add or keep lightweight smoke tests (integration):
  - `tusz-eval --help` and `szcore-run --help` run.
  - Shims still executable for one release (e.g., `python evaluation/tusz/run_tusz_eval.py --help`).
- Ensure no reliance on `sys.path` hacks:
  - Grep for `sys.path.insert` and `sys.path.append` outside vendored trees and eliminate.
- Keep existing NEDC-marked tests behavior (skip if binary not present).

## Removal Checklist (proposed 1-release window)

- [ ] Announce new imports/CLIs in README and docs.
- [ ] Migrate Makefile and Docker targets to new CLIs.
- [ ] Grep and fix all in-repo imports:
  - [ ] `rg -n "from evaluation\.tusz|evaluation\.utils|evaluation\.szcore_scoring"`
- [ ] Decide `nedc-run` policy:
  - [ ] Dev-only entry or wrapper under `src/seizure_evaluation/nedc/cli.py`.
- [ ] Add minimal CLI smoke tests (optional but recommended).
- [ ] Remove shims:
  - [ ] `evaluation/tusz/run_tusz_eval.py`
  - [ ] `evaluation/utils/edf_repair.py`
  - [ ] `evaluation/utils/enhance_evaluation_robustness.py`
  - [ ] `evaluation/szcore_scoring/run_szcore.py`
  - [ ] `evaluation/szcore_scoring/convert_to_hedscore.py`

## Open Decisions / Tech Debt Log

- nedc-run entry point: dev-only vs. packaged wrapper (choose one).
- Makefile Docker commands still reference `eval`/`nedc` aliases — update to new CLIs.
- CRLF normalization: one or two files showed EOL normalization in prior work; keep `.gitattributes` consistent if needed.

## Ready-to-run Commands

- Lint/format/tests: `make format && make lint && make test`
- New TUSZ CLI: `tusz-eval --data_dir /path/to/TUSZ/dev --out_dir experiments/dev/baseline --device auto`
- NEDC tools (unchanged): `make -C evaluation/nedc_eeg_eval/nedc_scoring all CHECKPOINT=../../experiments/eval/baseline/checkpoint.pkl OUTDIR=../../experiments/eval/baseline/nedc_results`

---

When the checklist is complete, the repository will be fully clean: no shims, no path hacks, clear boundaries, and consistent tooling/docs.
