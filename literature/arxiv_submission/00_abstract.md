# Abstract

SeizureTransformer achieved state-of-the-art performance in the 2025 EpilepsyBench Challenge, claiming 1 false alarm per 24 hours on the Dianalund dataset. However, the model trained on Temple University Hospital Seizure (TUSZ) dataset has never been evaluated using TUSZ's clinical scoring standard. We present the first such evaluation, revealing a 27-fold gap between benchmark claims and clinical reality.

We evaluated SeizureTransformer on TUSZ v2.0.3's held-out evaluation set (865 files, 127.7 hours) using Temple's NEDC v6.0.0, the clinical gold standard designed specifically for TUSZ annotations. Using the authors' pretrained weights, we systematically compared four scoring methodologies on identical predictions to quantify the impact of evaluation choices.

Our results reveal that scoring methodology alone creates dramatic performance differences. The same model outputs yield 26.89 false alarms per 24 hours with NEDC's clinical OVERLAP scoring, but only 8.59 FA/24h with SzCORE—a 3.1-fold difference. This gap arises from SzCORE's 30-second pre-ictal and 60-second post-ictal tolerances, designed for clinical early warning rather than the temporal precision required by NEDC. The strictest scorer, NEDC TAES, yields 136.73 FA/24h, representing a 137-fold gap from the Dianalund claim.

Parameter optimization targeting clinical deployment shows SeizureTransformer cannot meet standard thresholds when properly evaluated. Targeting 10 FA/24h yields 33.90% sensitivity—below the 50% clinical requirement. The model achieves acceptable false alarm rates only under SzCORE's permissive scoring.

We contribute: (1) reproducible NEDC evaluation infrastructure, (2) comprehensive operating points for clinical deployment, and (3) quantitative evidence that meaningful clinical AI evaluation requires dataset-matched scoring standards, not generic benchmarks.