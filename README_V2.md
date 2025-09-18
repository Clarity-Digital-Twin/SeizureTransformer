# SeizureTransformer on TUSZ: First Clinical Evaluation with NEDC v6.0.0
## Reveals 27× False Alarm Gap from Reported Performance

[![arXiv](https://img.shields.io/badge/arXiv-2025.XXXXX-b31b1b.svg)](https://arxiv.org/abs/2025.XXXXX)
[![EpilepsyBench Winner](https://img.shields.io/badge/EpilepsyBench%202025-%231-gold.svg)](https://epilepsybenchmarks.com/challenge/)
[![NEDC v6.0.0](https://img.shields.io/badge/NEDC-v6.0.0-brightgreen.svg)](https://www.isip.piconepress.com/projects/nedc/)
[![TUSZ v2.0.3](https://img.shields.io/badge/TUSZ-v2.0.3-blue.svg)](https://isip.piconepress.com/projects/tuh_eeg/)

**TL;DR:** SeizureTransformer won EpilepsyBench 2025 with 1 FA/24h on Dianalund. We evaluated it on TUSZ v2.0.3 using the clinical standard NEDC v6.0.0 scorer. **Result: 26.89 FA/24h** — a 27× gap from the reported performance.

## 🎯 Key Finding

The same model that achieves 1 FA/24h on Dianalund (Nordic dataset, SzCORE scoring) produces **26.89 FA/24h** on TUSZ (Temple dataset, NEDC scoring). This isn't a model failure — it's a demonstration of how dataset and scoring choices fundamentally shape reported metrics.

## 📊 Results

| Dataset | Scorer | Sensitivity | FA/24h | Note |
|---------|--------|-------------|--------|------|
| **Dianalund** | SzCORE¹ | 37% | **1** | EpilepsyBench Winner |
| **TUSZ eval** | NEDC OVERLAP² | 45.63% | **26.89** | Clinical Standard |
| **TUSZ eval** | SzCORE Event¹ | 52.35% | **8.59** | With Tolerances |
| **TUSZ eval** | NEDC TAES² | 65.21% | **136.73** | Strictest (Partial Credit) |

¹ SzCORE: 30s pre-ictal, 60s post-ictal tolerances, merges events <90s apart
² NEDC: Temple's clinical scorer for TUSZ. OVERLAP = any-overlap, TAES = time-aligned

**Key insight:** Same predictions, different scorers → 3.1× difference in FA/24h (26.89 vs 8.59). This demonstrates how evaluation methodology fundamentally shapes reported performance.

## 🚀 Quick Start

```bash
# 1. Setup
git clone https://github.com/Clarity-Digital-Twin/SeizureTransformer
cd SeizureTransformer
make setup-dev && source .venv/bin/activate

# 2. Get pretrained weights from https://github.com/keruiwu/SeizureTransformer
# Place at: wu_2025/src/wu_2025/model.pth

# 3. Get TUSZ eval data (5.2GB, requires Temple data agreement)
# From https://isip.piconepress.com/projects/nedc/html/tuh_eeg/
rsync -auxvL nedc-tuh-eeg@www.isip.piconepress.com:data/tuh_eeg/tuh_eeg_seizure/v2.0.3/edf/eval .

# 4. Run evaluation
tusz-eval --data_dir ./eval --out_dir experiments/baseline

# 5. Score with NEDC v6.0.0
nedc-run --checkpoint experiments/baseline/checkpoint.pkl --outdir results/
```

See [full documentation](docs/README.md) for Docker, GPU support, and parameter tuning.

## 📂 Key Components

- **`wu_2025/`** — Original SeizureTransformer (vendored, unmodified)
- **`evaluation/nedc_eeg_eval/v6.0.0/`** — Temple's official NEDC scorer
- **`src/seizure_evaluation/`** — Our evaluation pipeline
- **`literature/arxiv_submission/`** — Full paper and figures

## 📝 Paper & Citation

```bibtex
@article{clarity2025seizuretransformer,
  title = {SeizureTransformer on TUSZ: Clinical Evaluation Reveals 27-137x False Alarm Gap},
  author = {{Clarity Digital Twin Team}},
  journal = {arXiv preprint arXiv:2025.XXXXX},
  year = {2025}
}
```

For the original model, please cite [Wu et al. 2025](https://arxiv.org/abs/2504.00336).

## ⚖️ License

Apache-2.0 (our code) • MIT (SeizureTransformer) • Temple License (NEDC)

## 🙏 Acknowledgments

Kerui Wu for the model • Temple NEDC for tools and dataset • EpilepsyBench for infrastructure

---

**Questions?** Open an [issue](https://github.com/Clarity-Digital-Twin/SeizureTransformer/issues) • **Paper:** [arXiv:2025.XXXXX](https://arxiv.org/abs/2025.XXXXX)
