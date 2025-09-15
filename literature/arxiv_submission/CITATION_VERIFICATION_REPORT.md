# Citation Verification Report

## Critical Citations Verified

### ✅ Reference [10] - Beniczky & Ryvlin (2018) - PARTIALLY CORRECT
**Citation in Paper:** "Beniczky S, Ryvlin P. Standards for testing and clinical validation of seizure detection algorithms. Epilepsia. 2018;59(S1):9-13."

**ACTUAL Paper Found:**
- Title: "Standards for testing and clinical validation of seizure detection devices" (NOT "algorithms")
- Journal: Epilepsia 2018 (CORRECT)
- DOI: 10.1111/epi.14049
- Pages: Cannot confirm S1:9-13 from PDF

**CRITICAL ISSUE:**
- ⚠️ **This paper does NOT explicitly state "10 FA/24h with ≥50% sensitivity" as a clinical threshold**
- The paper mentions "false alarms per 24 hours" as a metric to report (line 461-462)
- It defines 5 phases of validation but does NOT specify numeric thresholds
- We may need a different citation for the "10 FA/24h, 50% sensitivity" claim

### ✅ Reference [11] - Haibe-Kains et al. (2020) - CORRECT
**Citation in Paper:** "Haibe-Kains B, Adam GA, Hosny A, et al. Transparency and reproducibility in artificial intelligence. Nature. 2020;586(7829):E14-E16."

**Verification:**
- Title: CORRECT ✅
- Journal: Nature 2020;586(7829):E14-E16 ✅
- DOI: 10.1038/s41586-020-2766-y ✅
- Authors: 30+ authors including all named ✅
- Content: About AI reproducibility crisis - supports our argument ✅

### ✅ Reference [12] - Kelly et al. (2019) - CORRECT
**Citation in Paper:** "Kelly CJ, Karthikesalingam A, Suleyman M, Corrado G, King D. Key challenges for delivering clinical impact with artificial intelligence. BMC Med. 2019;17(1):195."

**Verification:**
- Title: CORRECT ✅
- Journal: BMC Medicine (2019) 17:195 ✅
- DOI: https://doi.org/10.1186/s12916-019-1426-2 ✅
- Authors: All 5 authors correct and in order ✅
- Content: Discusses deployment challenges, dataset shift, generalization - supports our discussion ✅

## URGENT ACTION NEEDED

### Problem: Clinical Threshold Citation
We claim throughout the paper that "≤10 FA/24h with ≥50% sensitivity" is THE clinical standard, citing Beniczky 2018. However, Beniczky 2018 does NOT specify these exact numbers.

### Options to Fix:
1. **Find the actual source** for "10 FA/24h, 50% sensitivity" threshold
2. **Remove specific numbers** and say "clinically acceptable false alarm rates"
3. **Check if it's from FDA guidance** or another regulatory document
4. **Look in other papers** we already have that might cite this threshold

### What Beniczky 2018 DOES Say:
- Phase 3 validation needs ≥20 patients, ≥30 seizures
- Phase 4 needs ≥50 patients, ≥75 seizures
- Must report sensitivity with 95% CI
- Must report false alarms per 24 hours
- Does NOT specify what values are "acceptable"

## References Already Verified (from earlier work)
✅ [1] SeizureTransformer - Wu et al. 2025 - Verified from source
✅ [2] NEDC Scoring - Shah/Picone 2021 - Verified from source
✅ [3] TUSZ Dataset - Shah et al. 2018 - Verified from source
✅ [4] SzCORE - Dan et al. 2024 - Verified from source
✅ [5] EpilepsyBench 2025 - Website exists
✅ [6] NEDC Software v6.0.0 - Verified from AAREADME.txt

## Next Steps
1. **URGENT**: Find correct citation for "10 FA/24h, 50% sensitivity" threshold
2. Consider downloading papers [7-9] for verification
3. Check if the clinical threshold comes from:
   - FDA guidance documents
   - Other seizure detection papers
   - Clinical consensus statements
   - Industry standards

## Papers Still to Verify
- [7] Obeid & Picone 2016 - Temple EEG Corpus
- [8] Goldberger 2000 - PhysioNet
- [9] Shoeb 2009 - CHB-MIT thesis
- [13] Shoeibi 2021 - Review paper
- [14] Gemein 2020 - NeuroImage
- [15] Roy 2019 - J Neural Eng review