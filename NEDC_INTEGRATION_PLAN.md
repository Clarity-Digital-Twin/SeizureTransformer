# NEDC Integration Plan for SeizureTransformer

## Current Situation
- **Running**: TUSZ evaluation at 49% (ETA: ~15 minutes)
- **Output**: Will produce per-second seizure probabilities
- **Goal**: Use NEDC to get standardized metrics

## Implementation Decision Tree

### Critical Question: Do We Need Full NEDC?

**YES if:**
- Publishing paper comparing to other TUSZ systems
- Need exact TAES scores for comparison
- Want Temple/NEDC certification

**NO if:**
- Just verifying model works
- Internal evaluation only  
- Don't need exact TAES implementation

## Recommended Approach: Hybrid Solution

### Phase 1: Simple Metrics (Today)
```python
# evaluation/metrics/seizure_metrics.py
def calculate_simple_metrics(predictions, labels):
    """
    Calculate basic metrics without NEDC dependency
    """
    # Sensitivity/Specificity
    # False Alarms per 24h
    # AUROC (already in our script)
    return metrics
```

### Phase 2: NEDC Format Export (Optional)
```python
# evaluation/converters/to_nedc_format.py
def export_nedc_csv(predictions, output_dir):
    """
    Convert SeizureTransformer output to NEDC CSV
    """
    # Apply threshold and post-processing
    # Convert to events
    # Write CSV files
```

### Phase 3: Full NEDC Integration (If Needed)
```bash
# Only if publishing/comparing
./reference_repos/nedc/bin/nedc_eeg_eval \
    data/tusz_ref.list \
    output/tusz_hyp.list
```

## What We Actually Need

### For Paper Replication
- **AUROC**: ✅ Already calculating
- **Sensitivity**: ⚠️ Need to add
- **FA/24h**: ⚠️ Need to add

### For Clinical Use
- **FA/24h < 10**: Critical threshold
- **Sensitivity > 80%**: Minimum useful
- **Latency**: How fast to detect onset

## Implementation Steps

### Step 1: Finish Current Evaluation
```bash
# Wait for completion
tmux attach -t seizure_eval
```

### Step 2: Add Simple Metrics
```python
# After line 190 in run_tusz_eval.py
def calculate_event_metrics(predictions, labels, threshold=0.8):
    # Convert to events
    # Calculate overlaps
    # Return sensitivity, FA/24h
```

### Step 3: Document Results
```markdown
## Results
- AUROC: 0.XXX (Paper: 0.876)
- Sensitivity: XX% 
- FA/24h: XX
```

## File Structure Decision

### Keep It Simple
```
evaluation/
├── tusz/
│   ├── run_tusz_eval.py      # Current script
│   └── results/               # AUROC, etc.
├── nedc/
│   ├── convert_to_nedc.py    # Format converter
│   └── run_nedc_scoring.py   # Wrapper (if needed)
└── metrics/
    └── event_metrics.py       # Our implementation
```

### Don't Overthink
- NEDC is powerful but complex (1695 lines for TAES alone)
- Start with simple metrics
- Add NEDC only if required for publication

## Action Items

### Immediate (After TUSZ Completes)
1. ✅ Check if AUROC ≈ 0.876
2. ⚠️ Calculate sensitivity and FA/24h
3. ⚠️ Document performance

### Later (If Publishing)
1. Convert outputs to NEDC format
2. Run official NEDC scoring
3. Compare with other published systems

## Bottom Line

**For now**: Focus on getting basic metrics working. NEDC is overkill unless you're:
1. Publishing results
2. Comparing to competition entries
3. Need Temple/NEDC certification

**Simple is better**: Can always add NEDC later if needed. The hard part (running inference) is already happening!