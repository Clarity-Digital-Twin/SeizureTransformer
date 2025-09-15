#!/bin/bash
# Complete NEDC evaluation pipeline for SeizureTransformer
# Run this after TUSZ evaluation completes

set -e  # Exit on error

# Resolve this script's directory for robust relative paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

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
source "$SCRIPT_DIR/setup_nedc_env.sh"

echo ""

echo "Step 1: Testing pipeline with synthetic data"
echo "------------------------------------------"
python "$SCRIPT_DIR/test_pipeline.py"

echo ""

echo "Step 2: Converting SeizureTransformer predictions to NEDC format"
echo "---------------------------------------------------------------"
python "$SCRIPT_DIR/convert_predictions.py" \
    --checkpoint "$CHECKPOINT" \
    --outdir "$SCRIPT_DIR/output"

echo ""

echo "Step 3: Running NEDC scorer (TAES metrics)"
echo "------------------------------------------"
python "$SCRIPT_DIR/run_nedc.py" \
    --outdir "$SCRIPT_DIR/output" \
    --score-only

echo ""

echo "Step 4: Running NEDC scorer (OVLP metrics)"
echo "------------------------------------------"
# OVLP and EPOCH summaries are produced by the same run in v6.0.0; rerun not required.

echo ""

echo "Step 5: Running NEDC scorer (EPOCH metrics)"
echo "-------------------------------------------"
# See "$SCRIPT_DIR/output/results" for all summaries.

echo ""

echo "=========================================="
echo "EVALUATION COMPLETE"
echo "=========================================="
echo "Results saved to: $SCRIPT_DIR/output/results/"
echo ""
echo "Key metrics files:"
echo "  - Summaries: $SCRIPT_DIR/output/results/summary*.txt"

