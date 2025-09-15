#!/usr/bin/env python3
"""Quick test for EDF header repair/fallback on the known problematic file.

Run:
  python scripts/test_edf_repair.py 
"""

from __future__ import annotations

from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from evaluation.utils.edf_repair import (  # noqa: E402
    load_with_fallback,
    validate_edf_header,
    repair_edf_header_copy,
)


def main():
    problem = Path(
        "data/tusz/edf/eval/aaaaaaaq/s007_2014/01_tcp_ar/aaaaaaaq_s007_t000.edf"
    )
    print(f"Testing: {problem}")
    if not problem.exists():
        print("File not found; nothing to test.")
        return

    hv = validate_edf_header(problem)
    print("Before:")
    print("  date:", hv.date_bytes, hv.date_str, "OK=" + str(hv.date_ok))
    print("  time:", hv.time_bytes, hv.time_str, "OK=" + str(hv.time_ok))

    # Try fallback loader
    try:
        eeg, method = load_with_fallback(problem)
        print(f"SUCCESS: loaded via {method}")
        print(f"  data shape: {eeg.data.shape}, fs: {eeg.fs}")
        return
    except Exception as e:
        print("Fallback failed:", e)

    # Try explicit repair copy + basic load (diagnostic)
    try:
        repaired = repair_edf_header_copy(problem)
        print("Repaired copy at:", repaired)
        hv2 = validate_edf_header(repaired)
        print("After repair:")
        print("  date:", hv2.date_bytes, hv2.date_str, "OK=" + str(hv2.date_ok))
        print("  time:", hv2.time_bytes, hv2.time_str, "OK=" + str(hv2.time_ok))
    finally:
        try:
            Path(repaired).unlink(missing_ok=True)
        except Exception:
            pass


if __name__ == "__main__":
    main()
