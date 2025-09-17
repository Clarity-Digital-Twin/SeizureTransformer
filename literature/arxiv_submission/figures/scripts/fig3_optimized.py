#!/usr/bin/env python3
"""Generate optimized Figure 3: Scoring Impact Flow Diagram"""

import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path
import numpy as np

# Add parent directory to path for config import
sys.path.append(str(Path(__file__).parent))
from config import *

def generate_fig3_optimized():
    """Generate publication-quality Figure 3 with improved flow diagram"""

    fig, ax = plt.subplots(figsize=(10, 6), dpi=DPI_ARXIV)

    # Define positions
    input_x, input_y = 1, 2
    model_x, model_y = 4, 2
    scorer_x = 7
    result_x = 10

    # Y positions for scorers (only 3 now)
    scorer_y = [3.0, 2.0, 1.0]

    # ============ Input Box ============
    input_box = FancyBboxPatch((input_x-0.8, input_y-0.4), 1.6, 0.8,
                               boxstyle="round,pad=0.05",
                               facecolor='lightgray',
                               edgecolor='black',
                               linewidth=LINE_WIDTH['box'])
    ax.add_patch(input_box)
    ax.text(input_x, input_y, '865 EDF Files\n469 Seizures\n127.7 Hours',
            ha='center', va='center', fontsize=FONT_SIZE['annotation']+1,
            fontweight='normal')

    # ============ Model Box ============
    model_box = FancyBboxPatch((model_x-1, model_y-0.4), 2, 0.8,
                               boxstyle="round,pad=0.05",
                               facecolor='lightblue',
                               edgecolor='black',
                               linewidth=LINE_WIDTH['box']+0.5)
    ax.add_patch(model_box)
    ax.text(model_x, model_y, 'SeizureTransformer\nPredictions',
            ha='center', va='center', fontsize=FONT_SIZE['label'],
            fontweight='bold')

    # ============ Scorer and Result Boxes ============
    scorers = ['NEDC TAES', 'NEDC OVERLAP', 'SzCORE']
    results = ['136.73 FA/24h\n65.21% Sens',
               '26.89 FA/24h\n45.63% Sens',
               '8.59 FA/24h\n52.35% Sens']
    colors = [COLORS['nedc_taes'], COLORS['nedc_overlap'], COLORS['szcore']]

    for scorer, result, color, y in zip(scorers, results, colors, scorer_y):
        # Scorer box
        scorer_box = FancyBboxPatch((scorer_x-0.7, y-0.25), 1.4, 0.5,
                                    boxstyle="round,pad=0.02",
                                    facecolor=color,
                                    alpha=0.7,
                                    edgecolor='black',
                                    linewidth=LINE_WIDTH['box'])
        ax.add_patch(scorer_box)
        ax.text(scorer_x, y, scorer, ha='center', va='center',
               fontsize=FONT_SIZE['annotation'], fontweight='bold')

        # Result box
        result_box = FancyBboxPatch((result_x-0.8, y-0.3), 1.6, 0.6,
                                   boxstyle="round,pad=0.02",
                                   facecolor='white',
                                   edgecolor=color,
                                   linewidth=LINE_WIDTH['box']+0.5)
        ax.add_patch(result_box)
        ax.text(result_x, y, result, ha='center', va='center',
               fontsize=FONT_SIZE['annotation'], fontweight='bold')

    # ============ Arrows ============
    # Input to Model arrow
    arrow1 = FancyArrowPatch((input_x+0.8, input_y), (model_x-1, model_y),
                            connectionstyle="arc3,rad=0",
                            arrowstyle='->,head_width=0.3,head_length=0.3',
                            lw=LINE_WIDTH['arrow']+0.5,
                            color='gray',
                            zorder=1)
    ax.add_patch(arrow1)

    # Model to Scorers arrows (fan out)
    for y in scorer_y:
        arrow = FancyArrowPatch((model_x+1, model_y), (scorer_x-0.7, y),
                               connectionstyle="arc3,rad=0.2",
                               arrowstyle='->,head_width=0.2,head_length=0.2',
                               lw=LINE_WIDTH['arrow'],
                               color='gray',
                               alpha=0.6,
                               zorder=1)
        ax.add_patch(arrow)

    # Scorers to Results arrows
    for color, y in zip(colors, scorer_y):
        arrow = FancyArrowPatch((scorer_x+0.7, y), (result_x-0.8, y),
                               connectionstyle="arc3,rad=0",
                               arrowstyle='->,head_width=0.2,head_length=0.2',
                               lw=LINE_WIDTH['arrow']+0.3,
                               color=color,
                               alpha=0.8,
                               zorder=1)
        ax.add_patch(arrow)

    # ============ Annotation Box ============
    # Use 'x' instead of × to avoid font encoding issues
    annotation = '15.9x difference in FA/24h\nbetween TAES and SzCORE'
    annotation_box = FancyBboxPatch((result_x-1.5, -0.3), 3, 0.6,
                                   boxstyle="round,pad=0.05",
                                   facecolor='yellow',
                                   alpha=0.3,
                                   edgecolor='orange',
                                   linewidth=LINE_WIDTH['box'])
    ax.add_patch(annotation_box)
    ax.text(result_x, 0, annotation,
            ha='center', va='center',
            fontsize=FONT_SIZE['annotation']+1,
            style='italic',
            fontweight='bold')

    # ============ Styling ============
    ax.set_xlim(0, 11.5)
    ax.set_ylim(-0.8, 3.5)
    ax.axis('off')

    # Title
    ax.set_title('Figure 3: How Scoring Methodology Determines Performance Metrics',
                fontsize=FONT_SIZE['title']+1,
                fontweight='bold',
                pad=20)

    # Add subtle annotations
    ax.text(2.5, 2.5, 'Same data', ha='center', fontsize=8,
           style='italic', color='gray', alpha=0.7)
    ax.text(5.5, 3.5, 'Identical\npredictions', ha='center', fontsize=8,
           style='italic', color='gray', alpha=0.7)
    ax.text(8.5, 3.8, 'Different\nscorers', ha='center', fontsize=8,
           style='italic', color='gray', alpha=0.7)
    ax.text(10, 3.8, 'Vastly different\nresults', ha='center', fontsize=8,
           style='italic', color='red', alpha=0.7, fontweight='bold')

    plt.tight_layout()

    # Save in multiple formats
    output_dir = Path('../output/arxiv')
    output_dir.mkdir(parents=True, exist_ok=True)

    for fmt in ['pdf', 'png']:
        filename = output_dir / f'fig3_scoring_impact_optimized.{fmt}'
        plt.savefig(filename,
                   dpi=DPI_ARXIV if fmt == 'pdf' else DPI_WEB,
                   metadata=METADATA if fmt == 'pdf' else None,
                   **EXPORT_SETTINGS)
        print(f"✓ Saved: {filename}")

    # Also save web version
    web_dir = Path('../output/web')
    web_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(web_dir / 'fig3_scoring_impact.png',
               dpi=DPI_SCREEN,
               **EXPORT_SETTINGS)

    # No need to save in additional locations

    plt.close()
    print("✓ Figure 3 optimized generation complete")

if __name__ == "__main__":
    generate_fig3_optimized()