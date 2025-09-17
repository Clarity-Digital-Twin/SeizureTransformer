#!/usr/bin/env python3
"""Wrapper CLI for running NEDC scoring pipeline.

Delegates to `evaluation.nedc_eeg_eval.nedc_scoring.run_nedc:main` in the
vendored tools tree. This is intended for in-repo or editable installs where
the `evaluation/` directory is available at runtime.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_repo_root_on_path() -> None:
    """Add repository root to sys.path if running from a checkout.

    This allows importing `evaluation.*` modules that are not packaged.
    """
    # Try common layouts: site-packages → src → repo-root
    here = Path(__file__).resolve()
    # src/seizure_evaluation/nedc/cli.py → repo root is parents[3]
    # 0: nedc, 1: seizure_evaluation, 2: src, 3: repo-root
    try:
        repo_root = here.parents[3]
        if (repo_root / "evaluation").exists():
            p = str(repo_root)
            if p not in sys.path:
                sys.path.insert(0, p)
    except IndexError:
        # Installed into a path without the repo structure; ignore
        pass


def main() -> int:
    _ensure_repo_root_on_path()
    try:
        from evaluation.nedc_eeg_eval.nedc_scoring.run_nedc import main as nedc_main
    except Exception as e:
        msg = (
            "nedc-run requires the vendored NEDC tools directory 'evaluation/nedc_eeg_eval'\n"
            "to be present (e.g., running from a repository checkout or editable install).\n"
            f"Import error: {e}"
        )
        print(msg)
        return 1
    return int(nedc_main())


if __name__ == "__main__":
    raise SystemExit(main())

