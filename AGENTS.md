# Repository Guidelines

This document is a concise contributor guide tailored to this repository.

## Project Structure & Module Organization

- `src/seizure_evaluation/` — First‑party package (our code):
  - `tusz/cli.py` — TUSZ inference CLI (entry point: `tusz-eval`).
  - `szcore/` — SzCORE wrappers.
  - `ovlp/` — Native OVERLAP scorer (parity/testing).
  - `utils/` — EDF repair and helpers.
- `evaluation/` — Vendored tools and orchestration only:
  - `nedc_eeg_eval/nedc_scoring/` — NEDC conversion, scoring, sweeps (tools only).
  - `nedc_eeg_eval/v6.0.0/` — official NEDC software (untouched).
  - `tusz/`, `szcore_scoring/` — temporary shims that forward to `src/` (deprecated).
- `wu_2025/` — Original SeizureTransformer (vendored; do not modify).
- `experiments/` — Results and metadata (dev/eval runs, sweeps, logs).
- `scripts/` — Utilities (e.g., `experiment_tracker.py`).
- `tests/` — Pytest suite (fast, unit‑level checks).
- `docs/` — Technical docs and evaluation reports.

Keep tools in `evaluation/` and artifacts in `experiments/`. First‑party code lives under `src/`.

## Build, Test, and Development Commands

- Environment (dev):
  - `make setup-dev && source .venv/bin/activate`
- Lint/format/tests:
  - `make lint` (Ruff), `make format` (Ruff format + fixes), `make test` (pytest).
- Run TUSZ predictions:
  - `tusz-eval --data_dir /path/to/TUSZ/dev --out_dir experiments/dev/baseline --device auto`
- NEDC pipeline:
  - `make -C evaluation/nedc_eeg_eval/nedc_scoring all CHECKPOINT=../../experiments/eval/baseline/checkpoint.pkl OUTDIR=../../experiments/eval/baseline/nedc_results`

## Coding Style & Naming Conventions

- Python 3.10+, PEP8 via Ruff (line length 100).
- Names: modules/functions `snake_case`, classes `CamelCase`.
- Type hints encouraged; be pragmatic with third‑party interfaces.
- Do not lint/modify: `wu_2025/`, `evaluation/nedc_eeg_eval/`, `.venv/`, `literature/`.

Notes:
- Shims under `evaluation/{tusz,utils,szcore_scoring}` exist for backward compatibility and will be removed after migration; prefer importing from `seizure_evaluation.*`.

## Testing Guidelines

- Framework: `pytest` (see `tests/`).
- Test files: `tests/test_*.py`; keep tests fast and deterministic.
- Run: `make test` or `pytest -k <pattern>`.
- Don’t add tests inside third‑party directories.

## Commit & Pull Request Guidelines

- Use clear, actionable commits (Conventional Commits preferred: `feat:`, `fix:`, `docs:`…).
- Scope changes to “our” code; never edit `wu_2025/` or `nedc_eeg_eval/`.
- PRs should include: purpose, summary of changes, how to run/verify, and any impacts on docs.
- Do not commit large binaries or dataset files; store run outputs under `experiments/`.
- Ensure `make lint` and `make test` pass before opening a PR.

## Security & Configuration Tips

- NEDC env is auto‑handled by tools; avoid hard‑coding absolute paths in code.
- Keep PHI/PII out of logs and committed artifacts.
- Windows users: prefer Python CLIs or WSL; Makefiles and `.sh` scripts assume POSIX.
