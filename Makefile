# Modern Python project Makefile - 2025 best practices
.PHONY: help install test format lint typecheck check-all clean run-eval

# Default target
help:
	@echo "SeizureTransformer Development Commands"
	@echo "======================================="
	@echo "make install    - Set up environment and install dependencies"
	@echo "make test       - Run test suite with coverage"
	@echo "make format     - Format code with ruff"
	@echo "make lint       - Check code style with ruff"
	@echo "make typecheck  - Run mypy type checking"
	@echo "make check-all  - Run all quality checks (lint + typecheck + tests)"
	@echo "make clean      - Remove build artifacts and cache"
	@echo "make run-eval   - Run TUSZ evaluation (requires data)"

# Environment setup
install:
	uv venv
	@if [ -f uv.lock ]; then \
		echo "📦 Using uv.lock to sync pinned deps"; \
		uv sync --dev; \
	else \
		echo "⚠️  uv.lock not found; installing base deps"; \
		. .venv/bin/activate && uv pip install ./wu_2025 ruff pytest pytest-cov; \
	fi
	@echo "✅ Environment ready! Activate with: source .venv/bin/activate"

# Testing
test:
	. .venv/bin/activate && python -m pytest tests/ -v

test-cov:
	. .venv/bin/activate && python -m pytest tests/ --cov --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

# Code quality
format:
	. .venv/bin/activate && ruff format .
	. .venv/bin/activate && ruff check --fix .

lint:
	. .venv/bin/activate && ruff check .

typecheck:
	. .venv/bin/activate && mypy evaluation/ scripts/ tests/ --exclude="evaluation/nedc_eeg_eval"

check-all: lint typecheck test
	@echo "✅ All quality checks passed!"

# Clean up
clean:
	rm -rf .venv/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Run evaluation
run-eval-tusz:
	@echo "Running TUSZ evaluation..."
	. .venv/bin/activate && python evaluation/tusz/run_tusz_eval.py

run-eval-nedc:
	@echo "Running NEDC official evaluation..."
	. .venv/bin/activate && $(MAKE) -C evaluation/nedc_scoring all

# Quick inference test
test-inference:
	. .venv/bin/activate && python tests/test_inference.py
