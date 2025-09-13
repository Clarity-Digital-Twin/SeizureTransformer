#!/bin/bash
# Complete NEDC evaluation pipeline for SeizureTransformer
# Run this after TUSZ evaluation completes

set -e  # Exit on error

echo "=========================================="
echo "NEDC EVALUATION PIPELINE"
echo "=========================================="
echo ""

# Check if checkpoint exists (allow override via env)
CHECKPOINT="${CHECKPOINT:-experiments/eval/baseline/checkpoint.pkl}"
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
    --outdir evaluation/nedc_scoring/output \
    --score-only

echo ""
echo "Step 4: Running NEDC scorer (OVLP metrics)"
echo "------------------------------------------"
# OVLP and EPOCH summaries are produced by the same run in v6.0.0; rerun not required.

echo ""
echo "Step 5: Running NEDC scorer (EPOCH metrics)"
echo "-------------------------------------------"
# See evaluation/nedc_scoring/output/results for all summaries.

echo ""
echo "=========================================="
echo "EVALUATION COMPLETE"
echo "=========================================="
echo "Results saved to: evaluation/nedc_scoring/output/results/"
echo ""
echo "Key metrics files:"
echo "  - Summaries: evaluation/nedc_scoring/output/results/summary*.txt"
