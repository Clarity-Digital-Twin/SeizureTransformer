# Post-Processing Merge Gap Policy

Status: Fully removed from evaluation; hard-blocked and guarded in CI
Last updated: 2025-09-15

Summary
- `merge_gap_sec` merged nearby events during post-processing and could reduce FA/24h by ~4×.
- It is NOT part of the SeizureTransformer paper nor NEDC/Temple evaluation.
- Policy: Do not merge. The flag and plumbing have been removed from evaluation codepaths.

Why this matters
- NEDC TAES/OVERLAP assess temporal localization. Merging events destroys precise start/stop evidence and inflates performance.
- Using a non-zero merge gap invalidates direct comparisons to Temple/NEDC results and to the paper’s defaults.

What is enforced now
- No evaluation CLI or API accepts `merge_gap_sec`; attempts will fail type checks or CI guards.
- CI fails if artifacts contain `merge_gap_sec` or `NONSTANDARD_POSTPROCESSING.txt`.
- Parameter manifests (`params.json`, `metrics.json`/`operating_point.json`) contain no merge fields.

Defaults and recommendations
- Academic/NEDC compliance: No merging. Evaluation codepaths do not support it.
- If you experiment with merging in notebooks, use the standalone `merge_nearby_events(...)` helper explicitly and never present as NEDC‑comparable.

Where it exists now
- Post-processing: `merge_nearby_events(...)` utility only (not used by evaluation).
- SzCORE wrapper: does not merge in our post-processing; SzCORE merges internally (90s).

References
- See `docs/policy/CRITICAL_MERGE_GAP_ISSUE.md` for the full incident write-up and history.

Quick verification
- Paper-default, no merging:
  - `python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py \
     --checkpoint experiments/eval/baseline/checkpoint.pkl \
     --outdir experiments/eval/baseline/paper_default_nomerge \
     --threshold 0.8 --kernel 5 --min_duration_sec 2.0`
- Non-zero merge gaps are not supported anywhere in evaluation CLIs/APIs. CI will fail if any artifact or manifest contains merge-related fields.

