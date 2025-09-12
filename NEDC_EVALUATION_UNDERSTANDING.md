# NEDC Evaluation Tool Understanding

## What is NEDC?
NEDC (Neural Engineering Data Consortium) is Temple University's standardized evaluation system for EEG event detection, particularly seizure detection. Version 6.0.0 is their latest release.

## What Does NEDC Evaluate?
NEDC evaluates **how well a seizure detection model performs** by comparing:
- **Reference (Ground Truth)**: Human expert annotations of when seizures occur
- **Hypothesis (Model Output)**: Your model's predictions of when seizures occur

## How NEDC Works

### 1. Input Format
NEDC expects two sets of CSV files:

**Reference File (Ground Truth):**
```csv
channel,start_time,stop_time,label,confidence
TERM,42.2786,81.7760,seiz,1.0000
TERM,133.8040,162.1105,seiz,1.0000
```

**Hypothesis File (Model Predictions):**
```csv
channel,start_time,stop_time,label,confidence
TERM,49.0000,674.0000,seiz,1.0000
TERM,767.0000,925.0000,seiz,1.0000
```

### 2. Evaluation Metrics

NEDC provides multiple scoring methods:

1. **TAES (Time-Aligned Event Scoring)**
   - Temple/NEDC's primary metric
   - Evaluates temporal overlap between predicted and actual seizures
   - Provides sensitivity, specificity, false alarm rate

2. **OVLP (Overlap-based scoring)**
   - Measures how much predicted events overlap with true events

3. **EPOCH (Epoch-based scoring)**
   - Divides recordings into fixed time windows
   - Scores each epoch as correct/incorrect

4. **IRA (Inter-rater agreement)**
   - Measures agreement between systems

### 3. Key Metrics Produced
- **Sensitivity**: % of true seizures detected
- **False Alarms/24h**: Number of false detections per day
- **Specificity**: % of non-seizure correctly identified
- **AUROC**: Area under ROC curve

## How SeizureTransformer Relates to NEDC

### Current SeizureTransformer Output
SeizureTransformer produces:
- **Per-second probabilities**: [0.1, 0.2, 0.9, 0.8, ...] 
- Values between 0-1 for each second of EEG

### What NEDC Needs
NEDC needs:
- **Event segments**: [(start_time, stop_time, "seiz"), ...]
- Discrete events with start/stop times

### The Conversion Process

```python
# SeizureTransformer output (per-sample probabilities @256 Hz)
probabilities = [0.1, 0.2, 0.9, 0.95, 0.88, 0.3, 0.1, ...]

# Step 1: Downsample/aggregate to per-second (if needed) or operate per-sample
# Step 2: Apply threshold (paper uses 0.8)
binary = probabilities > 0.8  # [0, 0, 1, 1, 1, 0, 0, ...]

# Step 3: Post-process (morphological operations)
# - Opening (kernel=5): Remove small false positives
# - Closing (kernel=5): Fill small gaps
# - Remove events < 2 seconds

# Step 4: Convert to events (seconds)
events = [
    {"start": 2.0, "stop": 5.0, "label": "seiz"},
    {"start": 45.0, "stop": 67.0, "label": "seiz"}
]

# Step 5: Write NEDC CSV format
```

## Why Use NEDC for SeizureTransformer?

### Advantages
1. **Standardized**: Industry-standard metrics from Temple/NEDC
2. **Comprehensive**: Multiple scoring methods (TAES, OVLP, EPOCH)
3. **Clinical Relevance**: FA/24h is critical for real-world deployment
4. **Comparison**: Can compare with other published systems

### What NEDC Tells Us About SeizureTransformer
- **Does the model find seizures?** (Sensitivity)
- **How many false alarms?** (FA/24h)
- **Clinical usability?** (Too many false alarms = unusable)
- **Better than baseline?** (Compare TAES scores)

## Implementation Strategy for Our Fork

### Option 1: Direct NEDC Integration (Canonical)
```bash
# Convert SeizureTransformer output to NEDC CSV
python evaluation/nedc_scoring/convert_predictions.py \
  --checkpoint evaluation/tusz/checkpoint.pkl \
  --outdir evaluation/nedc_scoring/output

# Environment for NEDC tools (in-repo)
export NEDC_NFC=$(pwd)/evaluation/nedc_eeg_eval/v6.0.0
export PATH=$NEDC_NFC/bin:$PATH
export PYTHONPATH=$NEDC_NFC/lib:$PYTHONPATH

# Run NEDC scoring (lists contain absolute paths)
$NEDC_NFC/bin/nedc_eeg_eval \
  evaluation/nedc_scoring/output/lists/ref.list \
  evaluation/nedc_scoring/output/lists/hyp.list \
  -o evaluation/nedc_scoring/output/results
```

### Option 2: Extract Key Metrics (Simpler)
```python
# evaluation/nedc/simple_metrics.py
def calculate_metrics(predictions, labels):
    # Implement simplified event metrics if NEDC is not required
    # Calculate sensitivity, FA/24h, AUROC
```

## Current Status
- TUSZ evaluation produces per-sample probabilities and event labels
- Predictions are stored in `evaluation/tusz/checkpoint.pkl`
- Full NEDC integration is the chosen path (see NEDC_INTEGRATION_PLAN.md)

## Key Insight
NEDC is NOT just for SeizureTransformer - it's Temple's universal seizure detection scoring system. Any seizure detection model (CNN, RNN, Transformer) can be evaluated with NEDC if you convert outputs to their event format.

## References
- Shah et al. 2021: "Objective Evaluation Metrics for Automatic Classification of EEG Events"
- NEDC v6.0.0 documentation
- TUSZ dataset (uses NEDC scoring in competitions)
