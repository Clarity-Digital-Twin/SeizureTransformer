## Abstract

Claims about deep learning model performance in seizure detection are difficult to verify without standardized evaluation protocols. We report the first evaluation of SeizureTransformer on the Temple University Hospital EEG Seizure Corpus (TUSZ) [2] using the Neural Engineering Data Consortium (NEDC) v6.0.0 scoring tools [3]—the same evaluation framework used in peer-reviewed literature for two decades. Despite being trained on TUSZ, SeizureTransformer has never been evaluated on it using Temple's official scoring software. We find a 27-137x gap between the ~1 false alarm per 24 hours reported on the EpilepsyBench Dianalund dataset [1] and clinical reality.

We evaluate the authors' pretrained model on TUSZ v2.0.3's held-out set (865 files, 127.7 hours) and assess identical predictions with three scoring methodologies. With NEDC OVERLAP [3], the model produces 26.89 FA/24h; with SzCORE Event [4], 8.59 FA/24h (~=3.1x lower due solely to scoring tolerances); with NEDC TAES [5], 136.73 FA/24h.

When tuned toward deployment goals, the model cannot meet clinical thresholds with NEDC scoring: targeting 10 FA/24h achieves only 33.90% sensitivity, far below the 75% sensitivity goal for clinical systems [13]. Acceptable false-alarm rates occur only under SzCORE Event's permissive tolerances [4].

We contribute a reproducible NEDC evaluation pipeline, operating points tailored to clinical targets, and quantitative evidence that scoring choice alone drives multi-fold differences. Dataset-matched, clinician-aligned evaluation is essential for credible seizure-detection claims.
