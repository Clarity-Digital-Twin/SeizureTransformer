#!/bin/bash
# Monitor evaluation progress

echo "📊 Evaluation Progress Monitor"
echo "=============================="

# Check tmux session
if tmux has-session -t dev_eval 2>/dev/null; then
    echo "✅ Dev evaluation is running in tmux"
    echo ""
    echo "Recent output:"
    tmux capture-pane -t dev_eval -p | tail -10
    echo ""
    echo "To attach: tmux attach -t dev_eval"
    echo "To detach: Ctrl+B then D"
else
    echo "❌ No dev_eval tmux session found"
fi

# Check checkpoint
CHECKPOINT_PATH="${1:-experiments/dev/baseline/checkpoint.pkl}"
if [ -f "$CHECKPOINT_PATH" ]; then
    echo ""
    echo "📦 Checkpoint status:"
    ls -lh "$CHECKPOINT_PATH"
    python3 -c "
import pickle
import sys
with open(sys.argv[1], 'rb') as f:
    ck = pickle.load(f)
    print(f'  Files processed: {len(ck["results"])}')
    print(f'  Next index: {ck.get(\"next_idx\", \"N/A\")}')
" "$CHECKPOINT_PATH"
fi
