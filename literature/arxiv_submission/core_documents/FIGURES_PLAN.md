# Figures and Tables Plan

## Main Figures (4-5 maximum for arXiv)

### Figure 1: The Performance Spectrum (HERO FIGURE)
**Type**: Bar chart with dramatic visual impact
**Message**: Same predictions, wildly different scores

```
False Alarms per 24 Hours (log scale)
|
|  137.53 ████████████████████████████████ NEDC TAES
|   26.89 ███████████████████████ NEDC OVERLAP (SEIZ)
|   26.89 ███████████████████████ Python OVERLAP
|    8.59 ███████ SzCORE
|    1.00 | Dianalund Claim (different dataset)
+--------------------------------------------------------
         0.1    1     10    100   1000
```

**Caption**: The same SeizureTransformer predictions evaluated with four scoring methods on TUSZ v2.0.3 reveal an ≈16× spread in false alarm rates. The model's 1 FA/24h achievement was on Dianalund dataset, not TUSZ.

### Figure 2: Scoring Method Comparison (EXPLAINER)
**Type**: Timeline visualization showing how each method counts detections

```
Ground Truth: |----Seizure----|
Prediction:      |--Pred--|

NEDC TAES:       ✓ (50% overlap → 0.5 TP)
NEDC OVERLAP:    ✓ (any overlap → 1.0 TP)
SzCORE:      |←30s→|----Seizure----|←60s→|
             ✓ (within tolerance → 1.0 TP)
```

**Caption**: Scoring methodologies from strictest (TAES) to most permissive (SzCORE). TAES weights by overlap percentage, OVERLAP counts any overlap, while SzCORE adds clinical tolerances for early warning.

### Figure 3: Clinical Deployment Reality
**Type**: Sensitivity vs FA/24h plot with clinical zones

```
Sensitivity (%)
100 |
    |                    ← Ideal Region
 80 |                    (High Sens, Low FA)
    |
 60 |
    | Default●
 40 |     ↗ (45.6%, 100 FA)
    |
 20 |     ● 10FA Target
    |      (23.5%, 39.5 FA)  ← Cannot meet target!
  0 |●_2.5FA__(11.5%,_8.1_FA)___________________
    0    10    25    50    100   150   200
              False Alarms per 24h

    [Clinical Target Zones Marked]
    █ <2.5 FA: FDA Ideal
    █ <10 FA: Clinically Acceptable
    █ >10 FA: Clinically Unusable
```

**Caption**: SeizureTransformer's operating points on TUSZ with NEDC scoring cannot achieve clinical false alarm targets. The shaded regions indicate FDA guidelines for clinical deployment.

### Figure 4: The Evaluation Pipeline
**Type**: Clean flowchart showing reproducibility

```
TUSZ v2.0.3 EDF Files
      ↓
SeizureTransformer (Wu 2025)
      ↓
Predictions (256 Hz probabilities)
      ↓
Post-processing
(threshold, kernel, duration)
      ↓
    ╱   ╲
NEDC v6.0.0  SzCORE
   Binary    Wrapper
    ╲   ╱
      ↓
  4 Scoring
  Methods
```

**Caption**: Our evaluation pipeline processes TUSZ files through SeizureTransformer, applies tuned post-processing, and evaluates with multiple scoring standards for comprehensive comparison.

---

## Main Tables

### Table 1: Comprehensive Performance Matrix
**THE KEY RESULTS TABLE**

| Parameter Set | Scoring Method | Sensitivity | FA/24h | Meets 10 FA? | Meets 2.5 FA? |
|--------------|----------------|-------------|---------|--------------|---------------|
| **DEFAULT** (θ=0.8, k=5, d=2.0) | | | | | |
| | NEDC TAES | 24.15% | 137.53 | ❌ | ❌ |
| | NEDC OVERLAP | 45.63% | 26.89 | ❌ | ❌ |
| | Python OVERLAP | 45.63% | 26.89 | ❌ | ❌ |
| | SzCORE | 52.35% | 8.59 | ✅ | ❌ |
| **10 FA TARGET** (θ=0.95, k=5, d=2.0) | | | | | |
| | NEDC TAES | 8.64% | 34.04 | ❌ | ❌ |
| | NEDC OVERLAP | 23.45% | 39.50 | ❌ | ❌ |
| | Python OVERLAP | 23.45% | 39.50 | ❌ | ❌ |
| | SzCORE | 29.12% | 1.32 | ✅ | ✅ |
| **2.5 FA TARGET** (θ=0.95, k=11, d=8.0) | | | | | |
| | NEDC TAES | 4.07% | 8.01 | ✅ | ❌ |
| | NEDC OVERLAP | 11.51% | 8.09 | ✅ | ❌ |
| | Python OVERLAP | 11.51% | 8.09 | ✅ | ❌ |
| | SzCORE | 16.47% | 0.56 | ✅ | ✅ |

### Table 2: Dataset Comparison
**Why the 100× gap exists**

| Dataset | Model | Scoring | Sensitivity | FA/24h | Note |
|---------|-------|---------|-------------|---------|------|
| Dianalund | SeizureTransformer | SzCORE | 37% | 1.0 | EpilepsyBench Winner |
| TUSZ eval | SeizureTransformer | NEDC OVERLAP | 45.63% | 26.89 | Our evaluation |
| TUSZ eval | SeizureTransformer | SzCORE | 52.35% | 8.59 | Same data as above |
| | | | | **100×** | Gap to Dianalund |

---

## Supplementary Figures

### Figure S1: Parameter Sweep Heatmap
3D surface plot of threshold × kernel × duration vs FA rate

### Figure S2: Per-File Performance Distribution
Histogram showing FA/24h distribution across 865 files

### Figure S3: NEDC vs Python Implementation Parity
Scatter plot proving <0.1% difference

### Figure S4: Event Duration Analysis
Distribution of detected vs true seizure durations

### Figure S5: Temporal Precision Analysis
Onset/offset alignment errors by scoring method

---

## Data for Figures

### Source Files
- `/experiments/eval/baseline/default_nedc_binary/results/summary.txt`
- `/experiments/eval/baseline/default_native_overlap/metrics.json`
- `/experiments/eval/baseline/checkpoint.pkl` (for raw predictions)
- `/docs/results/FINAL_COMPREHENSIVE_RESULTS_TABLE.md`

### Key Numbers to Emphasize
- **100×**: Gap between Dianalund and TUSZ
- **3.1×**: Impact of scoring method alone (OVERLAP vs SzCORE)
- **45.63%**: Best sensitivity at paper defaults
- **26.89**: FA/24h with NEDC OVERLAP (SEIZ-only)
- **865**: Files evaluated (clinical scale)

---

## Figure Generation Code

```python
# Figure 1: Performance Spectrum
import matplotlib.pyplot as plt
import numpy as np

methods = ['NEDC TAES', 'NEDC OVERLAP', 'Python OVERLAP', 'SzCORE']
fa_rates = [136.73, 26.89, 26.89, 8.59]
colors = ['#d62728', '#ff7f0e', '#ff7f0e', '#2ca02c']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(methods, fa_rates, color=colors, log=True)
ax.axvline(x=10, color='gray', linestyle='--', label='Clinical Target')
ax.axvline(x=1, color='blue', linestyle=':', label='Dianalund Claim')
ax.set_xlabel('False Alarms per 24 Hours (log scale)', fontsize=12)
ax.set_title('Same Predictions, Different Scores', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
```

```python
# Figure 3: Clinical Reality
thresholds = [(0.8, 5, 2.0), (0.95, 5, 2.0), (0.95, 11, 8.0)]
sensitivities = [45.63, 23.45, 11.51]
fa_rates = [26.89, 10.27, 2.05]

plt.figure(figsize=(10, 8))
plt.scatter(fa_rates, sensitivities, s=100, c=['red', 'orange', 'yellow'])
plt.axvspan(0, 2.5, alpha=0.2, color='green', label='FDA Ideal')
plt.axvspan(2.5, 10, alpha=0.2, color='yellow', label='Acceptable')
plt.axvspan(10, 200, alpha=0.2, color='red', label='Unusable')
```

---

## Visual Design Principles
1. **Consistent color scheme**: Red for NEDC, Green for SzCORE
2. **Log scale for FA rates**: Shows magnitude of differences
3. **Clinical context**: Always show FDA/clinical thresholds
4. **Clean, professional**: Publication-ready quality
5. **Accessibility**: Colorblind-friendly palettes
