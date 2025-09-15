# CORE 3: EpilepsyBench Challenge and SzCORE Scoring

## Executive Summary

- EpilepsyBench provides a useful cross-dataset benchmark, standardizing on SzCORE’s Any-Overlap scoring with clinical tolerances. That choice prioritizes clinical deployment over strict temporal precision and materially changes reported FA/24h.
- For TUSZ, the clinical standard is Temple/NEDC v6.0.0. Our repo includes the official NEDC tools and wrappers for reproducible scoring alongside a SzCORE wrapper using the official timescoring library.
- When citing results, state the scorer explicitly. The same predictions can differ by multiples between NEDC and SzCORE (≈3.1× at default in our CLEAN run).

---

## What EpilepsyBench Uses (SzCORE)

- Scoring philosophy: Any-Overlap within extended clinical windows.
  - 30 s pre-ictal tolerance; 60 s post-ictal tolerance; events <90 s apart are merged.
  - See in-repo implementation of these parameters in `evaluation/szcore_scoring/run_szcore.py` (EventScoring.Parameters: `toleranceStart=30`, `toleranceEnd=60`, `minDurationBetweenEvents=90`).
- Library: `timescoring` (official SzCORE/EpilepsyBench package).
  - Version pinned in this repo’s lockfile: `uv.lock` → `timescoring==0.0.6`.
  - Our wrapper: `evaluation/szcore_scoring/run_szcore.py` (outputs `szcore_summary.json` with micro-averaged metrics including `fpRate` = FA/24h).

References in repo:
- Parameters and defaults: `evaluation/szcore_scoring/run_szcore.py` lines 60–100, 120–145 (tolerances, merge=90 s, micro-averaging, FA/24h formula).
- Usage and notes: `evaluation/szcore_scoring/README.md` (install `timescoring`; do not double-merge in post-proc; SzCORE merges internally).

---

## What TUSZ Uses Clinically (Temple/NEDC)

- Official evaluator: NEDC EEG Evaluation Tools v6.0.0 (included in repo, unmodified): `evaluation/nedc_eeg_eval/v6.0.0`.
  - AAREADME: installation, environment variables, and CLI usage. See `AAREADME.txt` sections “INSTALLATION REQUIREMENTS” and “Running NEDC EEG Eval”.
  - CLI help enumerating algorithms: `src/nedc_eeg_eval/nedc_eeg_eval.help` (lists 5 algorithms run by the binary: DPALIGN, EPOCH, OVERLAP, TAES, IRA).
  - Overlap algorithm description: `lib/nedc_eeg_eval_ovlp.py` header explains any-overlap methodology and FA/min normalization.
  - TAES algorithm: `lib/nedc_eeg_eval_taes.py` (time-aligned event scoring; stricter temporal alignment).
  - Parameter defaults: `src/nedc_eeg_eval/nedc_eeg_eval_params_v00.toml` (e.g., epoch_duration, component toggles).

How we integrate NEDC (reproducible, in-repo):
- Convert predictions to NEDC CSV_bi and generate file lists: `evaluation/nedc_eeg_eval/nedc_scoring/convert_predictions.py`.
- Run official scorer and parse outputs: `evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py`.
- Outputs: `evaluation/nedc_eeg_eval/nedc_scoring/output/results/summary.txt` (Temple summary with TAES/OVERLAP/EPOCH/IRA sections).
- Quick setup: `evaluation/nedc_eeg_eval/nedc_scoring/setup_nedc_env.sh` sets `NEDC_NFC`, `PATH`, and `PYTHONPATH` for v6.0.0.

Direct binary usage (from AAREADME):
```
export NEDC_NFC="$(pwd)/evaluation/nedc_eeg_eval/v6.0.0"
export PATH="$NEDC_NFC/bin:$PATH"
export PYTHONPATH="$NEDC_NFC/lib:$PYTHONPATH"
$NEDC_NFC/bin/nedc_eeg_eval ref.list hyp.list -o output/results
```

Input format (from AAREADME “Input Files”):
- CSV with columns: `channel,start_time,stop_time,label,confidence`; TERM indicates all channels.
- Since v5.0.0, only non-background events are required; background is inferred by the scorer.

---

## SzCORE vs NEDC: Practical Differences

- SzCORE (EpilepsyBench): Any-Overlap within extended windows; merges events <90 s apart; reports FA/24h as an event rate post-merge. Implemented in `evaluation/szcore_scoring/run_szcore.py` using `timescoring`.
- NEDC OVERLAP (Temple): Any-Overlap without clinical tolerances; counts FP rate normalized by record duration. Implemented in Temple’s `lib/nedc_eeg_eval_ovlp.py` and surfaced in `summary.txt`.
- NEDC TAES (Temple): Time-aligned event scoring providing stricter clinical temporal precision. Implemented in `lib/nedc_eeg_eval_taes.py` and summarized in `summary.txt`.

In-repo example demonstrating the impact (same predictions, different scorers):
- See `docs/evaluation/EVALUATION_RESULTS_TABLE.md` → Default row shows NEDC OVERLAP (SEIZ FA) 26.89 FA/24h vs SzCORE 8.59 FA/24h on TUSZ eval.
- Screenshot of EpilepsyBench leaderboard context: `docs/images/wu_ebench.png` (TUSZ marked with 🚂 when trained on TUSZ).

---

## Reproducibility: How to Run Both Scorers Here

NEDC (Temple v6.0.0):
- Convert and score:
  - `python evaluation/nedc_eeg_eval/nedc_scoring/convert_predictions.py --checkpoint experiments/eval/baseline/checkpoint.pkl --outdir evaluation/nedc_eeg_eval/nedc_scoring/output`
  - `python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py`
- Inspect metrics in `evaluation/nedc_eeg_eval/nedc_scoring/output/results/summary.txt` (TAES, OVERLAP, EPOCH, IRA, DPALIGN).

SzCORE (timescoring):
- Install dependency: `pip install timescoring`
- Run: `python evaluation/szcore_scoring/run_szcore.py --checkpoint experiments/eval/baseline/checkpoint.pkl --outdir experiments/eval/baseline/szcore_results`
- Inspect `experiments/eval/baseline/szcore_results/szcore_summary.json` for `sensitivity`, `f1`, and `fpRate` (FA/24h).

---

## Writing Guidance (Paper/Report)

Do say:
- “EpilepsyBench provides valuable cross-dataset benchmarking; SzCORE prioritizes clinical early warning.”
- “Temple/NEDC v6.0.0 is the clinical standard scorer for TUSZ.”
- “Scoring philosophies differ; results are not directly comparable without context.”

Avoid:
- “SzCORE inflates performance” or “EpilepsyBench is misleading.” Prefer neutral framing about different goals.

Precision in claims (anchor to repo where possible):
- TUSZ eval counts we use operationally are documented in `docs/evaluation/EVALUATION_RESULTS_TABLE.md` (e.g., 865 files; 469 seizures; all processed — one file required header repair on a temporary copy via `pyedflib+repaired`).
- All NEDC usage and definitions are anchored to files under `evaluation/nedc_eeg_eval/v6.0.0` (AAREADME, help, lib sources, params). Cite file paths when describing metrics/CLI.
- SzCORE parameters are anchored to `evaluation/szcore_scoring/run_szcore.py` and dependency pin in `uv.lock`.

---

## Appendix: Exact Anchors for Reviewers

- NEDC tools and docs: `evaluation/nedc_eeg_eval/v6.0.0/AAREADME.txt` (Installation and “Running NEDC EEG Eval”).
- NEDC algorithms run by binary: `evaluation/nedc_eeg_eval/v6.0.0/src/nedc_eeg_eval/nedc_eeg_eval.help` (lists DPALIGN, EPOCH, OVERLAP, TAES, IRA).
- OVERLAP algorithm synopsis: `evaluation/nedc_eeg_eval/v6.0.0/lib/nedc_eeg_eval_ovlp.py` (header block).
- TAES implementation: `evaluation/nedc_eeg_eval/v6.0.0/lib/nedc_eeg_eval_taes.py`.
- Default parameters (epoch duration, etc.): `evaluation/nedc_eeg_eval/v6.0.0/src/nedc_eeg_eval/nedc_eeg_eval_params_v00.toml`.
- Our NEDC integration: `evaluation/nedc_eeg_eval/nedc_scoring/` (convert, run, parse). Summary at `.../output/results/summary.txt`.
- SzCORE integration: `evaluation/szcore_scoring/run_szcore.py` (parameters: 30/60 tolerances; merge 90 s; micro-avg). Results at `.../szcore_summary.json`.
- Dependency pin: `uv.lock` (`timescoring==0.0.6`).
