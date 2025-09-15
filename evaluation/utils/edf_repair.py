"""
Utilities for handling malformed EDF files during evaluation.

Scope and constraints (per AGENTS.md):
- We do not modify third-party code (`wu_2025/`, `epilepsy2bids`, or NEDC tools).
- We add non-invasive helpers here and call them from our evaluation scripts.

Primary goal:
- Gracefully handle the known TUSZ eval file with malformed EDF startdate bytes
  (byte offsets 168–176 contain `01:01:85` instead of `01.01.85`).

Functions:
- validate_edf_header: returns parsed date/time fields and compliance flags.
- repair_edf_header_copy: creates a repaired copy by replacing common separators.
- load_with_fallback: tries standard loader, then repair+reload, then optional MNE.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import shutil
from typing import Optional, Tuple

import numpy as np


DATE_OFFSET = 168  # EDF header startdate bytes [168:176]
TIME_OFFSET = 176  # EDF header starttime bytes [176:184]
FIELD_LEN = 8


@dataclass
class HeaderValidation:
    date_bytes: bytes
    time_bytes: bytes
    date_str: str
    time_str: str
    date_ok: bool
    time_ok: bool


_DATE_PAT = re.compile(r"^\d{2}\.\d{2}\.\d{2}$")  # DD.MM.YY
_TIME_PAT = re.compile(r"^\d{2}\.\d{2}\.\d{2}$")  # HH.MM.SS


def _read_header_fields(edf_path: Path) -> Tuple[bytes, bytes]:
    with open(edf_path, "rb") as f:
        f.seek(DATE_OFFSET)
        date_bytes = f.read(FIELD_LEN)
        f.seek(TIME_OFFSET)
        time_bytes = f.read(FIELD_LEN)
    return date_bytes, time_bytes


def validate_edf_header(edf_path: Path) -> HeaderValidation:
    date_b, time_b = _read_header_fields(edf_path)
    date_s = date_b.decode("ascii", errors="ignore")
    time_s = time_b.decode("ascii", errors="ignore")
    return HeaderValidation(
        date_bytes=date_b,
        time_bytes=time_b,
        date_str=date_s,
        time_str=time_s,
        date_ok=bool(_DATE_PAT.match(date_s)),
        time_ok=bool(_TIME_PAT.match(time_s)),
    )


def repair_edf_header_copy(edf_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Create a repaired copy of EDF header where common separator mistakes are fixed.

    - Replaces ':', '/', '-' with '.' in date/time fields.
    - Only modifies bytes [168:176] and [176:184].
    - Leaves the original file intact; returns path to the repaired copy.
    """
    edf_path = Path(edf_path)
    if output_path is None:
        output_path = edf_path.with_name(edf_path.stem + "_repaired.edf")

    shutil.copy2(edf_path, output_path)

    with open(output_path, "r+b") as f:
        # Date field
        f.seek(DATE_OFFSET)
        date_b = f.read(FIELD_LEN)
        date_s = date_b.decode("ascii", errors="ignore")
        fixed_date = (
            date_s.replace(":", ".").replace("/", ".").replace("-", ".")
        )[:FIELD_LEN].ljust(FIELD_LEN)
        f.seek(DATE_OFFSET)
        f.write(fixed_date.encode("ascii"))

        # Time field
        f.seek(TIME_OFFSET)
        time_b = f.read(FIELD_LEN)
        time_s = time_b.decode("ascii", errors="ignore")
        fixed_time = (
            time_s.replace(":", ".").replace("/", ".").replace("-", ".")
        )[:FIELD_LEN].ljust(FIELD_LEN)
        f.seek(TIME_OFFSET)
        f.write(fixed_time.encode("ascii"))

    return output_path


def load_with_fallback(edf_path: Path):
    """
    Try to load EDF using epilepsy2bids.Eeg.loadEdf first.
    If it fails due to known header issues, attempt repair+reload; finally optional MNE.

    Returns (eeg, method_str) or raises the last exception.
    """
    from epilepsy2bids.eeg import Eeg

    try:
        eeg = Eeg.loadEdf(str(edf_path))
        return eeg, "pyedflib"
    except Exception as e1:  # noqa: BLE001
        msg = str(e1)
        header_issue = (
            ("startdate" in msg) or ("not EDF" in msg) or ("not EDF(+)" in msg) or ("BDF" in msg)
        )

        # Strategy 2: Header repair + reload
        if header_issue:
            try:
                repaired = repair_edf_header_copy(Path(edf_path))
                try:
                    eeg = Eeg.loadEdf(str(repaired))
                    return eeg, "pyedflib+repaired"
                finally:
                    # Best-effort cleanup; ignore errors
                    try:
                        Path(repaired).unlink(missing_ok=True)
                    except Exception:
                        pass
            except Exception as e2:  # noqa: BLE001
                last = e2
        else:
            last = e1

        # Strategy 3: optional MNE fallback (if installed)
        try:
            import mne  # type: ignore

            raw = mne.io.read_raw_edf(str(edf_path), preload=True, verbose=False)
            # Convert MNE Raw to a minimal Eeg-like object used by our pipeline.
            # We mimic the attributes accessed in evaluation: .data and .fs
            data = raw.get_data()  # shape: (n_channels, n_samples)
            class _EegAdapter:
                def __init__(self, data: np.ndarray, sfreq: float):
                    self.data = data.astype(np.float32, copy=False)
                    self.fs = float(sfreq)

            return _EegAdapter(data, float(raw.info["sfreq"])), "mne"
        except Exception as e3:  # noqa: BLE001
            raise RuntimeError(
                f"All strategies failed: primary={e1}; repaired={last if 'last' in locals() else None}; mne={e3}"
            )

