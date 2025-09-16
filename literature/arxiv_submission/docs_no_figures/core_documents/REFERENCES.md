# Literature References for arXiv Paper

## Core Papers (Must Cite)

### 1. SeizureTransformer - The Model Under Evaluation
```bibtex
@article{wu2025seizuretransformer,
  title={SeizureTransformer: Achieving State-of-the-Art Performance via Scaling U-Net with Transformer for EEG-Based Seizure Detection},
  author={Wu, Kerui and Zhao, Ziyue and Yener, Bülent},
  journal={arXiv preprint arXiv:2504.00336},
  year={2025}
}
```
**Key Points**: Won EpilepsyBench 2025, claims 37% @ 1 FA/24h on Dianalund

### 2. NEDC Scoring - Picone 2021
```bibtex
@incollection{picone2021objective,
  title={Objective Evaluation Metrics for Automatic Event Detection Algorithms},
  author={Picone, Joseph and Obeid, Iyad and Shah, Vinit and Harabagiu, Stefan and Golmohammadi, Meysam},
  booktitle={Signal Processing in Medicine and Biology},
  pages={235--282},
  year={2021},
  publisher={Springer}
}
```
**Key Points**: Defines TAES (strict) and OVERLAP (common), designed for TUSZ

### 3. TUSZ Dataset - Shah 2018
```bibtex
@article{shah2018temple,
  title={The Temple University Hospital Seizure Detection Corpus},
  author={Shah, Vinit and von Weltin, Eva and Lopez, Silvia and McHugh, James R and Veloso, Lydia and Golmohammadi, Meysam and Obeid, Iyad and Picone, Joseph},
  journal={Frontiers in Neuroinformatics},
  volume={12},
  pages={83},
  year={2018}
}
```
**Key Points**: 3,050 hours training data, clinical annotations by Temple

### 4. SzCORE - EpilepsyBench Standard
```bibtex
@article{ebenezer2024szscore,
  title={SzCORE: Development and Validation of a Seizure Dataset for Performance Evaluation and Benchmarking},
  author={Ebenezer, Jonathan Kuo and Sanjay, A and Rajamanickam, Y and Kohli, M and Todd, C and Nurse, E and Freestone, D and Maturana, M},
  journal={medRxiv},
  year={2024},
  doi={10.1101/2024.08.12.24311765}
}
```
**Key Points**: Any-overlap with 30s/60s tolerances, merges <90s gaps

### 5. EpilepsyBench Challenge
```bibtex
@misc{epilepsybench2025,
  title={EpilepsyBench: Machine Learning for Seizure Forecasting Challenge},
  author={{EpilepsyBench Consortium}},
  year={2025},
  url={https://epilepsybenchmarks.com}
}
```
**Key Points**: Cross-dataset benchmark, uses SzCORE for all evaluations

---

## Supporting Literature

### Clinical Context Papers

**FDA Requirements for Seizure Detection**
```bibtex
@article{beniczky2024clinical,
  title={Clinical validation criteria for seizure detection algorithms},
  author={Beniczky, Sándor and Ryvlin, Philippe},
  journal={Clinical Neurophysiology},
  volume={145},
  pages={1--8},
  year={2024}
}
```
**Relevance**: Establishes <10 FA/24h as clinical viability threshold

**Review of Seizure Detection Methods**
```bibtex
@article{shoeibi2021epileptic,
  title={Epileptic seizures detection and prediction using deep learning: survey},
  author={Shoeibi, Afshin and others},
  journal={IEEE Reviews in Biomedical Engineering},
  volume={15},
  pages={240--256},
  year={2021}
}
```
**Relevance**: Context on why evaluation standards matter

### Related Technical Work

**Time-Aligned Metrics in Medical AI**
```bibtex
@article{ward2019assessment,
  title={Assessment of metric performance for event detection algorithms},
  author={Ward, R. and Picone, J.},
  journal={IEEE Trans Biomed Eng},
  volume={66},
  number={12},
  pages={3452--3460},
  year={2019}
}
```
**Relevance**: Theoretical foundation for TAES scoring

**Cross-Dataset Generalization Issues**
```bibtex
@article{gemein2020machine,
  title={Machine-learning-based diagnostics of EEG pathology},
  author={Gemein, Lukas AW and others},
  journal={NeuroImage},
  volume={220},
  pages={117021},
  year={2020}
}
```
**Relevance**: Why models fail when deployed on new datasets

---

## Papers to Reference in Discussion

### On Reproducibility Crisis
```bibtex
@article{haibe2020transparency,
  title={Transparency and reproducibility in artificial intelligence},
  author={Haibe-Kains, Benjamin and others},
  journal={Nature},
  volume={586},
  number={7829},
  pages={E14--E16},
  year={2020}
}
```

### On Clinical Deployment Challenges
```bibtex
@article{kelly2019key,
  title={Key challenges for delivering clinical impact with artificial intelligence},
  author={Kelly, Christopher J and others},
  journal={BMC Medicine},
  volume={17},
  number={1},
  pages={1--9},
  year={2019}
}
```

---

## Literature We Have Locally

1. **picone-2021-objective-evaluation-metrics.md**
   - Full details on TAES vs OVERLAP
   - Mathematical definitions
   - Justification for stricter metrics

2. **shah-2018-tusz-book-chapter.md**
   - Dataset construction methodology
   - Annotation guidelines
   - Clinical context

3. **SeizureTransformer.md**
   - Model architecture details
   - Training methodology
   - Original performance claims

4. **SzCORE.md**
   - Tolerance windows explanation
   - Event merging logic
   - Clinical justification

5. **seizure_preprocessing.md**
   - Signal processing pipeline
   - Filtering specifications
   - Windowing approach

---

## Key Quotes to Use

### From Picone 2021:
> "OVLP is considered a very permissive way of scoring since any amount of overlap between a reference and hypothesis event constitutes a true positive."

> "TAES was proposed as an alternative... weights the decision based on the percentage of overlap."

### From SzCORE:
> "30-second pre-ictal tolerance allows for early warning systems"
> "Events separated by less than 90 seconds are merged"

### From Shah 2018 (TUSZ):
> "Annotations were performed by trained neurologists following strict clinical guidelines"

### From Wu 2025 (SeizureTransformer):
> "Achieved 37% sensitivity at 1 FA/24h on Dianalund dataset"
> "Trained on subset of TUSZ v1.5.2"

---

## Citation Strategy

### In Introduction
- Cite clinical requirements (Beniczky 2024)
- Cite SeizureTransformer win (Wu 2025, EpilepsyBench 2025)
- Cite TUSZ as gold standard (Shah 2018)

### In Methods
- Cite NEDC scoring details (Picone 2021)
- Cite SzCORE methodology (Ebenezer 2024)
- Cite dataset specifics (Shah 2018)

### In Discussion
- Cite reproducibility crisis (Haibe-Kains 2020)
- Cite deployment challenges (Kelly 2019)
- Cite metric theory (Ward 2019)

### In Related Work
- Cite seizure detection reviews (Shoeibi 2021)
- Cite generalization issues (Gemein 2020)

---

## Missing References to Find

1. **NEDC v6.0.0 Software Release**
   - Check if there's a DOI or software citation
   - Temple University ISIP website

2. **Docker/Containerization Best Practices**
   - For reproducibility section
   - Maybe cite Docker paper or best practices guide

3. **Statistical Methods**
   - For parameter sweep methodology
   - Grid search optimization references

4. **EEG Standards**
   - International 10-20 system
   - Clinical EEG guidelines