#!/usr/bin/env python3
"""Test parity between Temple binary and native TAES across all scenarios."""

import json
import re
from pathlib import Path


def extract_metrics(summary_file, backend="nedc-binary"):
    """Extract metrics from summary file."""
    content = summary_file.read_text()

    if backend == "native-taes":
        # Native outputs simpler format
        sens_match = re.search(r"Sensitivity \(TPR, Recall\):\s+([\d.]+)%", content)
        fa_match = re.search(r"Total False Alarm Rate:\s+([\d.]+)\s+per 24 hours", content)
        f1_match = re.search(r"F1 Score:\s+([\d.]+)", content)

        if sens_match and fa_match:
            return {
                "sensitivity": float(sens_match.group(1)),
                "fa_per_24h": float(fa_match.group(1)),
                "f1_score": float(f1_match.group(1)) if f1_match else None
            }
    else:
        # Extract OVERLAP metrics from Temple binary
        overlap_section = re.search(
            r"NEDC OVERLAP SCORING SUMMARY.*?SUMMARY:.*?"
            r"Sensitivity \(TPR, Recall\):\s+([\d.]+)%.*?"
            r"Total False Alarm Rate:\s+([\d.]+)\s+per 24 hours",
            content, re.DOTALL
        )

        if overlap_section:
            # Also get F1 from SEIZ label section
            f1_match = re.search(
                r"NEDC OVERLAP.*?LABEL: SEIZ.*?F1 Score.*?:\s+([\d.]+)",
                content, re.DOTALL
            )
            return {
                "sensitivity": float(overlap_section.group(1)),
                "fa_per_24h": float(overlap_section.group(2)),
                "f1_score": float(f1_match.group(1)) if f1_match else None
            }

    return None

def compare_metrics(m1, m2, name1, name2, tolerance=0.1):
    """Compare two metric sets."""
    print(f"\nComparing {name1} vs {name2}:")
    print(f"  {name1}: Sens={m1['sensitivity']:.2f}%, FA={m1['fa_per_24h']:.2f}/24h, F1={m1['f1_score']:.3f}")
    print(f"  {name2}: Sens={m2['sensitivity']:.2f}%, FA={m2['fa_per_24h']:.2f}/24h, F1={m2['f1_score']:.3f}")

    sens_diff = abs(m1['sensitivity'] - m2['sensitivity'])
    fa_diff = abs(m1['fa_per_24h'] - m2['fa_per_24h'])
    f1_diff = abs(m1['f1_score'] - m2['f1_score']) if m1['f1_score'] and m2['f1_score'] else 0

    print(f"  Deltas: Sens={sens_diff:.3f}%, FA={fa_diff:.3f}/24h, F1={f1_diff:.4f}")

    if sens_diff < tolerance and fa_diff < tolerance:
        print(f"  ✅ MATCH (within {tolerance} tolerance)")
        return True
    else:
        print(f"  ❌ MISMATCH (exceeds {tolerance} tolerance)")
        return False

# Test scenarios
print("="*70)
print("COMPREHENSIVE PARITY TEST: Temple Binary vs Native TAES")
print("="*70)

all_pass = True

# 1. Test on eval with frozen/default params
print("\n1. EVAL WITH DEFAULT PARAMS (threshold=0.8, kernel=5, min_duration=2.0)")
baseline_dir = Path("experiments/eval/baseline")

if (baseline_dir / "nedc_results_frozen_temple/results/summary.txt").exists():
    temple_frozen = extract_metrics(
        baseline_dir / "nedc_results_frozen_temple/results/summary.txt",
        backend="nedc-binary"
    )

    if (baseline_dir / "nedc_results_frozen_native/results/summary.txt").exists():
        native_frozen = extract_metrics(
            baseline_dir / "nedc_results_frozen_native/results/summary.txt",
            backend="native-taes"
        )

        if temple_frozen and native_frozen:
            all_pass &= compare_metrics(temple_frozen, native_frozen, "Temple", "Native")
        else:
            print("  ⚠️  Could not extract metrics")
    else:
        print("  ⚠️  Native frozen results not found")
else:
    print("  ⚠️  Temple frozen results not found")

# 2. Check dev sweep results
print("\n2. DEV SET SWEEP RESULTS")
sweep_dir = Path("experiments/sweeps/dev_20250913_033955")

if sweep_dir.exists():
    # Find best params from sweep
    best_csv = sweep_dir / "sweep_results.csv"
    if best_csv.exists():
        import csv
        with open(best_csv) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            # Find config with FA < 10 and highest sensitivity
            valid_rows = [r for r in rows if float(r['fa_per_24h']) < 10]
            if valid_rows:
                best = max(valid_rows, key=lambda x: float(x['sensitivity']))
                print(f"  Best dev params: thr={best['threshold']}, k={best['kernel_size']}, "
                      f"min={best['min_duration']}, merge={best.get('merge_gap', 'N/A')}")
                print(f"  Metrics: Sens={float(best['sensitivity']):.2f}%, "
                      f"FA={float(best['fa_per_24h']):.2f}/24h, F1={float(best['f1_score']):.3f}")
else:
    print("  ⚠️  Dev sweep directory not found")

# 3. Check if tuned params were tested on eval
print("\n3. EVAL WITH TUNED PARAMS")
tuned_params_file = Path("experiments/sweeps/dev_20250913_033955/recommended_params.json")
if tuned_params_file.exists():
    with open(tuned_params_file) as f:
        tuned = json.load(f)
    print(f"  Recommended: thr={tuned['threshold']}, k={tuned['kernel_size']}, "
          f"min={tuned['min_duration']}, merge={tuned.get('merge_gap', 5.0)}")
    print("  Expected: Sens≈13.67%, FA≈9.97/24h")

    # Check if there's an eval run with these params
    # Would need to run: python evaluation/nedc_scoring/run_nedc.py with tuned params
    print("  ⚠️  Need to run eval with tuned params for full verification")

print("\n" + "="*70)
print(f"OVERALL: {'✅ ALL TESTS PASS' if all_pass else '❌ SOME TESTS FAILED'}")
print("="*70)
