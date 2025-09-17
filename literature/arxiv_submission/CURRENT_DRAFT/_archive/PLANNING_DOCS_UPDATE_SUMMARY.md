# Planning Documents Update Summary

Date: 2025-09-17
Purpose: Document all planning doc updates to remove Native OVERLAP reporting

## Decision Implemented

**Native OVERLAP will not be reported as a separate scorer in the paper.**
- Rationale: NEDC OVERLAP is the canonical source for TUSZ; Native OVERLAP adds redundancy
- Policy: Keep implementation for validation/tests but don't report in tables/figures
- Documentation: Add one-line Methods note about parity validation

## Planning Documents Updated

### 1. COMPLETE_RESULTS_COLLATED.md ✅
**Changes:**
- Added reporting policy note at top
- Removed Native OVERLAP rows from all 3 primary tables
- Added validation notes about parity
- Updated supporting evidence section

### 2. ADDITIONAL_INTEGRATIONS/RESULTS.md ✅
**Changes:**
- Added reporting policy header
- Removed Native OVERLAP from primary results table
- Removed Native OVERLAP from clinical operating points (10 FA, 2.5 FA)
- Updated scorers list to show only 3 (NEDC TAES, NEDC OVERLAP, SzCORE Event)
- Added validation note about parity

### 3. ADDITIONAL_INTEGRATIONS/RESULTS_ROOT.md ✅
**Changes:**
- Changed "Report all four scorers" → "Report three scorers"
- Removed Python OVERLAP rows from all tables
- Updated TBD values with final numbers
- Added validation note
- Fixed difference calculation (3× not 12×)

### 4. MISSING_COMPONENTS.md ✅
**Status:** No changes needed (doesn't mention Native OVERLAP)

### 5. SCORING_COMPARISON.md ✅
**Status:** No changes needed (focuses on NEDC vs SzCORE taxonomy)

## Numbers Confirmed (Unchanged)

All performance numbers remain exactly the same:

**Default (θ=0.80, k=5, d=2.0s):**
- NEDC TAES: 65.21% sens, 136.73 FA/24h
- NEDC OVERLAP: 45.63% sens, 26.89 FA/24h
- SzCORE Event: 52.35% sens, 8.59 FA/24h

**10 FA/24h Target (θ=0.88, k=5, d=3.0s):**
- NEDC TAES: 60.45% sens, 83.88 FA/24h
- NEDC OVERLAP: 33.90% sens, 10.27 FA/24h
- SzCORE Event: 40.59% sens, 3.36 FA/24h

**2.5 FA/24h Target (θ=0.95, k=5, d=5.0s):**
- NEDC TAES: 18.12% sens, 10.64 FA/24h
- NEDC OVERLAP: 14.50% sens, 2.05 FA/24h
- SzCORE Event: 19.71% sens, 0.75 FA/24h

**~1 FA/24h Comparison (θ=0.98, k=5, d=5.0s):**
- NEDC OVERLAP: 8.10% sens, 0.86 FA/24h
- vs Dianalund: 37% sens @ 1 FA/24h (4.6× drop)

## Next Steps (Split Draft Updates)

Files requiring surgical edits:
1. **01_abstract.md** - Change "four scoring methodologies" to "three"
2. **02_introduction.md** - Change "four scoring methodologies" to "three"
3. **04_methods.md** - Remove Native OVERLAP listing, add parity note
4. **05_results.md** - Remove Native OVERLAP from tables and text
5. **11_appendix.md** - Remove Native OVERLAP from Table A1, update C.3 section

## Verification Checklist

After split draft updates:
- [ ] Run `bash assemble.sh` to reassemble
- [ ] Search for "Native OVERLAP" - should only appear in Methods parity note and Appendix C.3
- [ ] Search for "four scoring" - should return 0 results
- [ ] Verify tables show only 3 scorers
- [ ] Check figure captions updated to "three scoring methodologies"

## Key Message Preserved

The core argument remains unchanged:
- **27-137× performance gap** between claimed and actual performance
- **8.6× degradation** with identical SzCORE scoring across datasets
- **15.9× spread** in FA rates from scoring methodology alone
- **4.6× sensitivity drop** to achieve 1 FA/24h on TUSZ

All critical numbers are preserved; we're simply streamlining the presentation by removing redundant Native OVERLAP reporting.
