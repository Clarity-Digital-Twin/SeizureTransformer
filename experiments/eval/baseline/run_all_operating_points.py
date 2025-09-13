#!/usr/bin/env python3
"""Run comprehensive operating point tests with both Temple and Native backends."""

import json
import subprocess
from pathlib import Path

# Operating points to test
OPERATING_POINTS = {
    "default": {
        "desc": "Default (non-tuned)",
        "threshold": 0.8,
        "kernel": 5,
        "min_duration_sec": 2.0,
        "merge_gap_sec": 5.0,
    },
    "10fa": {
        "desc": "10 FA/24h target",
        "threshold": 0.8,
        "kernel": 5,
        "min_duration_sec": 2.0,
        "merge_gap_sec": 5.0,
    },
    "2.5fa": {
        "desc": "2.5 FA/24h target",
        "threshold": 0.95,
        "kernel": 11,
        "min_duration_sec": 8.0,
        "merge_gap_sec": 10.0,
    },
    "1fa": {
        "desc": "1 FA/24h target",
        "threshold": 0.99,
        "kernel": 21,
        "min_duration_sec": 16.0,
        "merge_gap_sec": 10.0,
    },
}

BACKENDS = ["nedc-binary", "native-taes"]
SPLITS = ["dev", "eval"]

def run_test(split, op_name, op_params, backend):
    """Run a single test configuration."""
    checkpoint = f"experiments/{split}/baseline/checkpoint.pkl"
    outdir = f"experiments/{split}/baseline/results_{op_name}_{backend.replace('-', '_')}"

    cmd = [
        "python", "evaluation/nedc_scoring/run_nedc.py",
        "--checkpoint", checkpoint,
        "--outdir", outdir,
        "--threshold", str(op_params["threshold"]),
        "--kernel", str(op_params["kernel"]),
        "--min_duration_sec", str(op_params["min_duration_sec"]),
        "--merge_gap_sec", str(op_params["merge_gap_sec"]),
        "--backend", backend,
        "--force"
    ]

    print(f"\n{'='*70}")
    print(f"Running: {split.upper()} - {op_params['desc']} - {backend}")
    print(f"{'='*70}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        # Extract metrics from output
        metrics_file = Path(outdir) / "results" / "metrics.json"
        if metrics_file.exists():
            with open(metrics_file) as f:
                metrics = json.load(f)
                taes = metrics.get("taes", {})
                return {
                    "sensitivity": taes.get("sensitivity_percent", "N/A"),
                    "fa_per_24h": taes.get("fa_per_24h", "N/A"),
                    "f1_score": taes.get("f1_score", "N/A"),
                }
        else:
            print(f"ERROR: No metrics file found at {metrics_file}")
            return None

    except subprocess.TimeoutExpired:
        print(f"ERROR: Timeout for {split} - {op_name} - {backend}")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def main():
    """Run all tests and create results table."""
    results = {}

    # Run all tests
    for split in SPLITS:
        results[split] = {}
        for op_name, op_params in OPERATING_POINTS.items():
            results[split][op_name] = {}
            for backend in BACKENDS:
                metrics = run_test(split, op_name, op_params, backend)
                results[split][op_name][backend] = metrics

    # Generate markdown table
    print("\n\n" + "="*100)
    print("COMPREHENSIVE SEIZURETRANSFORMER OPERATING POINTS RESULTS")
    print("="*100)

    # Table header
    print("\n| Operating Point | Split | Temple Binary | Native TAES | Parity |")
    print("|-----------------|-------|---------------|-------------|--------|")

    for op_name, op_params in OPERATING_POINTS.items():
        print(f"\n**{op_params['desc']}** (thr={op_params['threshold']}, k={op_params['kernel']}, min={op_params['min_duration_sec']}s)")

        for split in SPLITS:
            temple = results[split][op_name].get("nedc-binary", {})
            native = results[split][op_name].get("native-taes", {})

            if temple and native:
                temple_str = f"{temple['sensitivity']:.2f}% @ {temple['fa_per_24h']:.2f}/24h"
                native_str = f"{native['sensitivity']:.2f}% @ {native['fa_per_24h']:.2f}/24h"

                # Check parity
                sens_diff = abs(temple['sensitivity'] - native['sensitivity'])
                fa_diff = abs(temple['fa_per_24h'] - native['fa_per_24h'])
                parity = "✅" if sens_diff < 0.1 and fa_diff < 0.1 else "❌"
            else:
                temple_str = "ERROR"
                native_str = "ERROR"
                parity = "❓"

            print(f"| {op_params['desc']:<15} | {split:<5} | {temple_str:<13} | {native_str:<11} | {parity:<6} |")

    # Save results to JSON
    with open("experiments/eval/baseline/all_operating_points.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n✅ Results saved to experiments/eval/baseline/all_operating_points.json")

if __name__ == "__main__":
    main()
