# Abstract

SeizureTransformer reports ~1 false alarm per 24 hours on the EpilepsyBench Dianalund dataset. Despite being trained on the Temple University Hospital Seizure (TUSZ) dataset, it has not been evaluated on TUSZ using Temple’s official scoring software. We provide the first such evaluation with NEDC v6.0.0 and find a 27–137× gap between benchmark claims and clinical reality.

We evaluate the authors’ pretrained model on TUSZ v2.0.3’s held‑out set (865 files, 127.7 hours) and assess identical predictions with four scoring methodologies. With NEDC OVERLAP, the model produces 26.89 FA/24h; with SzCORE, 8.59 FA/24h (≈3.1× lower due solely to scoring tolerances); with NEDC TAES, 136.73 FA/24h.

When tuned toward deployment goals, the model cannot meet clinical thresholds with NEDC scoring: targeting 10 FA/24h achieves only 33.90% sensitivity, far below the 75% sensitivity goal for clinical systems (Roy et al., 2021). Acceptable false‑alarm rates occur only under SzCORE's permissive tolerances.

We contribute a reproducible NEDC evaluation pipeline, operating points tailored to clinical targets, and quantitative evidence that scoring choice alone drives multi‑fold differences. Dataset‑matched, clinician‑aligned evaluation is essential for credible seizure‑detection claims.
