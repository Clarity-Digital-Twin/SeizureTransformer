# 🔧 Docker Troubleshooting and Status

This guide helps diagnose and fix Docker build issues for this repo. It reflects
the current, working configuration that uses the single root `Dockerfile`.

## Current Status (canonical)
- Build verified: `seizure-transformer:latest` builds and runs (CLI help prints).
- Model weights: baked in from `wu_2025/src/wu_2025/model.pth` (~169MB).
- Datasets: keep out of the image; mount at runtime.
- `.dockerignore`: excludes `data/`, `experiments/`, `*.pkl`, `.git/`, `.venv/`.
- Compose: the sample `docker-compose.yml` references non-existent Dockerfiles and
  is considered experimental. Prefer the single-image commands below.

## Quick Environment Checks
- `docker --version` (24+ recommended)
- `docker info` (daemon reachable)
- `docker buildx version` (BuildKit available)

If buildx is missing in WSL/Windows:
- Enable Docker Desktop integration for your WSL distro, or
- Temporarily disable BuildKit: `export DOCKER_BUILDKIT=0`

## Minimal Smoke Build (environment sanity)
```bash
DOCKER_BUILDKIT=1 docker buildx build -t st:smoke -f- . <<'EOF'
FROM alpine:3.19
RUN echo "Docker build works!"
CMD ["/bin/sh", "-c", "echo SMOKE_OK"]
EOF

docker run --rm st:smoke  # expect: SMOKE_OK
```

## Canonical Build and Run
```bash
# Build (from repo root)
DOCKER_BUILDKIT=1 docker buildx build -t seizure-transformer:latest -f Dockerfile .

# Show CLI help (sanity)
docker run --rm seizure-transformer:latest

# Inference example (mount input EDF and output dir)
docker run --rm \
  -v /abs/path/in.edf:/app/data/input.edf:ro \
  -v /abs/path/out:/app/experiments \
  seizure-transformer:latest /app/data/input.edf /app/experiments/output.tsv
```

## Keep Build Context Small
- Ensure `.dockerignore` is at the repo root you pass as build context.
- Exclude: `data/`, `experiments/`, `.git/`, `.venv/`, `*.pkl`, large artifacts.
- Confirm “Sending build context …” is reasonably small (< 30–200 MB).

## GPU Notes (optional)
- Install NVIDIA Container Toolkit on the host.
- Run with `--gpus all` and set `CUDA_VISIBLE_DEVICES` as needed.

## Common Pitfalls
- Building from the wrong directory (root vs subfolder) → `.dockerignore` ignored.
- BuildKit plugin error (`docker-buildx: no such file`) → enable Desktop or set `DOCKER_BUILDKIT=0`.
- Very slow first pull of base image → pre-pull: `docker pull pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime`.

## WSL2: Slow or Stuck "Sending build context"
- Keep your repo on the Linux filesystem (e.g., `~/src/SeizureTransformer`), not under `/mnt/c/...`.
- Ensure BuildKit is available: `sudo apt-get install -y docker-buildx-plugin` (or Docker 24+).
- Enable BuildKit globally (optional):
  - `echo '{ "features": { "buildkit": true } }' | sudo tee /etc/docker/daemon.json`
  - `sudo systemctl restart docker`
- Retry the build from the repo root on ext4:
  - `docker buildx build --progress=plain -t seizure-transformer:latest -f Dockerfile .`
