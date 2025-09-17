# Vendored Sources and Provenance

This repository vendors select third‑party code for durability and reproducibility. Vendoring means the source lives in this repo and is installed locally during setup; we do not fetch from the network at runtime.

Never modify vendored trees directly. Add adapters/wrappers in `src/` if behavior must change.

## 1) SeizureTransformer (original, Wu et al.)

- Location: `wu_2025/`
- Upstream: https://github.com/keruiwu/SeizureTransformer
- License: MIT (per upstream)
- Purpose: Model architecture, dataloader utilities, and inference utilities used by our TUSZ pipeline.
- Install method: `pip install ./wu_2025` (done by `make setup`/`make setup-dev`)
- Imported by: `src/seizure_evaluation/tusz/cli.py`
- Provenance: vendored snapshot of upstream (exact commit not recorded here). If known, record:
  - Upstream commit: <add-hash-here>
  - Snapshot date: <add-date-here>
- Policy: Treat as read‑only. If fixes are required, prefer wrappers/adapters in `src/seizure_evaluation/`. If a change must be upstreamed, fork and track your fork/tag.

## 2) Temple NEDC EEG Eval (v6.0.0, official)

- Location: `evaluation/nedc_eeg_eval/v6.0.0/`
- Provider: Temple University, Neural Engineering Data Consortium (NEDC)
- License/Docs: See AAREADME and license files in that directory
- Purpose: Official TAES/OVERLAP/EPOCH scorers and support binaries
- Used by: `evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py` and related tools
- Policy: Do not modify the `v6.0.0/` folder. Our orchestration wrappers live beside it under `evaluation/nedc_eeg_eval/nedc_scoring/`.

## 3) Non‑vendored dependencies

These are installed via pip and not included in the repo. Examples: PyTorch, NumPy, pandas, mne, epilepsy2bids, etc. See `pyproject.toml` dependencies.

---

Rationale for vendoring critical code:
- Reproducibility and durability: Builds succeed offline and remain stable even if upstream repos change or disappear.
- Supply‑chain safety: We control the exact code version that runs.
- Clear boundaries: Vendored code remains read‑only; our logic lives under `src/`.

