# SeizureTransformer: The Missing TUSZ Benchmark
## First NEDC v6.0.0 Evaluation Reveals 137x False Alarm Gap

[![EpilepsyBench #1](https://img.shields.io/badge/EpilepsyBench%202025-%231%20Winner-gold.svg)](https://www.epfl.ch/labs/esl/research/systems-for-biomedicals/seizure-detection-challenge-2025/)
[![NEDC v6.0.0](https://img.shields.io/badge/NEDC-v6.0.0%20Pioneer-brightgreen.svg)](https://www.isip.piconepress.com/projects/nedc/)
[![TUSZ v2.0.3](https://img.shields.io/badge/TUSZ-v2.0.3%20eval-blue.svg)](https://isip.piconepress.com/projects/tuh_eeg/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## What This Repository Provides (Industry Firsts)

**We are the FIRST to:**
- Evaluate SeizureTransformer on TUSZ v2.0.3 eval split with NEDC v6.0.0
- Systematically tune on TUSZ dev set and publish operating points
- Reveal the 137x FA discrepancy between Dianalund and TUSZ
- Provide complete reproducible pipeline with official Temple scoring

**Deliverables:**
- Stock results (paper defaults: threshold=0.8) showing 137.5 FA/24h
- Clinically tuned operating points (1-137.5 FA/24h targets)
- Official NEDC binaries unmodified in `evaluation/nedc_eeg_eval/v6.0.0`
- Maintained wrappers in `evaluation/nedc_scoring` for CSV_bi conversion

## Why TUSZ Isn’t Shown on EpilepsyBench (and Why It Should Be)

- SzCORE marks datasets used for training with a locomotive icon and often omits same-dataset results.
- TUSZ provides strict patient-disjoint train/dev/eval splits; evaluating on eval after tuning on dev is standard ML practice with no leakage.
- The community needs these numbers: performance differs markedly between Dianalund (challenge) and TUSZ (clinical standard). Showing TUSZ results is informative and valid.

## TUSZ v2.0.3 Dataset Structure

<details>
<summary>📊 Split sizes and usage (click to expand)</summary>

| Split | Files | Hours | Seizures | Usage |
|-------|-------|-------|----------|--------|
| Train | 1,557 | 3,050 | ~2,900 | Model training (per paper) |
| Dev | 1,013 | 1,015 | ~920 | **We tune thresholds here** |
| Eval | 865 | 127.6 | 469 | **We report results here** |

- ✅ **No patient overlap** between splits (prevents leakage)
- ✅ **Standard ML practice**: train → dev → eval
- ✅ **864/865 files processed** (1 format error)

</details>

---

## 🚨 Key Finding: 137x False Alarm Gap

| Dataset | Context | F1 Score | Sensitivity | False Alarms/24h |
|---------|---------|----------|-------------|------------------|
| **Dianalund** | EpilepsyBench #1 Winner | 43% | 37% | **1** ✅ |
| **TUSZ eval** | Clinical Standard | 31.19% | 24.15% | **137.5** ❌ |

> **Critical Insight**: The celebrated "1 FA/day" on Dianalund becomes **137.5 FA/day** on TUSZ — a 137x increase that fundamentally changes deployment viability.

## Results at a Glance

- AUROC: 0.9021 (sample-level discrimination on TUSZ eval)
- NEDC TAES (official):
  - Sensitivity: 24.15% (113/469)
  - Precision: 43.98%
  - F1: 31.19%
  - False alarms: 137.5 per 24h

### Operating Points (tuned on TUSZ dev, validated on eval)

- 1 FA/24h → threshold ≈ 0.999 → sens ≈ 0.43%
- 5 FA/24h → threshold ≈ 0.982 → sens ≈ 5.13%
- 10 FA/24h → threshold ≈ 0.965 → sens ≈ 9.87% (typical clinical target)
- 30 FA/24h → threshold ≈ 0.925 → sens ≈ 18.65%
- 50 FA/24h → threshold ≈ 0.895 → sens ≈ 22.34%
- 100 FA/24h → threshold ≈ 0.835 → sens ≈ 24.02%
- 137.5 FA/24h → threshold = 0.800 → sens = 24.15% (paper-like default)

These illustrate the sensitivity/false-alarm trade-off using official TAES scoring.

## Reproducing the Evaluation

Prerequisites
- Python 3.10+, CUDA GPU recommended, TUSZ v2.0.3.

Setup
```bash
make install && source .venv/bin/activate
```

Run TUSZ eval (held-out)
```bash
python evaluation/tusz/run_tusz_eval.py \
  --data_dir /path/to/TUSZ/v2.0.3/eval \
  --out_dir experiments/eval/baseline \
  --device auto
```

Score with official NEDC v6.0.0
```bash
make -C evaluation/nedc_scoring all \
  CHECKPOINT=../../experiments/eval/baseline/checkpoint.pkl \
  OUTDIR=../../experiments/eval/baseline/nedc_results
```

Sweep/tune operating point (requires dev split)
```bash
python evaluation/nedc_scoring/sweep_operating_point.py \
  --checkpoint experiments/dev/baseline/checkpoint.pkl \
  --outdir_base experiments/dev/sweeps/fa10 \
  --target_fa_per_24h 10
```

## Notes on NEDC Integration

- Official Temple binaries live under `evaluation/nedc_eeg_eval/v6.0.0/` and are not modified.
- Our `evaluation/nedc_scoring/` tools convert predictions to Temple’s CSV_bi format and invoke the official scorer.
- We also include parity checks and documentation to show equivalence with Temple outputs.

## Repository Structure (abridged)

- `wu_2025/` — Original SeizureTransformer (untouched)
- `evaluation/` — TUSZ evaluation and NEDC scoring tools
- `experiments/` — Run outputs and sweeps
- `tests/` — Fast pytest suite
- `docs/` — Technical docs and evaluation reports

## Citations

```bibtex
@software{seizuretransformer_tusz_2025,
  title = {SeizureTransformer: TUSZ Evaluation with NEDC v6.0.0 and Clinical Tuning},
  author = {Clarity Digital Twin Team},
  year = {2025},
  note = {Evaluation on TUSZ with official NEDC v6.0.0; operating-point sweeps on dev, held-out eval reporting},
  url = {https://github.com/Clarity-Digital-Twin/SeizureTransformer}
}

@article{shah2018temple,
  title = {The Temple University Hospital Seizure Detection Corpus},
  author = {Shah, V. and von Weltin, E. and Lopez, S. and McHugh, J. and Veloso, L. and Golmohammadi, M. and Obeid, I. and Picone, J.},
  journal = {Frontiers in Neuroinformatics},
  volume = {12},
  pages = {83},
  year = {2018},
  doi = {10.3389/fninf.2018.00083}
}

@incollection{shah2021objective,
  title = {Objective Evaluation Metrics for Automatic Classification of EEG Events},
  author = {Shah, V. and Golmohammadi, M. and Obeid, I. and Picone, J.},
  booktitle = {Signal Processing in Medicine and Biology},
  publisher = {Springer},
  year = {2021},
  pages = {1--26}
}

@article{wu2025seizuretransformer,
  title = {SeizureTransformer: Versatile Seizure Detection Model},
  author = {Wu, Kerui and others},
  year = {2025},
  journal = {arXiv preprint}
}
```

## Acknowledgments

- Kerui Wu and collaborators for the SeizureTransformer model and weights.
- Temple University’s NEDC for the dataset and scoring tools.
- SzCORE/EpilepsyBench for community benchmarking and reproducibility efforts.

## License

- Original SeizureTransformer: MIT (Kerui Wu)
- Our evaluation framework: MIT
- NEDC tools: Temple University license

---

Note: Results differ from the paper due to dataset (TUSZ vs Dianalund), scoring (TAES vs event-based), and our explicit dev-tuned operating points vs stock defaults.

