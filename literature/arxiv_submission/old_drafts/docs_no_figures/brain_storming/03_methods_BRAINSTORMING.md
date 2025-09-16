# Methods Section Brainstorming

## Key Goal
Write a crystal-clear, reproducible methods section that allows anyone to replicate our evaluation exactly.

## Core Components to Cover

### 1. Dataset and Splits
- TUSZ v2.0.3 eval set: 865 files, 127.7 hours, 469 seizures, 43 patients
- Patient-disjoint from train/dev (no data leakage)
- One file required header repair (pyedflib)
- 100% coverage achieved

### 2. Model and Inference
- Used authors' pretrained weights (168MB, no modifications)
- Input: 19-channel unipolar montage, 256 Hz
- Preprocessing: z-score, resample, bandpass 0.5-120Hz, notch at 1Hz and 60Hz
- 60-second windows, no overlap during inference
- Post-processing: threshold 0.8, morphological kernel 5, min duration 2.0s

### 3. Scoring Methodologies (4 scorers, same predictions)
- NEDC TAES: Time-aligned event scoring with partial credit
- NEDC OVERLAP: Temple's binary any-overlap implementation
- Native OVERLAP: Our Python implementation (perfect parity with NEDC)
- SzCORE: Any-overlap with -30s/+60s tolerances and 90s merge

### 4. Parameter Tuning Protocol
- Grid search on TUSZ dev set (1,832 files, 53 patients)
- Target: ≤10 FA/24h with maximum sensitivity (NEDC OVERLAP)
- Explored: thresholds [0.6-0.95], kernels [3-15], durations [1-5s]
- Selected three operating points for comprehensive reporting

### 5. Implementation and Validation
- Python wrapper around original wu_2025 code
- NEDC v6.0.0 binary for clinical scoring
- CSV_bi format conversion for NEDC compatibility
- Parity validation: <0.1% variance between implementations

## Structure Flow

### Opening
"We evaluated SeizureTransformer on the TUSZ v2.0.3 held-out test set using the authors' pretrained weights without modification. Our evaluation employed four distinct scoring methodologies on identical model predictions to quantify the impact of evaluation standards on reported performance."

### Section 3.1: Dataset
- TUSZ eval set characteristics
- Patient-disjoint design importance
- File processing and coverage

### Section 3.2: Model Inference Pipeline
- Pretrained weights usage
- Preprocessing details
- Window-based inference
- Post-processing parameters

### Section 3.3: Scoring Methodologies
- Four scorers explained
- Mathematical definitions
- Clinical vs research priorities

### Section 3.4: Parameter Optimization
- Dev set tuning protocol
- Grid search space
- Clinical target (≤10 FA/24h)
- Operating point selection

### Section 3.5: Implementation Details
- Software architecture
- NEDC integration
- Validation procedures
- Reproducibility measures

## Key Technical Details to Include

### Preprocessing Pipeline
```
Raw EDF → Channel normalization → Z-score → Resample 256Hz →
Bandpass 0.5-120Hz → Notch 1Hz, 60Hz → 60s windows
```

### Post-processing Parameters
- Default: θ=0.80, k=5, d=2.0s
- Clinical: θ=0.95, k=15, d=5.0s
- Aggressive: θ=0.60, k=3, d=1.0s

### NEDC CSV_bi Format
```csv
# version = csv_v1.0.0
# duration = 1800.0000 secs
channel,start_time,stop_time,label,confidence
TERM,42.2786,81.7760,seiz,1.0000
```

### Channel Handling
- epilepsy2bids.Eeg.loadEdfAutoDetectMontage
- Enforces unipolar montage
- Stable 19-channel ordering
- Automatic alias normalization

## Important Clarifications

### What We Did NOT Do
- Did not retrain the model
- Did not fine-tune on TUSZ
- Did not modify architecture
- Did not use eval set for tuning

### What We DID Do
- Used exact pretrained weights
- Tuned post-processing on dev only
- Evaluated on held-out test set
- Compared scoring methodologies

### Siena Note
"While the pretrained model was trained on both TUSZ train and Siena datasets, our evaluation focuses exclusively on the TUSZ eval set, which provides patient-disjoint held-out testing."

## Key Numbers to Include
- 865 EDF files processed
- 127.7 hours of recordings
- 469 seizures annotated
- 43 unique patients
- 100% file coverage
- 256 Hz sampling rate
- 60-second windows
- 19 channels (10-20 system)

## Reproducibility Elements
- Code: github.com/[to-be-released]
- Weights: wu_2025/model.pth (168MB)
- NEDC: v6.0.0 from Temple
- Dataset: TUSZ v2.0.3 eval split

## Professional Language Examples

### On evaluation philosophy:
"Our evaluation prioritizes transparency and reproducibility. By applying multiple scoring standards to identical predictions, we isolate the impact of evaluation methodology from model performance."

### On NEDC usage:
"We employed NEDC v6.0.0, the clinical scoring standard developed by Temple University specifically for TUSZ evaluation, ensuring dataset-matched assessment."

### On parameter tuning:
"Post-processing parameters were optimized exclusively on the development set to identify configurations meeting clinical deployment criteria while maintaining evaluation integrity."

## Pitfalls to Avoid
- Don't claim we improved the model
- Don't suggest TUSZ is the only valid test
- Don't dismiss SzCORE as "wrong"
- Don't overstate clinical readiness

## Strong Closing
"This comprehensive evaluation framework, combining the authors' pretrained model with multiple clinical scoring standards, reveals how methodological choices fundamentally shape reported performance metrics in seizure detection systems."