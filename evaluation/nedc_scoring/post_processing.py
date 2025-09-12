#!/usr/bin/env python3
"""
Post-processing for SeizureTransformer predictions.
Applies threshold, morphological operations, and event filtering.
"""

import numpy as np
from scipy.ndimage import binary_opening, binary_closing


def apply_seizure_transformer_postprocessing(
    predictions: np.ndarray, 
    threshold: float = 0.8,
    morph_kernel_size: int = 5,
    min_duration_sec: float = 2.0,
    fs: int = 256
) -> list:
    """
    Apply paper's post-processing pipeline.
    
    Args:
        predictions: Per-sample probabilities at fs Hz
        threshold: Probability threshold (paper uses 0.8)
        morph_kernel_size: Kernel size for morphological ops (paper uses 5)
        min_duration_sec: Minimum event duration in seconds (paper uses 2.0)
        fs: Sampling frequency in Hz
        
    Returns:
        List of (start_sec, end_sec) tuples for seizure events
    """
    # Step 1: Apply threshold
    binary = predictions > threshold
    
    # Step 2: Morphological opening (remove small false positives)
    kernel = np.ones(morph_kernel_size)
    binary = binary_opening(binary, structure=kernel)
    
    # Step 3: Morphological closing (fill small gaps)
    binary = binary_closing(binary, structure=kernel)
    
    # Step 4: Convert binary mask to events
    events = binary_mask_to_events(binary, fs)
    
    # Step 5: Remove events shorter than minimum duration
    min_samples = int(min_duration_sec * fs)
    filtered_events = []
    for start_idx, end_idx in events:
        if (end_idx - start_idx) >= min_samples:
            # Convert samples to seconds
            start_sec = start_idx / fs
            end_sec = end_idx / fs
            filtered_events.append((start_sec, end_sec))
    
    return filtered_events


def binary_mask_to_events(binary_mask: np.ndarray, fs: int = 256) -> list:
    """
    Convert binary mask to list of (start_idx, end_idx) tuples.
    
    Args:
        binary_mask: Binary array (1 = seizure, 0 = background)
        fs: Sampling frequency (for reference, not used in conversion)
        
    Returns:
        List of (start_sample, end_sample) tuples
    """
    # Add padding to handle edge cases
    padded = np.pad(binary_mask, (1, 1), mode='constant', constant_values=0)
    
    # Find edges (transitions)
    diff = np.diff(padded.astype(int))
    starts = np.where(diff == 1)[0]  # 0→1 transitions
    ends = np.where(diff == -1)[0]   # 1→0 transitions
    
    # Pair up starts and ends
    events = []
    for start, end in zip(starts, ends):
        events.append((start, end))
    
    return events


def merge_nearby_events(events: list, gap_sec: float = 1.0) -> list:
    """
    Merge events that are close together.
    
    Args:
        events: List of (start_sec, end_sec) tuples
        gap_sec: Maximum gap in seconds to merge
        
    Returns:
        Merged list of events
    """
    if not events:
        return []
    
    # Sort by start time
    sorted_events = sorted(events)
    merged = [sorted_events[0]]
    
    for start, end in sorted_events[1:]:
        last_start, last_end = merged[-1]
        
        # If gap is small enough, merge
        if start - last_end <= gap_sec:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    
    return merged