# SeizureTransformer Inference Container
FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy model weights first (rarely changes)
COPY wu_2025/src/wu_2025/model.pth /app/model/model.pth

# Install project dependencies via pyproject (modern PEP 517)
# Copy project metadata and source first for better layer caching
COPY pyproject.toml README.md ./
COPY evaluation/ evaluation/
COPY scripts/ scripts/
RUN pip install --no-cache-dir .

# Copy wu_2025 package (frozen upstream)
COPY wu_2025/setup.py wu_2025/setup.cfg wu_2025/pyproject.toml wu_2025/
COPY wu_2025/src wu_2025/src
RUN pip install --no-cache-dir ./wu_2025

# Copy evaluation code
COPY evaluation/ evaluation/
COPY scripts/ scripts/

# Set environment
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/model/model.pth
ENV CUDA_VISIBLE_DEVICES=0

# Data and experiments as volumes
VOLUME ["/app/data", "/app/experiments"]

# Default: show help
ENTRYPOINT ["python", "-m", "wu_2025"]
CMD ["--help"]
