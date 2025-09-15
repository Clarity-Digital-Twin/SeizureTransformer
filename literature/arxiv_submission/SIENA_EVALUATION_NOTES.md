# Siena Scalp EEG Database – Usage and Evaluation Notes

## What It Is
- Small EEG dataset (≈128 hours) from 14 subjects at 512 Hz.
- Directory structure: `data/siena/PNXX/*.edf` with per‑patient text files `Seizures-list-PNXX.txt` listing clock times for seizure episodes.
- No official train/dev/eval splits are provided in the public distribution.

## How SeizureTransformer Uses It (per paper)
- Training combines TUSZ v2.0.3 train and the entire Siena dataset.
- 60‑second, 256 Hz windows, unified 19‑channel montage; 75% overlap between windows.

## Implications for Our Evaluation
- We use the authors’ pretrained weights, which were trained using Siena.
- Therefore, any metrics computed on Siena are in‑sample and not held‑out.
- We report Siena results only as descriptive diagnostics; they are not comparable to held‑out TUSZ eval metrics.

## Annotation Parsing
- Each `Seizures-list-PNXX.txt` file contains:
  - Registration start/end clock times
  - One or more seizure start/end clock times per EDF file
- To evaluate, convert clock times to seconds since EDF start using the EDF header start time:

```text
offset_seconds = (seizure_clock_time - registration_start_clock_time)
```

Then emit intervals in our standard TSV (or CSV_BI) format. Suggested target: per‑file TSV with `start_time, stop_time, label`.

Known quirks to handle:
- Some patient notes use `PNO6` vs `PN06` in file names; normalize basenames when matching.
- Clock times use dots (e.g., `05.54.25`) instead of colons; convert to `HH:MM:SS` before parsing.

## Recommended Scoring for Siena
- Use SzCORE (any‑overlap with tolerances) for consistency with EpilepsyBench cross‑dataset philosophy.
- Optionally add Python OVERLAP for a research‑style view; do not use NEDC (Temple’s scorer is specific to TUSZ).

## Cautions in Writing
- Always state that Siena was part of training; results are in‑sample.
- Do not present Siena as a held‑out evaluation or claim generalization from it.
- Use Siena results only as qualitative context (e.g., showing model behavior at 512 Hz sources).

## Minimal Evaluation Pseudocode
```python
from pathlib import Path
from wu_2025.utils import load_models, get_dataloader, predict
from epilepsy2bids.eeg import Eeg
from seizure_evaluation.scores import OverlapScorer  # native overlap

def parse_siena_annotation(txt_path):
    # parse registration start/end and seizure clock times
    # return list of (file_basename, start_sec, end_sec)
    ...

def evaluate_siena(edf_dir):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = load_models(device)
    refs, hyps = [], []
    for edf in Path(edf_dir).glob('PN*/**/*.edf'):
        eeg = Eeg.loadEdfAutoDetectMontage(edfFile=str(edf))
        dl = get_dataloader(eeg.data, eeg.fs, batch_size=512, window_size=15360)
        y_mask = predict(model, dl, device, seq_len=eeg.data.shape[1])
        # convert mask to events (tsv)
        hyp_events = mask_to_events(y_mask, fs=eeg.fs)
        ref_events = load_parsed_siena_events_for_file(edf)
        refs.append(ref_events); hyps.append(hyp_events)
    # scoring
    ovlp = OverlapScorer().evaluate(refs, hyps)
    # optionally SzCORE if available
    return ovlp
```

## Where to Cite
- CORE_2 (Model): note Siena’s use in training and lack of splits.
- Methods: add a brief “Siena (in‑sample) diagnostics” subsection.
- Appendix/Supplement: place detailed Siena parsing/evaluation and any summary numbers with clear caveats.
