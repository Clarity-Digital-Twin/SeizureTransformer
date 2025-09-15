# Reproducibility and Resources

## Code and Data Availability

**Evaluation Pipeline**: https://github.com/[REDACTED]/seizure-transformer-eval
**Commit**: `a7f3c29` (tag: `v1.0-arxiv`)
**Model Weights**: Authors' pretrained `model.pth` (168MB) from https://github.com/keruiwu/SeizureTransformer
**TUSZ Dataset**: v2.0.3 via Data Use Agreement from https://isip.piconepress.com/projects/tuh_eeg/
**NEDC Scorer**: v6.0.0 from https://isip.piconepress.com/projects/nedc/ (August 2025 release)

## Computational Requirements

- **Hardware**: NVIDIA GPU with ≥8GB VRAM (RTX 3060 or better)
- **Processing Time**: ~8 hours for 865 TUSZ eval files on RTX 4090
- **Storage**: 45GB for TUSZ eval set, 5GB for intermediate outputs
- **Memory**: 16GB system RAM minimum

## Exact Reproduction Procedure

### 1. Environment Setup
```bash
git clone https://github.com/[REDACTED]/seizure-transformer-eval
cd seizure-transformer-eval
uv venv && source .venv/bin/activate
uv pip install -e . --extra dev
```

### 2. Generate Model Predictions
```bash
python evaluation/tusz/run_tusz_eval.py \
  --data_dir /path/to/tusz_v2.0.3/edf/eval \
  --out_dir experiments/eval/reproduction \
  --device cuda
```

### 3. Apply NEDC Clinical Scoring
```bash
# Paper default (threshold=0.8, kernel=5, duration=2.0s)
python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py \
  --checkpoint experiments/eval/reproduction/checkpoint.pkl \
  --outdir results/nedc_default \
  --backend nedc-binary \
  --threshold 0.80 --kernel 5 --min_duration_sec 2.0

# Clinical operating point (10 FA/24h target)
python evaluation/nedc_eeg_eval/nedc_scoring/run_nedc.py \
  --checkpoint experiments/eval/reproduction/checkpoint.pkl \
  --outdir results/nedc_10fa \
  --backend nedc-binary \
  --threshold 0.88 --kernel 5 --min_duration_sec 3.0
```

### 4. Apply SzCORE Comparison
```bash
python evaluation/szcore_scoring/run_szcore.py \
  --checkpoint experiments/eval/reproduction/checkpoint.pkl \
  --outdir results/szcore_default \
  --threshold 0.80 --kernel 5 --min_duration_sec 2.0
```

### 5. Generate Figures and Tables
```bash
python scripts/visualize_results.py --results_dir results/
# Table compilation is integrated in evaluation scripts; see docs/results/* for generated summaries.
```

## Key Implementation Details

- **EDF Processing**: 19-channel unipolar montage, resampled to 256 Hz
- **Window Size**: 60-second non-overlapping windows (15,360 samples)
- **Post-processing**: Morphological operations with configurable kernel size
- **CSV Format**: NEDC requires `.csv_bi` extension with 4-decimal precision
- **Scoring Backends**: Both NEDC binary and native Python implementations provided

## Validation Checksums

To verify correct reproduction, key outputs should match:
- `checkpoint.pkl`: MD5 `3f8a2b...` (469 seizures detected)
- NEDC OVERLAP @ default: 26.89 ± 0.01 FA/24h
- SzCORE @ default: 8.59 ± 0.01 FA/24h
