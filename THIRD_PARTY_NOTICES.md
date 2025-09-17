# Third-Party Notices

This repository includes or integrates with the following third-party software. Please review and comply with their respective licenses.

1) NEDC EEG Eval (v6.0.0)
- Provider: Temple University, Neural Engineering Data Consortium (NEDC)
- Location: `evaluation/nedc_eeg_eval/v6.0.0/`
- Notes: Used for official TAES/OVLP/EPOCH scoring; see the package’s own AAREADME and license files in that directory.

2) epilepsy2bids
- Provider: Upstream project authors
- Usage: Data loading and EDF handling via `Eeg` utilities used by the original SeizureTransformer code.

3) SeizureTransformer (original)
- Provider: Kerui Wu et al.
- Upstream: https://github.com/keruiwu/SeizureTransformer
- Location (vendored): `wu_2025/` (installed via `pip install ./wu_2025`)
- License: MIT (per upstream repository)

See also: `docs/VENDORED_SOURCES.md` for provenance and vendoring policy.

If you are redistributing this repository, ensure all third-party license terms are met. If redistribution of any third-party component is restricted, remove the bundled copy and provide installation instructions instead.
