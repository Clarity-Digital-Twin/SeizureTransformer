# Channels and Montage Policy

Status: Canonical guidance for SeizureTransformer inputs
Last updated: 2025-09-15

Summary
- Model input: 19-channel unipolar (referential) montage at 256 Hz, 60 s windows.
- OSS code asserts unipolar montage and input shape (19, 15360) but does not publish a channel name order.
- To avoid ambiguity, we document a Proposed Standard Channel Order below and recommend enforcing it at load time.

Requirements
- Montage: Unipolar (referential), not bipolar. Reject or convert bipolar recordings.
- Channel count: Exactly 19. Pad/trim only if clinically justified (prefer fail-fast).
- Sampling rate: 256 Hz (resample if needed).
- Windowing: 60 s windows, no overlap at inference.

Proposed Standard Channel Order (TUH 10–20 referential)
1. Fp1
2. Fp2
3. F7
4. F3
5. Fz
6. F4
7. F8
8. T3 (aka T7)
9. C3
10. Cz
11. C4
12. T4 (aka T8)
13. T5 (aka P7)
14. P3
15. Pz
16. P4
17. T6 (aka P8)
18. O1
19. O2

Notes
- Aliases: Some datasets use T7/T8 instead of T3/T4; P7/P8 instead of T5/T6. Normalize names during load.
- If a channel is missing, do not silently substitute; raise and handle explicitly.
- If additional channels are present, select and reorder to the standard 19 layout.

Resolution (validated)
- We rely on `epilepsy2bids>=0.0.6` `Eeg.loadEdfAutoDetectMontage` to normalize TUH/TUSZ unipolar recordings to a 19‑channel referential montage in a stable order.
- Verified on representative TUSZ eval files using `scripts/verify_channel_loading.py` (perfect match to expected indices on test files).
- Known aliases (T7/T8↔T3/T4; P7/P8↔T5/T6) are normalized by the loader; if normalization fails, the pipeline raises with a clear error.

Recommended enforcement
- Add a check in the TUSZ loader to:
  - Validate montage is unipolar.
  - Map aliases (T7→T3, T8→T4, P7→T5, P8→T6) to the standard names.
  - Reorder to the Proposed Standard Channel Order.
  - Fail-fast with a clear error if mapping is incomplete.

Cross-references
- docs/technical/IDEAL_REFERENCE_SEIZURE_TRANSFORMER_DATAFLOW.md (montage validation section)
- docs/analysis/SEIZURE_TRANSFORMER_DATAFLOW_TRACE.md (pipeline verification)
