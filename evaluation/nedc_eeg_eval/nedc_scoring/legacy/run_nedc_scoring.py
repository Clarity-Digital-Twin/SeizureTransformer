#!/usr/bin/env python3
"""
Legacy module preserved for backward-compat imports.

Moved to: evaluation/nedc_eeg_eval/nedc_scoring/legacy/run_nedc_scoring.py
Preferred entrypoint: evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py
"""

import warnings

warnings.warn(
    "run_nedc_scoring.py is deprecated. Use run_nedc.py instead.",
    DeprecationWarning,
)
