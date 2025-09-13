#!/usr/bin/env python3
"""
Experiment tracking utilities for SeizureTransformer evaluation.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def create_experiment_config(
    split: str,
    description: str,
    threshold: float = 0.8,
    kernel: int = 5,
    min_duration_sec: float = 2.0,
    merge_gap_sec: float | None = None,
    target_fa_per_24h: float | None = None,
    notes: str = "",
) -> dict:
    """Create standardized experiment configuration."""
    return {
        "experiment_info": {
            "split": split,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "target_fa_per_24h": target_fa_per_24h,
            "notes": notes,
        },
        "parameters": {
            "threshold": threshold,
            "kernel": kernel,
            "min_duration_sec": min_duration_sec,
            "merge_gap_sec": merge_gap_sec,
        },
        "paths": {
            "data_dir": f"/path/to/TUSZ/v2.0.3/{split}",
            "checkpoint": f"experiments/{split}/{description}/checkpoint.pkl",
            "nedc_results": f"experiments/{split}/{description}/nedc_results/",
        },
    }


def log_experiment_results(
    experiment_dir: Path,
    taes_sensitivity: float,
    taes_fa_per_24h: float,
    taes_f1: float,
    auroc: float,
    total_seizures: int,
    detected_seizures: int,
    notes: str = "",
) -> None:
    """Log experiment results in standardized format."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "metrics": {
            "taes_sensitivity_percent": taes_sensitivity,
            "taes_fa_per_24h": taes_fa_per_24h,
            "taes_f1_score": taes_f1,
            "auroc": auroc,
            "total_seizures": total_seizures,
            "detected_seizures": detected_seizures,
        },
        "clinical_assessment": {
            "clinically_viable": taes_fa_per_24h <= 10,
            "sensitivity_acceptable": taes_sensitivity >= 50,
            "deployment_ready": taes_fa_per_24h <= 10 and taes_sensitivity >= 50,
        },
        "notes": notes,
    }

    results_file = experiment_dir / "summary.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Results logged to: {results_file}")


def compare_experiments(experiments_dir: Path) -> None:
    """Generate comparison table of all experiments."""
    print("Experiment Comparison")
    print("=" * 80)
    print(f"{'Experiment':<20} {'TAES Sens':<10} {'FA/24h':<8} {'F1':<6} {'Clinical':<8}")
    print("-" * 80)

    for exp_dir in experiments_dir.glob("*/"):
        if not exp_dir.is_dir():
            continue

        summary_file = exp_dir / "summary.json"
        if not summary_file.exists():
            continue

        with open(summary_file) as f:
            results = json.load(f)

        metrics = results.get("metrics", {})
        clinical = results.get("clinical_assessment", {})

        sens = metrics.get("taes_sensitivity_percent", 0)
        fa = metrics.get("taes_fa_per_24h", 0)
        f1 = metrics.get("taes_f1_score", 0)
        viable = "✅" if clinical.get("clinically_viable", False) else "❌"

        print(f"{exp_dir.name:<20} {sens:<9.1f}% {fa:<7.1f} {f1:<5.2f} {viable:<8}")


def main():
    parser = argparse.ArgumentParser(description="Experiment tracking utilities")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create config command
    create_parser = subparsers.add_parser("create-config", help="Create experiment config")
    create_parser.add_argument("--split", required=True, choices=["dev", "eval"])
    create_parser.add_argument("--description", required=True)
    create_parser.add_argument("--threshold", type=float, default=0.8)
    create_parser.add_argument("--kernel", type=int, default=5)
    create_parser.add_argument("--min_duration_sec", type=float, default=2.0)
    create_parser.add_argument("--merge_gap_sec", type=float, default=None)
    create_parser.add_argument("--target_fa_per_24h", type=float, default=None)
    create_parser.add_argument("--notes", default="")

    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare experiments")
    compare_parser.add_argument("--split", required=True, choices=["dev", "eval"])

    args = parser.parse_args()

    if args.command == "create-config":
        config = create_experiment_config(
            split=args.split,
            description=args.description,
            threshold=args.threshold,
            kernel=args.kernel,
            min_duration_sec=args.min_duration_sec,
            merge_gap_sec=args.merge_gap_sec,
            target_fa_per_24h=args.target_fa_per_24h,
            notes=args.notes,
        )

        # Create experiment directory
        exp_dir = Path(f"experiments/{args.split}/{args.description}")
        exp_dir.mkdir(parents=True, exist_ok=True)

        # Write config
        config_file = exp_dir / "run_config.json"
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)

        print(f"Experiment config created: {config_file}")

    elif args.command == "compare":
        experiments_dir = Path(f"experiments/{args.split}")
        compare_experiments(experiments_dir)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
