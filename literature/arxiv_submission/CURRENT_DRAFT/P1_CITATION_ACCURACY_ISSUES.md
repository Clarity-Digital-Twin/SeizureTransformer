# P1: Citation Accuracy Issues Found - ALL FIXES COMPLETED

## FIX STATUS: ✅ ALL COMPLETED

### Summary of Changes Made:
1. ✅ Added Roy et al. 2021 as reference [13]
2. ✅ Changed all [6] → [13] for 75% sensitivity and 1 FA/24h claims (5 files)
3. ✅ Fixed TUSZ annotator claim: now correctly states "highly trained undergraduates validated against board-certified neurologists"
4. ✅ Fixed SzCORE 3-10x: removed unsupported quantitative claim, now references our own results
5. ✅ Fixed SeizureTransformer parameters: clarified as our measurements, not from paper

## Critical Issues Requiring Immediate Correction

### 1. ❌ Beniczky 2018 [ref 6] - WRONG CITATION BUT CLAIMS ARE VALID
**Issue**: Beniczky paper does NOT contain either cited claim, but the claims themselves are valid from other sources

#### 75% Sensitivity Claim - VALID BUT WRONG CITATION
- **Our claim**: "75% sensitivity goal for clinical systems [6]"
- **Beniczky reality**: Paper never mentions 75% as a clinical goal
- **ACTUAL SOURCE FOUND**:
  - Roy et al. 2021 (EBioMedicine): "This sensitivity goal for an automated system is 75% [24,36]"
  - Picone et al. 2021: "Feedback from clinicians has been consistent that FA rate is perhaps the single most important measure once sensitivity is above approximately 75%"
- **FIX NEEDED**: Replace [6] with proper citation to Roy et al. 2021 or add new reference

#### 1 FA/24h Human Performance - VALID BUT WRONG CITATION
- **Our claim**: "human reviewers achieve approximately 1 false alarm per 24 hours [6]"
- **Beniczky reality**: Paper never discusses human reviewer performance
- **ACTUAL SOURCE FOUND**:
  - Roy et al. 2021: "If false positive rates can be reduced to human levels of 1FA/24 h [36]"
  - References Golmohammadi et al. 2020 (Springer book chapter)
- **FIX NEEDED**: Replace [6] with proper citation to Roy et al. 2021 or Golmohammadi 2020

**Locations**:
- 01_abstract.md: "falling far short of the 75% sensitivity goal for clinical systems [6]"
- 02_introduction.md: "falling far short of the 75% sensitivity goal for clinical systems [6]"
- 03_background.md: "Clinical goals typically target 75% sensitivity or higher [6], while human reviewers achieve approximately 1 false alarm per 24 hours [6]"
- 06_discussion.md: "falling far short of the 75% sensitivity goal for clinical systems [6]" and "human reviewers achieve approximately 1 FA/24h [6]"
- 07_conclusion.md: "falling far short of the 75% sensitivity goal for clinical systems [6]"

### 2. ❌ TUSZ Annotator Claim [ref 2] - FACTUALLY INCORRECT
**Issue**: Annotations were NOT by neurologists
- **Our claim**: "annotations performed by board-certified neurologists at Temple University Hospital"
- **Reality**: Shah 2018 clearly states annotations were by "highly trained undergraduates" whose work was validated against neurologists

**Location**:
- 03_background.md: "The annotations, performed by board-certified neurologists at Temple University Hospital"

### 3. ⚠️ SzCORE "3-10x" Claim [ref 4] - NOT IN ORIGINAL
**Issue**: Quantitative claim not found in SzCORE paper
- **Our claim**: "can reduce reported false alarm rates by factors of 3-10x compared to stricter scoring methods [4]"
- **Reality**: SzCORE paper doesn't provide this specific quantitative range

**Location**:
- 03_background.md: "can reduce reported false alarm rates by factors of 3-10x compared to stricter scoring methods [4]"

## Minor Issues - Attribution Unclear

### 4. ⚠️ SeizureTransformer Model Details [ref 10] - NOT IN PAPER
**Issue**: Technical details we measured, not from paper
- **Our claims**: "41 million parameters" and "168 MB model weights"
- **Reality**: Not mentioned in original SeizureTransformer paper
- **Recommendation**: Present as our measurements, not paper claims

**Locations**:
- 03_background.md: "With roughly 41 million parameters and publicly available pretrained weights (~=168 MB) [10]"

## Verified Accurate Citations

### ✅ SeizureTransformer [10]
- 37% sensitivity at 1 FA/24h on Dianalund ✓
- Trained on TUSZ v2.0.3 + Siena ✓
- 19 channels, 256 Hz, 60-second windows ✓
- Won EpilepsyBench Challenge ✓

### ✅ TUSZ [2]
- Patient-disjoint splits ✓
- Largest publicly available dataset ✓
- (Note: 865 files/43 patients is for v2.0.3, paper describes v1.2.0)

### ✅ SzCORE [4]
- 30-second pre-ictal, 60-second post-ictal windows ✓
- Merges events <90 seconds apart ✓

## Recommended Actions - PRIORITIZED

### Option A: Minimal Changes (Keep claims, fix citations)
1. **ADD NEW REFERENCE**: Roy et al. 2021 (EBioMedicine) to references list
2. **REPLACE [6] → [NEW]** for both 75% and 1 FA/24h claims
3. **KEEP Beniczky [6]** but only cite it for validation methodology discussion

### Option B: Conservative Approach (Remove specific numbers)
1. **REMOVE** specific "75%" and "1 FA/24h" numbers
2. **REPLACE** with general statements about clinical requirements
3. **CITE Beniczky [6]** only for general validation standards

### Other Fixes Still Required:
1. **URGENT**: Correct TUSZ annotator claim to "trained undergraduates validated against neurologists"
2. **MODERATE**: Remove or clarify SzCORE "3-10x" as our observation from results
3. **MINOR**: Clarify SeizureTransformer parameters (41M, 168MB) as our measurements

## Source Documentation

### Roy et al. 2021 Full Citation
Roy S, et al. Evaluation of artificial intelligence systems for assisted annotation of epileptic seizure EEG signals using expert human reviewers. EBioMedicine. 2021;70:103512.

### Supporting Evidence Locations
- 75% claim: `/literature/markdown/roy-et-al-2021/Evaluation of artificial intelligence systems.md` line 831
- 1 FA/24h claim: Same file, line 836
- Picone support: `/literature/markdown/picone-evaluation/picone-2021-objective-evaluation-metrics.md` line 431

## Next Steps
1. Decide between Option A or B
2. Run fixes in individual 0x markdown files with surgical precision
3. Regenerate PDF after all fixes complete