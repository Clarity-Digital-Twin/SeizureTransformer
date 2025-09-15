# Production SeizureTransformer Docker - Best Practice Implementation
# Multi-stage build for optimal size and security
# Date: September 2025

# ==============================================================================
# Stage 1: Builder - Compile dependencies and prepare environment
# ==============================================================================
FROM python:3.10-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Create virtual environment for clean dependency management
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install build tools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy dependency files first (for optimal layer caching)
COPY pyproject.toml README.md ./
COPY wu_2025/pyproject.toml wu_2025/README.md ./wu_2025/

# Install all Python dependencies
RUN pip install --no-cache-dir \
    numpy>=1.25 \
    scipy>=1.14.1 \
    torch>=2.0.1 \
    epilepsy2bids>=0.0.6 \
    scikit-learn>=1.3.0 \
    pandas>=2.0.0 \
    matplotlib>=3.7.0 \
    mne>=1.5.0 \
    tqdm>=4.65.0 \
    pyedflib>=0.1.30

# ==============================================================================
# Stage 2: Runtime - Minimal production image
# ==============================================================================
FROM python:3.10-slim

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash seizure

WORKDIR /app

# Copy application code with correct ownership
COPY --chown=seizure:seizure wu_2025/ /app/wu_2025/
COPY --chown=seizure:seizure evaluation/ /app/evaluation/
COPY --chown=seizure:seizure scripts/ /app/scripts/
COPY --chown=seizure:seizure docker/entrypoint.py /app/entrypoint.py
COPY --chown=seizure:seizure pyproject.toml README.md /app/

# Install packages in editable mode for proper imports
RUN pip install --no-cache-dir -e . && \
    pip install --no-cache-dir ./wu_2025

# Set up environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app:/app/wu_2025/src:$PYTHONPATH"
ENV MODEL_PATH="/app/wu_2025/src/wu_2025/model.pth"

# Switch to non-root user
USER seizure

# Ensure entrypoint is executable
RUN chmod +x /app/entrypoint.py

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import torch; import wu_2025; import epilepsy2bids; print('OK')" || exit 1

# Data volumes (mount external data here)
VOLUME ["/data", "/experiments"]

# Default entrypoint
ENTRYPOINT ["python", "/app/entrypoint.py"]
CMD []
