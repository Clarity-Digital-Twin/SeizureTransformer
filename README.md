# SeizureTransformer - Private Development Fork

This is a private development fork of [SeizureTransformer](https://github.com/keruiwu/SeizureTransformer) for testing, evaluation, and potential contributions.

## Repository Structure

```
.
├── wu_2025/           # ORIGINAL CODE (untouched) - from upstream
├── scripts/           # Utility scripts (data download, etc.)
├── tests/            # Test suite for validation
├── evaluation/       # NEDC evaluation tools and metrics
├── docs/            # Additional documentation
└── literature/      # Paper references (gitignored)
```

## Quick Start

### 1. Environment Setup
```bash
# Create virtual environment
uv venv
source .venv/bin/activate

# Install original package
uv pip install ./wu_2025
```

### 2. Run Inference
```bash
# Run on single EDF file
python -m wu_2025 input.edf output.tsv

# Test inference works
python tests/test_inference.py
```

### 3. Data Setup
```bash
# Download Siena dataset (if needed)
bash scripts/download_siena.sh

# TUSZ dataset must be obtained separately
```

## Development Workflow

### For Local Development
- Add new features in `scripts/`, `tests/`, or `evaluation/`
- DO NOT modify anything in `wu_2025/` directory
- Document changes in `docs/`

### For Contributing Back
1. Create feature branch from public fork
2. Cherry-pick clean commits (no private data)
3. Submit PR from public fork to upstream

## Key Files

- `wu_2025/src/wu_2025/model.pth` - Pretrained weights (168MB)
- `docs/IDEAL_REFERENCE_SEIZURE_TRANSFORMER_DATAFLOW.md` - Implementation guide
- `evaluation/nedc_eeg_eval_v6.0.0.tar.gz` - NEDC evaluation tools

## Git Remotes

- `origin` - Our private repo (Clarity-Digital-Twin/SeizureTransformer)
- `upstream` - Original repo (keruiwu/SeizureTransformer)
- `fork` - Public fork for PRs (Clarity-Digital-Twin/SeizureTransformer-Fork)

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test
python tests/test_inference.py
```

## Notes

- Model requires exactly 19 channels, unipolar montage
- Preprocessing: z-score → resample 256Hz → bandpass 0.5-120Hz → notch 1,60Hz
- Post-processing: threshold 0.8 → morphological ops → remove <2s events

## License

Original code: MIT License (see wu_2025/LICENSE)
Our additions: MIT License