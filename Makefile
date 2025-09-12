# Modern Python project Makefile - 2025 best practices
.PHONY: help install test format lint clean run-eval

# Default target
help:
	@echo "SeizureTransformer Development Commands"
	@echo "======================================="
	@echo "make install    - Set up environment and install dependencies"
	@echo "make test       - Run test suite with coverage"
	@echo "make format     - Format code with ruff"
	@echo "make lint       - Check code style with ruff"
	@echo "make clean      - Remove build artifacts and cache"
	@echo "make run-eval   - Run TUSZ evaluation (requires data)"

# Environment setup
install:
	uv venv
	. .venv/bin/activate && uv pip install ./wu_2025
	. .venv/bin/activate && uv pip install ruff pytest pytest-cov
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
    . .venv/bin/activate && python evaluation/nedc_scoring/run_nedc_scoring.py

# Quick inference test
test-inference:
	. .venv/bin/activate && python tests/test_inference.py
