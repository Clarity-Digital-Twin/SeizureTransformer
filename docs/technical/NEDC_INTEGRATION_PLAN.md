# 🏆 NEDC EVALUATION SYSTEM INTEGRATION PLAN
## From External NEDC Dependencies to Owned Clinical Evaluation Engine

Branch: `feature/integrate-nedc-evaluation`
Status: APPROVAL NEEDED → EXECUTE
Owner: Evaluation Working Group (ML + Clinical)

Canonical: This document is the single source of truth (SSOT) for NEDC integration. All other files must link here; do not duplicate the plan.

## 🎯 Executive Summary

Current state
```
Pipeline → NEDC v6.0.0 binary (external) → TAES scoring
        → Temple Python libs (external) → CSV parsing
        → Shell scripts (fragile) → Results
```

Target state (owned, reproducible, clinically viable)
```
evaluation/               ← Integration layer (ours, typed, tested)
└── nedc_scoring/
    ├── convert_predictions.py   ← Checkpoint → CSV_bi
    ├── post_processing.py       ← Threshold/morphology/duration/merge
    ├── run_nedc.py              ← Orchestration + parsing
    └── sweep_operating_point.py ← Dev-only tuning

seizure_evaluation/       ← Optional: native Python TAES (future)
```

Why now
- Clinical bottleneck: FA/24h ≈ 137.5 vs target ≤ 10.
- Publication-grade metrics require official NEDC compatibility.
- Reproducibility: deterministic evaluations, pinned deps, audit trail.

Guiding principles
- Vendor isolation: never modify `evaluation/nedc_eeg_eval/**`.
- Evaluation-first: tune on dev only, freeze, run once on eval.
- Edge-case safe: 256 Hz per-sample, correct labels, no double sigmoid, truncation-safe.
- Tool/results separation: code in `evaluation/**`, artifacts in `experiments/**`.
- CI-grade hygiene: ruff, mypy, pytest on our code; vendor excluded.

## 🧭 Scope & Streams

- Scope: NEDC evaluation pipeline only (conversion, scoring, parsing, provenance, backend toggle). Model refactors live in `INTEGRATION_PLAN.md`. Tuning workflow is a separate stream.
- Streams and naming (to avoid phase confusion):
  - Stream E — Evaluation backend
    - E1: Integrate official NEDC v6.0.0 and CSV_bi pipeline
    - E2: Conformance suite + golden fixtures
    - E3: Backend toggle + side-by-side comparison
    - E4: Native TAES implementation (optional)
  - Stream T — Operating-point tuning
    - T1: Dev sweep (threshold/morph/min-duration/merge)
    - T2: Freeze parameters + provenance
    - T3: Single eval run + archive results

## 📊 Current Architecture (as-implemented in repo)

```
evaluation/
├── nedc_eeg_eval/v6.0.0/        # Official scorer (binary + py utils) — VENDORED
└── nedc_scoring/                # Our clean integration layer
    ├── convert_predictions.py
    ├── post_processing.py
    ├── run_nedc.py
    ├── sweep_operating_point.py
    └── Makefile (all|convert|score|test)

experiments/
├── dev/                         # Dev-only tuning results
└── eval/                        # Frozen operating point results
```

Known issues/risk areas
- NEDC binary is platform-specific; recommend WSL on Windows.
- CSV_bi formatting must be exact (headers, precision, durations, bname).
- Time alignment and event merging semantics must match NEDC expectations.

## 🏗️ Streams & Phases

- Stream E (Evaluation backend)
  - E1: Keep official NEDC v6.0.0 as source of truth; vendor isolate.
  - E1/E2: Own conversion→CSV_bi pipeline and build conformance suite with golden outputs.
  - E3: Implement backend toggle and side-by-side comparison output.
  - E4: Implement native `seizure_evaluation` TAES scorer matching NEDC within tolerance.
- Stream T (Operating-point tuning)
  - T1: Sweep post-processing parameters on dev.
  - T2: Freeze chosen parameters with provenance.
  - T3: Run once on eval and archive.

## 🧩 Technical Specifications (must-not-break invariants)

Data/time semantics
- Sampling: 256 Hz; per-sample labels; predictions truncated to recording length.
- No double-sigmoid: use raw logits→sigmoid exactly once (if needed) and only once.
- Event intervals: use [start, stop) semantics to avoid double counting touching events.
- Durations: compute in seconds with precise sample-to-time mapping: `t = idx / 256.0`.
- Rounding: match NEDC printing precision to 4 decimals in CSV_bi.

CSV_bi format (both ref and hyp)
- Headers:
  - `# version = csv_v1.0.0`
  - `# bname = <base_file_name>`
  - `# duration = <seconds> secs`
- Columns: `channel,start_time,stop_time,label,confidence`.
- Channel: `TERM`. Label: `seiz`. Confidence: `1.0000` for events.
- List files: absolute paths; stable ordering; paired `ref.list`/`hyp.list`.

Operating-point post-processing
- Parameters: `threshold ∈ [0,1]`, `kernel_size ∈ ℕ+ (odd)`, `min_duration_sec ≥ 0`, `merge_gap_sec ≥ 0`.
- Morphology defined in discrete time (samples), not seconds (convert via 256 Hz).
- Merge after duration filtering to reduce false splits.

NEDC TAES parsing
- Parse `summary.txt` with robust regex; capture sensitivity, F1, FA/24h.
- Persist parsed metrics to `experiments/*/metrics.json` with full provenance.

## 🧰 Tooling & CI Policy

- Ruff: `pyproject.toml` excludes `evaluation/nedc_eeg_eval/**`.
- Mypy: `mypy.ini` excludes vendor; check our modules only.
- Pytest: markers for `nedc`/`conformance`/`clinical`; strict markers.
- Make: top-level `make install|lint|typecheck|test|run-eval-*` and `make -C evaluation/nedc_scoring all`.
- Lockfiles: `uv.lock` present; `make install` uses `uv` for reproducible env.

Action items
- Add conformance tests and golden fixtures (see below).
- Add CI skip when NEDC binary missing; run nightly full conformance on a runner with NEDC.

## ✅ Conformance & Golden Tests (gating)

Fixtures (commit to repo)
- `tests/fixtures/nedc/ref/*.csv_bi`, `tests/fixtures/nedc/hyp/*.csv_bi` (tiny curated set).
- `tests/fixtures/nedc/expected_metrics.json` (from a one-time NEDC run).

Tests
- `tests/integration/test_nedc_compatibility.py`
  - Run official NEDC on fixtures and compare parsed metrics to `expected_metrics.json`.
  - Mark with `@pytest.mark.nedc`; auto-skip if binary not found.
- `tests/integration/test_native_taes.py` (E4)
  - Compare native scorer to official metrics within tolerance: ±0.1% sensitivity, ±0.1 FA/24h.

Gates (must pass before switching defaults)
- Conformance delta ≤ tolerance on fixtures AND a sampled subset of dev split.
- End-to-end dev run parity check: official vs native within tolerance.

## 🎛️ Backend Toggle & Migration

- `evaluation/nedc_scoring/run_nedc.py` supports `--backend {nedc-binary,native-taes}` (default: `nedc-binary`).
- Side-by-side mode: run both backends and emit `comparison.json` (diff per metric).
- Change default to `native-taes` only after conformance + clinical gates clear.

## 📈 Operating-Point Tuning Workflow (Stream T: T1→T3)

Dev-only tuning (T1)
- Sweep parameters: `threshold`, `kernel_size`, `min_duration_sec`, `merge_gap_sec`.
- Objective: minimize FA/24h subject to sensitivity ≥ 50%.
- Output: `experiments/dev/<tag>/recommendation.json` with chosen params + evidence.

Freeze (T2)
- Copy the chosen params to `experiments/eval/<tag>/operating_point.json`.
- Record provenance: commit SHA, data split hash, scorer backend, NEDC version.

Eval (single run) (T3)
- Run exactly once on eval split with frozen params.
- Store results in `experiments/eval/<tag>/metrics.json` and raw `summary.txt`.

CLI examples
```
# Convert + score with official NEDC
make -C evaluation/nedc_scoring all CHECKPOINT=experiments/dev/checkpoint.pkl

# Sweep operating points (dev)
python evaluation/nedc_scoring/sweep_operating_point.py \
  --checkpoint experiments/dev/checkpoint.pkl --outdir experiments/dev/sweeps

# Score eval with frozen params
python evaluation/nedc_scoring/run_nedc.py --outdir experiments/eval/<tag> \
  --threshold 0.82 --kernel 5 --min-duration 2.0 --merge-gap 1.0 --score-only
```

## 📜 Data Contracts & Artifacts

Artifacts (write-once)
- `experiments/**/checkpoint.pkl` — predictions (per-sample, 256 Hz), no double sigmoid.
- `experiments/**/metrics.json` — parsed metrics, operating point, backend, commit SHA.
- `experiments/**/summary.txt` — raw NEDC output (immutable evidence).
- `experiments/**/params.json` — frozen operating point.

Durability
- Never rename or mutate existing experiment directories; create new `<tag>` if re-running.
- Include a top-level `experiments/README.md` describing structure and retention policy.

## 🖥️ Environment & OS Support

Windows
- Prefer WSL for running `nedc_eeg_eval` binary; Python integration runs cross-platform.
- Use `pathlib` throughout; avoid shell path manipulation in Python.
- Normalize line endings when writing CSV (`newline='\n'`).

Env variables
- `NEDC_NFC`: points to `evaluation/nedc_eeg_eval/v6.0.0`.
- `PATH` and `PYTHONPATH` updated transiently in `run_nedc.py` before invocation.

## ⚙️ Performance & Robustness Budgets

- Dev sweep completes ≤ 2 hours on target hardware; use parallelization where safe.
- CSV_bi generation O(N) in samples with vectorized ops (NumPy preferred).
- Handle empty events, short recordings, malformed inputs; fail fast with actionable errors.

## 🔐 Compliance, Licensing, Audit

- Keep NEDC vendor code pristine; retain `CITATION.md` and any LICENSE files.
- Document dataset version (TUSZ) and split definitions; include hashes of list files.
- Provenance: include OS, Python, package versions (`pip freeze` snapshot in run folder).

## 🔄 Rollout & Gates

Rollout
- Stream E: E1/E2 first; E3 when stable; E4 optional.
- Stream T: T1 on dev; T2 freeze; T3 eval once.

Acceptance gates
- Conformance on fixtures: within tolerance.
- Dev split parity check: within tolerance.
- Clinical targets achieved on eval: FA/24h ≤ 10, sensitivity ≥ 50%.

Rollback
- Feature flag (`--backend`); keep official binary pipeline operational at all times.
- Results immutability and versioned params enable rapid rollback.

## 📅 Timeline & Milestones

| Stream | Phase | Duration | Milestone | Key Deliverables |
|--------|-------|----------|-----------|------------------|
| E      | E1/E2 | 3–5 days | Integration & Conformance | Golden fixtures, parsing, CI skip, gating |
| T      | T1/T2 | 3–4 days | Clinical Tuning | Dev sweeps, recommendation.json, freeze plan |
| T      | T3    | 2–3 days | Eval Run | Frozen params, single eval, metrics archived |
| E      | E4    | 4–7 days | Native TAES (optional) | Python scorer, parity tests, backend toggle |

Critical path
E1/E2 → T1/T2 → T3. E4 can run in parallel once E2 completes.

## ✅ Sign-off Checklist

Technical
- [ ] Vendor isolation (no lint/type/format on `evaluation/nedc_eeg_eval/**`).
- [ ] Golden fixtures and conformance tests committed.
- [ ] Backend toggle in place with side-by-side compare.
- [ ] Robust CSV_bi generator and list files (absolute paths).

Clinical
- [ ] Operating-point tuning documented; dev-only; freeze before eval.
- [ ] Clinical targets explicit (FA/24h ≤ 10; sensitivity ≥ 50%).
- [ ] Audit trail and provenance recorded in `experiments/**`.

Operational
- [ ] CI config: ruff, mypy, pytest on our code; skip NEDC-dependent tests if binary absent.
- [ ] Make targets documented (`make -C evaluation/nedc_scoring all`).
- [ ] Windows guidance (WSL) documented in `evaluation/README.md`.

— End of plan —

