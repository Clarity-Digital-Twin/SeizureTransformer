# Draft Abstract

## Version 1: The Hook-First Approach (250 words)

SeizureTransformer won the 2025 EpilepsyBench Challenge claiming 37% sensitivity at 1 false alarm per 24 hours on the Dianalund dataset. Despite being trained on the Temple University Hospital Seizure (TUSZ) dataset, no evaluation using TUSZ's clinical scoring standard existed. We present the first evaluation using Temple's NEDC v6.0.0, revealing a startling 100-fold gap: 100.06 FA/24h versus the 1 FA/24h achieved on Dianalund.

We evaluated SeizureTransformer on TUSZ v2.0.3's held-out set (865 files, 469 seizures) using the authors' pretrained weights. Our systematic comparison reveals that scoring methodology alone accounts for a 12-fold difference: the same predictions yield 100.06 FA/24h with NEDC's clinical standard but only 8.46 FA/24h with EpilepsyBench's SzCORE. This dramatic variance stems from SzCORE's 30-second pre-ictal and 60-second post-ictal tolerances designed for early clinical warning, versus NEDC's strict temporal alignment designed for research precision.

Our parameter tuning on TUSZ's development set shows that SeizureTransformer cannot meet clinical false alarm targets when evaluated with NEDC: attempting 10 FA/24h yields 39.50 FA/24h at only 23.45% sensitivity, while 2.5 FA/24h targets result in 8.09 FA/24h at 11.51% sensitivity. These findings highlight a critical gap between benchmark performance and clinical reality.

We contribute: (1) the first reproducible NEDC v6.0.0 evaluation pipeline for TUSZ, (2) comprehensive operating points across four scoring methods, and (3) evidence that scoring methodology can create 100-fold performance differences. Our work demonstrates the urgent need for dataset-matched clinical evaluation standards to bridge the gap between impressive benchmarks and hospital deployment.

---

## Version 2: The Technical-First Approach (250 words)

We present the first clinical evaluation of SeizureTransformer, the 2025 EpilepsyBench winner, using Temple University's NEDC v6.0.0 scoring standard on the TUSZ v2.0.3 dataset. Our evaluation reveals a 100-fold gap between reported benchmark performance (1 FA/24h on Dianalund) and clinical reality (100.06 FA/24h on TUSZ).

Using the authors' pretrained model, we evaluated 865 EEG files containing 469 seizures from TUSZ's held-out test set. We implemented a dual-track evaluation pipeline using both Temple's official NEDC binaries and a Python reimplementation, achieving <0.1% metric variance. Our systematic parameter tuning on the development set (1,013 files) optimized threshold, morphological kernel size, and minimum event duration.

The evaluation reveals that scoring methodology alone creates a 12-fold performance difference. The identical predictions yield: (1) 100.06 FA/24h with NEDC OVERLAP, the clinical standard for TUSZ, (2) 144.28 FA/24h with NEDC TAES, the proposed stricter metric, and (3) 8.46 FA/24h with SzCORE, EpilepsyBench's scoring method that includes 30s pre-ictal and 60s post-ictal tolerances.

When targeting clinical deployment thresholds, SeizureTransformer cannot achieve standard false alarm requirements using NEDC scoring. The 10 FA/24h target yields 39.50 FA/24h, while 2.5 FA/24h targeting produces 8.09 FA/24h. Only with SzCORE's permissive scoring can the model meet clinical targets.

We provide an open-source evaluation framework including containerized deployment, comprehensive operating points across scoring methods, and reproducible pipelines. This work highlights the critical importance of dataset-matched evaluation standards and transparent reporting of scoring methodologies for clinical AI deployment.

---

## Version 3: The Balanced Approach (247 words)

SeizureTransformer achieved state-of-the-art performance on the 2025 EpilepsyBench Challenge with 1 false alarm per 24 hours. However, models trained on the Temple University Hospital Seizure (TUSZ) dataset have never been evaluated using TUSZ's clinical scoring standard. We present the first such evaluation, revealing a 100-fold gap between benchmark claims and clinical reality.

We evaluated SeizureTransformer on TUSZ v2.0.3's held-out evaluation set (865 files, 469 seizures, 127.6 hours) using Temple's NEDC v6.0.0, the clinical gold standard designed specifically for TUSZ annotations. Using the authors' pretrained weights, we systematically compared four scoring methodologies on identical predictions.

Our results reveal that scoring methodology alone creates dramatic performance differences. The same model outputs yield 100.06 false alarms per 24 hours with NEDC's clinical OVERLAP scoring, but only 8.46 FA/24h with SzCORE—a 12-fold difference. This gap arises from SzCORE's 30-second pre-ictal and 60-second post-ictal tolerances plus event merging, designed for clinical early warning rather than temporal precision.

Parameter optimization targeting clinical deployment shows SeizureTransformer cannot meet standard false alarm thresholds when evaluated properly. Targeting 10 FA/24h yields 39.50 FA/24h at 23.45% sensitivity. The model achieves clinical targets only under SzCORE's permissive scoring.

We contribute: (1) reproducible NEDC evaluation infrastructure, (2) comprehensive operating points for clinical deployment, and (3) quantitative evidence of scoring's impact on reported performance. Our findings emphasize that meaningful clinical AI evaluation requires dataset-matched scoring standards, not generic benchmarks.

---

## Key Abstract Elements to Include:
1. **The Hook**: 100× gap between claimed and actual performance
2. **The Method**: First NEDC v6.0.0 evaluation on TUSZ
3. **The Finding**: Scoring alone creates 12× difference
4. **The Impact**: Cannot meet clinical targets with proper scoring
5. **The Contribution**: Reproducible pipeline + operating points