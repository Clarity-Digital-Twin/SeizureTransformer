# Repository Restructure Plan: src/ layout and clear vendored boundaries

This plan proposes a modest, professional reorganization that separates first‑party
code from vendored tools and establishes a conventional `src/` layout. The goal is
to improve clarity, packaging, imports, and long‑term maintainability without
disrupting existing evaluation capabilities or tests.

## Objectives

- Keep vendored code isolated and untouched:
  - `wu_2025/` (original SeizureTransformer)
  - `evaluation/nedc_eeg_eval/` (official NEDC software + our wrappers)
- Move our first‑party evaluation helpers and pipelines into a proper package under `src/`.
- Preserve backwards compatibility via import shims during a deprecation period.
- Make CLI entry points discoverable (optional) rather than relying on ad‑hoc paths.

## Target Top‑Level Layout

```
repo/
  src/
    seizure_evaluation/                # our first‑party evaluation code (Python package)
      __init__.py
      ovlp/                            # native OVERLAP scorer parity impl
        __init__.py
        overlap_scorer.py
      tusz/                            # TUSZ prediction pipeline (CLI)
        __init__.py
        cli.py
      szcore/                          # Szcore integration utilities (CLI)
        __init__.py
        cli.py
        convert_to_hedscore.py
      utils/
        __init__.py
        edf_repair.py
        enhance_evaluation_robustness.py

  evaluation/                          # vendored tooling only (unchanged)
    nedc_eeg_eval/
      v6.0.0/                          # official Temple package, untouched
      nedc_scoring/                    # wrappers, conversion, sweeps (ours, keep path stable)

  wu_2025/                             # vendored ST reference code (unchanged)
  scripts/                             # general utilities (non‑package scripts)
  experiments/                         # run outputs and metadata
  tests/                               # pytest suite
  docs/                                # documentation
```

Notes:
- The `evaluation/` directory becomes vendor‑only. All first‑party helpers formerly under
  `evaluation/tusz`, `evaluation/utils`, and `evaluation/szcore_scoring` move into the
  `src/seizure_evaluation/` package.
- We retain `evaluation/nedc_eeg_eval/nedc_scoring/*` under the same path to avoid breaking
  conformance scripts and to align with “tools only” intent.

## File Move Map (Phase 1)

- `seizure_evaluation/ovlp/*` → `src/seizure_evaluation/ovlp/*` (no rename)
- `evaluation/tusz/run_tusz_eval.py` → `src/seizure_evaluation/tusz/cli.py`
- `evaluation/utils/edf_repair.py` → `src/seizure_evaluation/utils/edf_repair.py`
- `evaluation/utils/enhance_evaluation_robustness.py` → `src/seizure_evaluation/utils/enhance_evaluation_robustness.py`
- `evaluation/szcore_scoring/run_szcore.py` → `src/seizure_evaluation/szcore/cli.py`
- `evaluation/szcore_scoring/convert_to_hedscore.py` → `src/seizure_evaluation/szcore/convert_to_hedscore.py`

Vendored paths remain:
- `evaluation/nedc_eeg_eval/**` (untouched)
- `wu_2025/**` (untouched)

## Backwards‑Compatible Import Shims (Phase 1)

To avoid breaking imports and tests immediately, keep thin modules under the original
paths, re‑exporting from the new package and emitting a deprecation warning:

- `evaluation/tusz/run_tusz_eval.py` (shim)
  - from `seizure_evaluation.tusz.cli` import `main` (and any helpers used directly)
  - if executed as a script, call `main()`

- `evaluation/utils/*.py` (shims)
  - re‑export from `seizure_evaluation.utils.*`

- `evaluation/szcore_scoring/*.py` (shims)
  - re‑export from `seizure_evaluation.szcore.*`

These shims let existing commands and tests continue to work while communicating the new
package location. We can remove the shims after one or two releases once callers migrate.

## Packaging and Tooling Updates

1) Switch to src‑layout packages in `pyproject.toml`:

```
[tool.hatch.build.targets.wheel]
packages = { find = { where = ["src"] } }
```

2) Optionally add console entry points for discoverable CLIs:

```
[project.scripts]
tusz-eval = "seizure_evaluation.tusz.cli:main"
szscore-run = "seizure_evaluation.szcore.cli:main"
nedc-run = "evaluation.nedc_eeg_eval.nedc_scoring.run_nedc:main"  # path unchanged
```

3) Ruff/mypy/pytest scopes:
- Lint/format `src/`, `tests/`, and keep excluding vendored `evaluation/nedc_eeg_eval/` and `wu_2025/`.
- Pytest coverage: include `src/` packages; keep current NEDC path stable for conformance tests.

4) Makefile adjustments:
- `lint`, `format`, `typecheck`: target `src/ tests/ scripts/` (+ keep excludes)
- `benchmark` and `sweep` targets can keep current NEDC paths; if referencing szcore/tusz,
  call the new console scripts or the shimmed paths for now.

## Code Changes (minimal but high‑value)

- Remove ad‑hoc `sys.path` edits from TUSZ CLI once installed in editable mode:
  - Import `wu_2025` as an installed package (Makefile already does `pip install ./wu_2025`).
  - Import `seizure_evaluation.utils` directly from the package.

- Keep `evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py` importing
  `seizure_evaluation.ovlp.overlap_scorer` (already aligned with the new package path).

## Tests and Validation

1) After moves and shims:
- `make format && make lint`
- `make test` (unit + integration)

2) Smoke CLI checks:
- `python -m seizure_evaluation.tusz.cli --help`
- `python -m evaluation.nedc_eeg_eval.nedc_scoring.run_nedc --help`
- `python -m seizure_evaluation.szcore.cli --help`

3) End‑to‑end (if data available):
- TUSZ predictions to checkpoint → NEDC convert → run scorer (binary/native) → parse metrics.

## Deprecation Policy

- Keep shims in `evaluation/tusz`, `evaluation/utils`, and `evaluation/szcore_scoring`
  for one release. Each shim prints a `DeprecationWarning` pointing to the new import path.
- Remove shims when downstream tools/docs have migrated.

## Name Choice: keep `seizure_evaluation` vs. rename

- Recommendation: keep `seizure_evaluation` to minimize churn (tests and current
  imports already use it). If we want a more specific alias (e.g., `modern_nedc_evaluation`),
  we can add `src/modern_nedc_evaluation/__init__.py` that re‑exports from
  `seizure_evaluation` without changing the canonical package name.

## Rollout Steps (proposed)

1. Create `src/` and move first‑party modules as listed (no functional changes).
2. Add shims at old paths with deprecation messages.
3. Update `pyproject.toml` to src‑layout and (optionally) console scripts.
4. Update Makefile lint/typecheck targets to include `src/`.
5. Run the full test suite and fix any stray imports.
6. Update `AGENTS.md` and `README.md` to reflect the new structure and commands.
7. Merge; keep shims for a release; remove them after downstream migration.

## Risks and Mitigations

- Risk: Missed import paths in tests/tools.
  - Mitigation: shims + CI runs + grep for `evaluation.utils` and `evaluation.tusz` imports.

- Risk: Packaging changes affect Docker builds.
  - Mitigation: keep Docker invoking module paths that remain stable; add console scripts as a convenience.

- Risk: Confusion around what is vendored vs. first‑party.
  - Mitigation: vendor‑only policy for `evaluation/` is explicit; docs updated accordingly.

---

If you approve this layout, I can implement Phase 1 (moves + shims) in a focused PR,
then follow with the pyproject/Makefile updates and doc changes. This keeps the diff
reviewable and preserves functionality throughout.

