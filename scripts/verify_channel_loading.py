#!/usr/bin/env python3
"""
FINAL VERIFICATION: Does loadEdf actually select the right 19 channels?
"""

import sys
from pathlib import Path
import pyedflib

sys.path.append(str(Path(__file__).parent.parent / "wu_2025/src"))
from epilepsy2bids.eeg import Eeg

def verify_channel_selection():
    """Verify loadEdf selects the correct 19 channels from 33 available."""

    test_file = "data/tusz/edf/eval/aaaaaaaq/s006_2014/01_tcp_ar/aaaaaaaq_s006_t000.edf"

    print("CHANNEL SELECTION VERIFICATION")
    print("=" * 60)

    # Get ALL channels
    with pyedflib.EdfReader(test_file) as f:
        all_channels = f.getSignalLabels()

    print(f"Total channels in file: {len(all_channels)}")

    # Load with loadEdf
    eeg = Eeg.loadEdf(test_file)
    selected_channels = eeg.channels if hasattr(eeg, 'channels') else None

    print(f"\nChannels selected by loadEdf: {len(selected_channels) if selected_channels else 'Unknown'}")

    if selected_channels:
        print("\nMAPPING (File Index -> Selected):")
        for selected in selected_channels:
            idx = all_channels.index(selected) if selected in all_channels else -1
            print(f"  File[{idx:2d}]: {selected}")

    # The critical 19 from the file
    critical_19_indices = [0,2,4,6,8,10,12,14,18,19,20,1,3,5,7,9,11,13,15]
    print(f"\nExpected indices for 19-channel montage: {critical_19_indices}")

    actual_indices = []
    if selected_channels:
        for ch in selected_channels:
            if ch in all_channels:
                actual_indices.append(all_channels.index(ch))

    print(f"Actual indices selected: {actual_indices}")

    if actual_indices == critical_19_indices:
        print("\n✅ PERFECT MATCH! loadEdf selects the right channels!")
    else:
        print("\n❌ MISMATCH! Channel selection may be wrong!")

if __name__ == "__main__":
    verify_channel_selection()