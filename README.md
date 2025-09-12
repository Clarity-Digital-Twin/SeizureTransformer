# SeizureTransformer - Independent Evaluation Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![NEDC v6.0.0](https://img.shields.io/badge/NEDC-v6.0.0-green.svg)](https://www.isip.piconepress.com/projects/nedc/)

## 🎯 Project Overview

This repository provides an **independent, reproducible evaluation** of the SeizureTransformer model ([Wu et al., 2025](https://github.com/keruiwu/SeizureTransformer)) on the Temple University Hospital EEG Seizure Corpus (TUSZ v2.0.3) using official NEDC scoring tools.

### Key Findings

| Metric | Paper Claim | Our Result (TUSZ v2.0.3) | Status |
|--------|------------|---------------------------|---------|
| **AUROC** | 0.876 | **0.9021** | ✅ Better |
| **Sensitivity** | 71.1%* | **24.15%** | ❌ Lower |
| **F1 Score** | 67.5%* | **31.19%** | ❌ Lower |
| **False Alarms/24h** | 1** | **137.5** | ❌ Much worse |

*Paper uses event-based scoring, we use TAES (stricter)  
**Paper reports on Dianalund dataset, not TUSZ

### What We Built

1. **Complete TUSZ evaluation pipeline** with GPU acceleration
2. **NEDC v6.0.0 integration** for official Temple University scoring
3. **Comprehensive documentation** of methodology and results
4. **Reproducible benchmark submission** for Epilepsy Bench/SzCORE
5. **Analysis revealing discrepancies** in paper's performance claims

## 📁 Repository Structure

```
.
├── wu_2025/                    # Original SeizureTransformer code (untouched)
│   └── src/wu_2025/model.pth   # Pretrained weights (168MB)
├── evaluation/                  # Our evaluation framework
│   ├── tusz/                   # TUSZ dataset evaluation
│   ├── nedc_scoring/           # NEDC format conversion & scoring
│   └── nedc_eeg_eval/v6.0.0/   # Official NEDC binaries
├── scripts/                     # Utility scripts
├── tests/                      # Test suite
├── docs/                       # Technical documentation
└── literature/                 # Papers (gitignored)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- CUDA-capable GPU (recommended)
- 32GB RAM
- TUSZ v2.0.3 dataset (127.6 hours)

### Installation

```bash
# Clone repository
git clone https://github.com/Clarity-Digital-Twin/SeizureTransformer
cd SeizureTransformer

# Setup environment (using uv for speed)
pip install uv
uv venv
source .venv/bin/activate

# Install packages
uv pip install ./wu_2025           # Original model
uv pip install -e . --extra dev    # Our evaluation tools
```

### Run Complete Evaluation

```bash
# 1. Run TUSZ evaluation (GPU recommended)
python evaluation/tusz/run_tusz_eval.py \
    --data_dir /path/to/TUSZ/v2.0.3/eval \
    --output_dir evaluation/tusz \
    --device cuda

# 2. Convert predictions to NEDC format
python evaluation/nedc_scoring/convert_predictions.py

# 3. Run official NEDC scoring
cd evaluation/nedc_scoring
make all  # Runs complete NEDC pipeline
```

## 📊 Results Summary

### NEDC TAES Scoring (Official Temple University Metrics)

```
Sensitivity:     24.15% (113/469 seizures detected)
Precision:       43.98% 
F1 Score:        31.19%
False Alarms:    137.5 per 24 hours
AUROC:           0.9021
```

### Clinical Implications

- **Good discrimination** (AUROC > 0.9) at sample level
- **Poor clinical performance** due to:
  - Low seizure detection rate (missing 76% of seizures)
  - Excessive false alarms (14x above clinical threshold)
- **137x discrepancy** between paper's "1 FA/day" claim and TUSZ reality

## 📚 Documentation

### Core Documents
- [README.md](README.md) - This file, project overview
- [ACKNOWLEDGMENTS.md](ACKNOWLEDGMENTS.md) - Credits and citations
- [CLAUDE.md](CLAUDE.md) - AI assistant guidance (for contributors)
- [CITATION.cff](CITATION.cff) - Structured citation metadata

### Evaluation Results
- [Complete Results](docs/evaluation/EVALUATION_RESULTS.md) - Full evaluation with analysis
- [Validation Report](docs/evaluation/TESTING_AND_VALIDATION.md) - Reproducibility & validation

  ### Technical Documentation
  - [NEDC Integration](docs/technical/NEDC_INTEGRATION_PLAN.md) - NEDC pipeline setup
  - [Architecture Guide](docs/technical/IDEAL_REFERENCE_SEIZURE_TRANSFORMER_DATAFLOW.md) - Model dataflow
  - [NEDC Understanding](docs/technical/NEDC_EVALUATION_UNDERSTANDING.md) - Scoring metrics explained
  - [Repository Structure](docs/technical/REPO_STRUCTURE_PLAN.md) - Project organization
  - [Third-Party Notices](THIRD_PARTY_NOTICES.md) - Licenses and attributions

### Benchmark Submissions
- [Epilepsy Bench Submission](docs/submissions/EPILEPSY_BENCH_SUBMISSION.md) - SzCORE format
- [Policy Clarification Request](docs/submissions/NOTE_TO_EPILEPSY_BENCH.md) - TUH reporting policy

## 🔬 Technical Details

### Model Architecture
- **Type**: U-Net encoder + Transformer decoder
- **Input**: 19-channel EEG, 60-second windows
- **Output**: Per-sample seizure probability at 256 Hz

### Preprocessing Pipeline
1. Z-score normalization (per channel)
2. Resample to 256 Hz
3. Bandpass filter: 0.5-120 Hz
4. Notch filter: 60 Hz

### Post-processing
- Probability threshold: 0.8
- Morphological operations (kernel=5)
- Minimum event duration: 2.0 seconds

### Evaluation Protocol
- **Dataset**: TUSZ v2.0.3 eval split
- **Files**: 864/865 processed
- **Duration**: 127.6 hours
- **Seizures**: 469 events
- **Scorer**: NEDC v6.0.0 TAES

## 🤝 Contributing

We encourage contributions to improve seizure detection evaluation:

1. Fork the repository
2. Create a feature branch
3. Run tests: `pytest tests/`
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📖 Citations

If you use this evaluation framework, please cite:

```bibtex
@software{seizuretransformer_eval2025,
  title = {SeizureTransformer: Independent Evaluation Framework with NEDC Integration},
  author = {Clarity Digital Twin Team},
  year = {2025},
  url = {https://github.com/Clarity-Digital-Twin/SeizureTransformer}
}
```

Also cite the original work:

```bibtex
@article{wu2025seizuretransformer,
  title = {SeizureTransformer: Versatile Seizure Detection Model},
  author = {Wu, Kerui and others},
  year = {2025},
  journal = {arXiv preprint}
}
```

## 📜 License

- Original SeizureTransformer: MIT License (Kerui Wu)
- Our evaluation framework: MIT License
- NEDC tools: Temple University license

## 🙏 Acknowledgments

- **Kerui Wu** and team for the SeizureTransformer model
- **Temple University** for TUSZ dataset and NEDC tools
- **SzCORE/Epilepsy Bench** for standardization efforts

## 📬 Contact

- **Issues**: [GitHub Issues](https://github.com/Clarity-Digital-Twin/SeizureTransformer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Clarity-Digital-Twin/SeizureTransformer/discussions)

---

**Note**: This is an independent evaluation. Results may differ from the original paper due to:
- Different datasets (TUSZ vs Dianalund)
- Different scoring methods (TAES vs event-based)
- Zero-shot evaluation (model not trained on TUSZ)
