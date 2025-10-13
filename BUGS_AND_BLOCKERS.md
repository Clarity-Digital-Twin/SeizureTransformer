# Bugs and Blockers - SeizureTransformer Evaluation

**Date**: 2025-10-13
**Audit Scope**: Deep repository search for bugs affecting mathematical calculations and benchmarking conclusions
**Status**: Complete deep audit performed

---

## 📋 Repository Architecture & Code Ownership

This repository contains code from multiple sources with different ownership:

### 🔒 UPSTREAM CODE (DO NOT MODIFY)

**Why**: These are external dependencies we need for reproducibility and compliance with original paper/standards.

1. **`wu_2025/`** - Original SeizureTransformer model wrapper from Wu et al. paper
   - Contains pretrained model (`model.pth`, 168MB)
   - Preprocessing, dataloader, and inference code
   - **Must preserve exactly as published for reproducibility**

2. **`evaluation/nedc_eeg_eval/v6.0.0/`** - Temple University Hospital NEDC Scoring System
   - Official NEDC v6.0.0 binaries and Python libraries
   - TAES, OVERLAP, EPOCH, IRA, DPALIGN scoring methods
   - **Must preserve exactly as distributed by Temple for standard compliance**

### ✅ OUR CODE (CAN AND SHOULD FIX)

**What we own and maintain**:

3. **`src/seizure_evaluation/`** - Our evaluation framework
   - `src/seizure_evaluation/tusz/` - TUSZ dataset evaluation runner
   - `src/seizure_evaluation/ovlp/` - Our Python implementation of Temple OVERLAP scoring (for parity testing)
   - `src/seizure_evaluation/szcore/` - SzCORE scoring via `timescoring` package
   - `src/seizure_evaluation/utils/` - EDF repair utilities, helpers
   - `src/seizure_evaluation/nedc/` - NEDC integration utilities

4. **`evaluation/nedc_eeg_eval/nedc_scoring/`** - Our NEDC integration wrappers
   - `convert_predictions.py` - Convert checkpoint to NEDC CSV_bi format
   - `run_nedc.py` - Orchestration script for NEDC pipeline
   - `post_processing.py` - Our post-processing implementation
   - `test_pipeline.py` - Synthetic data tests

---

## 🔴 CRITICAL: Upstream Bugs (Cannot Fix, But Must Be Aware)

These bugs exist in `wu_2025/` code that we cannot modify. They may affect results but we must accept them for reproducibility.

### 🔴 UPSTREAM-1: Division by Zero Risk in Z-score Normalization

**Location**: `wu_2025/src/wu_2025/utils.py:76` ⚠️ **UPSTREAM CODE**

**Code**:
```python
data = (data - np.mean(data, axis=1, keepdims=True)) / np.std(data, axis=1, keepdims=True)
```

**Issue**: No protection against division by zero if any EEG channel has flat signal (std=0).

**Impact**:
- Could produce `NaN`/`Inf` values that propagate through entire pipeline
- Would affect model inference for any file with flat channels
- Silent failures without detection

**Why We Can't Fix**: This is the original SeizureTransformer preprocessing from the paper. Modifying it would break reproducibility and we couldn't claim to be evaluating "SeizureTransformer" anymore.

**Mitigation Strategy**:
1. ✅ **Add validation in our post-processing** (see OUR-1 below)
2. ✅ **Check TUSZ dataset for flat channels** (verification script)
3. ✅ **Document this limitation** in paper/README
4. ❌ **Do NOT patch `wu_2025/` code**

**Verification Needed**:
```bash
# Check if any TUSZ files triggered this
python -c "
import pickle
ckpt = pickle.load(open('experiments/eval/baseline/checkpoint.pkl', 'rb'))
for fid, res in ckpt['results'].items():
    if res.get('predictions') is not None:
        import numpy as np
        if not np.all(np.isfinite(res['predictions'])):
            print(f'NaN/Inf detected in {fid}')
"
```

---

### 🔴 UPSTREAM-2: Edge Case in remove_short_events

**Location**: `wu_2025/src/wu_2025/utils.py:169-177` ⚠️ **UPSTREAM CODE**

**Code**:
```python
elif is_seizure and (out[i] == 0 or i == len(binary_output)-1):
    end_idx = i if out[i] == 0 else i+1
    length = end_idx - start_idx
    if length < min_samples:
        out[start_idx:end_idx] = 0
    is_seizure = False
```

**Issue**: If recording ends during an active seizure (last sample is 1), the final event may not be processed correctly because the loop exits at `i == len(binary_output)-1` before the `elif` can evaluate.

**Impact**:
- Final seizure events that are too short may not be removed
- Inconsistent behavior: end events vs middle events
- Potential false positives

**Why We Can't Fix**: Part of original SeizureTransformer post-processing.

**Mitigation Strategy**:
1. ✅ **Document this edge case**
2. ✅ **Check if any TUSZ files end during seizure with duration < 2s**
3. ✅ **Our post-processing implementations have this fixed** (in `src/`)
4. ❌ **Do NOT patch `wu_2025/` code**

---

### 🟠 UPSTREAM-3: Resampling Truncation

**Location**: `wu_2025/src/wu_2025/utils.py:78` ⚠️ **UPSTREAM CODE**

**Code**:
```python
new_n_samples = int(data.shape[1] * float(256) / fs)
```

**Issue**: Uses `int()` truncation instead of rounding.

**Impact**: Minor - for most common sampling rates (250, 256 Hz) the error is negligible (<1 sample per hour).

**Why We Can't Fix**: Upstream preprocessing.

**Mitigation**: Document this behavior. Impact is minimal on FA/24h calculations.

---

### 🟠 UPSTREAM-4: Window Count Calculation

**Location**: `wu_2025/src/wu_2025/utils.py:43` ⚠️ **UPSTREAM CODE**

**Code**:
```python
return 1 + math.ceil((self.data.shape[1] - self.window_size) / ((1-self.overlap_ratio) * self.window_size))
```

**Issue**: When data length is exact multiple of window_size, produces one extra zero-padded window.

**Impact**: Minor - slight dilution of predictions with zeros at end.

**Why We Can't Fix**: Upstream dataloader.

**Mitigation**: Accept as part of original implementation.

---

### 🟢 UPSTREAM-5: Notch Filter at 1 Hz

**Location**: `wu_2025/src/wu_2025/utils.py:33-38` ⚠️ **UPSTREAM CODE**

**Code**:
```python
notch_1_b, notch_1_a = iirnotch(1, Q=30, fs=fs)
notch_60_b, notch_60_a = iirnotch(60, Q=30, fs=fs)
```

**Issue**: Notch at 1 Hz is unusual (typically only 50/60 Hz for powerline).

**Impact**: Likely intentional design choice by paper authors.

**Why We Can't Fix**: Upstream preprocessing, probably intentional.

**Mitigation**: Document this in technical notes.

---

## ✅ OUR BUGS (Should Fix These)

These bugs are in code we own and maintain. We should fix them.

### 🔴 OUR-1: Missing NaN/Inf Validation in Our Post-Processing

**Location**:
- `src/seizure_evaluation/ovlp/post_processing.py`
- `evaluation/nedc_eeg_eval/nedc_scoring/post_processing.py`

**Issue**: No validation that predictions are finite before processing.

**Impact**: If UPSTREAM-1 triggers, NaN values would silently propagate through our scoring.

**✅ FIX REQUIRED**:
```python
def apply_seizure_transformer_postprocessing(
    predictions: np.ndarray,
    threshold: float = 0.8,
    morph_kernel_size: int = 5,
    min_duration_sec: float = 2.0,
    fs: int = 256,
) -> list[tuple[float, float]]:
    """Apply post-processing pipeline with validation."""

    # VALIDATE: Check for NaN/Inf from upstream preprocessing
    if not np.all(np.isfinite(predictions)):
        n_bad = np.sum(~np.isfinite(predictions))
        raise ValueError(
            f"Predictions contain {n_bad} non-finite values (NaN/Inf). "
            f"This likely indicates a flat EEG channel in the input data."
        )

    # Step 1: Apply threshold
    binary = predictions > threshold
    # ... rest of function
```

**Priority**: HIGH - Add this validation to both post-processing implementations.

---

### 🟡 OUR-2: Integer Truncation in Time Conversion

**Location**: `src/seizure_evaluation/tusz/cli.py:106-107` ✅ **OUR CODE**

**Code**:
```python
start_idx = int(start_sec * fs)
end_idx = min(int(end_sec * fs), duration_samples)
```

**Issue**: `int()` truncates fractional samples, causing off-by-one errors.

**Impact**: Events could be 1 sample shorter than intended. Minor sensitivity impact.

**✅ FIX REQUIRED**:
```python
start_idx = round(start_sec * fs)
end_idx = min(round(end_sec * fs), duration_samples)
```

**Priority**: MEDIUM - Fix for consistency.

---

### 🟡 OUR-3: Min Duration Truncation

**Location**:
- `evaluation/nedc_eeg_eval/nedc_scoring/post_processing.py:47` ✅ **OUR CODE**
- `src/seizure_evaluation/ovlp/post_processing.py:47` ✅ **OUR CODE**

**Code**:
```python
min_samples = int(min_duration_sec * fs)
```

**Issue**: `int(2.0 * 256)` = 512, but events could be as short as 511 samples (1.996 sec).

**Impact**: Minor inconsistency in minimum duration enforcement.

**✅ FIX REQUIRED**:
```python
import math
min_samples = math.ceil(min_duration_sec * fs)
```

**Priority**: MEDIUM - Fix for correctness.

---

### 🟡 OUR-4: Performance Issue in Background FA Calculation

**Location**: `src/seizure_evaluation/ovlp/overlap_scorer.py:136-142` ✅ **OUR CODE**

**Code**:
```python
for hb in hyp_bckg:
    if not any(
        (hb.start_time < rb.stop_time and rb.start_time < hb.stop_time) for rb in ref_bckg
    ):
        bckg_false_alarms += 1
```

**Issue**: O(n²) nested loop complexity. Slow for files with many background segments.

**Impact**: Performance only, no correctness issue.

**✅ OPTIMIZATION POSSIBLE**:
```python
# Sort intervals once
ref_bckg_sorted = sorted(ref_bckg, key=lambda e: e.start_time)

for hb in hyp_bckg:
    overlaps = False
    for rb in ref_bckg_sorted:
        # Early exit if past possible overlap region
        if rb.start_time >= hb.stop_time:
            break
        if hb.start_time < rb.stop_time and rb.start_time < hb.stop_time:
            overlaps = True
            break
    if not overlaps:
        bckg_false_alarms += 1
```

**Priority**: LOW - Only matters for files with many events.

---

### 🟡 OUR-5: Inconsistent Time Precision

**Location**: Multiple files in `src/` and `evaluation/nedc_eeg_eval/nedc_scoring/`

**Issue**: Some code uses `.4f` formatting, some uses full float precision.

**Impact**: Potential rounding differences when comparing events.

**✅ FIX REQUIRED**: Standardize on 4 decimal places everywhere:
- Internal calculations: Use full precision
- CSV_bi output: Use `.4f` (NEDC requirement)
- Event comparisons: Round to 4 decimals for comparison

**Priority**: LOW - Add comment documenting precision policy.

---

### 🟢 OUR-6: Duplicate Post-Processing Code

**Location**: ✅ **OUR CODE**
- `evaluation/nedc_eeg_eval/nedc_scoring/post_processing.py`
- `src/seizure_evaluation/ovlp/post_processing.py`

**Issue**: Two nearly identical implementations. Changes must be manually synchronized.

**Impact**: Maintenance burden, risk of divergence.

**✅ FIX REQUIRED**:
1. Keep `src/seizure_evaluation/ovlp/post_processing.py` as single source of truth
2. Make `evaluation/nedc_eeg_eval/nedc_scoring/post_processing.py` import from `src/`:

```python
# evaluation/nedc_eeg_eval/nedc_scoring/post_processing.py
"""Wrapper for backward compatibility."""
from seizure_evaluation.ovlp.post_processing import (
    apply_seizure_transformer_postprocessing,
    binary_mask_to_events,
)

__all__ = [
    'apply_seizure_transformer_postprocessing',
    'binary_mask_to_events',
]
```

**Priority**: MEDIUM - Reduces maintenance burden.

---

### 🟢 OUR-7: Missing Input Validation

**Location**: CLI entry points in `src/seizure_evaluation/` ✅ **OUR CODE**

**Issue**: No validation of input ranges (e.g., threshold ∈ [0,1], kernel > 0).

**Impact**: User error could produce confusing results.

**✅ FIX REQUIRED**: Add validation to argument parsers:

```python
parser.add_argument(
    "--threshold",
    type=float,
    default=0.8,
    help="Probability threshold (0-1)"
)
# Add after parsing:
if not 0 <= args.threshold <= 1:
    parser.error("threshold must be in range [0, 1]")
if args.kernel <= 0:
    parser.error("kernel must be positive")
if args.min_duration_sec <= 0:
    parser.error("min_duration_sec must be positive")
```

**Priority**: LOW - Nice to have.

---

## ✅ VERIFIED: Not Bugs

These patterns were investigated and confirmed correct:

- ✅ **Division operations in `src/seizure_evaluation/ovlp/overlap_scorer.py`**: All have proper zero-check guards
- ✅ **NEDC v6.0.0 divide-by-zero checks**: Temple code has comprehensive validation (upstream)
- ✅ **OVERLAP scoring logic**: Correctly implements any-overlap event counting
- ✅ **CSV_bi format generation**: Matches NEDC specification exactly (4 decimal places)
- ✅ **FA/24h calculations**: Correctly uses 86400.0 seconds per day
- ✅ **F1 score calculations**: Proper harmonic mean with zero-division protection
- ✅ **SzCORE integration**: Correctly uses `timescoring` package defaults

---

## 📊 Summary

| Category | Count | Can Fix? | Should Fix? |
|----------|-------|----------|-------------|
| **Upstream Critical** | 2 | ❌ No | N/A - Document & mitigate |
| **Upstream High** | 2 | ❌ No | N/A - Document |
| **Upstream Low** | 1 | ❌ No | N/A - Document |
| **Our High** | 1 | ✅ Yes | ✅ **YES** - Add NaN validation |
| **Our Medium** | 4 | ✅ Yes | ✅ **YES** - Fix truncation issues |
| **Our Low** | 2 | ✅ Yes | ⚠️ Optional - Improves code quality |

---

## 🔧 Action Plan

### Immediate (Before Next Evaluation Run)

1. **✅ OUR-1**: Add NaN/Inf validation in both post-processing files
2. **Verify UPSTREAM-1**: Check if any TUSZ files have flat channels
3. **Verify UPSTREAM-2**: Check if any recordings end during short seizures

### Short Term (This Sprint)

4. **✅ OUR-2**: Fix time conversion truncation → rounding
5. **✅ OUR-3**: Fix min_duration truncation → ceil
6. **✅ OUR-6**: Consolidate duplicate post-processing code

### Long Term (Technical Debt)

7. **✅ OUR-4**: Optimize background FA calculation (if performance becomes issue)
8. **✅ OUR-5**: Document time precision policy
9. **✅ OUR-7**: Add input validation to CLIs

### Documentation

10. **Document all upstream bugs** in paper limitations section
11. **Add inline comments** in `src/` explaining why we can't fix upstream issues
12. **Create verification scripts** for checking TUSZ dataset edge cases

---

## 🧪 Verification Scripts Needed

```bash
# 1. Check for flat channels
python scripts/check_flat_channels.py experiments/eval/baseline/checkpoint.pkl

# 2. Check for NaN/Inf in predictions
python scripts/check_predictions_validity.py experiments/eval/baseline/checkpoint.pkl

# 3. Check for end-of-recording seizures
python scripts/check_boundary_events.py experiments/eval/baseline/checkpoint.pkl

# 4. Verify time conversion precision
python scripts/verify_time_precision.py
```

---

## 📝 Notes

- **No "p012345" placeholder bugs found** - all code appears production-ready
- **Published results likely valid** - upstream bugs only trigger on edge cases (flat channels, boundary events)
- **Most urgent fix**: Add NaN validation (OUR-1) to catch upstream preprocessing issues
- **Best practice**: Keep upstream code frozen, fix issues in our evaluation layer

**Overall Assessment**: Repository is well-structured with clear separation between upstream dependencies and our evaluation code. The critical bugs are in upstream code we can't modify, but we can mitigate them in our evaluation layer. Our own code has minor numerical precision issues that should be fixed for correctness and robustness.
