# Post-Processing Merge Gap Policy

Status: Enforced warnings and manifesting in tooling
Last updated: 2025-09-15

Summary
- `merge_gap_sec` merges nearby events during post-processing and can reduce FA/24h by ~4x.
- This is NOT part of the SeizureTransformer paper nor NEDC/Temple evaluation.
- Default policy is: do not merge (merge_gap_sec=None). Use only for non-academic scenarios, with clear disclosure.

Why this matters
- NEDC TAES/OVERLAP assess temporal localization. Merging events destroys precise start/stop evidence and inflates performance.
- Using a non-zero merge gap invalidates direct comparisons to Temple/NEDC results and to the paper’s defaults.

What we enforce now
- CLI flags for `--merge_gap_sec` are marked DEPRECATED in help text and print runtime warnings.
- When a non-zero merge gap is used, the tooling writes a `NONSTANDARD_POSTPROCESSING.txt` disclaimer:
  - At the conversion outdir root (beside `hyp/`, `ref/`, `lists/`).
  - In the final `results/` directory.
- The pipeline writes parameter manifests for reproducibility:
  - `outdir/params.json` from conversion
  - `outdir/results/operating_point.json` from scoring

Defaults and recommendations
- Academic/NEDC compliance: `merge_gap_sec=None` (or `--merge_gap_sec` omitted).
- Clinical exploration: If you experiment with merging, document clearly and never present as NEDC-comparable.

Where it appears in code
- Conversion: `evaluation/nedc_eeg_eval/nedc_scoring/convert_predictions.py`
- Post-processing: `evaluation/nedc_eeg_eval/nedc_scoring/post_processing.py`
- Runner: `evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py`
- Dev sweep: `evaluation/nedc_eeg_eval/nedc_scoring/sweep_operating_point.py`
- SzCORE wrapper: `evaluation/szcore_scoring/run_szcore.py` (keeps `None` to avoid double-merge)

References
- See `docs/policy/CRITICAL_MERGE_GAP_ISSUE.md` for the full incident write-up and history.

Quick verification
- Paper-default, no merging:
  - `python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py \
     --checkpoint experiments/eval/baseline/checkpoint.pkl \
     --outdir experiments/eval/baseline/paper_default_nomerge \
     --threshold 0.8 --kernel 5 --min_duration_sec 2.0`
- If you try a non-zero merge gap, expect a WARNING and the disclaimer files.
