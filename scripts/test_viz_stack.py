#!/usr/bin/env python3
"""Test visualization stack - generate sample of Figure 1: The Gap Visualization"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotext as pltxt
from rich.console import Console
from rich.table import Table
import scienceplots

# Test data from our paper
methods = ['Dianalund\n(Claimed)', 'TUSZ\nNEDC OVERLAP', 'TUSZ\nNEDC TAES', 'TUSZ\nSzCORE']
fa_rates = [1.0, 26.89, 136.73, 8.59]
multipliers = ['1×', '27×', '137×', '8.6×']

# Color scheme
colors = ['#6A994E', '#2E86AB', '#C73E1D', '#F18F01']  # Green, Blue, Red, Orange

def terminal_viz():
    """Quick terminal visualization using plotext"""
    print("\n=== Terminal Visualization ===")
    pltxt.theme('dark')
    pltxt.bar(methods, fa_rates, orientation='vertical', width=0.3)
    pltxt.title("False Alarms per 24 Hours: The 27-137× Gap")
    pltxt.ylabel("FA/24h")
    pltxt.ylim(0, 150)
    pltxt.show()

def rich_table():
    """Pretty table using rich"""
    console = Console()
    table = Table(title="Performance Gap Analysis", show_header=True, header_style="bold magenta")
    table.add_column("Method", style="cyan", no_wrap=True)
    table.add_column("FA/24h", justify="right", style="yellow")
    table.add_column("Multiplier", justify="right", style="red")
    table.add_column("Clinical Viable?", justify="center")

    for method, fa, mult in zip(methods, fa_rates, multipliers):
        viable = "✓" if fa < 10 else "✗"
        style = "green" if fa < 10 else "red"
        table.add_row(method.replace('\n', ' '), f"{fa:.2f}", mult, f"[{style}]{viable}[/{style}]")

    console.print(table)

def publication_figure():
    """Publication-quality figure using matplotlib + scienceplots"""
    plt.style.use(['science', 'nature'])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=150)

    # Panel A: Bar chart with log scale
    bars = ax1.bar(range(len(methods)), fa_rates, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_yscale('log')
    ax1.set_ylabel('False Alarms per 24 Hours (log scale)', fontsize=11)
    ax1.set_xticks(range(len(methods)))
    ax1.set_xticklabels(methods, fontsize=10)
    ax1.axhline(y=10, color='gray', linestyle='--', alpha=0.5, label='Clinical threshold')
    ax1.grid(True, alpha=0.3, axis='y')

    # Add multiplier annotations
    for bar, mult, fa in zip(bars, multipliers, fa_rates):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                f'{mult}\n({fa:.1f})', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax1.set_title('A. The 27-137× Performance Gap', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right')

    # Panel B: Sensitivity at 10 FA/24h threshold
    scorers = ['NEDC OVERLAP', 'NEDC TAES', 'SzCORE']
    sensitivities = [33.90, 60.45, 40.59]  # At 10 FA/24h

    bars2 = ax2.bar(range(len(scorers)), sensitivities, color=colors[1:], alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.axhline(y=75, color='green', linestyle='--', alpha=0.5, label='Clinical goal (75%)')
    ax2.set_ylabel('Sensitivity (%)', fontsize=11)
    ax2.set_ylim(0, 100)
    ax2.set_xticks(range(len(scorers)))
    ax2.set_xticklabels(scorers, fontsize=10, rotation=15, ha='right')
    ax2.grid(True, alpha=0.3, axis='y')

    # Add value annotations
    for bar, sens in zip(bars2, sensitivities):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{sens:.1f}%', ha='center', va='bottom', fontsize=9)

    ax2.set_title('B. Sensitivity at 10 FA/24h Threshold', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper right')

    plt.suptitle('SeizureTransformer: Gap Between Benchmark Claims and Clinical Reality',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()

    # Save in multiple formats
    for fmt in ['pdf', 'png', 'svg']:
        filename = f'figures/test_gap_visualization.{fmt}'
        plt.savefig(filename, dpi=300 if fmt=='png' else None, bbox_inches='tight')
        print(f"Saved: {filename}")

    plt.show()

if __name__ == "__main__":
    print("Testing visualization stack for SeizureTransformer paper...")

    # Terminal visualizations
    terminal_viz()
    rich_table()

    # Create figures directory
    import os
    os.makedirs('figures', exist_ok=True)

    # Publication quality figure
    print("\n=== Generating publication-quality figure ===")
    publication_figure()

    print("\n✓ Visualization stack test complete!")
    print("Tools tested: plotext, rich, matplotlib, scienceplots")
    print("Next step: Implement full figure generation pipeline")