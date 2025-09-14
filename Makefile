# SeizureTransformer Makefile - NEDC Integration
.PHONY: help install test format lint typecheck check-all clean run-eval

# Default target
help:
	@echo "SeizureTransformer Development Commands"
	@echo "======================================="
	@echo ""
	@echo "Setup:"
	@echo "  install         - Install dependencies with uv"
	@echo "  install-dev     - Install with dev dependencies"
	@echo ""
	@echo "Quality:"
	@echo "  lint            - Run ruff linter (excludes vendor)"
	@echo "  format          - Format code with ruff"
	@echo "  typecheck       - Run mypy type checker"
	@echo "  test            - Run all tests"
	@echo "  test-fast       - Run tests excluding NEDC"
	@echo "  test-nedc       - Run NEDC conformance tests"
	@echo "  check-all       - Run all quality checks"
	@echo ""
	@echo "Evaluation:"
	@echo "  run-dev-eval    - Run TUSZ dev evaluation"
	@echo "  run-eval-sweep  - Run parameter sweep on dev"
	@echo "  run-nedc-score  - Run NEDC scoring pipeline"
	@echo "  run-szcore-score- Run SzCORE scoring (timescoring)"
	@echo "  check-dev       - Check dev evaluation status"
	@echo ""
	@echo "Utilities:"
	@echo "  clean           - Remove generated files"

# Environment setup
install:
	uv venv
	. .venv/bin/activate && uv pip install ./wu_2025
	. .venv/bin/activate && uv pip install -e .
	. .venv/bin/activate && uv pip install lxml  # For NEDC
	@echo "✅ Environment ready! Activate with: source .venv/bin/activate"

install-dev:
	uv venv
	. .venv/bin/activate && uv pip install ./wu_2025
	. .venv/bin/activate && uv pip install -e . --extra dev
	. .venv/bin/activate && uv pip install lxml
	@echo "✅ Dev environment ready!"

# Testing
test:
	. .venv/bin/activate && python -m pytest tests/ -v

test-fast:
	. .venv/bin/activate && pytest tests -v -m "not nedc"

test-nedc:
	. .venv/bin/activate && pytest tests -v -m "nedc"

test-conformance:
	. .venv/bin/activate && pytest tests/integration/test_nedc_conformance.py -v

test-cov:
	. .venv/bin/activate && python -m pytest tests/ --cov --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

# Code quality
format:
	. .venv/bin/activate && ruff format evaluation/ scripts/ tests/ --exclude evaluation/nedc_eeg_eval

lint:
	. .venv/bin/activate && ruff check evaluation/ scripts/ tests/ --exclude evaluation/nedc_eeg_eval

typecheck:
	. .venv/bin/activate && mypy evaluation/nedc_scoring scripts tests || true

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

# Evaluation workflows
run-dev-eval:
	@echo "Starting TUSZ dev evaluation..."
	. .venv/bin/activate && python evaluation/tusz/run_tusz_eval.py \
		--data_dir wu_2025/data/tusz/edf/dev \
		--out_dir experiments/dev/baseline \
		--device auto

run-eval-sweep:
	@echo "Running parameter sweep on dev checkpoint..."
	. .venv/bin/activate && python evaluation/nedc_scoring/sweep_operating_point.py \
		--checkpoint experiments/dev/baseline/checkpoint.pkl \
		--outdir_base experiments/dev/sweeps \
		--thresholds 0.3,0.4,0.5,0.6,0.7,0.8,0.9 \
		--kernels 3,5,7,11,15 \
		--min_durations 1,2,3,4,5 \
		--merge_gaps 0,5,10,15 \
		--target_fa_per_24h 10

run-nedc-score:
	$(MAKE) -C evaluation/nedc_scoring all

run-szcore-score:
	. .venv/bin/activate && python evaluation/szcore_scoring/run_szcore.py \
		--checkpoint experiments/eval/baseline/checkpoint.pkl \
		--outdir experiments/eval/baseline/szcore_results

# Monitoring
check-dev:
	@echo "Checking dev evaluation status..."
	@if [ -f experiments/dev/baseline/checkpoint.pkl ]; then \
		. .venv/bin/activate && python -c "import pickle; \
		c = pickle.load(open('experiments/dev/baseline/checkpoint.pkl', 'rb')); \
		total = len(c.get('results', {})); \
		print(f'Processed {total} files');"; \
	else \
		echo "No checkpoint found"; \
	fi

# Quick inference test
test-inference:
	. .venv/bin/activate && python tests/test_inference.py

.PHONY: install install-dev test test-fast test-nedc test-conformance test-cov format lint typecheck check-all clean run-dev-eval run-eval-sweep run-nedc-score run-szcore-score check-dev test-inference
