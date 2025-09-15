# Verified Key References for arXiv Paper

## Critical References - Now Corrected Based on Source Documents

### 1. SeizureTransformer (Wu et al., 2025)
**Corrected Citation:**
Wu K, Zhao Z, Yener B. SeizureTransformer: Scaling U-Net with Transformer for Simultaneous Time-Step Level Seizure Detection from Long EEG Recordings. International Conference on Artificial Intelligence in Epilepsy and Other Neurological Disorders. 2025. arXiv:2504.00336.

**Key Details from Source:**
- Won 2025 EpilepsyBench Challenge
- Achieved 37% sensitivity at 1 FA/24h on Dianalund dataset
- Trained on TUSZ v2.0.3 and Siena Scalp EEG Database
- Paper confirms AUROC of 0.876 on TUSZ test set

### 2. NEDC Scoring Software (Picone/Shah et al., 2021)
**Corrected Citation:**
Shah V, Golmohammadi M, Obeid I, Picone J. Objective Evaluation Metrics for Automatic Classification of EEG Events. In: Signal Processing in Medicine and Biology: Emerging Trends in Research and Applications. Obeid I, Selesnick I, Picone J, Eds. Springer; 2021. p. 1-26.

**Key Details from Source:**
- Defines TAES (Time-Aligned Event Scoring) and OVLP (Any-Overlap)
- Authors confirm OVLP is "very permissive"
- TAES provides partial credit based on temporal overlap
- Designed specifically for TUSZ evaluation

### 3. NEDC Software v6.0.0 (2025)
**New Citation Added:**
NEDC. Neural Engineering Data Consortium EEG Evaluation Software v6.0.0. Temple University; 2025. Available from: https://www.isip.piconepress.com/projects/nedc/

**Key Details from AAREADME.txt:**
- Version 6.0.0 released August 7, 2025
- Supports csv_bi format (NOT regular .csv)
- Implements both TAES and OVERLAP scoring
- Requires Python 3.9.x with numpy, scipy, lxml, toml

### 4. TUSZ Dataset (Shah et al., 2018)
**Corrected Citation:**
Shah V, von Weltin E, Lopez S, McHugh JR, Veloso L, Golmohammadi M, Obeid I, Picone J. The Temple University Hospital Seizure Detection Corpus. Front Neuroinform. 2018;12:83. doi:10.3389/fninf.2018.00083.

**Key Details from Source:**
- 16,986 sessions from 10,874 unique subjects
- Average age 51.6 years (range: <1 to >90)
- Most common: 31 EEG channels, 250Hz sampling (87%)
- Annotations by trained neurologists following strict clinical guidelines

### 5. SzCORE (Dan et al., 2024)
**Corrected Citation:**
Dan J, Pale U, Amirshahi A, Cappelletti W, Ingolfsson TM, Wang X, et al. SzCORE: A Seizure Community Open-source Research Evaluation framework for the validation of EEG-based automated seizure detection algorithms. 2024.

**Key Details from Source:**
- EPFL-led consortium (Embedded Systems Laboratory)
- Defines 30-second pre-ictal and 60-second post-ictal tolerances
- Merges events separated by <90 seconds
- Used as EpilepsyBench standard scorer

## Additional Important References

### 6. Temple University Hospital EEG Data Corpus (2016)
Obeid I, Picone J. The Temple University Hospital EEG Data Corpus. Front Neurosci. 2016;10:196.
- Earlier paper describing TUSZ corpus foundation

### 7. CHB-MIT Database (Shoeb, 2009)
Shoeb AH. Application of machine learning to epileptic seizure onset detection and treatment [PhD thesis]. MIT; 2009.
- Comparison dataset, 22 pediatric subjects

### 8. Clinical Standards (Beniczky & Ryvlin, 2018)
Beniczky S, Ryvlin P. Standards for testing and clinical validation of seizure detection algorithms. Epilepsia. 2018;59(S1):9-13.
- Establishes <10 FA/24h with ≥50% sensitivity as clinical threshold

## Verification Notes

✅ All author names verified from source documents
✅ Dates confirmed (2025 for SeizureTransformer and NEDC v6.0.0)
✅ arXiv number correct: 2504.00336
✅ NEDC v6.0.0 release date: August 7, 2025 (from AAREADME.txt)
✅ SzCORE authors confirmed from markdown file header
✅ TUSZ paper confirmed as Frontiers in Neuroinformatics, 2018

## Critical Facts for Paper

1. **SeizureTransformer Performance on Dianalund**: 37% sensitivity at 1 FA/24h (F1=0.43)
2. **SeizureTransformer AUROC on TUSZ**: 0.876 (from their paper)
3. **Our Finding on TUSZ**: 26.89 FA/24h with NEDC OVERLAP (27× worse)
4. **NEDC v6.0.0**: Released August 2025, implements both TAES and OVERLAP
5. **SzCORE Tolerances**: 30s pre-ictal, 60s post-ictal, <90s gap merging

## Citations to Use in Key Sections

### Introduction
- Cite [1] for SeizureTransformer winning EpilepsyBench
- Cite [3] for TUSZ dataset description
- Cite [6] for NEDC software

### Methods
- Cite [2] for NEDC scoring theory (Picone/Shah book chapter)
- Cite [4] for SzCORE methodology
- Cite [6] for NEDC v6.0.0 implementation

### Results
- Reference all scoring methods with appropriate citations
- Use [10] for clinical threshold standards

### Discussion
- Cite [11] for reproducibility crisis
- Cite [12] for deployment challenges