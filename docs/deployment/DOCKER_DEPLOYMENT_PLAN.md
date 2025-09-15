# [Maintained]

This page is the canonical Docker quickstart and deployment guide for this repo.
Sections describing multi-container stacks and multiple Dockerfiles
(`Dockerfile.inference`, `Dockerfile.nedc`, `Dockerfile.api`) are retained below
for reference but are not actively maintained. The supported path uses the
single root `Dockerfile` with BuildKit.

# 🐳 DOCKER DEPLOYMENT PLAN
## Production-Ready Containerization for SeizureTransformer TUSZ Pipeline

**Goal**: Create a bulletproof, GPU-accelerated Docker setup for both research reproducibility and production deployment of our 137x FA gap evaluation pipeline.

## Canonical Quickstart

- Prereqs
  - Docker 24+ with buildx/BuildKit enabled (Docker Desktop on WSL2 works).
  - Optional GPU: install NVIDIA Container Toolkit; run with `--gpus all`.
- Build (root Dockerfile)
  - `DOCKER_BUILDKIT=1 docker buildx build -t seizure-transformer:latest -f Dockerfile .`
- Smoke run (prints CLI help)
  - `docker run --rm seizure-transformer:latest`
- Inference example
  - `docker run --rm -v /abs/path/in.edf:/app/data/input.edf:ro -v /abs/out:/app/experiments seizure-transformer:latest /app/data/input.edf /app/experiments/output.tsv`
- Data policy
  - Do not bake datasets into the image. Keep large datasets outside the repo and mount at runtime.
  - `.dockerignore` excludes `data/`, `experiments/`, `*.pkl`, `.git/`, `.venv/` to keep context small.
- Troubleshooting
  - Missing buildx plugin: enable Docker Desktop integration or set `DOCKER_BUILDKIT=0` temporarily.
  - Context is huge: ensure you are building from the repo root and `.dockerignore` is present there.
  - Minimal smoke build to validate environment:
    - `DOCKER_BUILDKIT=1 docker buildx build -t st:smoke -f- . <<'EOF'
FROM alpine:3.19
RUN echo "Docker build works!"
CMD ["/bin/sh", "-c", "echo SMOKE_OK"]
EOF`
- Compose status
  - The provided `docker-compose.yml` references `Dockerfile.inference` and `Dockerfile.nedc`, which are not present. Treat it as experimental; prefer the single-image flow above.

## 🎯 Our Specific Requirements

### What We're Containerizing
1. **Core Model Inference** - SeizureTransformer with 168MB weights
2. **TUSZ Evaluation Pipeline** - Full 865-file eval processing
3. **NEDC Scoring Stack** - Both Temple binaries and native Python
4. **API Service** (Future) - FastAPI for real-time inference

### Key Challenges to Solve
- **GPU Access**: CUDA 12.4 for model inference
- **Large Files**: 168MB model weights + 5.2GB TUSZ data
- **Binary Dependencies**: NEDC v6.0.0 requires specific Python paths
- **Multi-Stage Pipeline**: Inference → Post-processing → Scoring
- **Reproducibility**: Exact NEDC v6.0.0 parity for publications

## 🏗️ Architecture Design

### Three-Container Strategy

```yaml
# docker-compose.yml structure
services:
  # 1. Model inference container (GPU)
  seizure-transformer:
    - CUDA 12.4 base
    - Model weights baked in
    - Optimized for batch processing

  # 2. NEDC scoring container (CPU)
  nedc-scorer:
    - Temple binaries included
    - Native Python scorer
    - Metrics aggregation

  # 3. API gateway (Future)
  api-gateway:
    - FastAPI
    - Health checks
    - Load balancing ready
```

## 📦 Dockerfile Improvements

### Current Issues with Existing Dockerfile
```dockerfile
# PROBLEMS:
- Using runtime image (need devel for full CUDA)
- No multi-stage build (168MB weights in final layer)
- No health checks
- Missing evaluation dependencies
- Volumes not optimal for our pipeline
```

### Proposed Multi-Stage Dockerfile

```dockerfile
# Stage 1: Builder (downloads, compiles)
FROM nvidia/cuda:12.4.0-devel-ubuntu22.04 AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    python3.10 python3.10-dev python3-pip \
    wget curl git && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download model weights (if not in repo)
RUN mkdir -p /opt/model && \
    wget -O /opt/model/model.pth \
    "https://github.com/keruiwu/SeizureTransformer/releases/download/v1.0/model.pth"

# Stage 2: Runtime (minimal, production)
FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    python3.10 python3-distutils \
    libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /opt/model /opt/model

# Copy application code
WORKDIR /app
COPY wu_2025/ ./wu_2025/
COPY evaluation/ ./evaluation/
COPY seizure_evaluation/ ./seizure_evaluation/

# Set environment
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH="/opt/model/model.pth"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import torch; assert torch.cuda.is_available()" || exit 1

# Non-root user
RUN useradd -m -u 1000 seizure && chown -R seizure:seizure /app
USER seizure

# Entry point for flexibility
ENTRYPOINT ["python3", "-m"]
CMD ["wu_2025", "--help"]
```

## 🚀 Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  # GPU-accelerated inference service
  seizure-transformer:
    build:
      context: .
      dockerfile: Dockerfile.inference
    image: seizuretransformer:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    volumes:
      - ./data/tusz:/data/tusz:ro
      - ./experiments:/experiments
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - BATCH_SIZE=32
    command: ["evaluation.tusz.run_tusz_eval",
              "--data_dir", "/data/tusz/v2.0.3/edf/eval",
              "--out_dir", "/experiments/eval/baseline"]
    restart: on-failure
    healthcheck:
      test: ["CMD", "python3", "-c", "import torch; assert torch.cuda.is_available()"]
      interval: 30s
      timeout: 10s
      retries: 3

  # NEDC scoring service (CPU only)
  nedc-scorer:
    build:
      context: .
      dockerfile: Dockerfile.nedc
    image: nedc-scorer:latest
    volumes:
      - ./experiments:/experiments
      - ./evaluation/nedc_eeg_eval:/nedc:ro
    environment:
      - NEDC_NFC=/nedc/v6.0.0
      - PYTHONPATH=/nedc/v6.0.0/lib:$PYTHONPATH
    depends_on:
      seizure-transformer:
        condition: service_healthy
    command: ["evaluation.nedc_eeg_eval.nedc_scoring.run_nedc",
              "--checkpoint", "/experiments/eval/baseline/checkpoint.pkl",
              "--outdir", "/experiments/eval/baseline/nedc_results",
              "--backend", "native-taes"]

  # Future: API service
  api-gateway:
    build:
      context: .
      dockerfile: Dockerfile.api
    image: seizure-api:latest
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/opt/model/model.pth
    depends_on:
      - seizure-transformer
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## 🛠️ Implementation Steps

### Phase 1: Core Infrastructure (Week 1)
- [ ] Create multi-stage Dockerfile.inference
- [ ] Create Dockerfile.nedc for scoring
- [ ] Set up docker-compose.yml
- [ ] Add .dockerignore for efficiency
- [ ] Test GPU passthrough

### Phase 2: Pipeline Integration (Week 2)
- [ ] Volume mounting strategy for TUSZ data
- [ ] Environment variable configuration
- [ ] Inter-container communication
- [ ] Logging aggregation
- [ ] Error handling and restarts

### Phase 3: Production Hardening (Week 3)
- [ ] Health checks for all services
- [ ] Resource limits (memory, CPU)
- [ ] Security scanning (Trivy/Snyk)
- [ ] Image size optimization
- [ ] Registry push (Docker Hub/ECR)

### Phase 4: API Service (Future)
- [ ] FastAPI implementation
- [ ] WebSocket for streaming results
- [ ] Authentication/authorization
- [ ] Rate limiting
- [ ] Prometheus metrics

## 📊 Performance Targets

| Metric | Target | Rationale |
|--------|--------|-----------|
| Image size (inference) | < 3GB | With CUDA runtime |
| Image size (NEDC) | < 500MB | CPU only |
| Build time | < 5 min | With cache |
| Startup time | < 30s | Including GPU init |
| Memory usage | < 8GB | Per container |
| Inference throughput | > 10 files/min | On single GPU |

## 🔒 Security Considerations

1. **No Secrets in Images**
   - Use Docker secrets for credentials
   - Environment variables for config
   - Never commit .env files

2. **Minimal Attack Surface**
   - Non-root users
   - Read-only root filesystem
   - No unnecessary packages

3. **Network Isolation**
   - Internal network for services
   - Only expose API port
   - Use TLS for external traffic

## 🧪 Testing Strategy

```bash
# Quick validation
make docker-test

# Full pipeline test
docker-compose run seizure-transformer \
  python -m pytest tests/integration/

# Performance benchmark
docker-compose run --rm seizure-transformer \
  python -m evaluation.benchmark --gpu

# Security scan
trivy image seizuretransformer:latest
```

## 📝 Documentation Needs

- [ ] Docker Quick Start guide
- [ ] Environment variable reference
- [ ] Troubleshooting guide
- [ ] Performance tuning tips
- [ ] Multi-GPU setup instructions

## 🎯 Success Criteria

1. **Reproducibility**: Anyone can run our TUSZ evaluation with one command
2. **Performance**: Match or exceed native performance
3. **Portability**: Runs on any CUDA-capable Linux host
4. **Maintainability**: Clear separation of concerns
5. **Scalability**: Ready for Kubernetes deployment

## 🚦 Next Steps

1. Review and approve this plan
2. Create feature/docker-deployment branch
3. Implement Phase 1 (core Dockerfiles)
4. Test on local GPU machine
5. Deploy to cloud (AWS/GCP) for validation

---

**Note**: This plan prioritizes production readiness while maintaining research reproducibility. The multi-stage approach ensures we can iterate quickly while keeping deployment artifacts lean and secure.
