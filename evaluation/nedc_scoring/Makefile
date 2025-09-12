# Makefile for NEDC evaluation pipeline
# Usage: make [target]

.PHONY: all test convert score clean help

# Default checkpoint path
CHECKPOINT ?= evaluation/tusz/checkpoint.pkl
OUTDIR ?= evaluation/nedc_scoring/output
METHOD ?= TAES

all: test convert score
	@echo "Complete NEDC evaluation pipeline finished"

test:
	@echo "Running pipeline tests..."
	python evaluation/nedc_scoring/test_pipeline.py

convert:
	@echo "Converting predictions to NEDC format..."
	python evaluation/nedc_scoring/convert_predictions.py \
		--checkpoint $(CHECKPOINT) \
		--outdir $(OUTDIR)

score:
	@echo "Running NEDC scorer ($(METHOD))..."
	python evaluation/nedc_scoring/run_nedc.py \
		--checkpoint $(CHECKPOINT) \
		--outdir $(OUTDIR) \
		--method $(METHOD) \
		--score-only

score-all: score-taes score-ovlp score-epoch
	@echo "All scoring methods complete"

score-taes:
	@echo "Running TAES scoring..."
	python evaluation/nedc_scoring/run_nedc.py \
		--outdir $(OUTDIR) \
		--method TAES \
		--score-only

score-ovlp:
	@echo "Running OVLP scoring..."
	python evaluation/nedc_scoring/run_nedc.py \
		--outdir $(OUTDIR) \
		--method OVLP \
		--score-only

score-epoch:
	@echo "Running EPOCH scoring..."
	python evaluation/nedc_scoring/run_nedc.py \
		--outdir $(OUTDIR) \
		--method EPOCH \
		--score-only

clean:
	@echo "Cleaning output directories..."
	rm -rf evaluation/nedc_scoring/output
	rm -rf evaluation/nedc_scoring/test_output
	rm -rf evaluation/nedc_scoring/__pycache__

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
	@echo "  CHECKPOINT - Path to checkpoint.pkl (default: evaluation/tusz/checkpoint.pkl)"
	@echo "  OUTDIR     - Output directory (default: evaluation/nedc_scoring/output)"
	@echo "  METHOD     - Scoring method: TAES|OVLP|EPOCH|IRA (default: TAES)"
	@echo ""
	@echo "Examples:"
	@echo "  make all"
	@echo "  make convert CHECKPOINT=my_checkpoint.pkl"
	@echo "  make score METHOD=OVLP"