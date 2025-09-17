# ruff: noqa
"""
Backwards compatibility shim for evaluation/tusz/run_tusz_eval.py
This module has been moved to src/seizure_evaluation/tusz/cli.py

THIS FILE IS DEPRECATED and will be removed in a future release.
Please update your imports to use: from seizure_evaluation.tusz.cli import main
"""

import warnings
import sys
from pathlib import Path

# Add src to path for the import
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

warnings.warn(
    "Importing from evaluation.tusz.run_tusz_eval is deprecated. "
    "Please use 'from seizure_evaluation.tusz.cli import main' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export everything from the new location
from seizure_evaluation.tusz.cli import *
from seizure_evaluation.tusz.cli import main

if __name__ == "__main__":
    main()
