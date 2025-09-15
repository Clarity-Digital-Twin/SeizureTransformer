# 🚨 CRITICAL BUG: NEDC Binary Wrapper Failure

**Status**: ACTIVE - Blocking all parameter tuning
**Severity**: CRITICAL
**Impact**: Cannot get Temple NEDC TAES or OVERLAP metrics
**Date**: September 14, 2025

## Problem Summary

The NEDC binary wrapper in `evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py` is FAILING SILENTLY:
- ✅ Conversion step works (creates CSV_bi files)
- ✅ List files created properly
- ❌ NEDC binary execution fails
- ❌ No summary.txt produced
- ❌ No error messages captured

## Evidence

### 1. Comprehensive Sweep Failure
```
42 parameter combinations tested:
- ALL returned "ERROR:" with empty stderr
- ALL have null TAES metrics
- ALL have null OVERLAP metrics
```

### 2. Test Output
```bash
# Single test run shows:
======================================================================
STEP 1: Converting SeizureTransformer predictions to NEDC format
======================================================================
✅ Converted 864 files to NEDC format
✅ List files created:
  experiments/eval/baseline/test_single/lists/hyp.list
  experiments/eval/baseline/test_single/lists/ref.list

======================================================================
STEP 2: Running NEDC scorer (backend: nedc-binary)
======================================================================
Traceback (most recent call last):
  File "run_nedc.py", line 576, in <module>
  File "run_nedc.py", line 464, in run_full_pipeline
  [CUTS OFF - ERROR NOT CAPTURED]
```

## ROOT CAUSE FOUND! ✅

### The Problem - Line 161 in run_nedc.py

**CURRENT CODE (BROKEN)**:
```python
# Line 161 - WRONG! Trying to execute Python script as binary
cmd = [str(nedc_binary), str(ref_list), str(hyp_list), "-o", str(results_dir)]
```

**PROOF - The "binary" is actually a Python script**:
```bash
$ head -1 /evaluation/nedc_eeg_eval/v6.0.0/bin/nedc_eeg_eval
#!/usr/bin/env python
```

### Complete Audit Trail

1. **Line 155**: Path construction is CORRECT
```python
nedc_binary = Path(env["NEDC_NFC"]) / "bin" / "nedc_eeg_eval"
```

2. **Line 157-159**: File existence check is CORRECT
```python
if not nedc_binary.exists():
    print(f"Error: NEDC binary not found at {nedc_binary}")
    return 1
```

3. **Line 161**: Command construction is WRONG!
```python
# WRONG - treating Python script as executable binary
cmd = [str(nedc_binary), str(ref_list), str(hyp_list), "-o", str(results_dir)]
```

4. **Line 167**: Execution with env is CORRECT
```python
result = subprocess.run(cmd, env=env, capture_output=True, text=True)
```

## Symptoms

1. **Silent Failure**: No stderr captured
2. **Partial Execution**: Conversion works, scoring doesn't
3. **Missing Output**: No summary.txt created
4. **Consistent Failure**: Happens for ALL parameter combinations

## CONFIRMED ROOT CAUSES (TWO ISSUES!)

### Issue 1: NEDC "binary" is a Python script
- File: `/evaluation/nedc_eeg_eval/v6.0.0/bin/nedc_eeg_eval`
- Shebang: `#!/usr/bin/env python`
- Execution: Needs `python3` prefix in command

### Issue 2: PYTHONPATH not properly configured
```bash
# Error when running:
ModuleNotFoundError: No module named 'nedc_cmdl_parser'
```

**The module is in**: `$NEDC_NFC/lib/python/`
**But PYTHONPATH expects**: `$NEDC_NFC/lib/python` (not just `$NEDC_NFC/lib`)

## THE COMPLETE FIX

### Fix 1: Line 161 - Add Python interpreter
**CHANGE FROM**:
```python
cmd = [str(nedc_binary), str(ref_list), str(hyp_list), "-o", str(results_dir)]
```

**CHANGE TO**:
```python
cmd = ["python3", str(nedc_binary), str(ref_list), str(hyp_list), "-o", str(results_dir)]
```

### Fix 2: setup_nedc_environment() - Fix PYTHONPATH
**CHANGE FROM**:
```python
env["PYTHONPATH"] = f"{nedc_root}/lib:{env.get('PYTHONPATH', '')}"
```

**CHANGE TO**:
```python
env["PYTHONPATH"] = f"{nedc_root}/lib/python:{env.get('PYTHONPATH', '')}"
```

## Complete Fix Implementation

```python
# evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py
# Line 161 - Add python3 interpreter

if backend == "nedc-binary":
    # Set up NEDC environment
    env = setup_nedc_environment()

    # Build NEDC command
    nedc_binary = Path(env["NEDC_NFC"]) / "bin" / "nedc_eeg_eval"

    if not nedc_binary.exists():
        print(f"Error: NEDC binary not found at {nedc_binary}")
        return 1

    # FIX: Add python3 interpreter since nedc_eeg_eval is a Python script
    cmd = ["python3", str(nedc_binary), str(ref_list), str(hyp_list), "-o", str(results_dir)]
    #      ^^^^^^^^^ THIS IS THE FIX!

    print(f"Running: {' '.join(cmd)}")
    print(f"Results will be saved to: {results_dir}")
```

## Files to Check

- `/evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py` (lines 200-250, 450-470)
- `/evaluation/nedc_eeg_eval/v6.0.0/bin/nedc_eeg_eval`
- Environment setup in wrapper

## Impact

**CANNOT**:
- Get Temple NEDC TAES metrics
- Get Temple NEDC OVERLAP metrics
- Find optimal operating points
- Complete parameter tuning

**CAN**:
- Run native Python OVERLAP scorer
- Do conversion to CSV_bi format
- Run SzCORE (when implemented)

## Validation Test

**Test the fix**:
```bash
cd /mnt/c/Users/JJ/Desktop/Clarity-Digital-Twin/SeizureTransformer
python3 evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py \
  --checkpoint experiments/eval/baseline/checkpoint.pkl \
  --outdir experiments/eval/baseline/test_fix \
  --backend nedc-binary \
  --threshold 0.8 --kernel 5 --min_duration_sec 2.0
```

**Expected**: Should produce `test_fix/results/summary.txt` with TAES metrics

## Senior Spec Review Checklist

✅ **Root causes identified**:
   1. NEDC "binary" is Python script (needs python3)
   2. Path calculation was wrong (fixed)
   3. PYTHONPATH correct (lib/ not lib/python/)
✅ **Fix locations**:
   - Line 162: Add "python3" to command
   - Line 26-31: Fix path calculation
   - Line 41: PYTHONPATH stays as lib/
✅ **Testing**: Ready to test with conversion+scoring
✅ **Impact**: Will unblock all Temple NEDC scoring

## All Fixes Applied ✅

1. **Line 162**: Added `"python3"` to command
2. **Line 26-31**: Fixed path calculation (nedc_eeg_eval_dir)
3. **Line 41**: PYTHONPATH correctly points to lib/

## Final Test Command

```bash
# This will run conversion + scoring (takes ~5 min)
python3 evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py \
  --checkpoint experiments/eval/baseline/checkpoint.pkl \
  --outdir experiments/eval/baseline/test_nedc_fixed \
  --backend nedc-binary \
  --threshold 0.8 --kernel 5 --min_duration_sec 2.0
```

## Next Steps After Fix Verified

1. Re-run comprehensive_sweep.py
2. Collect all TAES/OVERLAP metrics
3. Update TUNING_RESULTS_TRACKER.md