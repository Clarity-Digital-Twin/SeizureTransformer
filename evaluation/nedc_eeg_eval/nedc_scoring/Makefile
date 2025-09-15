# Makefile for NEDC evaluation pipeline
# Usage: make [target]

.PHONY: all test convert score clean help

# Default checkpoint path
CHECKPOINT ?= experiments/eval/baseline/checkpoint.pkl
OUTDIR ?= evaluation/nedc_eeg_eval/nedc_scoring/output

all: test convert score
	@echo "Complete NEDC evaluation pipeline finished"

test:
	@echo "Running pipeline tests..."
	python test_pipeline.py

convert:
	@echo "Converting predictions to NEDC format..."
	python convert_predictions.py \
		--checkpoint $(CHECKPOINT) \
		--outdir $(OUTDIR)

score:
	@echo "Running NEDC scorer..."
	python run_nedc.py \
		--outdir $(OUTDIR) \
		--score-only

clean:
	@echo "Cleaning output directories..."
	rm -rf evaluation/nedc_eeg_eval/nedc_scoring/output
	rm -rf evaluation/nedc_eeg_eval/nedc_scoring/test_output
	rm -rf evaluation/nedc_eeg_eval/nedc_scoring/__pycache__

help:
	@echo "NEDC Evaluation Pipeline Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  all        - Run complete pipeline (test, convert, score)"
	@echo "  test       - Test pipeline with synthetic data"
	@echo "  convert    - Convert checkpoint to NEDC format"
	@echo "  score      - Run NEDC scorer (default: TAES)"
	@echo "  score-all  - Run all scoring methods"
	@echo "  clean      - Remove output directories"
	@echo "  help       - Show this help message"
	@echo ""
	@echo "Variables:"
	@echo "  CHECKPOINT - Path to checkpoint.pkl (default: experiments/eval/baseline/checkpoint.pkl)"
	@echo "  OUTDIR     - Output directory (default: evaluation/nedc_eeg_eval/nedc_scoring/output)"
	@echo ""
	@echo "Examples:"
	@echo "  make all"
	@echo "  make convert CHECKPOINT=my_checkpoint.pkl"
