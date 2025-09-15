# GitHub Issue Draft for keruiwu/SeizureTransformer

## Title: Independent Evaluation on TUSZ v2.0.3 - Results and Discussion

## Body:

Hi @keruiwu and team,

Thank you for making SeizureTransformer publicly available. We've conducted an independent evaluation of your pretrained model on the Temple University Hospital EEG Seizure Corpus (TUSZ v2.0.3) using the official NEDC v6.0.0 scoring tools, and wanted to share our findings with you.

## Evaluation Setup
- **Dataset**: TUSZ v2.0.3 eval split (865 files, 127.6 hours, 469 seizures)
- **Model**: Your pretrained weights (unchanged)
- **Scoring**: NEDC v6.0.0 TAES (Time-Aligned Event Scoring)
- **Post-processing**: As per paper (threshold=0.8, morphological kernel=5, min duration=2s)

## Results

| Metric | Your Paper | Our TUSZ Results |
|--------|------------|------------------|
| **AUROC** | 0.876 | **0.9021** |
| **Sensitivity** | 71.1%* | **24.15%** |
| **Precision** | - | **43.98%** |
| **F1 Score** | 67.5%* | **31.19%** |
| **False Alarms/24h** | 1** | **137.5** |

*Using event-based scoring  
**On Dianalund dataset

## Key Observations

1. **Excellent discrimination**: The AUROC of 0.9021 shows the model has learned meaningful seizure patterns
2. **Dataset differences**: The significant difference in false alarm rates (1 on Dianalund vs 137.5 on TUSZ) highlights the challenge of cross-dataset generalization
3. **Scoring methodology**: TAES is stricter than event-based scoring, which partially explains sensitivity differences

## Reproducible Evaluation

We've made our complete evaluation pipeline publicly available:
- Repository: https://github.com/Clarity-Digital-Twin/SeizureTransformer
- Includes NEDC integration, preprocessing scripts, and full documentation
- Can reproduce all numbers with: `python evaluation/tusz/run_tusz_eval.py`

## Questions for Discussion

1. Have you experimented with dataset-specific threshold optimization? The 0.8 threshold might need adjustment for TUSZ.
2. Would you be interested in collaborating on improving TUSZ performance? The high AUROC suggests the model could perform much better with tuning.
3. Are there plans to release TUSZ-specific weights or fine-tuning code?

## Acknowledgment

This evaluation was conducted independently to contribute to reproducible research in seizure detection. We appreciate your work in advancing this field and making your model publicly available.

Would you like us to submit our evaluation to SzCORE/Epilepsy Bench to help establish TUSZ benchmarks for SeizureTransformer?

Best regards,
[Your Name/Team]

---

## Additional Notes for Posting:
- Be sure to link to specific files if they ask for details
- Offer to share the checkpoint.pkl with predictions if they want to verify
- Be prepared to explain NEDC TAES vs event-based scoring differences
- Emphasize this is meant to help the community, not criticize
# GitHub Issue Draft for keruiwu/SeizureTransformer (Archived Draft)

Note: This draft contains legacy numbers that were produced prior to our merge_gap deprecation. Before posting, update all figures to match docs/status/SINGLE_SOURCE_OF_TRUTH.md (no merge) and specify the exact NEDC metric used (TAES vs OVERLAP). Do not cite 60.83/137.x FA values without re‑extraction.
