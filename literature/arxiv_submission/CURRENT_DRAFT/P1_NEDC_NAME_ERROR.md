# P1: NEDC Name Error - CRITICAL ERROR FOUND

## STATUS: ✅ FIXED

### The Error
**We incorrectly call it**: "Neural Event Detection Competition (NEDC)"
**It actually is**: "Neural Engineering Data Consortium (NEDC)"

This is a fundamental factual error that must be corrected immediately.

## Evidence from Original Sources

### From Shah 2018 (TUSZ paper):
- `/literature/markdown/shah-2018/shah-2018.md` line 113:
  - "the Neural Engineering Data Consortium (NEDC) at Temple University"

### From TUSZ Book Chapter:
- `/literature/markdown/tusz/shah-2018-tusz-book-chapter.md` line 12:
  - "publicly available from the Neural Engineering Data Consortium"

### From Picone 2021:
- `/literature/markdown/picone-evaluation/picone-2021-objective-evaluation-metrics.md` line 6:
  - "The Neural Engineering Data Consortium, Temple University"

### From Our Own NEDC Citation File:
- `/evaluation/nedc_eeg_eval/CITATION.md` line 3:
  - "Temple University's Neural Engineering Data Consortium"

### From NEDC Website (www.nedcdata.org):
- Homepage header: "The Neural Engineering Data Consortium"
- About section: "Neural Engineering Data Consortium"
- NO mention of "competition" anywhere - it's a consortium/organization

## Locations Needing Correction

### 1. In 00_front_matter.md:
```markdown
Line 2: title: "Scoring Matters: A Reproducible NEDC Evaluation of SeizureTransformer on TUSZ"
```
This is OK - just using the acronym, no need to expand

### 2. In 01_abstract.md:
```markdown
Line 3: "using the Neural Engineering Data Consortium (NEDC) v6.0.0 scoring tools"
```
This is CORRECT! No change needed.

### 3. In 02_introduction.md: ✅ FIXED
```markdown
Line 10: "Moreover, Temple University developed the NEDC (Neural Event Detection Competition) scoring software"
```
Should be:
```markdown
"Moreover, Temple University's Neural Engineering Data Consortium (NEDC) developed the scoring software"
```

### 4. In 03_background.md: ✅ FIXED
```markdown
Line 5: "Alongside TUSZ, Temple University developed the Neural Event Detection Competition (NEDC) scoring software suite"
```
Should be:
```markdown
"Alongside TUSZ, Temple University's Neural Engineering Data Consortium (NEDC) developed the scoring software suite"
```

### 5. In 09_acknowledgments.md:
```markdown
Line 3: "We thank Joseph Picone and the Neural Engineering Data Consortium at Temple University"
```
This is CORRECT! No change needed.

### 6. In CURRENT_WORKING_DRAFT_ASSEMBLED.md:
- Contains the same errors from 02_introduction.md and 03_background.md
- Will be auto-fixed when we rebuild after fixing source files

## Why This Happened
Likely confusion because:
1. NEDC develops evaluation/scoring tools
2. These tools are used in competitions/challenges
3. But NEDC itself is NOT a competition - it's a consortium/organization

## Impact Assessment
- **Severity**: HIGH - This is a factual error about a major organization
- **Credibility Impact**: HIGH - Shows we don't know what NEDC stands for
- **Fix Complexity**: LOW - Simple text replacement

## Recommended Fix
Change all instances to properly reflect that NEDC is the Neural Engineering Data Consortium, which is an organization at Temple University that develops tools and datasets, NOT a competition.

## Next Steps
1. Fix in 02_introduction.md
2. Fix in 03_background.md
3. Rebuild PDF with corrected organization name
4. Verify no other instances exist