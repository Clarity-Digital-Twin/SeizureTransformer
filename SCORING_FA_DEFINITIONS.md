# NEDC FA/24h Definitions and Reporting Consistency

Why this matters
- We observed confusing comparisons where NEDC TAES appeared to have “better” FA/24h than OVERLAP.
- Cause: we mixed different FA definitions in summaries. TAES lines came from a per‑label (SEIZ) section, while OVERLAP used the TOTAL FA (SEIZ + BCKG) line.

What the NEDC summaries print
- TAES (Time‑Aligned Event Scoring):
  - Per‑label blocks (e.g., LABEL: SEIZ) include “False Alarm Rate: … per 24 hours” for that label only.
  - There is no explicit “Total False Alarm Rate” across labels in the TAES section.
- OVERLAP (Any‑overlap):
  - The OVERLAP section contains both per‑label info and an overall “Total False Alarm Rate: … per 24 hours”, which includes SEIZ + BCKG.

The mismatch we had
- We reported TAES FA/24h from the SEIZ label only.
- We reported OVERLAP FA/24h using OVERALL “Total False Alarm Rate” (SEIZ + BCKG).
- Result: OVERLAP looked worse on FA because it included BCKG false alarms that the TAES number did not.

Reporting policy (to avoid apples‑to‑oranges)
- When comparing TAES vs OVERLAP, choose one of the following and stick to it:
  - Report SEIZ‑only FA/24h for both scorers, or
  - Report TOTAL FA/24h for both scorers (if available).
- If clarity is critical, show both columns:
  - FA/24h (SEIZ)
  - FA/24h (TOTAL)

What we use in current root tables
- FINAL_COMPLETE_RESULTS.md now includes a note that merge_gap is disabled and numbers are verified.
- The current FA/24h entries are taken directly from the NEDC summaries as follows:
  - TAES: SEIZ label’s “False Alarm Rate”.
  - OVERLAP: OVERALL “Total False Alarm Rate”.
- This choice explains why OVERLAP FA/24h appears higher than TAES.

If you need strict apples‑to‑apples
- Use the SEIZ‑only FA/24h for both TAES and OVERLAP (ignore OVERLAP’s TOTAL line), or add both columns explicitly.
- Our native Python OVERLAP (seizure_evaluation/ovlp) also exposes BCKG false alarms, allowing SEIZ‑only and TOTAL to be computed consistently.

Quick extraction tips
- TAES (SEIZ): grep the TAES section for “LABEL: SEIZ” and extract “False Alarm Rate: … per 24 hours”.
- OVERLAP (SEIZ‑only): in OVERLAP, avoid the “Total False Alarm Rate” line and extract SEIZ label’s FA/24h.
- OVERLAP (TOTAL): use “Total False Alarm Rate” from the OVERLAP summary.

Bottom line
- TAES is stricter and typically yields lower sensitivity compared to OVERLAP.
- FA/24h can look inconsistent if you compare TAES (SEIZ‑only) vs OVERLAP (TOTAL). Align definitions to compare fairly.

