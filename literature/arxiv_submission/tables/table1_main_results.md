# Table 1: Main Performance Results

## Default Configuration (θ=0.80, k=5, d=2.0)

| Scoring Method | Sensitivity (%) | FA/24h  | Multiplier vs Claimed | F1 Score |
|:---------------|----------------:|--------:|----------------------:|---------:|
| **Dianalund (Claimed)** | 37.00 | 1.00 | 1× | 0.43* |
| SzCORE | 52.35 | 8.59 | 9× | 0.485 |
| NEDC OVERLAP | 45.63 | 26.89 | **27×** | 0.396 |
| Native OVERLAP | 45.63 | 26.89 | **27×** | 0.396 |
| NEDC TAES | 60.45 | 136.73 | **137×** | 0.237 |

*F1 score from competition leaderboard

## Clinical 10 FA/24h Target (θ=0.88, k=5, d=3.0)

| Scoring Method | Sensitivity (%) | FA/24h  | Clinical Goal Met† |
|:---------------|----------------:|--------:|:------------------:|
| SzCORE | 40.59 | 3.36 | ✗ |
| NEDC OVERLAP | 33.90 | 10.27 | ✗ |
| Native OVERLAP | 33.90 | 10.27 | ✗ |
| NEDC TAES | 47.76 | 51.29 | ✗ |

†Clinical goal: ≥75% sensitivity at ≤10 FA/24h (Roy et al., 2021)

## Ultra-Conservative 2.5 FA/24h Target (θ=0.95, k=5, d=5.0)

| Scoring Method | Sensitivity (%) | FA/24h |
|:---------------|----------------:|-------:|
| SzCORE | 19.71 | 0.75 |
| NEDC OVERLAP | 14.50 | 2.05 |
| Native OVERLAP | 14.50 | 2.05 |
| NEDC TAES | 21.32 | 10.84 |

**Table 1:** Performance comparison across scoring methodologies at three operating points. The same SeizureTransformer model predictions yield dramatically different metrics depending solely on the evaluation standard applied. Bold values indicate performance gaps exceeding one order of magnitude compared to the claimed Dianalund results.