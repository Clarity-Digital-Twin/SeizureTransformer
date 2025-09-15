# Repository Map and Single Source of Truth (SSOT)

Last updated: 2025-09-15

This document is the top‑level orientation for where things live, what is canonical, and what is legacy/experimental. It complements the detailed README and docs/ tree by calling out the Single Source of Truth (SSOT) for the TUSZ evaluation + scoring pipeline and highlighting cleanup items.

## TL;DR

- Canonical pipeline: `evaluation/tusz/run_tusz_eval.py` → `evaluation/nedc_eeg_eval/nedc_scoring/*` → results in `experiments/`.
- Vendored/immutable: `wu_2025/` (upstream model) and `evaluation/nedc_eeg_eval/v6.0.0/` (Temple NEDC binaries) — do not modify.
- Native scorer exists for parity/testing only: `seizure_evaluation/` — not used by the production pipeline.
- Channel order: correct by position; names differ only. Do not “fix” channels; use our evaluation entrypoint.

## What’s Canonical (SSOT)

- Inference (TUSZ): `evaluation/tusz/run_tusz_eval.py`
  - Loads EDFs positionally (19 channels required), matches Wu model expectations.
  - Produces `checkpoint.pkl` in `experiments/...` for scoring.
  - Config: `--batch_size` (default 512), device auto/cpu/cuda.

- NEDC Scoring Orchestration: `evaluation/nedc_eeg_eval/nedc_scoring/`
  - `convert_predictions.py` → writes NEDC CSV_bi + lists.
  - `post_processing.py` → thresholds, morphology, eventization (merge_gap deprecated).
  - `run_nedc.py` → invokes official NEDC v6.0.0, parses metrics.
  - Schema of `metrics.json` and pipeline behavior live here.

- Docker Entrypoint: `docker/entrypoint.py`
  - Modes: `eval` (default), `nedc`, `convert`, `wu`.
  - CPU image: `Dockerfile`. GPU image: `Dockerfile.gpu`.
  - Compose: removed to reduce confusion; prefer Make targets.
  - Make targets: `make docker-build`, `make docker-run`, `make docker-build-gpu`, `make docker-run-gpu`.

- Tests: `tests/`
  - Unit: post‑processing, conversion, native overlap.
  - Integration: NEDC conformance, native parity.
  - Treat test expectations as the contract for behavior.

## Vendored / Immutable

- Upstream Model (read‑only): `wu_2025/`
  - Original Wu code and weights. CLI available as `--mode wu` but not the default entrypoint.
  - Do not modify; our pipeline sits on top.

- Temple NEDC v6.0.0 (read‑only): `evaluation/nedc_eeg_eval/v6.0.0/`
  - Official scorer and libs. Do not modify; used via our wrappers in `nedc_scoring/`.

## Optional / Secondary

- SzCORE scoring wrapper: `evaluation/szcore_scoring/`
  - For EpilepsyBench Any‑Overlap comparisons using `timescoring`.
  - Not used for TUSZ clinical reporting; NEDC remains primary on TUSZ.

## Native Implementation (Parity Only)

- Native OVERLAP scorer: `seizure_evaluation/`
  - Our clean Python implementation of Temple’s OVERLAP logic lives under `seizure_evaluation/ovlp/`.
  - Purpose: testability and parity checks with NEDC binaries.
  - Not part of the production scoring path; use `nedc_scoring` for official results.

## Clarifications for Previously Confusing Folders

- “nedc_scoring”
  - Canonical location is nested: `evaluation/nedc_eeg_eval/nedc_scoring/`.
  - If you see a historical `evaluation/nedc_scoring/`, treat it as legacy; delete or archive. All code now lives under the nested path beside the vendored NEDC v6.0.0.

- “tuz” vs “tusz”
  - Canonical directory: `evaluation/tusz/` (with “s”). Any references to “tuz” are historical typos.

## Channel Ordering Truth

- TUSZ provides channels in the same positional order the Wu model expects; only names differ (e.g., `EEG FP1-REF` vs `Fp1`).
- Our evaluation loads by position and validates count (19 channels). No channel remapping is required or performed.
- Wu’s strict CLI enforces exact names and will reject TUSZ — that’s why our Docker entry defaults to `eval` (our pipeline) and exposes `wu` as an optional mode only.

## Clean Run Paths

Local (CPU):
- `python evaluation/tusz/run_tusz_eval.py --data_dir wu_2025/data/tusz/v2.0.3/edf/eval --out_dir experiments/eval/baseline`
- `python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py --checkpoint experiments/eval/baseline/checkpoint.pkl --outdir experiments/eval/baseline/nedc_results`

Docker (CPU):
- `make docker-build && make docker-run`

Docker (GPU):
- `make docker-build-gpu && make docker-run-gpu`

Quality gates:
- `make quality` (ruff + mypy + pytest)

## Cleanup TODOs (Surgical)

These are the only items worth cleaning to reduce confusion. Avoid broader refactors unless needed.

1) Eliminate legacy paths and typos
- Ensure there is no stray `evaluation/nedc_scoring/` at repo root; all code must live under `evaluation/nedc_eeg_eval/nedc_scoring/`.
- Sweep docs/scripts for “tuz” and correct to “tusz”.

2) Mark native scorer as non‑canonical
- Add a short README in `seizure_evaluation/` clarifying it’s for parity/tests only. Keep it because tests rely on it.

3) Dockerfile hygiene
- Keep `Dockerfile` and `Dockerfile.gpu` as the only supported builds. Legacy test/working compose/scripts/logs removed.

4) Consistent entrypoints and docs
- README already shows the repository map. Link this REPO_MAP.md from README if further clarity is needed.

Acceptance criteria
- One canonical evaluation path documented and runnable end‑to‑end (local + Docker).
- No duplicate “nedc_scoring” trees.
- Tests, ruff, mypy green.
- README + this file tell the same story.

## Pointers to Detailed Docs

- Topical truth about channels and Docker: `CRITICAL_ARCHITECTURE_TRUTH.md`
- Evaluation tools overview: `evaluation/README.md`
- SSOT status and metrics policy: `docs/status/SINGLE_SOURCE_OF_TRUTH.md`
- Application architecture (broader plan): `docs/APPLICATION_ARCHITECTURE.md`
