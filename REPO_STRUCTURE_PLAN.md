# Repository Structure & Git Flow Diagram

## Current Git Relationships:
```
┌─────────────────────────────────────────────────────────────────────┐
│                     ORIGINAL PUBLIC REPO                            │
│           github.com/keruiwu/SeizureTransformer                     │
│                         (PUBLIC)                                    │
└─────────────────────────────────────────────────────────────────────┘
                                ↑
                                │ (No connection currently)
                                │
┌─────────────────────────────────────────────────────────────────────┐
│                    YOUR PRIVATE REPO (Current)                      │
│      github.com/Clarity-Digital-Twin/SeizureTransformer             │
│                         (PRIVATE)                                   │
│                                                                     │
│  ├── wu_2025/                 ✅ Matches upstream                  │
│  ├── data/                    ❌ Wrong location!                   │
│  │   ├── datasets/                                                  │
│  │   │   ├── tusz/            (Should be in wu_2025/)              │
│  │   │   └── siena/           (Should be in wu_2025/)              │
│  │   └── models/                                                    │
│  │       └── pretrained/      (Should be in wu_2025/src/wu_2025/)  │
│  ├── literature/              🔶 Extra (keep, but gitignore)        │
│  ├── IDEAL_REFERENCE_*.md     🔶 Extra (keep, but gitignore)        │
│  └── .gitignore               ✅ Good                              │
└─────────────────────────────────────────────────────────────────────┘

## PROPOSED STRUCTURE (Matching Upstream Expectations):
```
┌─────────────────────────────────────────────────────────────────────┐
│                     ORIGINAL PUBLIC REPO                             │
│           github.com/keruiwu/SeizureTransformer                      │
└─────────────────────────────────────────────────────────────────────┘
                                ↑
                                │ PR (only code changes)
                                │
┌─────────────────────────────────────────────────────────────────────┐
│                    PUBLIC FORK (for PRs)                             │
│    github.com/Clarity-Digital-Twin/SeizureTransformer-Fork          │
│                         (PUBLIC)                                     │
│                                                                      │
│  ✅ ONLY CONTAINS:                                                  │
│  - Code improvements (siena_utils.py, bug fixes)                    │
│  - Original README.md updates                                       │
│                                                                      │
│  ❌ NEVER CONTAINS:                                                 │
│  - Data (no wu_2025/data/*)                                        │
│  - Weights (no model.pth)                                          │
│  - Private docs (no IDEAL_*.md, no literature/)                    │
└─────────────────────────────────────────────────────────────────────┘
                                ↑
                                │ cherry-pick commits
                                │
┌─────────────────────────────────────────────────────────────────────┐
│                YOUR PRIVATE WORKING REPO                             │
│      github.com/Clarity-Digital-Twin/SeizureTransformer             │
│                         (PRIVATE)                                    │
│                                                                      │
│  CORRECT STRUCTURE:                                                 │
│  ├── wu_2025/                                                       │
│  │   ├── src/                                                       │
│  │   │   └── wu_2025/                                              │
│  │   │       ├── model.pth            ← Model weights HERE         │
│  │   │       ├── architecture.py                                    │
│  │   │       ├── utils.py                                          │
│  │   │       ├── siena_utils.py       ← NEW: Siena loader          │
│  │   │       └── main.py                                           │
│  │   ├── data/                        ← Data goes HERE             │
│  │   │   ├── tusz/                                                 │
│  │   │   │   └── [TUSZ files]                                      │
│  │   │   └── siena/                                                │
│  │   │       └── [Siena files]                                     │
│  │   └── pyproject.toml                                            │
│  │                                                                  │
│  ├── literature/              (KEEP - private documentation)        │
│  ├── IDEAL_*.md              (KEEP - private documentation)        │
│  ├── .gitignore              (Updated to ignore data & weights)     │
│  └── README.md               (Original)                            │
└─────────────────────────────────────────────────────────────────────┘

## File Movement Commands:
```bash
# Move data to correct location
mv data/datasets/tusz wu_2025/data/
mv data/datasets/siena wu_2025/data/
mv data/models/pretrained/seizure_transformer_wu2025.pth wu_2025/src/wu_2025/model.pth

# Remove old data directory
rm -rf data/

# Update .gitignore
echo "wu_2025/data/" >> .gitignore
echo "wu_2025/src/wu_2025/model.pth" >> .gitignore
```

## What Gets Shared vs Private:

PUBLIC (Can PR):
- ✅ siena_utils.py (new loader code)
- ✅ Bug fixes to existing code
- ✅ Documentation improvements
- ✅ Training scripts

PRIVATE (Never commit):
- ❌ wu_2025/data/* (13GB Siena + TUSZ data)
- ❌ wu_2025/src/wu_2025/model.pth (weights)
- ❌ literature/* (paper PDFs/images)
- ❌ IDEAL_*.md (internal documentation)
