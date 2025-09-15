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
    tqdm>=4.65.0

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

# Create entrypoint script that routes to correct pipeline
RUN echo '#!/usr/bin/env python3' > /app/entrypoint.py && \
    echo 'import sys' >> /app/entrypoint.py && \
    echo 'import os' >> /app/entrypoint.py && \
    echo 'import subprocess' >> /app/entrypoint.py && \
    echo 'from pathlib import Path' >> /app/entrypoint.py && \
    echo '' >> /app/entrypoint.py && \
    echo 'def main():' >> /app/entrypoint.py && \
    echo '    if len(sys.argv) < 2:' >> /app/entrypoint.py && \
    echo '        print("SeizureTransformer Docker Container")' >> /app/entrypoint.py && \
    echo '        print("="*50)' >> /app/entrypoint.py && \
    echo '        print("Usage modes:")' >> /app/entrypoint.py && \
    echo '        print("  eval     - Run TUSZ evaluation pipeline (recommended)")' >> /app/entrypoint.py && \
    echo '        print("  nedc     - Run NEDC scoring on predictions")' >> /app/entrypoint.py && \
    echo '        print("  convert  - Convert predictions to NEDC format")' >> /app/entrypoint.py && \
    echo '        print("  wu       - Wu original CLI (fails on TUSZ/Siena)")' >> /app/entrypoint.py && \
    echo '        print()' >> /app/entrypoint.py && \
    echo '        print("Example: docker run -v ./data:/data st:latest eval --help")' >> /app/entrypoint.py && \
    echo '        sys.exit(0)' >> /app/entrypoint.py && \
    echo '' >> /app/entrypoint.py && \
    echo '    mode = sys.argv[1]' >> /app/entrypoint.py && \
    echo '    args = sys.argv[2:]' >> /app/entrypoint.py && \
    echo '' >> /app/entrypoint.py && \
    echo '    if mode == "eval":' >> /app/entrypoint.py && \
    echo '        cmd = ["python", "/app/evaluation/tusz/run_tusz_eval.py"] + args' >> /app/entrypoint.py && \
    echo '    elif mode == "nedc":' >> /app/entrypoint.py && \
    echo '        cmd = ["python", "/app/evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py"] + args' >> /app/entrypoint.py && \
    echo '    elif mode == "convert":' >> /app/entrypoint.py && \
    echo '        cmd = ["python", "/app/evaluation/nedc_eeg_eval/nedc_scoring/convert_predictions.py"] + args' >> /app/entrypoint.py && \
    echo '    elif mode == "wu":' >> /app/entrypoint.py && \
    echo '        print("WARNING: Wu CLI requires exact electrode names (Fp1, F3, etc)")' >> /app/entrypoint.py && \
    echo '        print("         Will fail on TUSZ/Siena data.")' >> /app/entrypoint.py && \
    echo '        cmd = ["python", "-m", "wu_2025"] + args' >> /app/entrypoint.py && \
    echo '    else:' >> /app/entrypoint.py && \
    echo '        print(f"Unknown mode: {mode}")' >> /app/entrypoint.py && \
    echo '        sys.exit(1)' >> /app/entrypoint.py && \
    echo '' >> /app/entrypoint.py && \
    echo '    result = subprocess.run(cmd)' >> /app/entrypoint.py && \
    echo '    sys.exit(result.returncode)' >> /app/entrypoint.py && \
    echo '' >> /app/entrypoint.py && \
    echo 'if __name__ == "__main__":' >> /app/entrypoint.py && \
    echo '    main()' >> /app/entrypoint.py && \
    chmod +x /app/entrypoint.py

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import torch; import wu_2025; import epilepsy2bids; print('OK')" || exit 1

# Data volumes (mount external data here)
VOLUME ["/data", "/experiments"]

# Default entrypoint
ENTRYPOINT ["python", "/app/entrypoint.py"]
CMD []
