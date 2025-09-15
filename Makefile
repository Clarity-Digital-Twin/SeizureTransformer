# SeizureTransformer Makefile
.PHONY: help setup test lint format typecheck clean docker-build docker-run benchmark sweep

help:
	@echo "SeizureTransformer Development Commands"
	@echo ""
	@echo "Setup & Environment:"
	@echo "  make setup          - Create venv and install dependencies"
	@echo "  make setup-dev      - Setup with dev dependencies"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           - Run ruff linting"
	@echo "  make format         - Format code with ruff"
	@echo "  make typecheck      - Run mypy type checking"
	@echo "  make test           - Run test suite"
	@echo "  make quality        - Run all quality checks"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-run     - Run Docker container"
	@echo "  make docker-shell   - Interactive Docker shell"
	@echo ""
	@echo "Evaluation:"
	@echo "  make benchmark      - Run all benchmarks at paper defaults"
	@echo "  make sweep          - Run parameter sweeps for clinical targets"
	@echo "  make nedc-test      - Test NEDC pipeline"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean          - Remove build artifacts"
	@echo "  make monitor-sweep  - Monitor parameter sweep progress"

# Setup
setup:
	python -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip
	. .venv/bin/activate && pip install ./wu_2025
	. .venv/bin/activate && pip install -r requirements.txt

setup-dev:
	python -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip
	. .venv/bin/activate && pip install ./wu_2025
	. .venv/bin/activate && pip install -e .[dev]

# Code Quality
lint:
	ruff check evaluation/ scripts/ tests/

format:
	ruff format evaluation/ scripts/ tests/

typecheck:
	mypy evaluation/ scripts/ tests/

test:
	pytest tests/ -v

quality: lint typecheck test
	@echo "✅ All quality checks passed"

# Docker
docker-build:
	docker build -t seizure-transformer:latest .

docker-run:
	docker run --gpus all \
		-v $$(pwd)/data:/app/data \
		-v $$(pwd)/experiments:/app/experiments \
		seizure-transformer:latest

docker-shell:
	docker run --gpus all -it \
		-v $$(pwd)/data:/app/data \
		-v $$(pwd)/experiments:/app/experiments \
		--entrypoint /bin/bash \
		seizure-transformer:latest

# Evaluation
benchmark:
	@echo "Running benchmarks at paper defaults (threshold=0.8)..."
	python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py \
		--checkpoint experiments/eval/baseline/checkpoint.pkl \
		--outdir experiments/eval/baseline/paper_default_nedc \
		--threshold 0.8 --kernel 5 --min_duration_sec 2.0
	python evaluation/szcore_scoring/run_szcore.py \
		--checkpoint experiments/eval/baseline/checkpoint.pkl \
		--outdir experiments/eval/baseline/paper_default_szcore \
		--threshold 0.8 --kernel 5 --min_duration_sec 2.0

sweep:
	@echo "Starting parameter sweeps in tmux..."
	@echo "Run 'make monitor-sweep' to check progress"
	tmux new-session -d -s sweep_10fa '. .venv/bin/activate && python evaluation/nedc_eeg_eval/nedc_scoring/sweep_operating_point.py --checkpoint experiments/eval/baseline/checkpoint.pkl --outdir_base experiments/eval/baseline/sweep_10fa --target_fa_per_24h 10'
	tmux new-session -d -s sweep_2_5fa '. .venv/bin/activate && python evaluation/nedc_eeg_eval/nedc_scoring/sweep_operating_point.py --checkpoint experiments/eval/baseline/checkpoint.pkl --outdir_base experiments/eval/baseline/sweep_2_5fa --target_fa_per_24h 2.5'

monitor-sweep:
	@echo "=== Sweep Progress ==="
	@echo "10 FA/24h: $$(ls experiments/eval/baseline/sweep_10fa 2>/dev/null | wc -l)/140 completed"
	@echo "2.5 FA/24h: $$(ls experiments/eval/baseline/sweep_2_5fa 2>/dev/null | wc -l)/120 completed"
	@echo "1.0 FA/24h: $$(ls experiments/eval/baseline/sweep_1fa 2>/dev/null | wc -l)/150 completed"
	@echo ""
	@echo "Attach to tmux: tmux attach -t sweep_10fa"

nedc-test:
	cd evaluation/nedc_eeg_eval/nedc_scoring && make test

# Utilities
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true