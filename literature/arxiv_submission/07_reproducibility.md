# Reproducibility and Resources

Concise, checklist-style reproducibility details.

- Code: repo URL + tag/commit
- Data: TUSZ v2.0.3 (DUA), Siena (note: training-only usage)
- Weights: authors’ `model.pth` (exact source)
- Containers: Docker images; how to build/run
- Command snippets to reproduce results (from `FIGURES_PLAN.md` and pipeline docs)

## Exact Rerun Procedure

1) Generate predictions (TUSZ eval)
```
python evaluation/tusz/run_tusz_eval.py \
  --data_dir /path/to/TUSZ/edf/eval \
  --out_dir experiments/eval/FINAL_CLEAN_RUN \
  --device auto
```

2) Score with NEDC OVERLAP (Temple) or native parity
```
# Default
python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py \
  --checkpoint experiments/eval/FINAL_CLEAN_RUN/checkpoint.pkl \
  --outdir experiments/eval/FINAL_CLEAN_RUN/DEFAULT_nedc_binary \
  --backend nedc-binary \
  --threshold 0.80 --kernel 5 --min_duration_sec 2.0

# 10 FA
python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py \
  --checkpoint experiments/eval/FINAL_CLEAN_RUN/checkpoint.pkl \
  --outdir experiments/eval/FINAL_CLEAN_RUN/10FA_nedc_binary \
  --backend nedc-binary \
  --threshold 0.88 --kernel 5 --min_duration_sec 3.0

# 2.5 FA
python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py \
  --checkpoint experiments/eval/FINAL_CLEAN_RUN/checkpoint.pkl \
  --outdir experiments/eval/FINAL_CLEAN_RUN/2_5FA_nedc_binary \
  --backend nedc-binary \
  --threshold 0.95 --kernel 5 --min_duration_sec 5.0
```

3) Score with SzCORE
```
# Default / 10 FA / 2.5 FA (same params as above)
python evaluation/szcore_scoring/run_szcore.py \
  --checkpoint experiments/eval/FINAL_CLEAN_RUN/checkpoint.pkl \
  --outdir experiments/eval/FINAL_CLEAN_RUN/DEFAULT_szcore \
  --threshold 0.80 --kernel 5 --min_duration_sec 2.0

python evaluation/szcore_scoring/run_szcore.py \
  --checkpoint experiments/eval/FINAL_CLEAN_RUN/checkpoint.pkl \
  --outdir experiments/eval/FINAL_CLEAN_RUN/10FA_szcore \
  --threshold 0.88 --kernel 5 --min_duration_sec 3.0

python evaluation/szcore_scoring/run_szcore.py \
  --checkpoint experiments/eval/FINAL_CLEAN_RUN/checkpoint.pkl \
  --outdir experiments/eval/FINAL_CLEAN_RUN/2_5FA_szcore \
  --threshold 0.95 --kernel 5 --min_duration_sec 5.0
```

Notes
- merge_gap is disallowed in all evaluation paths (policy); do not set it.
- NEDC OVERLAP reports SEIZ-only FA/24h as primary in our metrics; “Total FA” remains in raw summaries.
