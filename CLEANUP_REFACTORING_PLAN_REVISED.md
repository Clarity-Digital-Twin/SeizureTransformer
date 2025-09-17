# Phase 3 Cleanup Refactoring Plan (REVISED)

## Executive Summary
Complete the src/ migration by removing shims, eliminating path hacks, and finalizing clean separation between vendored tools and first-party code.

**Scope**: Limited to our code. Do NOT edit vendored trees (`wu_2025/`, `evaluation/nedc_eeg_eval/`).

## Critical Issues Found

### 1. **nedc-run Entry Point is BROKEN** ❌
- Entry point targets `evaluation.nedc_eeg_eval.nedc_scoring.run_nedc:main`
- This fails because `evaluation` is not a package in the installed wheel
- **Solution**: Create wrapper at `src/seizure_evaluation/nedc/cli.py`

### 2. **sys.path Hacks Still Exist in src/** ⚠️
- `src/seizure_evaluation/szcore/cli.py` still has `sys.path.insert()`
- `src/seizure_evaluation/szcore/convert_to_hedscore.py` likely has similar issue
- These import from `evaluation.nedc_eeg_eval.nedc_scoring.post_processing`
- **Solution**: Move post_processing module to src/ or accept vendored imports with proper handling

### 3. **Makefile Docker Commands Outdated** ⚠️
- Still references `eval --help` and `nedc --help`
- Should use `tusz-eval --help` and `nedc-run --help`

## Updated Task List

### Phase 3.1: Fix Critical Breakages (IMMEDIATE)

1. **Fix nedc-run entry point**
   ```python
   # Create: src/seizure_evaluation/nedc/cli.py
   """Wrapper for NEDC scoring tools."""
   import sys
   from pathlib import Path

   # Add evaluation dir to path for vendored code
   repo_root = Path(__file__).resolve().parents[4]
   sys.path.insert(0, str(repo_root))

   from evaluation.nedc_eeg_eval.nedc_scoring.run_nedc import main

   if __name__ == "__main__":
       sys.exit(main())
   ```

   Update `pyproject.toml`:
   ```toml
   nedc-run = "seizure_evaluation.nedc.cli:main"
   ```

2. **Handle vendored imports properly**
   - Option A: Move `post_processing.py` to `src/seizure_evaluation/ovlp/`
   - Option B: Keep vendored imports but document clearly
   - **Recommended**: Option A for clean separation

3. **Update Makefile Docker targets**
   ```makefile
   # Change from:
   docker run --rm seizure-transformer:latest eval --help
   docker run --rm seizure-transformer:latest nedc --help

   # To:
   docker run --rm seizure-transformer:latest tusz-eval --help
   docker run --rm seizure-transformer:latest nedc-run --help
   ```

### Phase 3.2: Remove Shims (After 3.1)

All shims to remove:
- `evaluation/tusz/run_tusz_eval.py` → Use `tusz-eval`
- `evaluation/utils/edf_repair.py` → Import from `seizure_evaluation.utils.edf_repair`
- `evaluation/utils/enhance_evaluation_robustness.py` → Import from `seizure_evaluation.utils.enhance_evaluation_robustness`
- `evaluation/szcore_scoring/run_szcore.py` → Use `szcore-run`
- `evaluation/szcore_scoring/convert_to_hedscore.py` → Import from `seizure_evaluation.szcore.convert_to_hedscore`

### Phase 3.3: Clean sys.path Hacks

Files needing cleanup:
- `src/seizure_evaluation/szcore/cli.py` (lines 35-37)
- `src/seizure_evaluation/szcore/convert_to_hedscore.py` (check for similar)

### Phase 3.4: Documentation Updates

- Update README.md with new CLI commands
- Update any notebooks in `literature/`
- Add migration guide for downstream users

## Execution Order

1. **FIRST**: Fix nedc-run (it's completely broken)
2. **SECOND**: Resolve vendored import issue in szcore
3. **THIRD**: Update Makefile
4. **FOURTH**: Remove shims after testing
5. **FIFTH**: Update documentation

## Testing Checklist

```bash
# After each phase, verify:
tusz-eval --help              # ✓ Works
szcore-run --help             # ✓ Works
nedc-run --help               # ❌ Currently broken, fix first
pytest tests/                 # ✓ All pass
make docker-smoke             # ⚠️ Needs Makefile update
```

## Decision Points

1. **post_processing.py location**:
   - Move to src/ (cleaner) vs. keep vendored import (simpler)
   - **Recommendation**: Move to src/seizure_evaluation/ovlp/post_processing.py

2. **Shim removal timing**:
   - Immediate vs. one release cycle
   - **Recommendation**: Fix critical issues first, then remove in next commit

3. **Docker entry points**:
   - Update Dockerfile to install package properly
   - Ensure all CLIs are available in container

## Commands to Execute

```bash
# Step 1: Create nedc wrapper
mkdir -p src/seizure_evaluation/nedc
cat > src/seizure_evaluation/nedc/__init__.py << 'EOF'
"""NEDC scoring wrapper."""
EOF

# Step 2: Fix nedc-run entry point in pyproject.toml
# (manual edit required)

# Step 3: Test everything
pip install -e .
tusz-eval --help
szcore-run --help
nedc-run --help  # Should work after fix

# Step 4: Run tests
pytest tests/

# Step 5: Update Makefile and test Docker
make docker-smoke
```

## Summary

The refactoring plan is **mostly accurate** but missed critical issues:

1. **nedc-run is completely broken** - needs immediate fix
2. **sys.path hacks persist in src/** - violates clean architecture
3. **Makefile has outdated commands** - breaks Docker testing

The plan is good but needs these fixes BEFORE proceeding with shim removal. The execution should be:
1. Fix breaking issues (nedc-run)
2. Clean architecture violations (sys.path)
3. Update tooling (Makefile)
4. Then remove shims
5. Finally update docs

This revised plan addresses all issues found and provides clear execution order.