# Request for Clarity on TUH/TUSZ Reporting Policy

Date: 2025-09-12

To: Epilepsy Bench maintainers and related stakeholders

## Context

- Our team reproduced SeizureTransformer evaluation on TUH/TUSZ using the official NEDC EEG Eval v6.0.0 tools and the standard TUH splits (train/dev/eval).
- We noticed Epilepsy Bench suppresses TUH metrics (shown as "🚂") when a model was trained on TUH at all, even if results are reported strictly on the held‑out TUH eval split.

## Why We’re Writing

In standard ML practice, reporting in‑distribution results on a held‑out test split (train → dev → eval) is valid and expected. Separately, cross‑dataset generalization (e.g., training off‑TUH and testing on TUH) is also valuable, but it serves a different goal.

The current Bench behavior appears to hide TUH results whenever TUH is used for training, which may conflate these two distinct evaluation regimes.

## Request

We respectfully ask for clarification and/or a policy update that distinguishes two tracks:

1) In‑Distribution (ID) — TUH‑train for training, TUH‑dev for tuning, TUH‑eval for final reporting (strict hold‑out, NEDC TAES).

2) Cross‑Dataset (OOD) — Train on non‑TUH data (e.g., Siena/SeizeIT/Dianalund), evaluate on TUH‑eval to measure out‑of‑domain robustness.

Publishing both tracks side‑by‑side would:

- Preserve the value of the TUH official split (ID generalization).
- Promote robustness comparisons across institutions (OOD generalization).
- Avoid penalizing valid, split‑respecting TUH eval reporting.

## Specific Questions

- Does the Bench currently hide TUH metrics for any submission that used TUH data in training, regardless of split provenance? If so, could that be reconsidered under an explicit “In‑Distribution TUH‑eval” track?
- What evidence or artifacts would you require to display TUH‑eval metrics under an ID track (e.g., training logs, data provenance, NEDC output summaries)?
- Are there recommended post‑processing or threshold calibration procedures to align reported TUH results with Bench expectations (e.g., tuning thresholds on TUH‑dev, reporting full TAES curves)?

## Our Method Summary (for reproducibility)

- Official scorer: NEDC EEG Eval v6.0.0 (in‑repo), invoked via `$NEDC_NFC/bin/nedc_eeg_eval`.
- Inputs: hypothesis/reference `.csv_bi` with headers `version`, `bname`, `duration`; channel `TERM`; times in seconds with 4‑decimal precision.
- Lists: absolute paths generated for `ref.list` and `hyp.list`.
- Post‑processing: threshold 0.8, morphological opening/closing (kernel=5 samples), minimum event duration 2s (mirrors OSS defaults).
- Reporting: we can provide full `summary_taes.txt`/`summary.txt` outputs for review.

## Proposed Outcome

If the Bench’s goal is to emphasize cross‑dataset robustness, we fully support an OOD track. We simply request that valid, split‑respecting TUH‑eval results also be visible under an ID track. This separation aligns with standard ML practice and improves clarity for the community.

We appreciate your work on benchmarking and would be happy to share our evaluation scripts or collaborate on a minimal reproducible pipeline specification for TUH/TUSZ.

Sincerely,

Clarity Digital Twin — SeizureTransformer Team

