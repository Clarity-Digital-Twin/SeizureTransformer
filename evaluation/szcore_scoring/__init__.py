"""
Backwards compatibility shim for evaluation/szcore_scoring package
This package has been moved to src/seizure_evaluation/szcore/

THIS FILE IS DEPRECATED and will be removed in a future release.
"""

import warnings

warnings.warn(
    "The evaluation.szcore_scoring package has been moved to seizure_evaluation.szcore. "
    "Please update your imports.",
    DeprecationWarning,
    stacklevel=2
)
