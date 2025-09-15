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
