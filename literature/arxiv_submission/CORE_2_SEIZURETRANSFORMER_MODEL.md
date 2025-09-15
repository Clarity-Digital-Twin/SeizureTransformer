# CORE 2: SeizureTransformer Model
## Understanding the State-of-the-Art Architecture

### Executive Summary
SeizureTransformer represents a significant advance in seizure detection architecture, winning the 2025 EpilepsyBench Challenge. Our evaluation uses the authors' pretrained weights without modification, ensuring fair assessment of their published claims.

---

## Model Architecture (Wu et al. 2025)

### Core Innovation
> "Scaling U-Net with Transformer for EEG-Based Seizure Detection"

Combines:
- **U-Net**: Proven biomedical segmentation architecture
- **Transformer**: Self-attention for long-range dependencies
- **Multi-scale**: Captures both local and global EEG patterns

### Technical Specifications

#### Input Requirements
```python
# Expected Input Format
- Channels: 19 (TCP montage)
- Sampling Rate: 256 Hz
- Window Size: 60 seconds
- Shape: (19, 15360)  # 19 channels × 60s × 256Hz
```

#### Processing Pipeline
```
Raw EDF (variable sample rate)
    ↓ Resample to 256 Hz
    ↓ Bandpass filter (0.5-120 Hz)
    ↓ Notch filter (60 Hz)
    ↓ Z-score normalization
    ↓ 60-second windows
SeizureTransformer
    ↓ Per-sample probabilities [0,1]
Output: (15360,) probability vector
```

### Model Parameters
- **Size**: 168MB (model.pth)
- **Parameters**: ~42M trainable parameters
- **Inference Speed**: ~0.5 seconds per 60-second window (GPU)
- **Memory**: 4GB GPU recommended

---

## Training Details (From Paper)

### Dataset
```
Training Data:
- TUSZ v1.5.2 subset (~910 hours)
- Siena Scalp EEG Database (128 hours)
- Total: ~1,038 hours

Validation:
- TUSZ dev split (patient-disjoint)
```

### Training Protocol
- **Optimizer**: AdamW
- **Learning Rate**: 1e-4 with cosine annealing
- **Batch Size**: 32
- **Epochs**: 100 (early stopping)
- **Loss**: Weighted binary cross-entropy

### Data Augmentation
- Time shifting
- Amplitude scaling
- Gaussian noise injection

---

## Published Performance Claims

### EpilepsyBench Results (Wu 2025)
| Dataset | Sensitivity | FA/24h | F1 Score |
|---------|------------|--------|----------|
| Dianalund | 37% | 1.0 | 43% |
| VHMUH | 42% | 2.3 | 48% |
| FNUSA | 35% | 1.8 | 41% |

### Key Claim
> "Achieved state-of-the-art performance with 37% sensitivity at 1 FA/24h on Dianalund dataset"

---

## Our Implementation Approach

### Philosophy
**Use pretrained weights exactly as published - no retraining, no fine-tuning**

### Rationale
1. **Fairness**: Evaluate actual published model
2. **Reproducibility**: Anyone can download same weights
3. **Focus**: Our contribution is evaluation, not model improvement

### Simple Wrapper Design
```python
class SeizureTransformerWrapper:
    def __init__(self, model_path):
        self.model = load_pretrained(model_path)
        self.model.eval()  # Inference mode only

    def predict(self, edf_path):
        # Load and preprocess
        data = load_edf(edf_path)
        data = preprocess(data)  # Their exact preprocessing

        # Run inference
        with torch.no_grad():
            probs = self.model(data)

        return probs  # Raw probabilities for scoring
```

### Post-Processing Parameters
From paper defaults:
- **Threshold**: 0.8
- **Morphological Kernel**: 5 samples
- **Minimum Duration**: 2.0 seconds

---

## Professional Assessment

### Genuine Strengths
1. **Architecture Innovation**: Transformer + U-Net is clever combination
2. **Strong Baseline**: Beats previous CNN-based approaches
3. **Open Weights**: Authors shared pretrained model (commendable!)
4. **Cross-Dataset**: Trained on multiple sources (TUSZ + Siena)

### Legitimate Limitations
1. **Computational Cost**: Transformer overhead vs pure CNN
2. **Window-Based**: 60-second windows might miss longer patterns
3. **Black Box**: Attention mechanisms hard to interpret clinically

### Critical but Fair Points
- **Never evaluated on TUSZ eval set** despite training on TUSZ
- **FA rates depend entirely on scoring** (not model's fault)
- **Clinical deployment gap** exists for all current models

---

## How to Write About SeizureTransformer

### DO Say
- "State-of-the-art architecture combining U-Net and Transformer"
- "Won EpilepsyBench 2025 Challenge with impressive cross-dataset performance"
- "Authors' openness in sharing weights enables reproducible evaluation"

### DON'T Say
- "The model doesn't really work" (it does, just different metrics)
- "Claims are misleading" (they're accurate for their evaluation)
- "Architecture is overly complex" (subjective judgment)

### Cutting but Fair Language
- "Despite training on TUSZ, no evaluation with clinical scoring existed"
- "The 1 FA/24h achievement was on Dianalund, not the training dataset"
- "Performance claims require context of scoring methodology used"

---

## Technical Details for Methods Section

### Preprocessing (Exact Replication)
```python
def preprocess_edf(edf_path):
    # 1. Load EDF
    raw = mne.io.read_raw_edf(edf_path)

    # 2. Select 19 channels (TCP montage)
    raw.pick_channels(TCP_CHANNELS)

    # 3. Resample to 256 Hz
    raw.resample(256)

    # 4. Bandpass filter
    raw.filter(0.5, 120, fir_design='firwin')

    # 5. Notch filter
    raw.notch_filter(60)

    # 6. Z-score normalization
    data = raw.get_data()
    data = (data - data.mean()) / data.std()

    return data
```

### Inference Pipeline
```python
def run_inference(model, edf_path):
    # Preprocess
    data = preprocess_edf(edf_path)

    # Window extraction (60s, no overlap)
    windows = extract_windows(data, window_sec=60)

    # Run model
    all_probs = []
    for window in windows:
        probs = model(window)
        all_probs.append(probs)

    # Concatenate
    full_probs = np.concatenate(all_probs)

    return full_probs
```

---

## Key Messages for Paper

### The Positive
1. SeizureTransformer represents genuine architectural advance
2. Authors' transparency with weights enables our evaluation
3. Cross-dataset training shows generalization effort

### The Neutral
1. We use model exactly as published - no modifications
2. Our focus is evaluation methodology, not architecture
3. Performance depends on evaluation standard chosen

### The Critical
1. Training on TUSZ but not evaluating with NEDC is significant gap
2. 100× difference between datasets highlights generalization challenge
3. Clinical deployment requires dataset-matched evaluation

---

## Quote Bank

### From Wu et al. 2025
> "Achieved state-of-the-art performance"
> "37% sensitivity at 1 FA/24h on Dianalund"
> "Scaling U-Net with Transformer"

### For Our Paper
- "We use the authors' pretrained weights without modification"
- "The model achieves strong performance when evaluated appropriately"
- "Architecture innovations are orthogonal to evaluation standards"

---

## Ethical Considerations

### Credit Where Due
- Acknowledge Wu et al.'s contribution
- Cite their paper prominently
- Thank them for open weights

### Constructive Criticism
- Focus on evaluation gap, not model quality
- Highlight systemic issue, not individual failing
- Propose solutions, not just problems