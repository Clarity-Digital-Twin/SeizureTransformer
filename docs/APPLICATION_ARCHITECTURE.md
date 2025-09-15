# Application Architecture & Deployment Plan

## Current State Issues

### 1. Docker Organization Problems
- **Issue**: Docker files buried in `docker/` subdirectory
- **Impact**: Cloud platforms (Colab, Modal, Railway) expect Dockerfile in root
- **Conflicts**: Data paths hardcoded for local development clash with container paths

### 2. Data Location Conflicts
- **Issue**: `wu_2025/data/` contains 65GB TUSZ dataset
- **Impact**: Docker builds fail when trying to copy entire wu_2025 directory
- **Problem**: Wu's original structure conflicts with containerization needs

### 3. Module Structure Confusion
- **`wu_2025/`**: Frozen upstream code (NEVER MODIFY)
- **`evaluation/`**: Active development area
- **`docker/`**: Orphaned containerization attempts
- **No clear API**: Mixed CLI scripts, notebooks, and modules

## Proposed Architecture

```
SeizureTransformer/
├── Dockerfile                 # Main production container
├── Dockerfile.dev            # Development environment
├── docker-compose.yml        # Local orchestration
├── .dockerignore            # Exclude data/, experiments/
├── pyproject.toml           # Single source of dependencies
├── Makefile                 # Unified commands
│
├── seizure_transformer/     # NEW: Clean API package
│   ├── __init__.py
│   ├── api.py              # High-level API
│   ├── inference.py        # Model inference wrapper
│   ├── postprocess.py      # Post-processing utilities
│   └── scoring/            # Scoring backends
│       ├── nedc.py
│       ├── szcore.py
│       └── native.py
│
├── wu_2025/                 # FROZEN upstream (read-only)
│   └── src/                # Original model code
│       └── model.pth       # 168MB pretrained weights
│
├── evaluation/              # Research & benchmarking
│   ├── tusz/              # TUSZ dataset evaluation
│   ├── nedc_eeg_eval/     # Temple NEDC binaries
│   └── szcore_scoring/    # EpilepsyBench integration
│
├── data/                    # MOVED FROM wu_2025/data/
│   ├── .gitignore          # Ignore all data files
│   ├── tusz/               # 65GB dataset (not in git)
│   └── siena/              # 45GB dataset (not in git)
│
├── experiments/             # Results & checkpoints
│   └── .gitignore          # Ignore all experiments
│
├── scripts/                 # CLI utilities
│   ├── inference.py        # Simple CLI wrapper
│   ├── sweep.py           # Parameter tuning
│   └── benchmark.py       # Run all benchmarks
│
└── tests/                   # Test suite
    ├── test_api.py
    ├── test_inference.py
    └── test_scoring.py
```

## Implementation Steps

### Phase 1: Data Reorganization (Immediate)
1. Move `wu_2025/data/*` to root `data/`
2. Update all data paths in evaluation scripts
3. Add comprehensive `.gitignore` and `.dockerignore`

### Phase 2: Docker Cleanup (Today)
1. Move `docker/Dockerfile.inference` → `Dockerfile`
2. Create minimal `Dockerfile.dev` for development
3. Delete redundant Docker files
4. Fix volume mounting for data/

### Phase 3: API Creation (This Week)
1. Create `seizure_transformer/` package with clean API
2. Wrap wu_2025 model in high-level interface
3. Unified scoring interface for all backends
4. Type-safe configuration management

### Phase 4: Deployment Ready (Next Week)
1. Test on Modal.com with GPU
2. Create Colab notebook
3. Docker Hub image publication
4. API documentation

## Docker Strategy

### Production Dockerfile (root)
```dockerfile
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
WORKDIR /app
COPY wu_2025/src/wu_2025/model.pth /app/model/
COPY seizure_transformer/ /app/seizure_transformer/
COPY wu_2025/src/ /app/wu_2025/
RUN pip install -e .
ENTRYPOINT ["python", "-m", "seizure_transformer"]
```

### Data Handling
- **Never** copy data into image
- Always use volume mounts: `-v /path/to/data:/app/data`
- Support S3/GCS URLs for cloud deployment

### GPU Support
```yaml
# docker-compose.yml
services:
  inference:
    build: .
    runtime: nvidia
    volumes:
      - ./data:/app/data
      - ./experiments:/app/experiments
```

## Cloud Deployment

### Modal.com
```python
import modal
app = modal.App("seizure-transformer")

@app.function(
    image=modal.Image.from_dockerfile("Dockerfile"),
    gpu="T4",
    timeout=3600
)
def predict(edf_path: str) -> dict:
    from seizure_transformer import SeizureTransformer
    model = SeizureTransformer()
    return model.predict(edf_path)
```

### Google Colab
```python
!pip install seizure-transformer
from seizure_transformer import SeizureTransformer

model = SeizureTransformer.from_pretrained()
results = model.predict("/content/drive/MyDrive/eeg.edf")
```

## Benefits

1. **Clean Separation**: Model code (wu_2025) vs API (seizure_transformer) vs research (evaluation)
2. **Docker Ready**: Root Dockerfile works with all platforms
3. **Data Flexible**: Volume mounts or cloud URLs
4. **API First**: Simple Python API for all use cases
5. **Type Safe**: Full mypy coverage on new code

## Migration Checklist

- [ ] Move data/ to root
- [ ] Update all data paths
- [ ] Move Dockerfile to root
- [ ] Create seizure_transformer package
- [ ] Test Docker build
- [ ] Test GPU inference
- [ ] Deploy to Modal
- [ ] Create Colab notebook
- [ ] Update documentation

## Commands After Migration

```bash
# Local development
make dev-setup
make test
make benchmark

# Docker
docker build -t seizure-transformer .
docker run --gpus all -v ./data:/app/data seizure-transformer predict input.edf

# Cloud
modal deploy
python scripts/inference.py --cloud modal --input s3://bucket/eeg.edf
```