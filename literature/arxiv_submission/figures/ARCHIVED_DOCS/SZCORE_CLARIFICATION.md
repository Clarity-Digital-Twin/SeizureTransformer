# SzCORE Clarification Summary

## Official SzCORE Scoring Modes

SzCORE officially provides two scoring modes:
1. **SzCORE Event** (Any-Overlap with tolerances) - What we report
2. **SzCORE Epoch** (Sample-based/time-aligned) - Not reported

## Our Reporting Decision

**We report only SzCORE Event** throughout the paper because:
- It's the standard mode used by EpilepsyBench
- It represents the clinical tolerance philosophy
- It provides the most meaningful comparison against strict NEDC scoring

## Implementation in Figures

All figures now clarify "SzCORE Event":
- **Figure 1**: Shows "SzCORE Event" in both panels
- **Figure 2**: Legend shows "SzCORE Event"
- **Figure 3**: Flow diagram shows "SzCORE Event"
- **Figure 4**: Caption references NEDC OVERLAP (most relevant for parameter analysis)

## Numbers Reported

**SzCORE Event** (Any-Overlap with tolerances):
- Default (θ=0.80): 52.35% sensitivity @ 8.59 FA/24h
- At NEDC 10‑FA settings (θ=0.88, k=5, d=3.0): 40.59% sensitivity @ 3.36 FA/24h
- Closest to 10 FA: 59.78% sensitivity @ 13.47 FA/24h
- 2.5 FA setting (θ=0.95, k=5, d=5.0): 19.71% sensitivity @ 0.75 FA/24h

## Why Not Report SzCORE Epoch?

We do not report SzCORE Epoch (sample-based) because:
1. It aligns with NEDC EPOCH (per‑second labels) and is not our focus
2. Our emphasis is on event-based metrics used in clinical comparison (TAES/OVERLAP/SzCORE Event)
3. The Event mode is what EpilepsyBench uses for benchmarking

## CSV Updates Complete

All data files updated to specify "SzCORE Event":
- performance_metrics.csv
- operating_curves.csv
- scoring_impact_flow.csv
- All other references

## Manuscript Consistency

The manuscript already correctly describes SzCORE as:
> "SzCORE Any-Overlap extends binary scoring with clinical tolerances: 30-second pre-ictal and 60-second post-ictal windows around each reference event, plus merging of predictions separated by less than 90 seconds"

This is the Event mode, correctly described.
