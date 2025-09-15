# Methods

We evaluated SeizureTransformer on the TUSZ v2.0.3 held-out test set using the authors' pretrained weights without modification. Our evaluation employed four distinct scoring methodologies on identical model predictions to quantify the impact of evaluation standards on reported performance.

## Dataset

We used the Temple University Hospital Seizure Corpus (TUSZ) v2.0.3, focusing on its carefully designed evaluation split. The eval set contains 865 EDF files totaling 127.7 hours from 43 patients with 469 expert-annotated seizures. Critically, this set is patient-disjoint from the training and development splits, ensuring no data leakage and enabling valid generalization assessment. We achieved 100% file coverage, with one file requiring automated header repair using pyedflib's repair functionality on a temporary copy.

The development set, containing 1,832 files (435.5 hours) from 53 distinct patients with 1,075 seizures, was used exclusively for post-processing parameter optimization. This maintains the integrity of the held-out evaluation while allowing systematic exploration of clinical operating points.

## Model and Inference Pipeline

We employed the authors' publicly available pretrained SeizureTransformer weights (≈168 MB) without any modifications, retraining, or fine-tuning. The model expects 19-channel unipolar montage EEG data sampled at 256 Hz, processing 60-second windows (15,360 samples per channel) through its U-Net‑Transformer architecture.

Our preprocessing pipeline, implemented as a wrapper around the original wu_2025 code, largely follows the paper's specifications. For each EDF file, we: (1) load the data with unipolar montage enforcement and normalized channel aliases; (2) apply per-channel z‑score normalization across the full recording; (3) resample to 256 Hz if necessary; (4) apply a 0.5–120 Hz bandpass filter (3rd‑order Butterworth); and (5) apply notch filters at 1 Hz and 60 Hz (Q=30). The 1 Hz notch (to suppress heart‑rate artifacts) reflects our released evaluation code and is an addition beyond the paper’s brief preprocessing description.

The model processes 60-second non-overlapping windows, outputting per-sample seizure probabilities at 256 Hz. Post-processing applies three sequential operations using configurable parameters: (1) threshold the probability values to create a binary mask; (2) apply morphological opening and closing operations with a specified kernel size; and (3) remove events shorter than a minimum duration. The paper's default configuration uses threshold θ=0.8, kernel size k=5 samples, and minimum duration d=2.0 seconds.

## Scoring Methodologies

We evaluated identical model predictions using four scoring methodologies, each representing different clinical and research priorities:

**NEDC TAES (Time-Aligned Event Scoring)** computes partial credit based on temporal overlap between predictions and ground truth. If a 60-second reference seizure has 45 seconds correctly detected, TAES awards 0.75 true positive credit. This methodology emphasizes temporal precision, making it the strictest evaluation standard.

**NEDC OVERLAP** implements Temple's binary any-overlap scoring within the NEDC v6.0.0 framework. Any temporal overlap between prediction and reference, regardless of duration, counts as a full true positive. This represents the clinical standard for TUSZ evaluation, matching the dataset's annotation philosophy.

**Native OVERLAP** is our Python implementation of binary any-overlap scoring, developed for computational efficiency and validation. We verified perfect parity with NEDC OVERLAP, achieving identical results to four decimal places across all metrics.

**SzCORE Any-Overlap** extends binary scoring with clinical tolerances: 30‑second pre‑ictal and 60‑second post‑ictal windows around each reference event, plus merging of predictions separated by less than 90 seconds. These modifications, designed for clinical deployment scenarios where early warnings and reduced alarm fatigue are prioritized, substantially reduce reported false alarm rates.

All scoring implementations process the same binary prediction masks, ensuring that performance differences stem solely from scoring philosophy rather than model behavior.

## Parameter Optimization

We conducted systematic post‑processing parameter optimization on the TUSZ development set, targeting clinical deployment criteria of ≤10 false alarms per 24 hours while maximizing sensitivity. Our grid search explored: thresholds θ ∈ {0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.88, 0.90, 0.92, 0.95, 0.98}, morphological kernel sizes k ∈ {3, 5, 7, 9, 11, 13, 15} samples, and minimum event durations d ∈ {1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0} seconds.

For each configuration, we computed sensitivity and false alarm rates using NEDC OVERLAP scoring, as this represents the clinical standard for TUSZ. From the resulting parameter space, we selected operating points for comprehensive evaluation: (1) **Default** (θ=0.80, k=5, d=2.0s) — the paper's published configuration; (2) **Clinical 10 FA/24h target** (θ=0.88, k=5, d=3.0s) — optimized to meet the ≤10 FA/24h constraint; and (3) **ICU‑like 2.5 FA/24h target** (θ=0.95, k=5, d=5.0s) — a more conservative operating point. We additionally report selected high‑threshold points (e.g., θ=0.98) when illustrating the full trade‑off curve.

## Implementation and Validation

Our evaluation pipeline integrates multiple software components to ensure reproducibility and clinical validity. Model inference uses the original wu_2025 codebase with our preprocessing wrapper. Predictions are converted to NEDC's CSV_bi format, which requires specific formatting: four decimal places for timestamps, "TERM" as the channel identifier, and standardized header metadata including file duration.

We validated our implementation through multiple approaches. First, we verified that our Native OVERLAP scorer produces identical results to NEDC OVERLAP, confirming correct interpretation of Temple's scoring standard. Second, we processed a subset of files through both pipelines to ensure preprocessing consistency. Third, we confirmed that all 865 eval files were successfully processed, with the single header-repair case properly handled.

To enable full reproducibility, we provide our complete evaluation codebase, including the preprocessing wrapper, scoring implementations, and parameter optimization scripts. The pretrained SeizureTransformer weights remain available from the authors' repository, and NEDC v6.0.0 can be obtained from Temple University.

## Statistical Analysis

We report standard seizure detection metrics for each configuration and scorer combination: sensitivity (seizure‑level recall), false alarm rate per 24 hours (computed from total recording duration), and F1 score. For NEDC scorers, we report SEIZ‑only FA/24h as the primary metric (Temple’s "Total FA" is archived in summaries). For SzCORE, we follow its event‑based false positive definition. We also computed AUROC across threshold values to assess overall discriminative capability independent of operating point selection.

This comprehensive evaluation framework, combining the authors' pretrained model with multiple clinical scoring standards applied to a properly held-out test set, reveals how methodological choices fundamentally shape reported performance metrics in seizure detection systems.
