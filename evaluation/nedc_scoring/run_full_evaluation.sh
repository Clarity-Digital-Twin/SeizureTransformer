#!/bin/bash
# Complete NEDC evaluation pipeline for SeizureTransformer
# Run this after TUSZ evaluation completes

set -e  # Exit on error

echo "=========================================="
echo "NEDC EVALUATION PIPELINE"
echo "=========================================="
echo ""

# Check if checkpoint exists
CHECKPOINT="evaluation/tusz/checkpoint.pkl"
if [ ! -f "$CHECKPOINT" ]; then
    echo "Error: Checkpoint not found at $CHECKPOINT"
    echo "Please ensure TUSZ evaluation has completed"
    exit 1
fi

# Set up NEDC environment
source evaluation/nedc_scoring/setup_nedc_env.sh

echo ""
echo "Step 1: Testing pipeline with synthetic data"
echo "------------------------------------------"
python evaluation/nedc_scoring/test_pipeline.py

echo ""
echo "Step 2: Converting SeizureTransformer predictions to NEDC format"
echo "---------------------------------------------------------------"
python evaluation/nedc_scoring/convert_predictions.py \
    --checkpoint "$CHECKPOINT" \
    --outdir evaluation/nedc_scoring/output

echo ""
echo "Step 3: Running NEDC scorer (TAES metrics)"
echo "------------------------------------------"
python evaluation/nedc_scoring/run_nedc.py \
    --checkpoint "$CHECKPOINT" \
    --outdir evaluation/nedc_scoring/output \
    --method TAES \
    --score-only

echo ""
echo "Step 4: Running NEDC scorer (OVLP metrics)"
echo "------------------------------------------"
python evaluation/nedc_scoring/run_nedc.py \
    --checkpoint "$CHECKPOINT" \
    --outdir evaluation/nedc_scoring/output \
    --method OVLP \
    --score-only

echo ""
echo "Step 5: Running NEDC scorer (EPOCH metrics)"
echo "-------------------------------------------"
python evaluation/nedc_scoring/run_nedc.py \
    --checkpoint "$CHECKPOINT" \
    --outdir evaluation/nedc_scoring/output \
    --method EPOCH \
    --score-only

echo ""
echo "=========================================="
echo "EVALUATION COMPLETE"
echo "=========================================="
echo "Results saved to: evaluation/nedc_scoring/output/results/"
echo ""
echo "Key metrics files:"
echo "  - TAES results: evaluation/nedc_scoring/output/results/taes_*.txt"
echo "  - OVLP results: evaluation/nedc_scoring/output/results/ovlp_*.txt"
echo "  - EPOCH results: evaluation/nedc_scoring/output/results/epoch_*.txt"