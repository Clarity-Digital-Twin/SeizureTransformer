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
# SeizureTransformer output (per-second probabilities)
probabilities = [0.1, 0.2, 0.9, 0.95, 0.88, 0.3, 0.1, ...]

# Step 1: Apply threshold (paper uses 0.8)
binary = probabilities > 0.8  # [0, 0, 1, 1, 1, 0, 0, ...]

# Step 2: Post-process (morphological operations)
# - Opening (kernel=5): Remove small false positives
# - Closing (kernel=5): Fill small gaps
# - Remove events < 2 seconds

# Step 3: Convert to events
events = [
    {"start": 2.0, "stop": 5.0, "label": "seiz"},
    {"start": 45.0, "stop": 67.0, "label": "seiz"}
]

# Step 4: Write NEDC CSV format
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

### Option 1: Direct NEDC Integration (Complex)
```bash
# Convert SeizureTransformer output to CSV
python convert_to_nedc.py

# Run NEDC scoring
./reference_repos/nedc/bin/nedc_eeg_eval ref.list hyp.list
```

### Option 2: Extract Key Metrics (Simpler)
```python
# evaluation/nedc/simple_metrics.py
def calculate_metrics(predictions, labels):
    # Implement core TAES logic
    # Calculate sensitivity, FA/24h
    # No dependency on NEDC codebase
```

## Current Status
- **TUSZ Evaluation Running**: 49% complete (21/43 subjects)
- **Next Step**: After TUSZ completes, we'll have predictions to convert to NEDC format
- **Decision Needed**: Full NEDC integration vs. simplified metrics extraction

## Key Insight
NEDC is NOT just for SeizureTransformer - it's Temple's universal seizure detection scoring system. Any seizure detection model (CNN, RNN, Transformer) can be evaluated with NEDC if you convert outputs to their event format.

## References
- Shah et al. 2021: "Objective Evaluation Metrics for Automatic Classification of EEG Events"
- NEDC v6.0.0 documentation
- TUSZ dataset (uses NEDC scoring in competitions)