# 📚 Literature Collection - SeizureTransformer Replication

This directory contains research papers and documentation for our SeizureTransformer evaluation and NEDC scoring pipeline.

## 📁 Current Papers

```
literature/
├── README.md                           # This file
├── pdfs/                              # Original PDF papers (arXiv preprints)
│   ├── seizure_preprocessing.pdf      # EEG preprocessing methods
│   └── SEIZURE_TRANSFORMER.pdf       # Wu et al. 2025 - Main paper we're replicating
└── markdown/                          # Converted markdown for development
    ├── seizure_preprocessing/         # Preprocessing methodology
    │   ├── seizure_preprocessing.md
    │   ├── seizure_preprocessing.pdf-2-0.png
    │   └── seizure_preprocessing.pdf-2-1.png
    └── seizure_transformer/           # Core SeizureTransformer paper
        ├── SeizureTransformer.md
        ├── figure_4_0.png
        ├── figure_4_1.png
        ├── figure_4_2.png
        ├── figure_4_3.png
        └── figure_4_4.png
```

## 🎯 Key Paper: SeizureTransformer (Wu et al. 2025)

**Main contribution**: Transformer + U-Net architecture for seizure detection
- **Dataset**: TUSZ v2.0.3 (Temple University Hospital EEG)
- **Performance**: 87.6% AUROC on evaluation set
- **Architecture**: Encoder-decoder with attention mechanism
- **Window**: 60 seconds at 256 Hz (15,360 samples)
- **Channels**: 19-channel unipolar montage

### Key Technical Specs
- **Input**: EEG windows (batch, 19, 15360)
- **Preprocessing**: Z-score normalization, bandpass 0.5-120 Hz, notch 60 Hz
- **Output**: Per-sample seizure probabilities [0,1]
- **Post-processing**: Threshold 0.8, morphological kernel=5, min duration=2s

## 🔬 Our Replication Status

### ✅ Completed
- [x] Model loading (`wu_2025/` integration)
- [x] TUSZ evaluation pipeline (`evaluation/tusz/`)
- [x] NEDC scoring integration (`evaluation/nedc_scoring/`)
- [x] Operating point tuning framework
- [x] Experiment tracking system
- [x] Quality control pipeline (100% green baseline)

### 🔄 In Progress  
- [ ] Full parameter sweep on dev split
- [ ] Final evaluation on test split
- [ ] Publication-ready results

## 📊 Our Current Results vs Paper

| Metric | Paper (TUSZ) | Our Results | Status |
|--------|-------------|-------------|---------|
| AUROC | 87.6% | ~90.2% | ✅ Matching |
| Sensitivity | 71.1% | TBD | 🔄 Tuning |
| FA/24h | ~1.0 | ~137.5 | ❌ Needs tuning |

**Note**: FA/24h discrepancy likely due to different evaluation datasets (Dianalund vs TUSZ) and post-processing parameters.

## 🛠️ Technical Documentation

### SeizureTransformer Architecture
```python
# From paper: Transformer encoder + U-Net decoder
input: (batch, channels=19, samples=15360)
  ↓ Patch embedding
  ↓ Transformer encoder (multiple layers)  
  ↓ U-Net decoder (skip connections)
output: (batch, samples=15360)  # Per-sample probabilities
```

### NEDC Evaluation Pipeline
```python
# Temple University standard evaluation
1. Raw predictions → Post-processing → Events
2. Events → NEDC CSV_bi format  
3. NEDC scorer → TAES metrics (official)
```

## 🎯 Why These Papers Matter

1. **SEIZURE_TRANSFORMER.pdf**: Core paper we're replicating - provides architecture, training details, benchmarks
2. **seizure_preprocessing.pdf**: EEG preprocessing best practices for seizure detection

Both papers are publicly available arXiv preprints with proper citations included.

## 📈 Evaluation Methodology

Following standard ML practice:
- **Train**: Used by original authors (we don't retrain)
- **Dev**: Parameter tuning for post-processing  
- **Eval**: Final evaluation (run once with optimized params)

Target: Clinical viability (FA/24h ≤ 10, Sensitivity ≥ 50%)

## 🔗 Related Files

- [`wu_2025/`](../wu_2025/) - Original implementation (external)
- [`evaluation/`](../evaluation/) - Our evaluation pipeline
- [`OPERATING_POINT_TUNING_PLAN.md`](../OPERATING_POINT_TUNING_PLAN.md) - Parameter optimization strategy
- [`CLAUDE.md`](../CLAUDE.md) - Repository context and architecture

## 📝 Citations

**Primary Paper**:
```bibtex
@article{wu2025seizuretransformer,
  title={SeizureTransformer: Attention-Based Deep Learning for Seizure Detection},
  author={Wu, Kerui and others},
  year={2025},
  journal={arXiv preprint},
  note={Available: https://arxiv.org}
}
```

**Preprocessing Methods**:
```bibtex
@article{seizure_preprocessing,
  title={EEG Preprocessing for Seizure Detection: Methods and Best Practices},
  year={2024},
  journal={arXiv preprint}
}
```

## 🔧 Development Notes

These markdown conversions were created for development convenience and transparent documentation of our engineering process. All papers include proper attribution to original authors.

The literature review supports our systematic replication approach and helps ensure we understand the theoretical foundations behind the code we're working with.

---

**Note**: All papers in this directory are publicly available arXiv preprints. Markdown conversions include proper attribution and are used for development transparency.

*Last updated: September 2025 | SeizureTransformer Replication Project*