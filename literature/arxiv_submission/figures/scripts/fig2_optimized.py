#!/usr/bin/env python3
"""Generate optimized Figure 2: Operating Characteristic Curves"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add parent directory to path for config import
sys.path.append(str(Path(__file__).parent))
from config import *

def generate_fig2_optimized():
    """Generate publication-quality Figure 2 with precise control"""

    # Load the actual operating curves data
    data = pd.read_csv('../data/operating_curves.csv')

    # Create figure
    fig, ax = plt.subplots(figsize=(DOUBLE_COL, HEIGHT_DEFAULT), dpi=DPI_ARXIV)

    # Separate data by scorer
    nedc_overlap = data[data['scorer'] == 'NEDC OVERLAP'].copy()
    nedc_taes = data[data['scorer'] == 'NEDC TAES'].copy()
    szcore = data[data['scorer'] == 'SzCORE Event'].copy()

    # Sort by FA rate for smooth curves
    nedc_overlap = nedc_overlap.sort_values('fa_per_24h')
    nedc_taes = nedc_taes.sort_values('fa_per_24h')
    szcore = szcore.sort_values('fa_per_24h')

    # Plot NEDC OVERLAP
    ax.semilogx(nedc_overlap['fa_per_24h'], nedc_overlap['sensitivity'], 'o-',
                color=COLORS['nedc_overlap'],
                linewidth=2.5,
                markersize=7,
                label='NEDC OVERLAP',
                alpha=0.9,
                markeredgecolor='black',
                markeredgewidth=0.5,
                zorder=8)

    # Plot NEDC TAES
    ax.semilogx(nedc_taes['fa_per_24h'], nedc_taes['sensitivity'], 's-',
                color=COLORS['nedc_taes'],
                linewidth=2.5,
                markersize=6,
                label='NEDC TAES',
                alpha=0.9,
                markeredgecolor='black',
                markeredgewidth=0.5,
                zorder=7)

    # Plot SzCORE with triangles
    ax.semilogx(szcore['fa_per_24h'], szcore['sensitivity'], '^-',
                color=COLORS['szcore'],
                linewidth=2.5,
                markersize=8,
                label='SzCORE Event',
                alpha=0.9,
                markeredgecolor='black',
                markeredgewidth=0.5,
                zorder=9)

    # Clinical viability zone
    ax.axvspan(0.1, 10, ymin=0.75, ymax=1, alpha=0.15, color='green',
               label='Clinical target zone', zorder=1)
    ax.axhline(y=75, color='green', linestyle='--', alpha=0.5, linewidth=1, zorder=2)
    ax.axvline(x=10, color=COLORS['threshold'], linestyle='--', alpha=0.5, linewidth=1, zorder=2)
    ax.axvline(x=1, color='red', linestyle=':', alpha=0.4, linewidth=1.5, zorder=2)

    # Annotations - position carefully to avoid overlaps
    ax.annotate('Clinical\ntarget',
                xy=(3, 85),
                fontsize=9,
                ha='center',
                color='green',
                fontweight='bold',
                zorder=15)

    # Human level annotation
    ax.annotate('Human level\n(1 FA/24h)',
                xy=(1.0, 22),
                fontsize=8,
                ha='center',
                color='red',
                bbox=dict(boxstyle='round,pad=0.3',
                         facecolor='white',
                         alpha=0.95,
                         edgecolor='red',
                         linewidth=0.5),
                zorder=20)

    # Mark paper's default operating point
    default_point = nedc_overlap[nedc_overlap['threshold'] == 0.80].iloc[0]
    ax.plot(default_point['fa_per_24h'], default_point['sensitivity'],
            'o', color='black', markersize=10, zorder=15)
    ax.annotate('Paper default\n(θ=0.8, k=5, d=2.0)',
                xy=(default_point['fa_per_24h'], default_point['sensitivity']),
                xytext=(50, 30),
                fontsize=8,
                ha='center',
                bbox=dict(boxstyle='round,pad=0.3',
                         facecolor='white',
                         alpha=0.95,
                         edgecolor='black',
                         linewidth=0.5),
                arrowprops=dict(arrowstyle='-',
                               color='black',
                               alpha=0.7,
                               lw=1),
                zorder=15)

    # Mark 10 FA/24h operating point
    ten_fa_point = nedc_overlap[nedc_overlap['threshold'] == 0.88].iloc[0]
    ax.plot(ten_fa_point['fa_per_24h'], ten_fa_point['sensitivity'],
            'D', color='purple', markersize=8, zorder=14)
    ax.annotate('10 FA/24h\ntarget',
                xy=(ten_fa_point['fa_per_24h'], ten_fa_point['sensitivity']),
                xytext=(15, 50),
                fontsize=8,
                ha='left',
                bbox=dict(boxstyle='round,pad=0.3',
                         facecolor='white',
                         alpha=0.95,
                         edgecolor='purple',
                         linewidth=0.5),
                arrowprops=dict(arrowstyle='-',
                               color='purple',
                               alpha=0.7,
                               lw=1),
                zorder=14)

    # Axes configuration
    ax.set_xlabel('False Alarms per 24 Hours', fontsize=FONT_SIZE['label'])
    ax.set_ylabel('Sensitivity (%)', fontsize=FONT_SIZE['label'])
    ax.set_xlim(0.2, 400)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3, which='both', zorder=0)

    # Legend - order by performance
    handles, labels = ax.get_legend_handles_labels()
    # Find indices
    szcore_idx = labels.index('SzCORE Event')
    overlap_idx = labels.index('NEDC OVERLAP')
    taes_idx = labels.index('NEDC TAES')
    zone_idx = labels.index('Clinical target zone')
    # Reorder: SzCORE, NEDC OVERLAP, NEDC TAES, Clinical target zone
    new_order = [szcore_idx, overlap_idx, taes_idx, zone_idx]
    ax.legend([handles[i] for i in new_order],
              [labels[i] for i in new_order],
              loc='lower right', fontsize=FONT_SIZE['legend'], framealpha=0.95)

    # Title
    ax.set_title('Figure 2: Operating Characteristic Curves Across Scoring Methods',
                 fontsize=FONT_SIZE['title'], fontweight='bold', pad=15)

    # Clean up
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=FONT_SIZE['tick'])

    plt.tight_layout()

    # Save in multiple formats
    output_dir = Path(__file__).parent.parent / 'output' / 'arxiv'
    output_dir.mkdir(exist_ok=True, parents=True)

    for fmt in ['png', 'pdf']:
        output_path = output_dir / f'fig2_operating_curves_optimized.{fmt}'
        plt.savefig(output_path,
                   dpi=DPI_ARXIV if fmt == 'png' else None,
                   bbox_inches='tight',
                   pad_inches=0.1,
                   facecolor='white',
                   edgecolor='none')
        print(f"✓ Saved: {output_path}")

    plt.close()
    print("✓ Figure 2 generated successfully!")

if __name__ == "__main__":
    generate_fig2_optimized()