#!/usr/bin/env python3
"""Generate optimized Figure 1: The Performance Gap Visualization"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add parent directory to path for config import
sys.path.append(str(Path(__file__).parent))
from config import *

def generate_fig1_optimized():
    """Generate publication-quality Figure 1 with all optimizations"""

    # Load data
    data = pd.read_csv('../data/performance_metrics.csv')

    # Create figure with golden ratio
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(DOUBLE_COL, HEIGHT_DEFAULT),
                                   dpi=DPI_ARXIV)

    # ============ Panel A: False Alarm Rates ============
    methods = data['method'].str.replace(' ', '\n', regex=False)
    fa_rates = data['fa_per_24h']
    colors = data['color_hex']
    multipliers = data['multiplier']
    fa_std = data['fa_std'].fillna(0)  # Fill NaN with 0 for Dianalund

    # Create bars with error bars
    bars = ax1.bar(range(len(methods)), fa_rates,
                   color=colors,
                   alpha=ALPHA['bar'],
                   edgecolor='black',
                   linewidth=LINE_WIDTH['box'],
                   yerr=fa_std,
                   capsize=4,
                   error_kw={'linewidth': LINE_WIDTH['reference'],
                            'ecolor': COLORS['annotation']})

    # Set log scale and limits
    ax1.set_yscale('log')
    ax1.set_ylim(0.5, 200)

    # Add clinical threshold line
    ax1.axhline(y=CLINICAL_THRESHOLDS['fa_per_24h'],
               color=COLORS['threshold'],
               linestyle='--',
               linewidth=LINE_WIDTH['reference'],
               label=f"Clinical threshold ({CLINICAL_THRESHOLDS['fa_per_24h']} FA/24h)",
               zorder=0)

    # Enhanced multiplier annotations with background boxes
    for i, (fa, mult, std) in enumerate(zip(fa_rates, multipliers, fa_std)):
        y_pos = fa + std if std > 0 else fa  # Position above error bar
        ax1.annotate(mult,
                    xy=(i, y_pos),
                    xytext=(0, 8),
                    textcoords='offset points',
                    ha='center',
                    fontsize=FONT_SIZE['annotation'] + 1,
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3',
                             facecolor='white',
                             alpha=ALPHA['annotation_bg'],
                             edgecolor='none'))

    # Styling
    ax1.set_xticks(range(len(methods)))
    ax1.set_xticklabels(methods, fontsize=FONT_SIZE['tick'])
    setup_axes(ax1,
              title='A. False Alarm Rates Across Evaluation Methods',
              ylabel='False Alarms per 24 Hours (log scale)',
              grid=True)

    # Legend with better positioning
    ax1.legend(loc='upper left', fontsize=FONT_SIZE['legend'],
              framealpha=0.95, edgecolor='none')

    # Add panel label
    add_panel_label(ax1, 'A')

    # ============ Panel B: Sensitivity at 10 FA/24h ============
    scorers = ['NEDC\nOVERLAP', 'NEDC\nTAES', 'SzCORE']
    sensitivities = data['sensitivity_at_10fa'].dropna().tolist()  # Get all non-NaN values
    sens_std = data['sens_std'].dropna().tolist()  # Get all non-NaN values
    colors_b = [COLORS['nedc_overlap'], COLORS['nedc_taes'], COLORS['szcore']]

    # Create bars with error bars
    bars2 = ax2.bar(range(len(scorers)), sensitivities,
                   color=colors_b,
                   alpha=ALPHA['bar'],
                   edgecolor='black',
                   linewidth=LINE_WIDTH['box'],
                   yerr=sens_std,
                   capsize=4,
                   error_kw={'linewidth': LINE_WIDTH['reference'],
                            'ecolor': COLORS['annotation']})

    # Add clinical goal line
    ax2.axhline(y=CLINICAL_THRESHOLDS['sensitivity'],
               color='green',
               linestyle='--',
               linewidth=LINE_WIDTH['reference'],
               label=f"Clinical goal ({CLINICAL_THRESHOLDS['sensitivity']}%)",
               zorder=0)

    # Add 50% reference line
    ax2.axhline(y=50,
               color=COLORS['threshold'],
               linestyle=':',
               alpha=0.4,
               linewidth=LINE_WIDTH['grid'])

    # Value annotations with percentage signs
    for i, (bar, sens, std) in enumerate(zip(bars2, sensitivities, sens_std)):
        y_pos = sens + std
        ax2.annotate(f'{sens:.1f}%',
                    xy=(i, y_pos),
                    xytext=(0, 3),
                    textcoords='offset points',
                    ha='center',
                    fontsize=FONT_SIZE['annotation'],
                    fontweight='normal')

    # Styling
    ax2.set_ylim(0, 100)
    ax2.set_xticks(range(len(scorers)))
    ax2.set_xticklabels(scorers, fontsize=FONT_SIZE['tick'])
    setup_axes(ax2,
              title='B. Sensitivity at 10 FA/24h Threshold',
              ylabel='Sensitivity (%)',
              grid=True)

    # Legend
    ax2.legend(loc='upper right', fontsize=FONT_SIZE['legend'],
              framealpha=0.95, edgecolor='none')

    # Add panel label
    add_panel_label(ax2, 'B')

    # ============ Overall Figure Title ============
    plt.suptitle('Figure 1: The Gap Between Benchmark Claims and Clinical Reality',
                fontsize=FONT_SIZE['title'] + 1,
                fontweight='bold',
                y=1.02)

    # Adjust layout
    plt.tight_layout()

    # Save in multiple formats
    output_dir = Path('../output/arxiv')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save with metadata
    for fmt in ['pdf', 'png']:
        filename = output_dir / f'fig1_performance_gap_optimized.{fmt}'
        plt.savefig(filename,
                   dpi=DPI_ARXIV if fmt == 'pdf' else DPI_WEB,
                   metadata=METADATA if fmt == 'pdf' else None,
                   **EXPORT_SETTINGS)
        print(f"✓ Saved: {filename}")

    # Also save web version
    web_dir = Path('../output/web')
    web_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(web_dir / 'fig1_performance_gap.png',
               dpi=DPI_SCREEN,
               **EXPORT_SETTINGS)

    plt.close()
    print("✓ Figure 1 optimized generation complete")

if __name__ == "__main__":
    generate_fig1_optimized()