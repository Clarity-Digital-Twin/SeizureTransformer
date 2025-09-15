#!/usr/bin/env python3
"""Compatibility shim: taes is deprecated; use seizure_evaluation.ovlp instead."""

import warnings

from seizure_evaluation.ovlp import overlap_scorer as _ovlp

# Re-export for backward compatibility
Event = _ovlp.Event
OverlapMetrics = _ovlp.OverlapMetrics
OverlapScorer = _ovlp.OverlapScorer
__all__ = ["Event", "OverlapMetrics", "OverlapScorer"]

warnings.warn(
    "seizure_evaluation.taes is deprecated; use seizure_evaluation.ovlp instead",
    DeprecationWarning,
    stacklevel=2,
)
