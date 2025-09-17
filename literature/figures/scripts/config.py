"""Configuration for publication-quality figures - 2025 best practices"""

import matplotlib.pyplot as plt
import scienceplots

# Style configuration
plt.style.use(['science', 'nature', 'no-latex'])  # Avoid LaTeX rendering issues

# Resolution and sizing
DPI_ARXIV = 600      # ArXiv submission requirement
DPI_SCREEN = 150     # Quick preview
DPI_WEB = 300        # Web/GitHub display

# Figure dimensions (inches) - Nature specifications
SINGLE_COL = 3.5     # Single column width (89mm)
DOUBLE_COL = 7.0     # Double column width (183mm)
HEIGHT_DEFAULT = 4.5 # Default height for good aspect ratio
HEIGHT_TALL = 6.0    # Taller figures when needed

# Font specifications (Nature requirements)
FONT_SIZE = {
    'title': 12,
    'label': 11,
    'tick': 9,
    'legend': 9,
    'annotation': 8,
    'panel_label': 14  # For A, B, C panel labels
}

# Line specifications
LINE_WIDTH = {
    'data': 2.5,      # Main data lines
    'grid': 0.5,      # Grid lines
    'reference': 1.0, # Reference lines (thresholds)
    'box': 1.5,       # Box/bar edges
    'arrow': 1.2      # Arrow lines
}

# Marker sizes
MARKER_SIZE = {
    'default': 7,
    'highlight': 10,
    'small': 5
}

# Color palette (colorblind-friendly, validated with Coblis)
COLORS = {
    'dianalund': '#6A994E',     # Green - success/claimed
    'nedc_overlap': '#2E86AB',  # Blue - primary scorer
    'nedc_taes': '#C73E1D',     # Red - worst performer
    'szcore': '#F18F01',        # Orange - alternative
    'native': '#2E86AB',        # Same as OVERLAP
    'threshold': '#666666',     # Gray - reference lines
    'clinical_zone': '#90EE90', # Light green - target zone
    'grid': '#E0E0E0',          # Light gray for grids
    'annotation': '#333333'     # Dark gray for text
}

# Alpha values for transparency
ALPHA = {
    'bar': 0.85,
    'zone': 0.15,
    'grid': 0.2,
    'annotation_bg': 0.8
}

# Metadata for PDF files
METADATA = {
    'Creator': 'SeizureTransformer Analysis Pipeline',
    'Producer': 'Matplotlib with SciencePlots',
    'Subject': 'Clinical Reality vs Benchmark Claims in Seizure Detection',
    'Keywords': 'seizure detection, TUSZ, NEDC, clinical validation',
    'Author': 'SeizureTransformer Research Team'
}

# Export settings
EXPORT_SETTINGS = {
    'bbox_inches': 'tight',
    'pad_inches': 0.1,
    'transparent': False,
    'facecolor': 'white',
    'edgecolor': 'none'
}

# Validation thresholds
CLINICAL_THRESHOLDS = {
    'fa_per_24h': 10.0,      # Maximum acceptable false alarms
    'sensitivity': 75.0,     # Minimum acceptable sensitivity
    'human_fa': 1.0          # Human expert baseline
}

def setup_axes(ax, title=None, xlabel=None, ylabel=None, grid=True):
    """Apply consistent styling to axes"""
    if title:
        ax.set_title(title, fontsize=FONT_SIZE['title'], fontweight='bold', pad=10)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=FONT_SIZE['label'])
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=FONT_SIZE['label'])

    ax.tick_params(axis='both', which='major', labelsize=FONT_SIZE['tick'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    if grid:
        ax.grid(True, alpha=ALPHA['grid'], linewidth=LINE_WIDTH['grid'],
                linestyle='-', color=COLORS['grid'])
        ax.set_axisbelow(True)

def add_panel_label(ax, label, x=-0.08, y=1.05):
    """Add panel labels (A, B, C, etc.) to subplots"""
    ax.text(x, y, label, transform=ax.transAxes,
            fontsize=FONT_SIZE['panel_label'], fontweight='bold',
            va='top', ha='right')