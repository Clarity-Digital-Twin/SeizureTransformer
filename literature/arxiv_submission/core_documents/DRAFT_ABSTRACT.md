# Draft Abstract

## Version 1: The Hook-First Approach (250 words)

SeizureTransformer won the 2025 EpilepsyBench Challenge claiming 37% sensitivity at 1 false alarm per 24 hours on the Dianalund dataset. Despite being trained on the Temple University Hospital Seizure (TUSZ) dataset, no evaluation using TUSZ's clinical scoring standard existed. We present the first evaluation using Temple's NEDC v6.0.0, revealing a multi‑fold gap: 26.89–136.73 FA/24h (depending on scorer) versus the ~1 FA/24h achieved on Dianalund.

We evaluated SeizureTransformer on TUSZ v2.0.3's held-out set (865 files, 469 seizures) using the authors' pretrained weights. Our systematic comparison reveals that scoring methodology alone accounts for a ≈3.1× difference at default: the same predictions yield 26.89 FA/24h (SEIZ) with NEDC's OVERLAP but only 8.59 FA/24h with EpilepsyBench's SzCORE. This variance stems from SzCORE's 30-second pre‑ictal and 60-second post‑ictal tolerances designed for early clinical warning, versus NEDC's strict temporal alignment designed for research precision.

Our parameter tuning on TUSZ's development set shows that SeizureTransformer cannot meet clinical deployment thresholds (≤10 FA/24h and ≥50% sensitivity) with NEDC: the best ~10 FA setting yields 10.27 FA/24h at 33.90% sensitivity, and the best ~2.5 FA setting yields 2.05 FA/24h at 14.50% sensitivity. These findings highlight a critical gap between benchmark performance and clinical reality.

We contribute: (1) the first reproducible NEDC v6.0.0 evaluation pipeline for TUSZ, (2) comprehensive operating points across four scoring methods, and (3) evidence that scoring methodology can create 100-fold performance differences. Our work demonstrates the urgent need for dataset-matched clinical evaluation standards to bridge the gap between impressive benchmarks and hospital deployment.

---

## Version 2: The Technical-First Approach (250 words)

We present the first clinical evaluation of SeizureTransformer, the 2025 EpilepsyBench winner, using Temple University's NEDC v6.0.0 scoring standard on the TUSZ v2.0.3 dataset. Our evaluation reveals a multi‑fold gap between reported benchmark performance (~1 FA/24h on Dianalund) and clinical reality (26.89–136.73 FA/24h on TUSZ, depending on scorer).

Using the authors' pretrained model, we evaluated 865 EEG files containing 469 seizures from TUSZ's held-out test set. We implemented a dual-track evaluation pipeline using both Temple's official NEDC binaries and a Python reimplementation, achieving <0.1% metric variance. Our systematic parameter tuning on the development set (1,832 files) optimized threshold, morphological kernel size, and minimum event duration.

The evaluation reveals that scoring methodology alone creates a ≈3.1× performance difference at default. The identical predictions yield: (1) 26.89 FA/24h (SEIZ) with NEDC OVERLAP, the clinical standard for TUSZ, (2) 136.73 FA/24h with NEDC TAES (time‑aligned), and (3) 8.59 FA/24h with SzCORE, EpilepsyBench's scoring method that includes 30s pre‑ictal and 60s post‑ictal tolerances.

When targeting clinical deployment thresholds, SeizureTransformer cannot achieve ≤10 FA/24h at ≥50% sensitivity with NEDC scoring. Only with SzCORE's permissive scoring can the model meet FA targets at higher sensitivity than OVERLAP.

We provide an open-source evaluation framework including containerized deployment, comprehensive operating points across scoring methods, and reproducible pipelines. This work highlights the critical importance of dataset-matched evaluation standards and transparent reporting of scoring methodologies for clinical AI deployment.

---

## Version 3: The Balanced Approach (247 words)

SeizureTransformer achieved state-of-the-art performance on the 2025 EpilepsyBench Challenge with 1 false alarm per 24 hours. However, models trained on the Temple University Hospital Seizure (TUSZ) dataset have never been evaluated using TUSZ's clinical scoring standard. We present the first such evaluation, revealing a 27-fold gap between benchmark claims and clinical reality.

We evaluated SeizureTransformer on TUSZ v2.0.3's held-out evaluation set (865 files, 469 seizures, 127.7 hours) using Temple's NEDC v6.0.0, the clinical gold standard designed specifically for TUSZ annotations. Using the authors' pretrained weights, we systematically compared four scoring methodologies on identical predictions.

Our results reveal that scoring methodology alone creates dramatic performance differences. The same model outputs yield 26.89 false alarms per 24 hours with NEDC's clinical OVERLAP scoring (SEIZ-only), but only 8.59 FA/24h with SzCORE—a 3.1-fold difference. This gap arises from SzCORE's 30-second pre-ictal and 60-second post-ictal tolerances, designed for clinical early warning rather than temporal precision.

Parameter optimization targeting clinical deployment shows SeizureTransformer cannot meet standard false alarm thresholds when evaluated properly. Targeting 10 FA/24h yields 10.27 FA/24h at 33.90% sensitivity. The model achieves clinical targets only under SzCORE's permissive scoring.

We contribute: (1) reproducible NEDC evaluation infrastructure, (2) comprehensive operating points for clinical deployment, and (3) quantitative evidence of scoring's impact on reported performance. Our findings emphasize that meaningful clinical AI evaluation requires dataset-matched scoring standards, not generic benchmarks.

---

## Key Abstract Elements to Include:
1. **The Hook**: 27× gap between claimed and actual performance (OVERLAP) or 137× (TAES)
2. **The Method**: First NEDC v6.0.0 evaluation on TUSZ
3. **The Finding**: Scoring alone creates 3.1× difference (OVERLAP vs SzCORE)
4. **The Impact**: Cannot meet clinical targets with proper scoring
5. **The Contribution**: Reproducible pipeline + operating points
