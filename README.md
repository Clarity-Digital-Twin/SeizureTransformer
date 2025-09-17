# SeizureTransformer TUSZ Evaluation
## First NEDC v6.0.0 Evaluation Reveals ≈100× False Alarm Gap

[![EpilepsyBench #1](https://img.shields.io/badge/EpilepsyBench%202025-%231%20Winner-gold.svg)](https://epilepsybenchmarks.com/challenge/)
[![NEDC v6.0.0](https://img.shields.io/badge/NEDC-v6.0.0%20Pioneer-brightgreen.svg)](https://www.isip.piconepress.com/projects/nedc/)
[![TUSZ v2.0.3](https://img.shields.io/badge/TUSZ-v2.0.3%20eval-blue.svg)](https://isip.piconepress.com/projects/tuh_eeg/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-orange.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## 📋 Summary
- SeizureTransformer won EpilepsyBench 2025 with 1 FA/24h on Dianalund (using SzCORE's "Any-Overlap" scoring)
- Despite TUSZ having train/dev/eval splits, EpilepsyBench doesn't report eval results for models trained on it
- We evaluated it on TUSZ v2.0.3 using Temple's NEDC v6.0.0 - the clinical standard scorer for this dataset
- Result: 100.06 FA/24h at paper defaults (NEDC) vs 8.46 FA/24h (SzCORE), revealing a ≈12× scoring impact and ≈100× gap from Dianalund's 1 FA/24h

## 🎯 Background

### SeizureTransformer Model
Wu et al.'s transformer-based seizure detector won the 2025 EpilepsyBench Challenge. The model achieved 37% sensitivity with 1 FA/24h on the Dianalund dataset, ranking #1 on the [SzCORE leaderboard](https://epilepsybenchmarks.com/benchmark/).

### The Gap in Current Evaluations
- EpilepsyBench uses SzCORE's simplified "Any-Overlap" scoring for all datasets, not dataset-specific clinical scorers
- TUSZ results for models trained on it are marked with 🚂, despite patient-disjoint splits enabling valid held-out evaluation
- TUSZ paired with NEDC scoring represents the clinical gold standard
- No one had evaluated SeizureTransformer on TUSZ using Temple's official NEDC scorer
- See `docs/CORE3_EPILEPSYBENCH_SZCORE.md` for a professional, source-anchored writeup of EpilepsyBench vs. NEDC.

<p align="center">
<img src="docs/images/wu_ebench.png" alt="EpilepsyBench showing SeizureTransformer #1 but no TUSZ results" width="700">
<br>
<em>SeizureTransformer ranks #1 on EpilepsyBench but TUSZ evaluation is marked with 🚂</em>
</p>

### Our Contribution
- First TUSZ v2.0.3 evaluation using NEDC v6.0.0 - Temple's official clinical scorer (2025)
- Reveals performance gap when using proper dataset-matched scoring vs generic SzCORE
- Systematic threshold tuning on dev set, validation on eval set
- Dual-track implementation: Temple binaries + production Python code
- Complete operating points for clinical deployment decisions

## 🚨 Results

### Performance Comparison

| Dataset | Scoring Method | Sensitivity | False Alarms/24h | F1 Score |
|---------|---------------|-------------|------------------|-----------|
| **Dianalund** | SzCORE Any-Overlap¹ | 37% | **1 FA/24h** ✅ | 43% |
| **TUSZ eval (Paper defaults)** | NEDC v6.0.0 TAES² | 24.15% | **137.53 FA/24h** ❌ | 0.30 |
| **TUSZ eval (Paper defaults)** | NEDC v6.0.0 OVERLAP² | 45.63% | **100.06 FA/24h** ❌ | 0.519 |
| **TUSZ eval (Paper defaults)** | Python OVERLAP | 45.63% | **100.06 FA/24h** ❌ | 0.519 |
| **TUSZ eval (Paper defaults)** | SzCORE³ | 52.35% | **8.46 FA/24h** ✅ | - |
| **TUSZ eval (10 FA target)** | NEDC v6.0.0 TAES² | 8.64% | **34.04 FA/24h** ❌ | - |
| **TUSZ eval (10 FA target)** | NEDC v6.0.0 OVERLAP² | 23.45% | **39.50 FA/24h** ❌ | 0.331 |
| **TUSZ eval (10 FA target)** | SzCORE³ | 29.12% | **1.32 FA/24h** ✅ | - |
| **TUSZ eval (2.5 FA target)** | NEDC v6.0.0 TAES² | 4.07% | **8.01 FA/24h** ❌ | - |
| **TUSZ eval (2.5 FA target)** | NEDC v6.0.0 OVERLAP² | 11.51% | **8.09 FA/24h** ❌ | - |
| **TUSZ eval (2.5 FA target)** | SzCORE³ | 16.47% | **0.56 FA/24h** ✅ | - |

Note: Python OVERLAP matches NEDC OVERLAP at all operating points (omitted for brevity).

FA/24h reporting: For NEDC and Python OVERLAP rows, values are Temple’s Total False Alarm Rate (SEIZ + BCKG) from v6.0.0 summaries. SzCORE FA/24h follows its event-based definition.

¹ SzCORE: Event-based scoring with 30s pre-ictal, 60s post-ictal tolerances, merges events <90s apart (on Dianalund dataset)
² NEDC: Clinical standard scorer for TUSZ. TAES = strict time-alignment, OVERLAP = any-overlap within NEDC framework
³ SzCORE: Same tolerances applied to TUSZ eval - note ~10x FA reduction vs NEDC due to event merging

**Critical Note**: These are different datasets AND different scoring methods. The 1 FA/24h was achieved on Dianalund (small Nordic dataset), not TUSZ. SzCORE includes 30s pre-ictal and 60s post-ictal tolerances plus event merging (<90s gaps), making it ~10x more permissive than NEDC. Both scoring approaches have merit - SzCORE prioritizes clinical early warning while NEDC prioritizes temporal precision.

### Understanding Scoring Differences

TUSZ annotations were created by Temple University following specific clinical guidelines, with NEDC scoring designed by the same team as the matched evaluator. When evaluated with SzCORE (which adds tolerances for early detection), the same predictions yield dramatically different FA rates (~10x lower). Neither approach is "wrong" - they measure different aspects:

- **NEDC**: Prioritizes temporal precision for research
- **SzCORE**: Prioritizes clinical utility with early warning tolerances

### Authoritative Results

- See [`docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md`](docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md) for the single source of truth: 4 scoring methods × 3 operating points (Default, 10 FA, 2.5 FA), all without merge_gap.
- See [`docs/evaluation/PARAMETER_TUNING_METHODOLOGY.md`](docs/evaluation/PARAMETER_TUNING_METHODOLOGY.md) for why we tuned on NEDC OVERLAP and how to interpret differences across scoring methods.

Note: Earlier drafts included merge_gap-based operating points. Those are deprecated and archived. All current numbers are computed with merge_gap disabled.

### Key Metrics (TUSZ v2.0.3 eval)
- **Primary scorer**: NEDC v6.0.0 (Temple's official metrics for TUSZ)
- **Comparison scorer**: SzCORE (EpilepsyBench standard with clinical tolerances)
- **Dataset**: TUSZ v2.0.3 eval split (865 files, 469 seizures)
- **Tuning methodology**: Parameters tuned on dev using NEDC OVERLAP
- **AUROC**: 0.9021 (excellent discrimination capacity)
- **Files processed**: 865/865 (one header repaired on a temporary copy via `pyedflib+repaired`)

## 🔧 Evaluation Framework

### Components
1. **Model Wrapper**: Integrated Wu's pretrained SeizureTransformer for TUSZ inference (no retraining - using authors' weights)
2. **NEDC Integration**: Temple's v6.0.0 binaries (unmodified) for official scoring
3. **Evaluation Pipeline**: Dev-set tuning → Eval-set validation (only post-processing thresholds tuned)

### NEDC v6.0.0 Integration

| Implementation | Purpose | Location |
|----------------|---------|----------|
| Temple Binaries | Research validity | `evaluation/nedc_eeg_eval/v6.0.0/` |
| Native Python | Production deployment | `seizure_evaluation/` |

Both produce identical metrics (±0.1%). Temple's for papers, Python for deployment.

**Verify Parity:**
```bash
make -C evaluation/nedc_eeg_eval/nedc_scoring all BACKEND=temple
python tests/integration/test_nedc_conformance.py  # Confirms ±0.1% match
```

### Dataset and Methodology

| TUSZ Split | Files | Hours | Seizures | Our Use |
|------------|-------|-------|----------|----------|
| Train | 1,557 | 3,050 | ~2,900 | Not used (pretrained model) |
| Dev | 1,013 | 1,015 | ~920 | Threshold tuning |
| Eval (held-out) | 865 | 127.6 | 469 | Final results |

**Note**: Paper trains on TUSZ train subset (≈910h) + Siena (128h). We use the authors' pretrained weights; no retraining performed. Post-processing parameters were tuned on dev set using NEDC OVERLAP as target, then evaluated across all scoring methods for transparency.

## 🚀 Installation and Usage

### Prerequisites
- Python 3.10+, CUDA GPU (recommended), 32GB RAM
- TUSZ v2.0.3 dataset (see below for access)
- SeizureTransformer weights from [Wu's repo](https://github.com/keruiwu/SeizureTransformer)

### Quick Start
```bash
git clone https://github.com/Clarity-Digital-Twin/SeizureTransformer
cd SeizureTransformer

# Get model weights from https://github.com/keruiwu/SeizureTransformer
# Place at: wu_2025/src/wu_2025/model.pth

make setup-dev && source .venv/bin/activate
```

### Obtaining TUSZ Dataset
1. Request access: [Temple data use agreement](https://isip.piconepress.com/projects/nedc/html/tuh_eeg/)
2. Email signed form to `help@nedcdata.org`
3. Download with provided credentials:
```bash
# Eval split only (5.2GB, sufficient for reproduction)
rsync -auxvL nedc-tuh-eeg@www.isip.piconepress.com:data/tuh_eeg/tuh_eeg_seizure/v2.0.3/edf/eval .
```
4. Place at: `wu_2025/data/tusz/v2.0.3/`

### Running the Evaluation (Local)
```bash
# 1. Run inference on TUSZ (new CLI)
tusz-eval \
  --data_dir wu_2025/data/tusz/v2.0.3/edf/eval \
  --out_dir experiments/eval/baseline

# 2. Score with NEDC v6.0.0
make -C evaluation/nedc_eeg_eval/nedc_scoring all \
  CHECKPOINT=../../experiments/eval/baseline/checkpoint.pkl \
  OUTDIR=../../experiments/eval/baseline/nedc_results
# Output: experiments/eval/baseline/nedc_results/

# 3. Tune thresholds (optional)
python evaluation/nedc_eeg_eval/nedc_scoring/sweep_operating_point.py \
  --checkpoint experiments/dev/baseline/checkpoint.pkl \
  --target_fa_per_24h 10

### Docker Quick Start

CPU image:

```
make docker-build
make docker-run
# Note: Docker container routes eval → tusz-eval and nedc → nedc-run internally.
# For local runs outside Docker, prefer the `tusz-eval` and `nedc-run` CLIs.
```

GPU image (requires NVIDIA Container Toolkit):

```
make docker-build-gpu
make docker-run-gpu
```

NEDC scoring on saved predictions:

```
docker run -v $(pwd)/experiments:/experiments \
  --entrypoint nedc-run \
  seizure-transformer:latest \
  --checkpoint /experiments/results/checkpoint.pkl \
  --outdir /experiments/nedc_results
```
```

## 📂 Repository Structure

```
SeizureTransformer/
├── src/
│   └── seizure_evaluation/           # First‑party package (our code)
│       ├── tusz/                     # TUSZ inference CLI (tusz-eval)
│       ├── szcore/                   # SzCORE wrappers
│       ├── ovlp/                     # Native OVERLAP scorer (parity)
│       └── utils/                    # Utilities (EDF repair, etc.)
├── evaluation/                       # Vendored tools only
│   ├── nedc_eeg_eval/
│   │   ├── v6.0.0/                   # Official Temple NEDC (untouched)
│   │   └── nedc_scoring/             # Orchestration tools (ours)
├── wu_2025/                          # Original SeizureTransformer (vendored; do not modify)
└── experiments/                      # Results & checkpoints
```

## 📚 Technical Documentation

<details>
<summary>For Deep Dives</summary>

- [Documentation Index](docs/README.md) - Full, up‑to‑date docs map
- [Vendored Sources](docs/VENDORED_SOURCES.md) - Provenance and policy for vendored code
- [Complete Results](docs/evaluation/EVALUATION_RESULTS_TABLE.md) - Canonical metrics & analysis
- [Operating Points](docs/planning/OPERATIONAL_TUNING_PLAN.md) - Threshold tuning methodology (no merge, kernel=5)
- [NEDC Integration](docs/planning/NEDC_INTEGRATION_PLAN.md) - Temple scorer details
- [Model Architecture](docs/technical/IDEAL_REFERENCE_SEIZURE_TRANSFORMER_DATAFLOW.md) - Internals

</details>

## 📝 Citations

<details>
<summary>BibTeX Entries</summary>

```bibtex
# Our Evaluation
@software{seizuretransformer_tusz_2025,
  title = {SeizureTransformer TUSZ Evaluation with NEDC v6.0.0},
  author = {{Clarity Digital Twin Team}},
  year = {2025},
  url = {https://github.com/Clarity-Digital-Twin/SeizureTransformer}
}

# Original Model
@article{wu2025seizuretransformer,
  title = {SeizureTransformer: Scaling U-Net with Transformer},
  author = {Wu, Kerui and Zhao, Ziyue and Yener, Bülent},
  journal = {arXiv preprint arXiv:2504.00336},
  year = {2025}
}

# NEDC Scoring
@incollection{shah2021nedc,
  title = {Objective Evaluation Metrics for EEG Events},
  author = {Shah, V. and Golmohammadi, M. and Obeid, I. and Picone, J.},
  booktitle = {Signal Processing in Medicine and Biology},
  year = {2021}
}

# TUSZ Dataset
@article{shah2018temple,
  title = {The Temple University Hospital Seizure Detection Corpus},
  author = {Shah, V. and others},
  journal = {Frontiers in Neuroinformatics},
  year = {2018}
}
```

</details>

## ⚖️ License

- Our code: Apache-2.0
- SeizureTransformer: MIT (Wu et al.)
- NEDC tools: Temple University License
- TUSZ data: Requires data use agreement

## 🙏 Acknowledgments

- Kerui Wu for SeizureTransformer model and weights
- Temple University NEDC for dataset and scoring tools
- SzCORE/EpilepsyBench for benchmark infrastructure

## 🔮 Future Work

- **SzCORE Integration**: Implement SzCORE's "Any-Overlap" scoring wrapper to enable direct comparisons with EpilepsyBench leaderboard results
- **Cross-scoring Analysis**: Evaluate TUSZ predictions with both NEDC and SzCORE to quantify scoring methodology impact
- **Threshold Optimization**: Explore patient-specific thresholds for clinical deployment

## 📧 Contact

For issues or questions: [GitHub Issues](https://github.com/Clarity-Digital-Twin/SeizureTransformer/issues)
