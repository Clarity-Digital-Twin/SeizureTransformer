# Parameter Tuning Results Tracker
**Started**: September 14, 2025
**Status**: IN PROGRESS

## ✅ Verified Baseline (Paper Default) - UPDATED Sep 14, 20:54
| Params | NEDC TAES | NEDC OVERLAP | Native OVERLAP | SzCORE | Notes |
|--------|-----------|--------------|----------------|---------|-------|
| **t0.80_k5_m2.0** | TBD / TBD FA | 45.63% / 100.06 FA | 45.63% / 100.06 FA | 52.35% / 8.46 FA | **Wu et al. 2025 Default - VERIFIED (no merge)** |

## 🔄 Parameter Sweep Results

### Format: Sensitivity% / FA per 24h (EXACT values)

| Threshold | Kernel | MinDur(s) | TAES Sen/FA | OVERLAP-T Sen/FA | OVERLAP-N Sen/FA | SzCORE Sen/FA | Best Match (Exact FA) |
|-----------|--------|-----------|-------------|------------------|------------------|---------------|--------------|
| 0.80 | 5 | 2.0 | TBD/TBD | 45.63/100.06 | 45.63/100.06 | 52.35/8.46 | Baseline ✅ |
| 0.85 | 5 | 2.0 | - | - | - | - | - |
| 0.85 | 5 | 3.0 | - | - | - | - | - |
| 0.85 | 5 | 4.0 | - | - | - | - | - |
| 0.90 | 5 | 2.0 | - | - | - | - | - |
| 0.90 | 5 | 3.0 | - | - | - | - | - |
| 0.90 | 5 | 4.0 | - | - | - | - | - |
| 0.90 | 5 | 5.0 | - | - | - | - | - |
| 0.92 | 5 | 3.0 | - | - | - | - | - |
| 0.92 | 5 | 4.0 | - | - | - | - | - |
| 0.92 | 5 | 5.0 | - | - | - | - | - |
| 0.94 | 5 | 4.0 | - | - | - | - | - |
| 0.94 | 5 | 5.0 | - | - | - | - | - |
| 0.94 | 5 | 6.0 | - | - | - | - | - |
| 0.96 | 5 | 5.0 | - | - | - | - | - |
| 0.96 | 5 | 6.0 | - | - | - | - | - |
| 0.96 | 5 | 7.0 | - | - | - | - | - |
| 0.98 | 5 | 6.0 | - | - | - | - | - |
| 0.98 | 5 | 7.0 | - | - | - | - | - |
| 0.98 | 5 | 8.0 | - | - | - | - | - |
| 0.99 | 5 | 7.0 | - | - | - | - | - |
| 0.99 | 5 | 8.0 | - | - | - | - | - |

## 🎯 Target Operating Points

### Found Parameters (with EXACT FA values)
| Target FA/24h | Best Params | TAES (Sen% / **Exact FA**) | OVERLAP-T | OVERLAP-N | SzCORE | Status |
|---------------|-------------|----------------------------|-----------|-----------|---------|--------|
| **10 ± 1** | TBD | - / **-** | - | - | - | ⏳ Searching |
| **2.5 ± 0.5** | TBD | - / **-** | - | - | - | ⏳ Searching |
| **1.0 ± 0.2** | TBD | - / **-** | - | - | - | ⏳ Searching |

**Note**: We record EXACT FA values achieved (e.g., "20.5% / **10.2 FA**") not just "~10 FA"

## 📊 Quick Analysis

### FA Reduction Pattern (TAES)
```
Threshold ↑ → FA ↓ (expected)
MinDur ↑ → FA ↓ (expected)
Kernel ↑ → FA ↑ (AVOID!)
```

### Sensitivity vs FA Trade-off
- Best sensitivity: Default (t0.80_k5_m2.0)
- Best FA reduction: TBD (pending sweep)
- Best balance: TBD (pending sweep)

## 📝 Notes

1. **Kernel FIXED at 5** - Previous testing proved larger kernels increase FA
2. **All metrics from eval set** - No dev set contamination
3. **Temple OVERLAP vs Native OVERLAP** - Should match within 0.1%
4. **SzCORE** - Uses different tolerance windows, expect different results

## 🔄 Update Log

- 2025-09-14 18:45: Created tracker, baseline verified
- 2025-09-14 TBD: Parameter sweep started
- 2025-09-14 TBD: Results collection in progress
