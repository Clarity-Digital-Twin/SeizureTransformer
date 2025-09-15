[ARCHIVED]

This document has been archived. The canonical, maintained Docker docs now live at:

- docs/deployment/DOCKER_DEPLOYMENT_PLAN.md (current plan and quickstart)
- docs/deployment/DOCKER_FIX_PLAN.md (troubleshooting and environment checks)

The content below is preserved for historical context and may reference older
multi-container and multi-Dockerfile layouts (e.g., Dockerfile.inference,
Dockerfile.nedc) that are no longer in active use. Use the canonical docs above
for up-to-date instructions.

# Docker Implementation Plan

## 🚨 CRITICAL FINDING: 80GB of Data Inside Codebase!

**DISCOVERED**:
- `wu_2025/data/tusz/` contains **62GB** of actual EEG data
- `wu_2025/data/siena/` contains **18GB** of actual EEG data
- **Total: 80GB** embedded in the codebase!

**IMMEDIATE ACTION REQUIRED**: Run `./scripts/migrate_data.sh` to fix this

## Current Architecture Problems

### 1. Data Location Chaos
```
Current mess:
wu_2025/data/tusz/     ← 62GB dataset lives here (Wu's original structure)
wu_2025/data/siena/    ← 18GB dataset here
experiments/           ← Results scattered everywhere
```

**PROBLEM**: Docker tries to COPY wu_2025/ including 80GB of data = BUILD FAILS

### 2. Module Import Hell
```python
# Current imports are a disaster:
sys.path.append("../wu_2025/src")  # Relative path hacks
from wu_2025.utils import ...      # Sometimes works
from evaluation.nedc_eeg_eval...   # Path depends on CWD
```

## THE FIX: Data Separation Strategy

### Step 1: Move Data OUT of wu_2025 (CRITICAL)
```bash
# Move data to root level (outside Docker build context)
mv wu_2025/data /mnt/c/Users/JJ/Desktop/Clarity-Digital-Twin/SeizureTransformer/data
ln -s ../../data wu_2025/data  # Symlink for backward compatibility
```

### Step 2: Update .dockerignore (DONE ✅)
```
# Already excludes:
data/
wu_2025/data/
experiments/
*.edf
*.pkl
```

### Step 3: Docker Volume Strategy
```yaml
# docker-compose.yml
services:
  seizure:
    volumes:
      # Data stays on host, mounted into container
      - /mnt/c/Users/JJ/Desktop/datasets/tusz:/app/data/tusz:ro
      - /mnt/c/Users/JJ/Desktop/datasets/siena:/app/data/siena:ro
      - ./experiments:/app/experiments  # Read-write for results
```

## Docker Build Flow

### 1. Minimal Base Image
```dockerfile
FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime
# Only 2GB base image with CUDA
```

### 2. Copy ONLY Code + Model
```dockerfile
# Model weights (168MB) - OK to include
COPY wu_2025/src/wu_2025/model.pth /app/model/

# Code only (few MB)
COPY wu_2025/src /app/wu_2025/src
COPY evaluation/ /app/evaluation/
```

### 3. Runtime Data Access
```bash
# Run with volume mounts
docker run --gpus all \
  -v /path/to/tusz:/app/data/tusz:ro \
  -v /path/to/siena:/app/data/siena:ro \
  -v ./experiments:/app/experiments \
  seizure-transformer
```

## Path Resolution Fix

### Current Problem
```python
# evaluation/tusz/run_tusz_eval.py
data_dir = Path(__file__).parent.parent.parent / "wu_2025/data/tusz"
# BREAKS in Docker because paths are different
```

### Solution: Environment Variables
```python
# New approach
import os
from pathlib import Path

def get_data_dir(dataset="tusz"):
    # Check environment first (Docker)
    if env_path := os.getenv(f"{dataset.upper()}_DATA_DIR"):
        return Path(env_path)

    # Fallback to local development paths
    repo_root = Path(__file__).parent.parent.parent
    return repo_root / "data" / dataset
```

### Docker Environment
```dockerfile
ENV TUSZ_DATA_DIR=/app/data/tusz
ENV SIENA_DATA_DIR=/app/data/siena
ENV EXPERIMENTS_DIR=/app/experiments
```

## Implementation Checklist

### Phase 1: Data Reorganization (TODAY)
- [ ] Move wu_2025/data/ to root data/
- [ ] Create symlink for backward compatibility
- [ ] Update all hardcoded paths to use get_data_dir()
- [ ] Test evaluation still works

### Phase 2: Docker Build (TODAY)
- [ ] Build minimal image with current Dockerfile
- [ ] Test with volume mounts
- [ ] Verify GPU access works
- [ ] Check model.pth loads correctly

### Phase 3: Path Abstraction (TOMORROW)
- [ ] Create seizure_transformer/config.py with path resolution
- [ ] Update all scripts to use config
- [ ] Remove all sys.path.append hacks
- [ ] Test in both local and Docker environments

### Phase 4: Cloud Deployment (THIS WEEK)
- [ ] Test on Modal.com with S3 data URLs
- [ ] Create Colab notebook with Drive mounting
- [ ] Publish to Docker Hub
- [ ] Documentation

## Quick Test Commands

```bash
# Build
docker build -t seizure-transformer .

# Test inference (no data needed)
docker run --gpus all seizure-transformer \
  python -c "import torch; print(torch.cuda.is_available())"

# Test with local data
docker run --gpus all \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/experiments:/app/experiments \
  seizure-transformer \
  python evaluation/nedc_eeg_eval/nedc_scoring/test_pipeline.py

# Full evaluation
docker run --gpus all \
  -v /mnt/c/datasets/tusz:/app/data/tusz:ro \
  -v $(pwd)/experiments:/app/experiments \
  seizure-transformer \
  python evaluation/tusz/run_tusz_eval.py
```

## Expected Outcomes

1. **Docker image size**: ~3GB (vs 100GB+ with data)
2. **Build time**: <5 minutes (vs impossible)
3. **Deployment**: Works on Modal, Colab, any GPU cloud
4. **Local dev**: No changes needed, backward compatible

## Current Blockers

1. **Data paths hardcoded** everywhere
2. **wu_2025/data/** contains actual data (not symlinks)
3. **No environment variable support** in evaluation scripts

## Next Actions

1. **IMMEDIATE**: Move data out of wu_2025/
2. **TODAY**: Test Docker build without data
3. **TOMORROW**: Update path resolution in scripts
4. **THIS WEEK**: Deploy to cloud

## Why This Will Work

- **Separation of concerns**: Code in image, data in volumes
- **Cloud-native**: S3/GCS URLs for cloud, volumes for local
- **Backward compatible**: Symlinks maintain current structure
- **Fast builds**: 3GB image vs 100GB+
- **Portable**: Same image works everywhere
