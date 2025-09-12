# Acknowledgments

## Original Work

This repository contains an independent evaluation of the **SeizureTransformer** model, originally developed by:

- **Kerui Wu** and team (2025)
- Original paper: "SeizureTransformer: Versatile Seizure Detection Model for Generalization Across Patients, Datasets, and Seizure Types"
- Original repository: https://github.com/keruiwu/SeizureTransformer

## Datasets

### Temple University Hospital EEG Seizure Corpus (TUSZ v2.0.3)
- **Temple University Neural Engineering Data Consortium**
- Citation: Shah, V., von Weltin, E., Lopez. S., McHugh, J., Veloso, L., Golmohammadi, M., Obeid, I., and Picone, J. (2018). The Temple University Hospital Seizure Detection Corpus. Frontiers in Neuroinformatics. 12:83. doi: 10.3389/fninf.2018.00083
- Available at: https://isip.piconepress.com/projects/tuh_eeg/

## Evaluation Tools

### NEDC EEG Eval v6.0.0
- **Joseph Picone** and **Iyad Obeid**, Temple University
- Official scoring software from the Neural Engineering Data Consortium
- Used for computing TAES (Time-Aligned Event Scoring) metrics
- Available at: https://www.isip.piconepress.com/projects/nedc/

### SzCORE Framework
- Standardized seizure detection evaluation framework
- Paper: Dan, J. et al. (2025). "SzCORE as a benchmark: report from the seizure detection challenge at the 2025 AI in Epilepsy and Neurological Disorders Conference"
- Website: https://szcore.org/

## Computing Resources

- GPU processing provided by NVIDIA GeForce RTX 4090
- Evaluation performed on WSL2 Ubuntu environment

## Open Source Dependencies

- **PyTorch** - Deep learning framework (Apache 2.0)
- **NumPy** - Numerical computing (BSD)
- **scikit-learn** - Machine learning utilities (BSD)
- **MNE-Python** - EEG processing (BSD)
- **pyEDFlib** - EDF file reading (BSD)
- **matplotlib/seaborn** - Visualization (PSF/BSD)

## Community Contributions

Special thanks to the epilepsy research community for:
- Establishing standardized evaluation protocols
- Maintaining public EEG datasets
- Developing open-source tools for EEG analysis
- Promoting reproducible research practices

## Funding and Support

This independent evaluation was conducted without external funding as a contribution to open science and reproducible research in epilepsy detection.

## Disclaimer

This evaluation is independent and not affiliated with the original SeizureTransformer authors or Temple University. All findings and conclusions are our own based on publicly available code and data.

## Contact

For questions about this evaluation framework:
- Repository: https://github.com/Clarity-Digital-Twin/SeizureTransformer
- Issues: https://github.com/Clarity-Digital-Twin/SeizureTransformer/issues

For questions about the original SeizureTransformer:
- Contact the original authors through their publication

For questions about TUSZ dataset or NEDC tools:
- Contact: help@nedcdata.org