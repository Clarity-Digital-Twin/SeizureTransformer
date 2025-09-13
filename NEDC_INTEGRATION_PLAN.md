# 🏆 NEDC EVALUATION SYSTEM INTEGRATION PLAN
## From External NEDC Dependencies to Owned Clinical Evaluation Engine

**Branch**: `feature/integrate-nedc-evaluation`  
**Status**: 📋 PLANNING (Requires Senior Sign-off)  
**Target**: Transform NEDC evaluation from external binaries to owned, production-grade clinical assessment system

---

## 🎯 **EXECUTIVE SUMMARY**

**Current State**: External NEDC dependency hell
```
Our Pipeline → NEDC v6.0.0 binaries (external) → TAES scoring
             → Temple's Python libs (external) → CSV parsing
             → Shell scripts (fragile) → Results
```

**Target State**: Owned clinical evaluation engine
```
seizure_evaluation/
├── core/           ← Pure Python NEDC implementation
├── formats/        ← Standard medical data formats  
├── clinical/       ← Clinical deployment metrics
└── research/       ← Research publication metrics
```

**Priority**: **HIGH** - Evaluation bottleneck is preventing clinical deployment (FA/24h = 137.5 vs target ≤10)

---

## 📊 **CURRENT NEDC ARCHITECTURE ANALYSIS**

### Current NEDC Pipeline Structure
```
evaluation/
├── nedc_eeg_eval/v6.0.0/          # Temple's external package
│   ├── bin/nedc_eeg_eval          # C++ binary scorer (black box)
│   ├── lib/                       # Python utilities (poor quality)
│   │   ├── nedc_debug_tools.py    # Debugging utilities  
│   │   ├── nedc_file_tools.py     # File I/O operations
│   │   ├── nedc_mont_tools.py     # Montage handling
│   │   └── nedc_eeg_eval_*.py     # Core evaluation logic
│   └── docs/                      # Limited documentation
└── nedc_scoring/                  # Our integration layer
    ├── convert_predictions.py     # Predictions → CSV_bi format
    ├── post_processing.py         # Threshold, morphology, duration
    ├── run_nedc.py                # Pipeline orchestration
    ├── sweep_operating_point.py   # Parameter optimization
    └── test_pipeline.py           # Validation tests
```

### Current Dependencies & Issues
```python
# External Dependencies (Problems)
evaluation/nedc_eeg_eval/v6.0.0/   # 🔴 Black box C++ binary
├── bin/nedc_eeg_eval              # 🔴 Platform-specific executable
├── lib/*.py                       # 🔴 Poor code quality, no types
└── docs/                          # 🔴 Minimal documentation

# Our Integration Layer (Good)  
evaluation/nedc_scoring/           # ✅ Our clean integration code
├── convert_predictions.py         # ✅ Well-structured conversion
├── post_processing.py            # ✅ Modular post-processing
├── run_nedc.py                   # ✅ Good orchestration
└── sweep_operating_point.py      # ✅ Parameter optimization
```

### Code Quality Assessment
| Component | Quality | Issues | Integration Effort |
|-----------|---------|--------|-------------------|
| **NEDC C++ Binary** | 🔴 Black Box | Opaque, platform-dependent | HIGH (Reverse engineer) |
| **NEDC Python Libs** | 🔴 Poor | No typing, poor structure | HIGH (Rewrite) |
| **Our Integration** | ✅ Good | Minor type issues | LOW (Enhance) |
| **TAES Algorithm** | 🟡 Documented | Complex time-alignment logic | MEDIUM (Implement) |

---

## 🏗️ **TARGET ARCHITECTURE**

### New Evaluation Package Structure
```
seizure_evaluation/
├── __init__.py                    # Package metadata, version
├── core/                         # Core evaluation algorithms
│   ├── __init__.py
│   ├── scorers/
│   │   ├── __init__.py
│   │   ├── base.py               # Abstract base scorer
│   │   ├── taes.py               # Time-Aligned Event Scoring
│   │   ├── ovlp.py               # Overlap-based scoring  
│   │   ├── epoch.py              # Epoch-based scoring
│   │   └── custom.py             # Custom scoring methods
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── clinical.py           # Clinical metrics (FA/24h, sensitivity)
│   │   ├── research.py           # Research metrics (AUROC, F1)
│   │   └── temporal.py           # Time-series specific metrics
│   └── alignment/
│       ├── __init__.py
│       ├── events.py             # Event alignment algorithms
│       └── temporal.py           # Time-based alignment
├── formats/                      # Data format handling
│   ├── __init__.py
│   ├── nedc/
│   │   ├── __init__.py
│   │   ├── csv_bi.py             # CSV_bi format (NEDC standard)
│   │   ├── parser.py             # NEDC file parsing
│   │   └── validator.py          # Format validation
│   ├── annotations/
│   │   ├── __init__.py
│   │   ├── events.py             # Event annotation classes
│   │   └── labels.py             # Label management
│   └── converters/
│       ├── __init__.py
│       ├── predictions.py        # Raw predictions → events
│       └── formats.py            # Cross-format conversion
├── postprocessing/               # Signal post-processing
│   ├── __init__.py
│   ├── thresholding.py          # Adaptive thresholding
│   ├── morphology.py            # Morphological operations
│   ├── duration.py              # Duration filtering
│   ├── merging.py               # Event merging logic
│   └── optimization.py          # Parameter optimization
├── clinical/                     # Clinical deployment tools
│   ├── __init__.py
│   ├── assessment.py            # Clinical viability assessment
│   ├── deployment.py            # Deployment readiness metrics
│   └── reporting.py             # Clinical reports
├── research/                     # Research publication tools
│   ├── __init__.py
│   ├── benchmarks.py            # Research benchmarking
│   ├── comparisons.py           # Cross-method comparisons
│   └── publications.py          # Publication-ready metrics
├── optimization/                 # Parameter optimization
│   ├── __init__.py
│   ├── grid_search.py           # Grid search optimization
│   ├── bayesian.py              # Bayesian optimization
│   ├── genetic.py               # Genetic algorithm optimization
│   └── validators.py            # Cross-validation
└── config/                       # Configuration management
    ├── __init__.py
    ├── base.py                   # Base configuration classes
    ├── clinical.py               # Clinical evaluation configs
    └── research.py               # Research evaluation configs
```

---

## 🎯 **TECHNICAL SPECIFICATIONS**

### NEDC TAES Algorithm Implementation
```python
# core/scorers/taes.py
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

@dataclass
class Event:
    """Represents a seizure event with temporal bounds."""
    start_time: float
    end_time: float
    label: str
    confidence: float = 1.0
    channel: str = "TERM"
    
    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

class AlignmentType(Enum):
    """TAES alignment types."""
    EXACT = "exact"
    OVERLAPPING = "overlapping"
    NEAREST = "nearest"

class TAESScorer:
    """Time-Aligned Event Scoring (TAES) implementation."""
    
    def __init__(self, 
                 tolerance: float = 0.1,
                 alignment: AlignmentType = AlignmentType.OVERLAPPING):
        self.tolerance = tolerance
        self.alignment = alignment
    
    def score(self, 
              reference: List[Event], 
              hypothesis: List[Event]) -> Dict[str, float]:
        """
        Compute TAES metrics.
        
        Returns:
            Dict with sensitivity, specificity, F1, FA/24h
        """
        aligned_pairs = self._align_events(reference, hypothesis)
        return self._compute_metrics(aligned_pairs, reference, hypothesis)
```

### Clinical Metrics Implementation
```python
# clinical/assessment.py
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class ClinicalAssessment:
    """Clinical deployment assessment."""
    sensitivity_percent: float
    fa_per_24h: float
    f1_score: float
    deployment_ready: bool
    clinical_notes: List[str]

class ClinicalEvaluator:
    """Clinical deployment evaluation."""
    
    def __init__(self, 
                 sensitivity_threshold: float = 50.0,
                 fa_threshold: float = 10.0):
        self.sensitivity_threshold = sensitivity_threshold
        self.fa_threshold = fa_threshold
    
    def assess(self, 
               metrics: Dict[str, float],
               duration_hours: float = 24.0) -> ClinicalAssessment:
        """
        Assess clinical deployment readiness.
        
        Clinical Targets:
        - Sensitivity ≥ 50% (detect half of seizures)
        - FA/24h ≤ 10 (max 10 false alarms per day)
        """
        sensitivity = metrics.get("sensitivity_percent", 0.0)
        fa_rate = metrics.get("fa_per_24h", float('inf'))
        f1 = metrics.get("f1_score", 0.0)
        
        deployment_ready = (
            sensitivity >= self.sensitivity_threshold and
            fa_rate <= self.fa_threshold
        )
        
        notes = self._generate_clinical_notes(sensitivity, fa_rate)
        
        return ClinicalAssessment(
            sensitivity_percent=sensitivity,
            fa_per_24h=fa_rate,
            f1_score=f1,
            deployment_ready=deployment_ready,
            clinical_notes=notes
        )
```

### Configuration System
```python
# config/clinical.py
from pydantic import BaseModel, Field
from typing import Optional, List

class PostProcessingConfig(BaseModel):
    """Post-processing parameters for clinical optimization."""
    threshold: float = Field(0.8, ge=0.0, le=1.0)
    kernel_size: int = Field(5, ge=1, le=51)
    min_duration_sec: float = Field(2.0, ge=0.1, le=60.0) 
    merge_gap_sec: Optional[float] = Field(None, ge=0.0, le=120.0)
    
    class Config:
        frozen = True

class ClinicalConfig(BaseModel):
    """Clinical evaluation configuration."""
    sensitivity_threshold: float = Field(50.0, ge=0.0, le=100.0)
    fa_threshold: float = Field(10.0, ge=0.1, le=1000.0)
    scoring_method: str = Field("TAES", regex="^(TAES|OVLP|EPOCH)$")
    postprocessing: PostProcessingConfig = PostProcessingConfig()
    
    class Config:
        frozen = True
```

---

## 📋 **INTEGRATION PHASES**

### **Phase 1: NEDC Format & Basic Scoring (High Priority)**
**Duration**: 4-6 days  
**Branch**: `feature/integrate-nedc-evaluation`

#### Deliverables:
1. **NEDC Format Handling**
   ```python
   # formats/nedc/csv_bi.py
   class CSVBiWriter:
       def write_events(self, events: List[Event], filepath: Path):
           """Write events to NEDC CSV_bi format."""
           
   class CSVBiReader:
       def read_events(self, filepath: Path) -> List[Event]:
           """Read events from NEDC CSV_bi format."""
   ```

2. **Basic TAES Implementation**
   ```python
   # core/scorers/taes.py  
   class TAESScorer:
       def score(self, ref: List[Event], hyp: List[Event]) -> Dict[str, float]:
           """Pure Python TAES implementation."""
   ```

3. **Integration Tests**
   ```python
   # tests/integration/test_nedc_compatibility.py
   def test_taes_matches_nedc_binary():
       """Ensure our TAES matches NEDC v6.0.0 output."""
   ```

#### Success Criteria:
- [ ] CSV_bi format read/write works correctly
- [ ] Basic TAES scorer produces same results as NEDC binary (±0.1%)
- [ ] Integration tests pass
- [ ] Performance within 200% of NEDC binary (acceptable for Python)

### **Phase 2: Clinical Metrics & Assessment**
**Duration**: 3-4 days
**Priority**: High (Needed for deployment decisions)

#### Tasks:
1. **Clinical Metrics Implementation**
   ```python
   # clinical/assessment.py
   class ClinicalMetrics:
       @staticmethod
       def false_alarms_per_24h(events: List[Event], duration_hours: float) -> float:
           """Calculate FA/24h metric."""
           
       @staticmethod
       def sensitivity(ref_events: List[Event], detected_events: List[Event]) -> float:
           """Calculate clinical sensitivity."""
   ```

2. **Automated Assessment**
   ```python
   # clinical/deployment.py
   class DeploymentAssessor:
       def assess_readiness(self, metrics: Dict[str, float]) -> bool:
           """Determine if system is deployment-ready."""
   ```

#### Success Criteria:
- [ ] Clinical metrics match literature standards
- [ ] Automated deployment assessment works
- [ ] FA/24h calculation matches manual verification
- [ ] Sensitivity calculation validated against ground truth

### **Phase 3: Advanced Post-Processing**
**Duration**: 5-7 days
**Priority**: High (Key to reducing FA/24h)

#### Tasks:
1. **Enhanced Post-Processing**
   ```python
   # postprocessing/optimization.py
   class AdaptiveThresholder:
       def optimize_threshold(self, predictions: np.ndarray, 
                            labels: np.ndarray) -> float:
           """Find optimal threshold for target FA rate."""
   
   class MorphologyOptimizer:
       def optimize_kernel(self, events: List[Event], 
                          target_fa: float) -> int:
           """Find optimal morphological kernel size."""
   ```

2. **Parameter Sweeping**
   ```python
   # optimization/grid_search.py
   class ParameterSweeper:
       def sweep_clinical_parameters(self, 
                                   checkpoint: Path,
                                   target_fa_24h: float = 10.0) -> Dict[str, Any]:
           """Comprehensive parameter sweep for clinical targets."""
   ```

#### Success Criteria:
- [ ] Parameter optimization reduces FA/24h to ≤10
- [ ] Maintains sensitivity ≥50%
- [ ] Optimization completes within reasonable time (<2 hours)
- [ ] Results reproducible across runs

### **Phase 4: Research & Publication Tools**
**Duration**: 2-3 days
**Priority**: Medium (Nice to have)

#### Tasks:
1. **Research Benchmarking**
   ```python
   # research/benchmarks.py
   class ResearchBenchmark:
       def compare_with_literature(self, results: Dict[str, float]) -> Dict[str, Any]:
           """Compare results with published benchmarks."""
   ```

2. **Publication Metrics**
   ```python
   # research/publications.py
   class PublicationMetrics:
       def generate_paper_table(self, results: List[Dict]) -> pd.DataFrame:
           """Generate publication-ready results table."""
   ```

#### Success Criteria:
- [ ] Research comparison tools work
- [ ] Publication-ready output formats
- [ ] Literature benchmark comparisons
- [ ] Cross-method evaluation tools

---

## 🧪 **TESTING STRATEGY**

### Test Categories
```python
# Unit Tests (Fast, Isolated)
tests/unit/
├── test_taes_scorer.py         # TAES algorithm tests
├── test_csv_bi_format.py       # Format parsing tests
├── test_clinical_metrics.py    # Clinical calculation tests
└── test_postprocessing.py      # Post-processing tests

# Integration Tests (NEDC Compatibility)
tests/integration/
├── test_nedc_compatibility.py  # Match NEDC v6.0.0 output
├── test_end_to_end.py          # Full pipeline tests
└── test_performance.py         # Performance benchmarks

# Clinical Tests (Real-world Validation)
tests/clinical/
├── test_deployment_ready.py    # Clinical readiness tests
├── test_parameter_sweep.py     # Parameter optimization tests
└── test_literature_match.py    # Literature comparison tests

# Fixtures (Realistic Test Data)
tests/fixtures/
├── data/
│   ├── sample_predictions.pkl  # Realistic predictions
│   ├── sample_events.csv_bi    # Ground truth events
│   └── benchmark_results.json  # Expected NEDC outputs
├── configs/
│   ├── clinical.yaml           # Clinical evaluation config
│   └── research.yaml           # Research evaluation config
└── expected/
    ├── taes_outputs.json       # Expected TAES results
    └── clinical_assessments.json # Expected clinical assessments
```

### Testing Requirements
- **NEDC Compatibility**: 99.9% match with NEDC v6.0.0 binary
- **Performance**: Within 300% of NEDC binary speed (Python overhead acceptable)
- **Clinical Accuracy**: FA/24h calculations within 0.1% of manual verification
- **Coverage Target**: 90% minimum (higher than code due to clinical importance)

---

## 🚦 **SUCCESS CRITERIA**

### Functional Requirements
- [ ] **NEDC Compatibility**: Outputs match NEDC v6.0.0 within 0.1% tolerance
- [ ] **Clinical Targets**: Can achieve FA/24h ≤ 10 with sensitivity ≥ 50%
- [ ] **Performance**: Parameter sweep completes within 2 hours on dev split
- [ ] **Robustness**: Handles edge cases (empty events, malformed files)
- [ ] **Documentation**: All clinical metrics clearly documented with references

### Code Quality Requirements
- [ ] **Type Safety**: 100% mypy compliance (critical for clinical software)
- [ ] **Code Style**: 100% ruff compliance
- [ ] **Test Coverage**: 90% minimum coverage (higher standard for clinical)
- [ ] **Documentation**: All public APIs documented with clinical context
- [ ] **Error Handling**: Comprehensive exception hierarchy with clinical error codes

### Clinical Requirements
- [ ] **Deployment Assessment**: Automated clinical readiness evaluation
- [ ] **Parameter Optimization**: Systematic optimization for clinical targets
- [ ] **Literature Compliance**: Metrics match published standards
- [ ] **Audit Trail**: Full traceability of evaluation decisions
- [ ] **Validation**: Independent validation against manual calculations

---

## 📊 **EXPECTED IMPACT**

### Immediate Benefits
- **FA/24h Reduction**: Target 137.5 → ≤10 (13x improvement)
- **Clinical Viability**: Move from research prototype to deployable system
- **Parameter Optimization**: Systematic rather than manual tuning
- **Reproducibility**: Deterministic evaluation independent of external binaries

### Long-term Benefits
- **Platform Independence**: No reliance on Temple's C++ binaries
- **Extensibility**: Easy to add new scoring methods or clinical metrics
- **Maintenance**: Full control over evaluation pipeline
- **Innovation**: Foundation for novel clinical assessment methods

### Research Impact
- **Publication Quality**: More rigorous evaluation methodology
- **Benchmarking**: Standard evaluation tools for seizure detection
- **Collaboration**: Open-source clinical evaluation tools for community
- **Translation**: Bridge between research metrics and clinical deployment

---

## 🔄 **ROLLOUT STRATEGY**

### Development Workflow
```bash
# 1. Start NEDC integration work
git checkout feature/integrate-nedc-evaluation

# 2. Implement phase (with extensive testing)
make test-clinical   # Clinical test suite
make test-nedc       # NEDC compatibility tests
make benchmark       # Performance benchmarks

# 3. Validate against NEDC binary
python tests/integration/test_nedc_compatibility.py
python tests/clinical/test_parameter_sweep.py

# 4. Clinical validation
python seizure_evaluation/clinical/assessment.py --checkpoint checkpoint.pkl
python seizure_evaluation/optimization/grid_search.py --target-fa 10.0

# 5. Integration with existing pipeline
python evaluation/nedc_scoring/run_nedc.py --use-native-scorer

# 6. Merge to development
git checkout development
git merge feature/integrate-nedc-evaluation
```

### Validation Strategy
- **Parallel Testing**: Run both NEDC binary and our implementation side-by-side
- **Clinical Validation**: Independent manual verification of key metrics
- **Literature Comparison**: Validate against published benchmarks
- **Performance Monitoring**: Continuous performance tracking during development

### Rollback Strategy
- **Keep NEDC binary**: Maintain existing pipeline as fallback
- **Feature flags**: Toggle between native and binary evaluation
- **Performance benchmarks**: Detect regressions immediately
- **Clinical validation**: Independent verification of all changes

---

## 📊 **RISK ASSESSMENT**

### High Risk
- **TAES Algorithm Complexity**: Time-alignment algorithm is non-trivial
  - *Mitigation*: Extensive testing against NEDC binary, literature validation
- **Clinical Metric Accuracy**: Incorrect FA/24h calculation impacts deployment decisions
  - *Mitigation*: Independent validation, manual verification, extensive testing
- **Performance Regression**: Python implementation may be too slow for large sweeps
  - *Mitigation*: Profile early, optimize hot paths, parallel processing

### Medium Risk
- **NEDC Format Changes**: Temple may update format specifications
  - *Mitigation*: Version-locked compatibility, flexible format handling
- **Parameter Space Explosion**: Too many parameters to optimize efficiently
  - *Mitigation*: Start with key parameters, use smart optimization algorithms
- **Clinical Interpretation**: Misunderstanding clinical requirements
  - *Mitigation*: Literature review, expert consultation, validation studies

### Low Risk
- **Test Suite Complexity**: Clinical test suite becomes unwieldy
  - *Mitigation*: Modular test design, automated test generation
- **Documentation Overhead**: Too much documentation slows development
  - *Mitigation*: Automated documentation generation, focus on key APIs

---

## 📅 **TIMELINE & MILESTONES**

| Phase | Duration | Milestone | Deliverables |
|-------|----------|-----------|--------------|
| **Phase 1** | 4-6 days | NEDC Compatibility | CSV_bi format, basic TAES, integration tests |
| **Phase 2** | 3-4 days | Clinical Metrics | FA/24h calculation, sensitivity, deployment assessment |
| **Phase 3** | 5-7 days | Parameter Optimization | Advanced post-processing, parameter sweeps |
| **Phase 4** | 2-3 days | Research Tools | Publication metrics, benchmarking tools |
| **Total** | **14-20 days** | **Clinical Evaluation Engine** | **Production-ready clinical assessment system** |

### Critical Path Dependencies
1. **Phase 1 → Phase 2**: Basic TAES required for clinical metrics
2. **Phase 2 → Phase 3**: Clinical metrics required for optimization targets
3. **Phase 3 → Deployment**: Parameter optimization required for clinical viability

---

## 🎯 **SIGN-OFF REQUIREMENTS**

This plan requires approval on:

### Technical Architecture
- [ ] **NEDC Compatibility**: Strategy for matching NEDC v6.0.0 binary output
- [ ] **Clinical Metrics**: Implementation of FA/24h, sensitivity, clinical assessment
- [ ] **Parameter Optimization**: Grid search and optimization strategy
- [ ] **Testing Strategy**: NEDC compatibility and clinical validation tests
- [ ] **Performance Requirements**: Acceptable performance targets for Python implementation

### Clinical Standards
- [ ] **Clinical Targets**: FA/24h ≤ 10, sensitivity ≥ 50% requirements approved
- [ ] **Deployment Assessment**: Automated clinical readiness evaluation approved
- [ ] **Validation Strategy**: Independent validation and manual verification approved
- [ ] **Literature Compliance**: Metrics alignment with published standards approved
- [ ] **Audit Requirements**: Traceability and documentation requirements approved

### Timeline & Resources
- [ ] **Estimated Duration**: 14-20 days acceptable for clinical-grade system
- [ ] **Milestone Deliverables**: Phase deliverables appropriate for clinical software
- [ ] **Risk Mitigation**: Risk assessment and mitigation strategies approved
- [ ] **Success Criteria**: Clinical and technical success criteria approved
- [ ] **Impact Assessment**: Expected FA/24h improvement and clinical viability approved

---

**SENIOR SIGN-OFF**: _________________________ **DATE**: _____________

**READY TO PROCEED**: ◯ YES ◯ NO ◯ REVISIONS REQUIRED

**PRIORITY vs WU_2025 INTEGRATION**: ◯ NEDC FIRST ◯ WU_2025 FIRST ◯ PARALLEL

---

*This document will be updated as implementation progresses and clinical requirements evolve.*