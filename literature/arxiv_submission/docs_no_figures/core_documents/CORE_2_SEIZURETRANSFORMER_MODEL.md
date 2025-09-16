# CORE 2: SeizureTransformer Model
## Understanding the State-of-the-Art Architecture

### Executive Summary
SeizureTransformer represents a significant advance in seizure detection architecture, winning the 2025 EpilepsyBench Challenge. Our evaluation uses the authors' pretrained weights without modification, ensuring fair assessment of their published claims.

Sources in repo:
- Paper (markdown extract): `literature/markdown/seizure_transformer/SeizureTransformer.md`
- Model code: `wu_2025/src/wu_2025/`
- Canonical results: `docs/status/SINGLE_SOURCE_OF_TRUTH.md`, `docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md`, `docs/results/BENCHMARK_RESULTS.md`

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

Repo confirmation: defaults in code — `SeizureTransformer(in_channels=19, in_samples=15360)` in `wu_2025/src/wu_2025/architecture.py`.

#### Processing Pipeline
```
Raw EDF (variable sample rate)
    ↓ Z-score per‑channel (mean/std)
    ↓ Resample to 256 Hz (if needed)
    ↓ Bandpass filter (0.5–120 Hz)
    ↓ Notch filters (1 Hz and 60 Hz)
    ↓ 60-second windows (no overlap)
SeizureTransformer (U‑Net + Transformer)
    ↓ Per‑sample probabilities [0,1]
Post‑processing
    ↓ Threshold 0.8 → binary
    ↓ Morphological opening/closing (kernel=5)
    ↓ Remove events < 2.0 s
Output: binary seizure mask (length = n_samples)
```

Repo confirmation: preprocessing, dataloader, and post‑processing are implemented in `wu_2025/src/wu_2025/utils.py`.

### Model Parameters
- Size: 169 MB (`wu_2025/src/wu_2025/model.pth`)
- Parameters: ~41.0M (computed from `architecture.py`)
- Inference speed and memory: environment dependent; not asserted here

---

## Training Details (From Paper)

Paper (repo extract): `literature/markdown/seizure_transformer/SeizureTransformer.md`

Training data:
- TUSZ v2.0.3 predefined train set (~910 hours)
- Siena Scalp EEG Database (~128 hours)
- Resampled to 256 Hz; 19‑channel 10–20 montage alignment

#### Important note on Siena usage
- The Siena Scalp EEG Database, as distributed, does not ship with official train/dev/eval splits.
- Wu et al. concatenate 60‑second windows from TUSZ train and the full Siena dataset for training.
- Implication: Any evaluation reported on Siena using the authors’ pretrained weights is in‑sample and not a held‑out test.
  - If shown, Siena results must be labeled as descriptive only (not comparable to held‑out TUSZ eval metrics).

Construction and sampling:
- 60‑second windows (15360 samples); 75% overlap during dataset construction
- Class‑balanced sampling across no‑seizure, partial‑seizure, full‑seizure windows

### Training Protocol
- Optimizer: RAdam
- Learning rate: 1e‑3
- Weight decay: 2e‑5
- Batch size: 256
- Dropout (drop_rate): 0.1
- Loss: Binary cross‑entropy
- Epochs: 100 with early stopping (no val‑improve over 12 epochs)

### Data Construction Notes
- The paper emphasizes windowing strategy and class balancing; no explicit data augmentation procedures are specified in the repo extract.

---

## Published Performance Claims

### EpilepsyBench Results (Wu 2025)
| Dataset | Sensitivity | FA/24h | F1 Score |
|---------|------------|--------|----------|
| Dianalund | 37% | 1.0 | 43% |
| VHMUH | 42% | 2.3 | 48% |
| FNUSA | 35% | 1.8 | 41% |

Source: Table I in `literature/markdown/seizure_transformer/SeizureTransformer.md` (FP per day = FA/24h).

### Key Claim
"Achieved state‑of‑the‑art performance with 37% sensitivity at 1 FA/24h on Dianalund dataset" — supported by the above table.

---

## Our Implementation Approach

### Philosophy
**Use pretrained weights exactly as published - no retraining, no fine-tuning**

### Rationale
1. **Fairness**: Evaluate actual published model
2. **Reproducibility**: Anyone can download same weights
3. **Focus**: Our contribution is evaluation, not model improvement

### Simple Wrapper Design (repo code)
```python
from wu_2025.utils import load_models, get_dataloader, predict
from epilepsy2bids.annotations import Annotations
from epilepsy2bids.eeg import Eeg

def run_on_edf(edf_path, out_tsv):
    eeg = Eeg.loadEdfAutoDetectMontage(edfFile=edf_path)
    assert eeg.montage is Eeg.Montage.UNIPOLAR

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = load_models(device)

    # Preprocess (z‑score per channel; resample to 256 Hz; BP 0.5–120 Hz; notch 1 Hz & 60 Hz)
    dl = get_dataloader(eeg.data, eeg.fs, batch_size=512, window_size=15360)

    # Inference + post‑processing → binary mask
    y_mask = predict(model, dl, device, seq_len=eeg.data.shape[1])

    # Save annotations TSV
    hyp = Annotations.loadMask(y_mask, eeg.fs)
    hyp.saveTsv(out_tsv)
```
Repo references: `wu_2025/src/wu_2025/main.py`, `wu_2025/src/wu_2025/utils.py`.

### Post-Processing Parameters (paper defaults; implemented in repo)
- Threshold: 0.8
- Morphological opening/closing kernel: 5 samples
- Minimum duration: 2.0 seconds

Repo confirmation: `wu_2025/src/wu_2025/utils.py` (`predict`, `morphological_filter_1d`, `remove_short_events`).

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

Repo context for scoring (defaults; no merge gap):
- NEDC OVERLAP (Temple): 45.63% sensitivity, 26.89 FA/24h (SEIZ) — `docs/status/SINGLE_SOURCE_OF_TRUTH.md`, `docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md`
- SzCORE Any‑Overlap (EpilepsyBench): 52.35% sensitivity, 8.59 FA/24h — `docs/results/BENCHMARK_RESULTS.md`
  - SzCORE tolerances/merge rules documented in `literature/markdown/SzCORE/SzCORE.md`.

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

### Preprocessing and Inference (repo‑accurate)
```python
def make_dataloader(eeg_data, fs):
    # Z‑score per channel; resample to 256 Hz
    return get_dataloader(eeg_data, fs, batch_size=512, window_size=15360)

def run_inference(model, dataloader, device, seq_len):
    # Model outputs per‑sample probabilities; repo returns post‑processed mask
    return predict(model, dataloader, device, seq_len)
```
Signal conditioning per 60‑s window (inside dataset): 0.5–120 Hz bandpass, 1 Hz and 60 Hz notch — see `SeizureDataset.preprocess_clip` in `wu_2025/src/wu_2025/utils.py`.

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

FA/24h semantics note:
- For NEDC and Python OVERLAP, FA/24h refers to Temple’s “Total False Alarm Rate” (SEIZ + BCKG) per v6.0.0 summaries; for SzCORE, FA/24h follows SzCORE’s event‑based definition. See `docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md`.

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
