#!/bin/bash
# Setup NEDC environment for evaluation

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$(dirname $(dirname "$SCRIPT_DIR"))"

# NEDC installation path
export NEDC_NFC="$REPO_ROOT/evaluation/nedc_eeg_eval/v6.0.0"

# Check if NEDC exists
if [ ! -d "$NEDC_NFC" ]; then
    echo "Error: NEDC not found at $NEDC_NFC"
    echo "Please ensure NEDC v6.0.0 is installed"
    exit 1
fi

# Set up paths
export PATH="$NEDC_NFC/bin:$PATH"
export PYTHONPATH="$NEDC_NFC/lib:$PYTHONPATH"

echo "NEDC environment configured:"
echo "  NEDC_NFC=$NEDC_NFC"
echo "  PATH includes: $NEDC_NFC/bin"
echo "  PYTHONPATH includes: $NEDC_NFC/lib"

# Check if NEDC binary exists
if [ -f "$NEDC_NFC/bin/nedc_eeg_eval" ]; then
    echo "  NEDC binary found: $NEDC_NFC/bin/nedc_eeg_eval"
else
    echo "  WARNING: NEDC binary not found at $NEDC_NFC/bin/nedc_eeg_eval"
fi

echo ""
echo "Environment ready. You can now run:"
echo "  python evaluation/nedc_scoring/run_nedc.py"