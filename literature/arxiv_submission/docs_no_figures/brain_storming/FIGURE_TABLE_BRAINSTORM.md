# Figure and Table Brainstorming for SeizureTransformer ArXiv Paper

## Core Message to Visualize
**27-137× performance gap between benchmark claims and clinical reality**

## Priority 1: Essential Figures (Must Have)

### Figure 1: The Gap Visualization
**Type**: Multi-panel comparison plot
- **Panel A**: Bar chart showing FA/24h across evaluation contexts
  - Dianalund: ~1 FA/24h (claimed)
  - TUSZ NEDC OVERLAP: 26.89 FA/24h (27× worse)
  - TUSZ NEDC TAES: 136.73 FA/24h (137× worse)
  - TUSZ SzCORE: 8.59 FA/24h
- **Panel B**: Sensitivity at different FA/24h thresholds
  - Show clinical target zone (75% sens, <10 FA/24h)
  - Show actual achievement (33.90% sens at 10 FA/24h)
- **Visual Impact**: Use log scale for FA axis, highlight the gap with annotations

### Figure 2: Operating Characteristic Curves
**Type**: Multi-line plot with shaded regions
- X-axis: False Alarms per 24 hours (log scale)
- Y-axis: Sensitivity (%)
- Lines: NEDC OVERLAP, NEDC TAES, SzCORE
- Annotations: Mark clinical viability zones
- Shading: Highlight clinically acceptable region (<10 FA/24h, >75% sensitivity)

### Figure 3: Scoring Methodology Impact
**Type**: Sankey diagram or flow chart
- Start: Same 865 predictions
- Branch: Three scoring methods
- End: Vastly different FA/24h rates
- Shows how identical predictions → 3.1× to 15.9× performance differences

### Figure 4: Parameter Sweep Heatmap
**Type**: 3D surface plot or contour map
- X-axis: Threshold (0.7-0.98)
- Y-axis: Minimum duration (1-6 seconds)
- Z-axis/Color: F1 score or FA/24h
- Separate panels for each kernel size
- Mark paper's default (θ=0.8, k=5, d=2.0) and optimized points

## Priority 2: Supporting Figures

### Figure 5: Error Analysis
**Type**: Stacked bar chart or pie charts
- False Positives breakdown: Movement (34%), Electrode pop (22%), etc.
- False Negatives breakdown: Brief seizures (42%), Low amplitude (28%), etc.

### Figure 6: Seizure Detection Examples
**Type**: Time series with annotations
- 3-4 panels showing EEG segments
- Ground truth seizures (shaded regions)
- Model predictions (colored bars)
- Examples of: True Positive, False Positive, False Negative

### Figure 7: Dataset Characteristics
**Type**: Distribution plots
- Seizure duration histogram (show heavy tail)
- Seizure types pie chart
- Files with/without seizures

## Priority 3: Enhanced Tables

### Table 1: Main Results (Already in paper, needs formatting)
- Use color gradients for FA/24h (red = bad, green = good)
- Bold best values in each column
- Add sparklines for trends

### Table 2: Sensitivity at Clinical Thresholds
- Expandable/collapsible sections for different scorers
- Visual indicators (✓/✗) for meeting clinical criteria

## Technical Stack for 2025 Best Practices

### Core Visualization Libraries
```bash
# Python scientific visualization stack
pip install matplotlib seaborn plotly
pip install altair vega_datasets
pip install holoviews panel hvplot

# Publication quality
pip install scienceplots  # Nature, Science, IEEE styles
pip install matplotlib-scalebar
pip install adjustText  # Smart label placement

# Advanced features
pip install datashader  # Large dataset visualization
pip install bokeh  # Interactive plots
pip install dash plotly-dash  # Web dashboards
```

### Table Generation
```bash
# Beautiful tables
pip install great-tables  # Modern table formatting
pip install tabulate rich  # Terminal and export
pip install pandas-profiling  # Auto EDA reports
```

### Color and Style
```bash
# Color schemes
pip install palettable colorcet
pip install cmocean  # Perceptually uniform colormaps
```

### Export and Integration
```bash
# High quality exports
pip install cairosvg  # SVG to PDF conversion
pip install pypdf2 reportlab  # PDF generation
pip install kaleido  # Static image export for plotly
```

### Terminal-Based Visualization
```bash
# For quick iteration in terminal
pip install plotext  # Matplotlib in terminal
pip install asciichartpy  # Simple ASCII charts
pip install termgraph  # Bar charts in terminal
```

## Figure Generation Pipeline

### 1. Quick Iteration (Terminal)
```python
# scripts/quick_viz.py
import plotext as plt
plt.scatter(fa_rates, sensitivities)
plt.show()
```

### 2. Draft Quality (Notebook/Script)
```python
# scripts/draft_figures.py
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid", palette="muted")
```

### 3. Publication Quality
```python
# scripts/publication_figures.py
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science', 'nature', 'no-latex'])

# 300 DPI, correct dimensions
fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
```

## Color Palette Strategy

### Accessible Color Scheme
- Primary: `#2E86AB` (Blue - NEDC OVERLAP)
- Secondary: `#A23B72` (Rose - NEDC TAES)
- Tertiary: `#F18F01` (Orange - SzCORE)
- Alert: `#C73E1D` (Red - Clinical failure zone)
- Success: `#6A994E` (Green - Clinical success zone)

### Ensure:
- Colorblind friendly (use Viridis/Cividis)
- Print friendly (works in grayscale)
- High contrast for accessibility

## Interactive Elements (Optional for Web)

### Plotly Dashboard
```python
# scripts/interactive_dashboard.py
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Performance Gap", "Operating Curves",
                    "Parameter Sensitivity", "Error Analysis")
)
```

## Export Formats

### For ArXiv
- PDF vector graphics (infinite zoom)
- PNG fallback at 300 DPI
- Include raw data tables as CSV

### For GitHub
- Interactive HTML versions
- Static PNG for README
- Jupyter notebooks with reproducible figures

## Implementation Order

1. **Week 1**: Install tools, create data loading pipeline
2. **Week 2**: Generate Figure 1 (Gap Visualization) - most critical
3. **Week 3**: Generate Figure 2 (Operating Curves) and Figure 3 (Scoring Impact)
4. **Week 4**: Polish, iterate on colors/styles, generate all formats

## Sample Code Structure

```
scripts/
├── visualization/
│   ├── __init__.py
│   ├── config.py          # Colors, fonts, sizes
│   ├── data_loader.py     # Load results from pickle/CSV
│   ├── fig1_gap.py        # Generate Figure 1
│   ├── fig2_curves.py     # Generate Figure 2
│   ├── fig3_sankey.py     # Generate Figure 3
│   ├── fig4_heatmap.py    # Generate Figure 4
│   └── utils.py           # Common plotting functions
├── generate_all_figures.py
└── quick_terminal_viz.py
```

## Notes for Maximum Impact

1. **Lead with the gap** - Make the 27-137× difference impossible to miss
2. **Use log scales wisely** - FA/24h spans orders of magnitude
3. **Annotate clinical thresholds** - Show why this matters
4. **Consistent color coding** - Same scorer = same color everywhere
5. **Tell a story** - Figures should flow: Problem → Analysis → Implications

## Terminal Workflow for 2025

```bash
# Quick iteration
python scripts/quick_terminal_viz.py --metric fa_rates

# Generate all figures
python scripts/generate_all_figures.py --style nature --dpi 300

# Export for different venues
python scripts/export_figures.py --format pdf --venue arxiv
python scripts/export_figures.py --format png --venue github
python scripts/export_figures.py --format html --venue web

# Validate accessibility
python scripts/validate_figures.py --check colorblind --check grayscale
```

## Success Metrics for Figures

- [ ] Can a reader understand the 27-137× gap in <3 seconds?
- [ ] Do the figures work in grayscale?
- [ ] Are all axes labeled with units?
- [ ] Do captions stand alone without main text?
- [ ] Is the clinical relevance immediately clear?
- [ ] Can figures be reproduced from provided code/data?