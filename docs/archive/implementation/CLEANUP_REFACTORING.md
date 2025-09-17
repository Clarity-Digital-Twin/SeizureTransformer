# Phase 3 Cleanup — Finalized

Scope: our code only. Vendored trees remain untouched: `wu_2025/`, `evaluation/nedc_eeg_eval/`.

## What Changed

- Adopted src/ layout fully; all first‑party code lives under `src/seizure_evaluation/`.
- Fixed `nedc-run` entry point with a wrapper at `src/seizure_evaluation/nedc/cli.py` (dev‑only; expects vendored `evaluation/` available).
- Removed remaining `sys.path` hacks from src/ (kept only the guarded addition inside the dev‑only NEDC wrapper).
- Updated Makefile + Docker entrypoint to use CLIs:
  - `tusz-eval` for TUSZ predictions
  - `szcore-run` for SzCORE scoring
  - `nedc-run` wrapper for NEDC orchestration
- Deleted all back‑compat shims under `evaluation/`.

## Shims Removed (complete)

- evaluation/tusz/run_tusz_eval.py
- evaluation/utils/edf_repair.py
- evaluation/utils/enhance_evaluation_robustness.py
- evaluation/szcore_scoring/run_szcore.py
- evaluation/szcore_scoring/convert_to_hedscore.py
- evaluation/szcore_scoring/__init__.py

## Docs Updated

- README: Docker notes and CLI guidance now use `tusz-eval` / `nedc-run` / `szcore-run`.
- RESULTS_ROOT.md: SzCORE step now uses `szcore-run`.
- evaluation/README.md: Removed shim references; utils tree cleaned.
- Technical docs: updated references in MERGE_GAP_POLICY.md and REPO_MAP.md.

## Verification

- Lint: `make lint` → OK
- Tests: `make test` → 53/53 passed
- Smoke: CLIs `--help` work in container via Makefile `docker-smoke` targets

## Notes / Policies

- License: Apache‑2.0 (LICENSE and pyproject synced)
- NEDC wrapper (`nedc-run`) is dev‑only by design; it defers to vendored NEDC tools.
- `evaluation/` is now tools/vendor only; no first‑party code remains there.

This completes Phase 3 cleanup. The repository now presents a clear, modern structure with vendor boundaries and stable CLIs.

