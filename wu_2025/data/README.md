# Data Directory Structure

This directory should contain the datasets after download:

## TUSZ Dataset
Place TUSZ v2.0.3 data here after obtaining access from Temple University:
```
tusz/
└── v2.0.3/
    └── edf/
        ├── train/   # Training data (not needed for evaluation only)
        ├── dev/     # Development set (for threshold tuning)
        └── eval/    # Evaluation set (for final results)
```

To obtain TUSZ:
1. Request access at: https://isip.piconepress.com/projects/nedc/html/tuh_eeg/
2. Download using rsync (see main README for commands)

## Siena Dataset
Place Siena Scalp EEG data here if needed for training:
```
siena/
└── 1.0.0/
    ├── PN00/
    ├── PN01/
    └── ...
```

To obtain Siena:
1. Download from PhysioNet: https://physionet.org/content/siena-scalp-eeg/1.0.0/
2. No registration required (open access)

Note: Both directories are gitignored to prevent accidental commits of large datasets.