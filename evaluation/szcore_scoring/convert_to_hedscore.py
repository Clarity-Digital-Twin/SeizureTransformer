# ruff: noqa
"""
Backwards compatibility shim for evaluation/szcore_scoring/convert_to_hedscore.py
This module has been moved to src/seizure_evaluation/szcore/convert_to_hedscore.py

THIS FILE IS DEPRECATED and will be removed in a future release.
Please update your imports to use: from seizure_evaluation.szcore.convert_to_hedscore import ...
"""

import warnings
import sys
from pathlib import Path

# Add src to path for the import
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

warnings.warn(
    "Importing from evaluation.szcore_scoring.convert_to_hedscore is deprecated. "
    "Please use 'from seizure_evaluation.szcore.convert_to_hedscore import ...' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export everything from the new location
from seizure_evaluation.szcore.convert_to_hedscore import *
