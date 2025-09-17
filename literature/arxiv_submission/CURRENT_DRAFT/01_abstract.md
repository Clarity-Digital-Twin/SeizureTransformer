## Abstract

SeizureTransformer reports ~1 false alarm per 24 hours on the EpilepsyBench Dianalund dataset [5]. Despite being trained on the Temple University Hospital Seizure (TUSZ) dataset [3], it has not been evaluated on TUSZ using Temple’s official scoring software [6]. We provide, to our knowledge, the first such evaluation with NEDC v6.0.0 [6] and find a 27-137x gap between benchmark claims and clinical reality.

We evaluate the authors’ pretrained model on TUSZ v2.0.3’s held-out set (865 files, 127.7 hours) and assess identical predictions with four scoring methodologies. With NEDC OVERLAP [6], the model produces 26.89 FA/24h; with SzCORE [4], 8.59 FA/24h (~=3.1x lower due solely to scoring tolerances); with NEDC TAES [2], 136.73 FA/24h.

When tuned toward deployment goals, the model cannot meet clinical thresholds with NEDC scoring: targeting 10 FA/24h achieves only 33.90% sensitivity, far below the 75% sensitivity goal for clinical systems [10]. Acceptable false-alarm rates occur only under SzCORE's permissive tolerances [4].

We contribute a reproducible NEDC evaluation pipeline, operating points tailored to clinical targets, and quantitative evidence that scoring choice alone drives multi-fold differences. Dataset-matched, clinician-aligned evaluation is essential for credible seizure-detection claims.

