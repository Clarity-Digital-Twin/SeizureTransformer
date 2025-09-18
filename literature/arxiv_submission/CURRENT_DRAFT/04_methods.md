# Methods

We evaluated SeizureTransformer on the TUSZ v2.0.3 held-out test set using the authors' pretrained weights without modification [8]. Our evaluation employed three distinct scoring methodologies on identical model predictions to quantify the impact of evaluation standards on reported performance.

## Dataset

We used the Temple University Hospital Seizure Corpus (TUSZ) v2.0.3, focusing on its carefully designed evaluation split [5]. The eval set contains 865 EDF files totaling 127.7 hours from 43 patients with 469 expert-annotated seizures [5]. Critically, this set is patient-disjoint from the training and development splits, ensuring no data leakage and enabling valid generalization assessment [5]. We achieved 100% file coverage, with one file requiring automated header repair using pyEDFlib's repair functionality on a temporary copy [12].

The development set, containing 1,832 files (435.5 hours) from 53 distinct patients with 1,075 seizures, was used exclusively for post-processing parameter optimization. This maintains the integrity of the held-out evaluation while allowing systematic exploration of clinical operating points.

## Model and Inference Pipeline

We employed the authors' publicly available pretrained SeizureTransformer weights (~=168 MB) without any modifications, retraining, or fine-tuning [8]. The model expects 19-channel unipolar montage EEG data sampled at 256 Hz, processing 60-second windows (15,360 samples per channel) through its U-Net-Transformer architecture [8].

Our preprocessing pipeline, implemented as a wrapper around the original wu_2025 code, largely follows the paper's specifications [8]. For each EDF file, we: (1) load the data with unipolar montage enforcement and normalized channel aliases; (2) apply per-channel z-score normalization across the full recording; (3) resample to 256 Hz if necessary; (4) apply a 0.5-120 Hz bandpass filter (3rd-order Butterworth); and (5) apply notch filters at 1 Hz and 60 Hz (Q=30). The 1 Hz notch (to suppress heart-rate artifacts) reflects our released evaluation code and is an addition beyond the paper’s brief preprocessing description [8].

The model processes 60-second non-overlapping windows, outputting per-sample seizure probabilities at 256 Hz. Post-processing applies three sequential operations using configurable parameters: (1) threshold the probability values to create a binary mask; (2) apply morphological opening and closing operations with a specified kernel size; and (3) remove events shorter than a minimum duration. The paper's default configuration uses threshold theta=0.8, kernel size k=5 samples, and minimum duration d=2.0 seconds [8].

## Scoring Methodologies

We evaluated identical model predictions using three scoring methodologies, each representing different clinical and research priorities:

**NEDC TAES (Time-Aligned Event Scoring)** computes partial credit based on temporal overlap between predictions and ground truth [5]. If a 60-second reference seizure has 45 seconds correctly detected, TAES awards 0.75 true positive credit [5]. This methodology emphasizes temporal precision, making it the strictest evaluation standard.

**NEDC OVERLAP** implements Temple's binary any-overlap scoring within the NEDC v6.0.0 framework [5]. Any temporal overlap between prediction and reference, regardless of duration, counts as a full true positive. This represents the commonly reported mode for TUSZ evaluation, matching the dataset's annotation philosophy [5].

**SzCORE Event (Any-Overlap + tolerances)** extends binary scoring with clinical tolerances: 30-second pre-ictal and 60-second post-ictal windows around each reference event, plus merging of predictions separated by less than 90 seconds [4]. These modifications, designed for clinical deployment scenarios where early warnings and reduced alarm fatigue are prioritized, substantially reduce reported false alarm rates [4].

All scoring implementations process the same binary prediction masks, ensuring that performance differences stem solely from scoring philosophy rather than model behavior.

![Figure 3: Impact of scoring methodology on reported performance. The same SeizureTransformer predictions flow through different scoring pipelines, yielding a 15.9x difference in false alarm rates between NEDC TAES and SzCORE Event. This visualization demonstrates how evaluation standards, not model improvements, can account for order-of-magnitude performance variations.](../figures/output/arxiv/fig3_scoring_impact.png){#fig:scoring-impact width=100%}

### Choice of Event-Based Metrics

We report only event-based metrics (NEDC OVERLAP, NEDC TAES, SzCORE Event) because clinical evaluation focuses on detecting discrete seizure events. Sample-based (epoch) methods (e.g., NEDC EPOCH; SzCORE Sample-based) compare 1 Hz labels and can inflate scores by rewarding long non-seizure periods, obscuring event detection quality. To avoid this pitfall, all reported results are event-based. “SzCORE Event” denotes any-overlap with ±30 s/60 s tolerances and merge/split rules (merge <90 s, split >5 min); we do not report SzCORE Sample-based.

## Parameter Optimization

We conducted systematic post-processing parameter optimization on the TUSZ development set, targeting clinical deployment criteria of <=10 false alarms per 24 hours while maximizing sensitivity. Our grid search explored: thresholds theta in {0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.88, 0.90, 0.92, 0.95, 0.98}, morphological kernel sizes k in {3, 5, 7, 9, 11, 13, 15} samples, and minimum event durations d in {1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0} seconds.

For each configuration, we computed sensitivity and false alarm rates using NEDC OVERLAP scoring, as this is the commonly reported mode for TUSZ. From the resulting parameter space, we selected operating points for comprehensive evaluation: (1) **Default** (theta=0.80, k=5, d=2.0s) — the paper's published configuration; (2) **Clinical 10 FA/24h target** (theta=0.88, k=5, d=3.0s) — optimized to meet the <=10 FA/24h constraint; and (3) **ICU-like 2.5 FA/24h target** (theta=0.95, k=5, d=5.0s) — a more conservative operating point. We additionally report selected high-threshold points (e.g., theta=0.98) when illustrating the full trade-off curve.

![Figure 4: Parameter sensitivity analysis showing F1 scores across threshold and minimum duration values for NEDC OVERLAP scoring. The heatmaps reveal that optimal parameters vary by morphological kernel size, with the paper's default (theta=0.8, d=2.0) marked. Higher thresholds are required to achieve clinically acceptable false alarm rates.](../figures/output/arxiv/fig4_parameter_heatmap.png){#fig:parameter-heatmap width=100%}

## Implementation and Validation

Our evaluation pipeline integrates multiple software components to ensure reproducibility and clinical validity. Model inference uses the original wu_2025 codebase with our preprocessing wrapper. Predictions are converted to NEDC's CSV_bi format, which requires specific formatting: four decimal places for timestamps, "TERM" as the channel identifier, and standardized header metadata including file duration.

We validated our implementation through consistency checks across tools and confirmed that all 865 eval files were successfully processed (with one automated header repair). Reported results use the official NEDC scorers and SzCORE Event.

To enable full reproducibility, we provide our complete evaluation codebase, including the preprocessing wrapper, scoring implementations, and parameter optimization scripts. The pretrained SeizureTransformer weights remain available from the authors' repository, and NEDC v6.0.0 can be obtained from Temple University.

## Statistical Analysis

We report standard seizure detection metrics for each configuration and scorer combination: sensitivity (seizure-level recall), false alarm rate per 24 hours (computed from total recording duration), and F1 score. For NEDC scorers, we report SEIZ-only FA/24h as the primary metric (Temple’s "Total FA" is archived in summaries). For SzCORE Event, we follow its event-based false positive definition. We also computed AUROC across threshold values to assess overall discriminative capability independent of operating point selection.

This comprehensive evaluation framework, combining the authors' pretrained model with multiple scoring standards applied to a properly held-out test set, reveals how methodological choices fundamentally shape reported performance metrics in seizure detection systems.

