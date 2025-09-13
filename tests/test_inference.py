#!/usr/bin/env python3
"""
Test that SeizureTransformer inference works with pretrained weights.
This doesn't modify wu_2025 at all - just tests it works.
"""

import sys
from pathlib import Path

import numpy as np
import torch


# Test model loading
def test_model_loads():
    """Test that model and weights load correctly."""
    from wu_2025.utils import load_models

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Testing on device: {device}")

    try:
        model = load_models(device)
        print("✅ Model loaded successfully")
        print(f"   Model type: {type(model).__name__}")

        # They set eval mode in predict(), not load_models()
        model.eval()
        print("✅ Model set to eval mode")

        # Test with dummy input
        batch_size = 1
        channels = 19
        samples = 15360  # 60 seconds at 256Hz

        dummy_input = torch.randn(batch_size, channels, samples).to(device)
        with torch.no_grad():
            output = model(dummy_input)

        print("✅ Inference successful")
        print(f"   Input shape: {dummy_input.shape}")
        print(f"   Output shape: {output.shape}")
        print(f"   Output range: [{output.min().item():.3f}, {output.max().item():.3f}]")

        assert True

    except Exception as e:
        print(f"❌ Error: {e}")
        assert False

def test_preprocessing():
    """Test preprocessing pipeline via dataloader."""
    from wu_2025.utils import get_dataloader

    # Create dummy EEG data (19 channels, 1 minute at 256Hz)
    eeg_data = np.random.randn(19, 15360) * 100  # Microvolts

    try:
        # Preprocessing happens inside get_dataloader
        dataloader = get_dataloader(eeg_data, fs=256, batch_size=1)

        # Get first batch
        for batch in dataloader:
            print("✅ Preprocessing successful")
            print(f"   Input shape: {eeg_data.shape}")
            print(f"   Batch shape: {batch.shape}")
            print(f"   Input range: [{eeg_data.min():.1f}, {eeg_data.max():.1f}]")
            print(f"   Output range: [{batch.min():.3f}, {batch.max():.3f}] (preprocessed)")
            break
        assert True
    except Exception as e:
        print(f"❌ Preprocessing error: {e}")
        assert False

def check_weights():
    """Check if model weights exist."""
    weight_path = Path("wu_2025/src/wu_2025/model.pth")
    if weight_path.exists():
        size_mb = weight_path.stat().st_size / (1024 * 1024)
        print(f"✅ Model weights found: {weight_path}")
        print(f"   Size: {size_mb:.1f} MB")
        return True
    else:
        print(f"❌ Model weights not found at {weight_path}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("SeizureTransformer Inference Test")
    print("=" * 60)

    # Check weights exist
    print("\n1. Checking model weights...")
    weights_ok = check_weights()

    # Test preprocessing
    print("\n2. Testing preprocessing pipeline...")
    preprocess_ok = test_preprocessing()

    # Test model loading and inference
    print("\n3. Testing model loading and inference...")
    model_ok = test_model_loads()

    # Summary
    print("\n" + "=" * 60)
    if all([weights_ok, preprocess_ok, model_ok]):
        print("✅ ALL TESTS PASSED - Ready for evaluation!")
    else:
        print("❌ Some tests failed - check errors above")
        sys.exit(1)
