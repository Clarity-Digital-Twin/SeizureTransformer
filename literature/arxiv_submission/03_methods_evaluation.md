# Methods: Evaluation Design

Purpose: how we evaluated — data, model, pipeline, scoring — with clarity.

Use SSOT: `core_documents/CORE_5_TUSZ_DATASET.md`, `CORE_4_NEDC_SOFTWARE.md`, `CORE_1_SCORING_METHODOLOGIES.md`, `CORE_2_SEIZURETRANSFORMER_MODEL.md`, `core_documents/SIENA_EVALUATION_NOTES.md`.

- Data: TUSZ v2.0.3 eval (865 files, 469 seizures, 127.7 h); dev=1,832 files for tuning
- Model: Authors’ pretrained SeizureTransformer (no retraining)
- Inference pipeline: preprocessing, windowing, post-processing params
- Scoring: NEDC TAES, NEDC OVERLAP, Python OVERLAP, SzCORE (same predictions)
- Tuning: grid on dev, target NEDC OVERLAP; report across all scorers
- Parity: NEDC binary vs Python OVERLAP (<0.1% variance)
- Siena note: used in training; any Siena numbers are in-sample diagnostics only (not held-out)

Guardrails (no leakage)
- Weights include training on TUSZ train + Siena (per Wu et al.); we do not retrain.
- Post-processing parameters are tuned on TUSZ dev only (1,832 files).
- Final metrics are reported on TUSZ eval only (865 files), patient‑disjoint from train/dev.
- Siena is never used for tuning or held‑out evaluation in our pipeline.

Channel and preprocessing truth
- Inputs are 19‑channel unipolar montage at 256 Hz, 60 s windows (shape: 19×15360).
- Loading: `epilepsy2bids.Eeg.loadEdfAutoDetectMontage` enforces unipolar; raises if not satisfied.
- Channel normalization: verified stable 19‑ch order on TUSZ eval exemplars; aliases normalized by loader.
- Preprocessing: per‑channel z‑score (full recording), resample→256 Hz, 0.5–120 Hz bandpass (order 3), 1 Hz and 60 Hz notch (Q=30).
- Post‑processing: threshold 0.8, morph open/close k=5, min duration 2.0 s (defaults); tuned configs reported explicitly.
