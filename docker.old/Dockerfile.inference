# Multi-stage build for SeizureTransformer inference
# Optimized for GPU inference with minimal runtime size

# Stage 1: Builder
FROM nvidia/cuda:12.4.0-devel-ubuntu22.04 AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    python3.10 python3.10-dev python3-pip \
    wget curl git \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment
RUN python3 -m pip install --upgrade pip setuptools wheel

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install PyTorch with CUDA support first (large, changes infrequently)
RUN pip install --no-cache-dir \
    torch==2.2.0 \
    torchvision==0.17.0 \
    --index-url https://download.pytorch.org/whl/cu121

# Copy and install project dependencies
WORKDIR /build
COPY wu_2025/setup.py wu_2025/setup.cfg wu_2025/pyproject.toml ./wu_2025/
COPY wu_2025/src/wu_2025/__init__.py ./wu_2025/src/wu_2025/
RUN pip install --no-cache-dir ./wu_2025/

# Copy evaluation dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-compile Python files for faster startup
COPY wu_2025/ ./wu_2025/
COPY evaluation/ ./evaluation/
COPY seizure_evaluation/ ./seizure_evaluation/
RUN python3 -m compileall /build

# Stage 2: Runtime
FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y \
    python3.10 python3-distutils \
    libgomp1 libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy compiled application code
WORKDIR /app
COPY --from=builder /build/wu_2025 ./wu_2025/
COPY --from=builder /build/evaluation ./evaluation/
COPY --from=builder /build/seizure_evaluation ./seizure_evaluation/

# Copy model weights (if included in repo)
COPY wu_2025/src/wu_2025/model.pth /opt/model/model.pth

# Set environment
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV MODEL_PATH="/opt/model/model.pth"
ENV CUDA_VISIBLE_DEVICES=0

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash seizure && \
    chown -R seizure:seizure /app && \
    chown -R seizure:seizure /opt/model

# Health check to verify GPU availability
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python3 -c "import torch; assert torch.cuda.is_available(), 'GPU not available'; print('GPU OK')" || exit 1

# Switch to non-root user
USER seizure

# Default volumes for data and output
VOLUME ["/data", "/experiments"]

# Flexible entrypoint
ENTRYPOINT ["python3"]
CMD ["-m", "wu_2025", "--help"]