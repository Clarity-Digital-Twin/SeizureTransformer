#!/bin/bash
# Monitor TUSZ evaluation progress

echo "============================================"
echo "TUSZ Evaluation Progress Monitor"
echo "============================================"
echo ""

while true; do
    clear
    echo "============================================"
    echo "TUSZ Evaluation Progress Monitor"
    echo "============================================"
    echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    # Check if tmux session exists
    if tmux has-session -t tusz_eval 2>/dev/null; then
        echo "✅ Tmux session 'tusz_eval' is running"
        echo ""

        # Get last 10 lines of log
        echo "Latest progress:"
        echo "----------------"
        tail -10 experiments/eval/FINAL_CLEAN_RUN/inference.log 2>/dev/null || echo "No log file yet"
        echo ""

        # Check for checkpoint file
        if [ -f "experiments/eval/FINAL_CLEAN_RUN/checkpoint.pkl" ]; then
            echo "✅ Checkpoint file exists"
            ls -lh experiments/eval/FINAL_CLEAN_RUN/checkpoint.pkl
        else
            echo "⏳ Checkpoint not yet created"
        fi
    else
        echo "❌ Tmux session 'tusz_eval' not found"
        echo ""

        # Check if completed
        if [ -f "experiments/eval/FINAL_CLEAN_RUN/checkpoint.pkl" ]; then
            echo "✅ INFERENCE COMPLETE!"
            echo ""
            echo "Checkpoint details:"
            ls -lh experiments/eval/FINAL_CLEAN_RUN/checkpoint.pkl
            echo ""
            echo "Final log entries:"
            tail -20 experiments/eval/FINAL_CLEAN_RUN/inference.log
            exit 0
        fi
    fi

    echo ""
    echo "Press Ctrl+C to exit monitoring"
    sleep 10
done