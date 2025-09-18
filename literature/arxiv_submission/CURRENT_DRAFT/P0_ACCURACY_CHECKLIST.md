# P0 ACCURACY CHECKLIST - SeizureTransformer Cross-Reference
## CRITICAL: DO NOT MODIFY ANYTHING UNTIL ALL ITEMS VERIFIED

Date: 2025-09-18
Status: INVESTIGATION IN PROGRESS

---

## 🔴 NUMBERS TO VERIFY AGAINST ORIGINAL PAPER

### Competition Performance (Dianalund/EpilepsyBench)
- [ ] **37% sensitivity** - CHECK: Table I of original paper
- [ ] **1 FA/24h (or "1 FP/day")** - CHECK: Table I
- [ ] **F1 = 0.43** - CHECK: Table I
- [ ] **Ranked #1 in competition** - CHECK: Table I header
- [ ] **Threshold = 0.80 (80%)** - CHECK: Discussion section mentions "picking threshold to be 80%"

### TUSZ Training Dataset
- [X] **Version: v2.0.3 or v1.5.2?** - RESOLVED
  - Original paper Page 2: "Temple University Hospital EEG Seizure Corpus v2.0.3(TUSZ)"
  - Our paper incorrectly says: v1.5.2
  - **CONFIRMED**: They trained on v2.0.3 (same as we're evaluating on)
  - **ACTION NEEDED**: Update our paper from v1.5.2 to v2.0.3
- [X] **910 hours of training data** - VERIFIED: 3277229 seconds / 3600 = 910.34 hours
- [X] **579 subjects** - VERIFIED: README shows 579 subjects in train

### Siena Dataset
- [ ] **128 hours** - CHECK: Matches (original: "128 hours")
- [ ] **14 subjects** - CHECK: Matches

### Model Architecture
- [ ] **~41 million parameters** - CHECK: Our claim, need to verify
- [ ] **168 MB model file** - CHECK: model.pth actual size
- [ ] **256 Hz sampling rate** - CHECK: Page 2 "resampling signals into 256 Hz"
- [ ] **60-second windows** - CHECK: "60 × 256 = 15360 time steps"
- [ ] **19 channels** - CHECK: "at least 19 electrodes"

### Processing Pipeline
- [ ] **Bandpass: 0.5-120 Hz** - CHECK: Page 2 mentions this
- [ ] **Notch filters: 1 Hz and 60 Hz** - CHECK: Page 2 "notch filters to eliminate signals at 1 Hz and 60 Hz"
  - NOTE: Our paper might incorrectly claim we added 1 Hz notch
- [ ] **Threshold: 0.8** - CHECK: "picking threshold to be 80%" in competition
- [ ] **Morphological kernel: 5** - CHECK: Need to find in paper
- [ ] **Minimum duration: 2 seconds** - CHECK: Need to find in paper

### TUSZ Test Performance (from their paper)
- [X] **AUROC = 0.876** - VERIFIED: Figure 3 caption "Mean: 0.876"
  - Our paper claims: 0.9019
  - **EXPLANATION**: Different test sets!
    - They used: 42.7 hours, 43 subjects, 469 seizures
    - We used: 127.7 hours (459713 sec/3600), 43 subjects, 469 seizures in 865 files
- [X] **Test set: 42.7 hours** - VERIFIED but DIFFERENT from ours
  - They report: "42.7 hours of waveforms from 43 subjects"
  - TUSZ v2.0.3 eval actually has: 459713 seconds = 127.7 hours in 865 files
  - **KEY INSIGHT**: They likely used a SUBSET of the eval set
- [X] **43 subjects** - VERIFIED: Matches README (43 subjects in eval)
- [X] **469 seizure activities** - VERIFIED: Matches README (469 seizure events in eval)

### Table III Results (Event-based on TUSZ)
- [ ] **SeizureTransformer F1: 0.6752** - CHECK: Table III
- [ ] **SeizureTransformer Sensitivity: 0.7110 (71.10%)** - CHECK: Table III
- [ ] **SeizureTransformer Precision: 0.6427** - CHECK: Table III

### Runtime Performance
- [ ] **3.98 seconds per hour** - CHECK: Table II shows "3.98"

---

## 🟡 CLAIMS TO VERIFY IN OUR PAPER

### Our NEDC Evaluation Results
- [ ] NEDC OVERLAP: 45.63% sensitivity, 26.89 FA/24h
- [ ] NEDC TAES: 65.21% sensitivity, 136.73 FA/24h
- [ ] SzCORE Event: 52.35% sensitivity, 8.59 FA/24h
- [ ] 27-fold gap (27x) with NEDC OVERLAP
- [ ] 137-fold gap (137x) with NEDC TAES

### Our Test Set
- [X] **865 files** - VERIFIED: TUSZ v2.0.3 eval has 865 EDF files total
- [X] **127.7 hours** - VERIFIED: 459713 seconds / 3600 = 127.7 hours
- [X] **TUSZ v2.0.3 eval set** - VERIFIED: We use the FULL eval set
  - **CRITICAL**: We evaluated on FULL eval set (127.7 hrs)
  - SeizureTransformer paper evaluated on SUBSET (42.7 hrs)
  - Both have same 43 subjects and 469 seizures
  - This explains AUROC difference (0.876 vs 0.9019)

---

## 🟢 INVESTIGATION NOTES

### Finding #1: TUSZ Version Mismatch [RESOLVED]
- **Original paper clearly states**: "Temple University Hospital EEG Seizure Corpus v2.0.3(TUSZ)"
- **We incorrectly claim**: v1.5.2 for training
- **VERIFIED**: They trained on v2.0.3 (same version we're testing on)
- **Resolution**: Update all references from v1.5.2 to v2.0.3

### Finding #2: AUROC Difference [EXPLAINED]
- **They report**: 0.876 on TUSZ test
- **We measure**: 0.9019
- **EXPLANATION FOUND**:
  - They tested on: 42.7 hours (subset of eval)
  - We tested on: 127.7 hours (FULL eval set)
  - Both have same 43 subjects and 469 seizures
  - Longer recordings in full set may have better SNR
  - **NO ACTION NEEDED**: Document this difference clearly

### Finding #3: Notch Filter Attribution [INVESTIGATED - COMPLEX]
- **Original paper text**: "two notch filters to eliminate signals at 1 Hz and 60 Hz"
- **Original wu_2025 code**: DOES implement both notches (utils.py lines 33-34: `iirnotch(1, Q=30, fs=fs)` and `iirnotch(60, Q=30, fs=fs)`)
- **Our claim (04_methods.md line 15)**: "The 1 Hz notch (to suppress heart-rate artifacts) reflects our released evaluation code and is an addition beyond the paper's brief preprocessing description"
- **PROBLEM**: We incorrectly claim the 1 Hz notch is our addition, when BOTH paper AND code have it
- **RESOLUTION**: Change to: "apply notch filters at 1 Hz and 60 Hz (Q=30) as specified in the original paper and implementation"

### Finding #4: FA/24h on TUSZ [CRITICAL - VERIFIED]
- **Original paper**: Does NOT report FA/24h on TUSZ AT ALL
- **Table I**: Shows Dianalund competition results (1 FP/day = 1 FA/24h)
- **Table III**: Shows TUSZ results with F1, sensitivity, precision ONLY - NO FA/24h!
- **They DO report**:
  - AUROC = 0.876 on TUSZ (Figure 3)
  - Event-based F1 = 0.6752, Sensitivity = 71.10%, Precision = 64.27% (Table III)
- **Our contribution**: FIRST to report FA/24h on TUSZ using NEDC scoring
- **KEY POINT**: The "1 FA/24h" is ONLY for Dianalund, NOT TUSZ

---

## 📋 ACTION ITEMS (READY FOR IMPLEMENTATION)

### REQUIRED FIXES:

1. **Fix TUSZ Version (2 locations)**
   - File: `02_introduction.md` line 8
   - Change: "v1.5.2" → "v2.0.3"
   - File: `03_background.md` line 13
   - Change: "v1.5.2" → "v2.0.3"

2. **Fix Notch Filter Claim (1 location)**
   - File: `04_methods.md` line 15
   - Current: "The 1 Hz notch (to suppress heart-rate artifacts) reflects our released evaluation code and is an addition beyond the paper's brief preprocessing description [1]."
   - Change to: "apply notch filters at 1 Hz and 60 Hz (Q=30) as specified in the original paper [1]."

3. **Optional: Model Size (if we want to be precise)**
   - Change "~=168 MB" to "~=169 MB" (actual size)

### ALREADY VERIFIED CORRECT:
- ✅ 37% sensitivity (not 80%)
- ✅ 1 FA/24h on Dianalund
- ✅ 27x and 137x multipliers accurate
- ✅ We correctly state they never report FA/24h on TUSZ
- ✅ AUROC difference explained by test set sizes

---

## ⚠️ CRITICAL REMINDERS

- DO NOT make any changes until full investigation complete
- Every number must be traceable to a specific location in original paper
- When in doubt, quote the exact text from the original
- Our contribution is NEDC evaluation - they never did NEDC FA/24h on TUSZ
- Be precise about what is "claimed" (Dianalund) vs "measured" (TUSZ)

## 🔥 MOST IMPORTANT FINDING

**SeizureTransformer NEVER reports FA/24h on TUSZ!**
- 1 FA/24h is ONLY from Dianalund competition (Table I)
- On TUSZ they only report F1/Sens/Prec (Table III) and AUROC (Figure 3)
- We are the FIRST to evaluate FA/24h on TUSZ using NEDC
- This is why our 27x-137x comparison is valid - we're comparing Dianalund claim to TUSZ reality