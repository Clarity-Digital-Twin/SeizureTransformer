#!/usr/bin/env python3
"""
CRITICAL INVESTIGATION: What channels does TUSZ actually provide?
This will reveal if we have a channel ordering bug.
"""

import sys
from pathlib import Path
import pyedflib

# Add paths
sys.path.append(str(Path(__file__).parent.parent / "wu_2025/src"))
from epilepsy2bids.eeg import Eeg

def investigate_tusz_channels():
    """Check actual channel names in TUSZ files."""

    # Find a TUSZ file
    tusz_dir = Path("data/tusz/edf/eval")
    if not tusz_dir.exists():
        print(f"ERROR: {tusz_dir} not found!")
        return

    # Get first EDF file
    edf_files = list(tusz_dir.glob("**/*.edf"))
    if not edf_files:
        print("ERROR: No EDF files found!")
        return

    test_file = edf_files[0]
    print(f"Investigating: {test_file}")
    print("=" * 60)

    # Method 1: Raw pyedflib (what channels ACTUALLY exist)
    print("\n1. RAW CHANNELS (via pyedflib):")
    with pyedflib.EdfReader(str(test_file)) as f:
        channel_names = f.getSignalLabels()
        print(f"  Channel count: {len(channel_names)}")
        for i, name in enumerate(channel_names):
            print(f"  [{i:2d}] {name}")

    # Method 2: Via loadEdf (what our evaluation uses)
    print("\n2. LOADED VIA loadEdf (our evaluation method):")
    try:
        eeg = Eeg.loadEdf(str(test_file))
        print(f"  Data shape: {eeg.data.shape}")
        print(f"  Montage: {eeg.montage}")
        if hasattr(eeg, 'channels'):
            print(f"  Channels: {eeg.channels}")
    except Exception as e:
        print(f"  ERROR: {e}")

    # Method 3: Via loadEdfAutoDetectMontage (Wu's method - will fail)
    print("\n3. VIA loadEdfAutoDetectMontage (Wu's CLI method):")
    try:
        eeg = Eeg.loadEdfAutoDetectMontage(str(test_file))
        print(f"  SUCCESS - Data shape: {eeg.data.shape}")
    except Exception as e:
        print(f"  EXPECTED FAILURE: {e}")

    # Expected by Wu's model
    print("\n4. WU'S EXPECTED CHANNEL ORDER:")
    wu_channels = ["Fp1", "F3", "C3", "P3", "O1", "F7", "T3", "T5",
                   "Fz", "Cz", "Pz", "Fp2", "F4", "C4", "P4", "O2",
                   "F8", "T4", "T6"]
    for i, name in enumerate(wu_channels):
        print(f"  [{i:2d}] {name}")

    print("\n" + "=" * 60)
    print("⚠️  CRITICAL QUESTION: Do the channel orders match?")
    print("If not, the model is seeing SCRAMBLED brain signals!")

if __name__ == "__main__":
    investigate_tusz_channels()