#!/usr/bin/env python3
"""
Test that SeizureTransformer inference works with pretrained weights.
This doesn't modify wu_2025 at all - just tests it works.
"""

import os
import sys
import torch
import numpy as np
from pathlib import Path

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
        
        # Check model is in eval mode
        assert not model.training, "Model should be in eval mode"
        print("✅ Model is in eval mode")
        
        # Test with dummy input
        batch_size = 1
        channels = 19
        samples = 15360  # 60 seconds at 256Hz
        
        dummy_input = torch.randn(batch_size, channels, samples).to(device)
        with torch.no_grad():
            output = model(dummy_input)
        
        print(f"✅ Inference successful")
        print(f"   Input shape: {dummy_input.shape}")
        print(f"   Output shape: {output.shape}")
        print(f"   Output range: [{output.min().item():.3f}, {output.max().item():.3f}]")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_preprocessing():
    """Test preprocessing pipeline."""
    from wu_2025.utils import preprocess_clip
    
    # Create dummy EEG data (19 channels, 60 seconds at 256Hz)
    eeg_data = np.random.randn(19, 15360) * 100  # Microvolts
    
    try:
        processed = preprocess_clip(eeg_data)
        print("✅ Preprocessing successful")
        print(f"   Input shape: {eeg_data.shape}")
        print(f"   Output shape: {processed.shape}")
        print(f"   Input range: [{eeg_data.min():.1f}, {eeg_data.max():.1f}] μV")
        print(f"   Output range: [{processed.min():.3f}, {processed.max():.3f}] (normalized)")
        return True
    except Exception as e:
        print(f"❌ Preprocessing error: {e}")
        return False

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