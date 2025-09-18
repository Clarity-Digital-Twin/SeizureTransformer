**ArXiv Paper Audit — Scoring Matters: A Reproducible NEDC Evaluation of SeizureTransformer on TUSZ**

- Scope: Reviewed final LaTeX in `literature/arxiv_submission/ARXIV_FINAL_VERSION/FINAL_PAPER.tex`, the assembled draft sources in `literature/arxiv_submission/current_draft/*`, data files under `literature/arxiv_submission/figures/data`, and figure scripts under `literature/arxiv_submission/figures/scripts`.
- Goal: Identify factual inaccuracies, citation issues, internal inconsistencies, and reproducibility gaps; recommend precise fixes with file references.

**Summary**
- Core claims (27×–137× FA/24h gap; NEDC vs SzCORE scoring impact; TUSZ stats; first FA/24h evaluation on TUSZ) are internally consistent and supported by repo data files.
- The final LaTeX generally reflects corrected citations and NEDC naming; however, several source Markdown files still contain outdated or incorrect text, and one figure is synthetic (not data-driven).
- A few quantitative tables and references lack an auditable trail in this repo (appendix error analysis percentages; docs/results paths).

**Critical Findings**
- Synthetic figure (must be replaced with real results):
  - `literature/arxiv_submission/figures/scripts/fig3_parameter_heatmap.py:1` generates a heatmap from synthetic/random values (not from a sweep). The paper includes `FIGURE_3_parameter_heatmap.pdf` as a result figure, which risks misleading readers.
  - Data dictionary acknowledges placeholder status: `literature/arxiv_submission/figures/data/DATA_DICTIONARY.md:30` (“requires regeneration from sweep outputs”).
  - Action: Replace synthetic generation with actual grid-search outputs saved to a CSV (e.g., `parameter_sweep_heatmap.csv`) and regenerate the figure.

- Outdated/incorrect text in source Markdown (draft chain not fully aligned to final LaTeX):
  - Incorrect NEDC expansion (“Neural Event Detection Competition”) persists in the clean MD:
    - `literature/arxiv_submission/FINAL_PAPER_CLEAN.md:35` and `:51` — should be “Neural Engineering Data Consortium (NEDC)”.
  - 75% sensitivity and 1 FA/24h human baseline are still cited to Beniczky 2018 [6] in MD sources; final LaTeX cites Roy 2021 [13] correctly:
    - Wrong in MD: `literature/arxiv_submission/FINAL_PAPER_CLEAN.md:23, 43, 156, 198, 226` (use [13], not [6]).
    - Correct in final LaTeX: `literature/arxiv_submission/ARXIV_FINAL_VERSION/FINAL_PAPER.tex:379, 754` ([13]).
  - Action: Update the Markdown SSOT files and re-run the build chain so the final LaTeX matches sources without manual edits.

**High-Priority Issues**
- Inconsistent F1 values across data files vs tables:
  - Default NEDC OVERLAP F1 is 0.414 in curves data and paper, but 0.396 in summary CSV:
    - Paper-aligned values: `literature/arxiv_submission/figures/data/operating_curves.csv:4` → F1 0.414
    - Conflicting summary: `literature/arxiv_submission/figures/data/key_results_summary.csv:3` → F1 0.396
  - Default SzCORE F1 in paper table (0.5880) conflicts with operating curves (0.485):
    - Paper table value: `literature/arxiv_submission/current_draft/11_appendix.md:7`
    - Curves data: `literature/arxiv_submission/figures/data/operating_curves.csv:23` → 0.485
  - Action: Make a single source of truth for F1. Prefer values computed from the same pipeline that produced `operating_curves.csv` and update the table(s) and `key_results_summary.csv` accordingly.

- Appendix error analysis percentages lack traceability in this repo:
  - Listed percentages have no linked data/artifacts here: `literature/arxiv_submission/ARXIV_FINAL_VERSION/FINAL_PAPER.tex:1443`–`:1479`.
  - Paper references “docs/results/*” multiple times, but that path does not exist in this repo:
    - `literature/arxiv_submission/ARXIV_FINAL_VERSION/FINAL_PAPER.tex:1027, 1314, 1398, 1417`.
  - Action: Either include the analysis artifacts (summaries/notebooks) that produce these percentages and results, or remove/caveat the sections and path references to avoid unverifiable claims.

**Medium-Priority Issues**
- Forward-dated or weakly specified references (confirm at submission):
  - [1] EpilepsyBench Consortium (2025) website; [3] NEDC EEG Evaluation Software v6.0.0 (2025); [10] SeizureTransformer arXiv:2504.00336 (2025); [12] pyEDFlib v0.1.42 (2025) — verify years, versions, and add DOIs/URLs where possible before submission.
  - Examples: `literature/arxiv_submission/ARXIV_FINAL_VERSION/FINAL_PAPER.tex:1087` ([3]) and `:1104`–`:1116` block for [10]–[12].

- Reproducibility commands reference external repo tooling:
  - `tusz-eval`, `nedc-run`, `szcore-run` are referenced but not present here: `literature/arxiv_submission/ARXIV_FINAL_VERSION/FINAL_PAPER.tex:989, 1492, 1494, 1496`.
  - Action: Ensure the external repo tags and instructions are frozen and correct (e.g., a release branch or commit hash), and consider adding a minimal “reproduction README” here that points to exact versions.

- AUROC comparison context could be clearer:
  - Your P0 notes explain 0.9019 (full eval set, 127.7 h) vs 0.876 (paper subset, 42.7 h). That nuance is key.
  - Action: Add a one-sentence note in Results stating the AUROC difference vs the paper arises from different eval durations/sets.

**Low-Priority/Editorial**
- Acknowledgments pluralization vs single author:
  - “authors’ institution” in draft: `literature/arxiv_submission/current_draft/CURRENT_WORKING_DRAFT_ASSEMBLED.md:326` — adjust to “author’s resources/institution” if solo author.
- Ensure consistent use of “Temple University’s Neural Engineering Data Consortium (NEDC)” throughout.
- Round AUROC to two or three decimals consistently (e.g., 0.902).

**Verified Within This Repo**
- TUSZ eval set stats are consistent across text and data:
  - 865 files, 127.7 hours, 469 seizures, 43 patients cited in paper; supported in figure data and draft.
  - Example references in final LaTeX and data files:
    - `literature/arxiv_submission/ARXIV_FINAL_VERSION/FINAL_PAPER.tex:319`–`:332`
    - `literature/arxiv_submission/figures/scripts/fig2_scoring_impact.py:24` (diagram labels)

- Main performance numbers match repo data:
  - Performance metrics CSV (used for Fig. 1):
    - `literature/arxiv_submission/figures/data/performance_metrics.csv:3` SzCORE Event → 8.59 FA/24h, 52.35%
    - `literature/arxiv_submission/figures/data/performance_metrics.csv:4` NEDC OVERLAP → 26.89 FA/24h, 45.63%
    - `literature/arxiv_submission/figures/data/performance_metrics.csv:5` NEDC TAES → 136.73 FA/24h, 65.21%
  - Operating curves CSV (used for Fig. 4):
    - `literature/arxiv_submission/figures/data/operating_curves.csv:4` NEDC OVERLAP default → FA/24h 26.89, Sens 45.63, F1 0.414
    - `literature/arxiv_submission/figures/data/operating_curves.csv:16` TAES at 10 FA target block shows 83.88 FA/24h alt point (consistent with table note)

- Corrected claims present in final LaTeX:
  - NEDC naming fixed (Consortium): `literature/arxiv_submission/ARXIV_FINAL_VERSION/FINAL_PAPER.tex:294, 1064`.
  - 75% sensitivity and human ~1 FA/24h cited to Roy 2021 [13]: `literature/arxiv_submission/ARXIV_FINAL_VERSION/FINAL_PAPER.tex:379, 754`.

**Actionable Fix List**
- Fix sources, then rebuild via the clean chain to eliminate drift:
  - Replace incorrect NEDC expansion in MD:
    - Edit `literature/arxiv_submission/FINAL_PAPER_CLEAN.md:35, 51`
  - Replace [6] → [13] for 75% sensitivity and human 1 FA/24h in MD:
    - Edit `literature/arxiv_submission/FINAL_PAPER_CLEAN.md:23, 43, 156, 198, 226`
  - Regenerate LaTeX/PDF via `literature/arxiv_submission/CLEAN_CONVERSION_CHAIN.sh`

- Reconcile F1 values:
  - Align `literature/arxiv_submission/figures/data/key_results_summary.csv:3-4` with `operating_curves.csv`
  - Update Appendix tables in sources to match the chosen F1 source

- Replace synthetic Fig. 3 with real data:
  - Implement sweep, export `parameter_sweep_heatmap.csv`, and modify `fig3_parameter_heatmap.py` to load and plot real values

- Either include or remove unverifiable references:
  - Add missing `docs/results/*` or remove those mentions from paper (`ARXIV_FINAL_VERSION/FINAL_PAPER.tex:1027, 1314, 1398, 1417`)
  - Add inline “accessed date” or DOIs where only websites are cited

- Minor edits:
  - Acknowledgments: switch to singular “author’s resources” if applicable
  - Consistent AUROC rounding (e.g., 0.902)

**Optional Improvements**
- Add a small top-level `REPRODUCING.md` that pins exact external repo release/tag and reproduces the CLI steps in the paper.
- Include a machine-readable results manifest (JSON/CSV) enumerating each figure/table → exact data source.

**Conclusion**
- With the above fixes, the submission will better align sources and final outputs, remove synthetic placeholders, and strengthen reproducibility and citation accuracy. The principal scientific findings appear well supported by the included data files and scripts.

