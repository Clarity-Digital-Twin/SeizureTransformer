# SzCORE Clarification - CORRECTED

## Scoring Method Definitions (From Primary Literature)

### SzCORE Methods
1. **SzCORE Sample-based (Epoch)**
   - Compares labels sample-by-sample at 1 Hz
   - Assigns "seizure" if overlap > 50%
   - Duration-weighted
   - **Aligns with NEDC EPOCH (NOT TAES!)**

2. **SzCORE Event-based (Any-Overlap + Tolerances)**
   - Any-overlap scoring
   - Adds clinical tolerances: -30s pre-ictal, +60s post-ictal
   - Merges events <90s apart, splits >5min
   - **More permissive than NEDC OVLP**

### NEDC Methods
1. **NEDC EPOCH**
   - Epoch-based scoring (typically 1 sec epochs)
   - Duration-weighted
   - **Similar to SzCORE Sample-based**

2. **NEDC OVLP (OVERLAP)**
   - Event-based any-overlap
   - Binary scoring (no partial credit)
   - **Similar to SzCORE Event but WITHOUT tolerances**

3. **NEDC TAES (Time-Aligned Event Scoring)**
   - Event-based with FRACTIONAL/PARTIAL credit
   - Scores based on percentage of temporal overlap
   - **NO direct SzCORE equivalent**
   - **Most strict of the event-based methods**

## What We Report in This Paper

**We report SzCORE Event (Any-Overlap + Tolerances)** because:
- It's the default in EpilepsyBench
- Represents clinical tolerance philosophy
- Most directly comparable to authors' Dianalund claims

We do NOT report:
- SzCORE Sample-based (would be redundant with NEDC EPOCH)
- Any EPOCH-based metrics (not clinically interpretable)

## Correct Mapping Table

| Scoring Method | Type | Partial Credit | Tolerances | What We Report |
|---|---|---|---|---|
| NEDC TAES | Event-based | Yes (fractional) | No | ✓ Reported |
| NEDC OVLP | Event-based | No (binary) | No | ✓ Reported |
| SzCORE Event | Event-based | No (binary) | Yes (-30/+60s) | ✓ Reported |
| NEDC EPOCH | Sample-based | N/A | No | ✗ Not reported |
| SzCORE Sample | Sample-based | N/A | No | ✗ Not reported |

## Key Insight: Why the Confusion?

The naming is confusing:
- "SzCORE Epoch" ≠ "NEDC EPOCH" (different context of "epoch")
- SzCORE uses "Sample-based" which aligns with NEDC EPOCH
- TAES is unique to NEDC - it's event-based with fractional credit

## Numbers We Report

All three are EVENT-BASED methods with different philosophies:

1. **NEDC TAES** (strictest - partial credit)
   - Default: 65.21% @ 136.73 FA/24h

2. **NEDC OVLP** (moderate - binary overlap)
   - Default: 45.63% @ 26.89 FA/24h

3. **SzCORE Event** (most permissive - overlap + tolerances)
   - Default: 52.35% @ 8.59 FA/24h

The 15.9× difference (136.73/8.59) between TAES and SzCORE Event reflects:
- TAES's strict partial credit scoring
- SzCORE's permissive clinical tolerances