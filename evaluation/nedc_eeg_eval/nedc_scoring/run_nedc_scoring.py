#!/usr/bin/env python3
"""
Deprecated shim. Use `evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py`.

Backwards-compatible for imports: re-exports from legacy module.
"""

from evaluation.nedc_eeg_eval.nedc_scoring.legacy.run_nedc_scoring import *  # noqa: F401,F403

if __name__ == "__main__":
    import sys

    print(
        "Deprecated: run_nedc_scoring.py is replaced by run_nedc.py.\n"
        "Please run: python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py"
    )
    sys.exit(1)

