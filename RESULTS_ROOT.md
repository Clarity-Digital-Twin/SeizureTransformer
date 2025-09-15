# Publication Results Plan (SSOT) — SeizureTransformer on TUSZ v2.0.3

Purpose: lock what we will publish at paper defaults, identify illustrative operating points, and define an exact rerun procedure to verify numbers end‑to‑end (865/865 files, no merge_gap).

## What We Publish

- Dataset: TUSZ v2.0.3 eval (865 files, 469 seizures, 127.7 hours). Dev set used for tuning: 1,832 files. Patient‑disjoint splits.
- Model: SeizureTransformer, authors’ pretrained weights (trained on TUSZ train + Siena). No retraining.
- Primary metric: NEDC OVERLAP (Temple) on identical predictions. Report all four scorers for transparency.

### Paper Defaults (threshold=0.8, kernel=5, min_duration=2.0; merge_gap=None)
- NEDC TAES: 24.15% sens, 137.53 FA/24h
- NEDC OVERLAP: 45.63% sens, 100.06 FA/24h
- Python OVERLAP: 45.63% sens, 100.06 FA/24h
- SzCORE: 52.35% sens, 8.46 FA/24h

### Clinical Operating Points (illustrative)
- 10 FA/24h target
  - NEDC TAES: 8.64% sens, 34.04 FA/24h (not met)
  - NEDC OVERLAP: 23.45% sens, 39.50 FA/24h (not met)
  - Python OVERLAP: 23.45% sens, 39.50 FA/24h (not met)
  - SzCORE: 29.12% sens, 1.32 FA/24h (met)
- 2.5 FA/24h target
  - NEDC TAES: 4.07% sens, 8.01 FA/24h (not met)
  - NEDC OVERLAP: 11.51% sens, 8.09 FA/24h (not met)
  - Python OVERLAP: 11.51% sens, 8.09 FA/24h (not met)
  - SzCORE: 16.47% sens, 0.56 FA/24h (met)

Notes
- The same predictions, scored four ways, produce ≈12× difference (OVERLAP vs SzCORE) and ≈16× (TAES vs SzCORE) in FA/24h.
- “1 FA/24h” claims hold under SzCORE on Dianalund; they do not hold under NEDC on TUSZ.

## Config Locks (must not drift)

- Preprocessing: 256 Hz, 19‑ch common montage, bandpass 0.5–120 Hz, 1/60 Hz notches, per‑clip z‑score. No leakage from eval.
- Inference windowing: 60 s, 75% overlap (per paper/OSS). Channel aliases normalized; unipolar enforced.
- Post‑processing: threshold=0.80, kernel=5, min_duration=2.0 s for paper defaults. merge_gap=None always.
- Scoring: NEDC TAES, NEDC OVERLAP (Temple v6.0.0), Python OVERLAP (parity), SzCORE (timescoring) — on the same predictions.
- Data integrity: 865/865 processed; one EDF header repaired on a copy for readout. No files skipped.

## Rerun Procedure (posterity + verification)

Goal: repeat the exact defaults and the two clinical targets, confirm parity across scorers, and archive outputs.

1) Generate predictions checkpoint (TUSZ eval)
- `python evaluation/tusz/run_tusz_eval.py --data_dir /path/to/TUSZ/eval --out_dir experiments/eval/baseline --device auto`
- Expect: `experiments/eval/baseline/checkpoint.pkl` and per‑file raw predictions.

2) Convert + score with NEDC (Temple) and native OVERLAP
- `bash evaluation/nedc_eeg_eval/nedc_scoring/run_full_evaluation.sh experiments/eval/baseline/checkpoint.pkl experiments/eval/baseline/CLEAN_NO_MERGE`
- Produces: Temple TAES/OVERLAP summaries and native OVERLAP parity, including FA/24h and sensitivity.

3) Score with SzCORE
- `python evaluation/szcore_scoring/run_szcore.py --checkpoint experiments/eval/baseline/checkpoint.pkl --outdir experiments/eval/baseline/paper_default_szcore --threshold 0.8 --kernel 5 --min_duration_sec 2.0`

4) Parameter sweeps for operating points (dev‑tuned, eval‑scored)
- Ensure dev sweep uses only TUSZ dev (1,832 files) to pick params.
- Use provided helper to sweep against eval checkpoint for reporting parity:
  - `make sweep`
  - Monitor: `make monitor-sweep`

5) Archive and snapshot
- Copy final summaries to `docs/results/` and ensure tables match: `docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md`.
- Record environment: `python --version`, `pip freeze | rg -E "pyedflib|timescoring|numpy|scipy"`.

## Guardrails (no surprises)

- Channels/montage: verified via loader tests; aliases normalized; unipolar enforced.
- merge_gap: must be None (disabled). If any tool writes a nonstandard post‑processing note, discard run.
- Missing files: none. If any read error occurs, repair header on a copy and re‑run; do not drop files.
- Siena: used in training; any Siena evaluation is in‑sample and not publishable as held‑out.

## Publication Artifacts

- Main table: paper defaults, 4 scorers (numbers above).
- Operating points figure: show trade‑offs at 10 and 2.5 FA/24h across NEDC OVERLAP vs SzCORE.
- Provenance: link to NEDC v6.0.0 summaries and SzCORE outputs; store under `experiments/eval/baseline/*`.

## Sign‑off Checklist

- [ ] Re‑ran defaults; matched 100.06 FA/24h (OVERLAP) and 8.46 FA/24h (SzCORE)
- [ ] Completed 10 FA and 2.5 FA targets; matched numbers above
- [ ] Verified 865/865 processed, no skips, merge_gap=None
- [ ] Updated `docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md` if any delta
- [ ] Snapshot env and attach summaries to the repo

References
- SSOT tables: `docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md`, `docs/status/SINGLE_SOURCE_OF_TRUTH.md`
- ArXiv scaffold: `literature/arxiv_submission/*` (Results and Methods sections reference these numbers)

