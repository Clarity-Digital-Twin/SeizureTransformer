# 🔥 IRONCLAD INTEGRATION PLAN
## SeizureTransformer: From External Dependencies to Owned Architecture

**Branch**: `feature/integrate-wu-transformer`  
**Status**: 📋 PLANNING (Requires Senior Sign-off)  
**Target**: Transform from wrapper to owned, production-grade seizure detection system

Note: This plan covers model/system architecture and packaging. The NEDC evaluation backend and clinical scoring workflow are specified separately in NEDC_INTEGRATION_PLAN.md (SSOT).

---

## 🎯 **EXECUTIVE SUMMARY**

**Current State**: External dependency hell
```
Our Code → wu_2025 (external) → model.pth
         → NEDC (external) → scoring
```

**Target State**: Full ownership & control
```
seizure_transformer/
├── core/           ← Refactored wu_2025 (our standards)
├── evaluation/     ← Enhanced NEDC integration  
├── data/           ← Universal dataset support
└── cli/            ← Production-ready interfaces
```

---

## 📊 **CURRENT ARCHITECTURE ANALYSIS**

### wu_2025 Package Structure
```
wu_2025/
├── src/wu_2025/
│   ├── __init__.py         # Minimal
│   ├── __main__.py         # CLI entry point
│   ├── main.py             # Core inference logic
│   ├── architecture.py     # SeizureTransformer model
│   ├── utils.py            # Data loading, preprocessing
│   └── model.pth          # Pretrained weights (168MB)
├── data/                   # Datasets (gitignored)
│   ├── tusz/              # Temple University Hospital
│   └── siena/             # Competition dataset
└── pyproject.toml         # Basic packaging
```

### Key Dependencies
```python
# Core ML Stack
torch>=2.0.1            # Model architecture & inference
numpy>=1.25             # Array operations
scipy>=1.14.1           # Signal processing (filters, morphology)
epilepsy2bids>=0.0.6    # EDF file loading

# Our Evaluation Stack  
scikit-learn>=1.3.0     # ROC curves, metrics
pandas>=2.0.0           # Data manipulation
matplotlib>=3.7.0       # Visualization
```

### Code Quality Assessment
| Component | Quality | Issues | Integration Effort |
|-----------|---------|--------|-------------------|
| `architecture.py` | 🟡 Medium | No typing, docs | Medium |
| `utils.py` | 🔴 Low | Hardcoded paths, no error handling | High |
| `main.py` | 🔴 Low | Monolithic, no separation of concerns | High |
| Model weights | ✅ Good | N/A (just load) | Low |

---

## 🏗️ **TARGET ARCHITECTURE**

### New Package Structure
```
seizure_transformer/
├── __init__.py                     # Package metadata, version
├── core/                          # Core model & inference
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── transformer.py         # SeizureTransformer (refactored)
│   │   ├── config.py              # Model configuration classes  
│   │   └── weights.py             # Weight loading utilities
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── pipeline.py            # Preprocessing pipeline
│   │   ├── filters.py             # Signal processing
│   │   └── transforms.py          # Data transformations
│   └── inference/
│       ├── __init__.py
│       ├── engine.py              # Inference engine
│       └── postprocessing.py      # Event detection, morphology
├── data/                          # Data loading & management
│   ├── __init__.py
│   ├── loaders/
│   │   ├── __init__.py
│   │   ├── base.py                # Abstract base loader
│   │   ├── edf.py                 # EDF file support
│   │   ├── tusz.py                # TUSZ dataset loader
│   │   └── siena.py               # Siena dataset loader
│   └── datasets/
│       ├── __init__.py
│       └── seizure.py             # PyTorch Dataset classes
├── evaluation/                    # Evaluation & metrics
│   ├── __init__.py
│   ├── metrics/
│   │   ├── __init__.py
│   │   ├── clinical.py            # Clinical metrics (FA/24h, sensitivity)
│   │   └── research.py            # Research metrics (AUROC, F1)
│   ├── scorers/
│   │   ├── __init__.py
│   │   ├── nedc.py                # NEDC/TAES integration
│   │   └── standard.py            # Standard ML metrics
│   └── experiments/
│       ├── __init__.py
│       ├── runner.py              # Experiment execution
│       └── tracker.py             # Results tracking
├── cli/                           # Command-line interfaces
│   ├── __init__.py
│   ├── predict.py                 # Single file prediction
│   ├── evaluate.py                # Batch evaluation
│   └── tune.py                    # Parameter tuning
└── config/                        # Configuration management
    ├── __init__.py
    ├── base.py                    # Base configuration classes
    ├── model.py                   # Model configurations
    └── evaluation.py              # Evaluation configurations
```

---

## 🎯 **TECHNICAL SPECIFICATIONS**

### Python Environment
- **Minimum Python**: 3.10 (for modern typing)
- **Package Manager**: UV (for speed & reproducibility)
- **Dependency Locking**: uv.lock (pinned dependencies)

### Code Quality Standards
```python
# Type Safety
from typing import Protocol, TypeVar, Generic
from dataclasses import dataclass, field
from pathlib import Path

# Error Handling  
from seizure_transformer.exceptions import (
    ModelLoadError,
    PreprocessingError,
    EvaluationError
)

# Configuration
from pydantic import BaseModel, Field, validator
```

### Test Suite Configuration
```toml
# pyproject.toml
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--disable-warnings", 
    "--cov=seizure_transformer",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=85"
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests", 
    "slow: Slow tests requiring data/models",
    "gpu: Tests requiring CUDA"
]
```

### Linting & Type Checking
```toml
[tool.ruff]
target-version = "py310"
line-length = 100
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings  
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
no_implicit_optional = true
check_untyped_defs = true
```

---

## 📋 **INTEGRATION PHASES**

### **Phase 1: Foundation & Testing Infrastructure**
**Duration**: 3-5 days  
**Branch**: `feature/integrate-wu-transformer`

#### Deliverables:
1. **Project Structure Setup**
   ```bash
   mkdir -p seizure_transformer/{core,data,evaluation,cli,config}
   mkdir -p seizure_transformer/core/{models,preprocessing,inference}
   mkdir -p seizure_transformer/data/{loaders,datasets}  
   mkdir -p seizure_transformer/evaluation/{metrics,scorers,experiments}
   mkdir -p tests/{unit,integration,fixtures}
   ```

2. **Configuration Management**
   ```python
   # config/base.py
   from pydantic import BaseModel
   from pathlib import Path
   
   class BaseConfig(BaseModel):
       class Config:
           frozen = True
           extra = "forbid"
   
   # config/model.py  
   class ModelConfig(BaseConfig):
       in_channels: int = 19
       in_samples: int = 15360
       drop_rate: float = 0.1
       device: str = "auto"
   ```

3. **Test Infrastructure** 
   ```python
   # tests/fixtures/model.py
   @pytest.fixture
   def mock_eeg_data():
       return np.random.randn(19, 15360).astype(np.float32)
   
   # tests/fixtures/data.py
   @pytest.fixture  
   def sample_edf_path():
       return Path("tests/data/sample.edf")
   ```

#### Success Criteria:
- [ ] Package structure created
- [ ] Configuration classes implemented
- [ ] Test fixtures ready
- [ ] All imports work correctly
- [ ] `make test` passes (even with empty implementations)

### **Phase 2: Core Model Integration**
**Duration**: 4-6 days  
**Priority**: High (Foundation for everything else)

#### Tasks:
1. **Extract & Refactor SeizureTransformer**
   ```python
   # core/models/transformer.py
   from typing import Dict, Any, Optional
   from dataclasses import dataclass
   import torch.nn as nn
   
   @dataclass
   class TransformerConfig:
       in_channels: int = 19
       in_samples: int = 15360  
       drop_rate: float = 0.1
       filters: list[int] = field(default_factory=lambda: [32, 64, 128, 256])
   
   class SeizureTransformer(nn.Module):
       def __init__(self, config: TransformerConfig):
           super().__init__()
           self.config = config
           # ... refactored architecture
   ```

2. **Weight Loading System**
   ```python
   # core/models/weights.py
   from pathlib import Path
   from typing import Union
   
   class WeightLoader:
       @staticmethod
       def load_pretrained(
           model: SeizureTransformer, 
           weights_path: Union[str, Path],
           device: str = "auto"
       ) -> SeizureTransformer:
           # Robust weight loading with validation
   ```

3. **Inference Engine**
   ```python  
   # core/inference/engine.py
   class InferenceEngine:
       def __init__(self, model: SeizureTransformer, device: str = "auto"):
           self.model = model
           self.device = self._setup_device(device)
       
       def predict_edf(self, edf_path: Path) -> np.ndarray:
           # Clean prediction interface
   ```

#### Success Criteria:
- [ ] Model loads weights successfully
- [ ] Inference produces same outputs as wu_2025
- [ ] All model tests pass
- [ ] Type checking passes
- [ ] Performance within 5% of original

### **Phase 3: Data Pipeline Unification**  
**Duration**: 3-5 days
**Priority**: High (Required for evaluation)

#### Tasks:
1. **Abstract Data Loader**
   ```python
   # data/loaders/base.py
   from abc import ABC, abstractmethod
   from typing import Protocol, Iterator
   
   class EEGLoader(Protocol):
       def load(self, file_path: Path) -> tuple[np.ndarray, float]:
           """Load EEG data and return (data, sampling_rate)"""
           ...
   
   class BaseEEGLoader(ABC):
       @abstractmethod
       def load(self, file_path: Path) -> tuple[np.ndarray, float]:
           pass
       
       @abstractmethod  
       def validate(self, data: np.ndarray) -> bool:
           pass
   ```

2. **Preprocessing Pipeline**
   ```python
   # core/preprocessing/pipeline.py
   from dataclasses import dataclass
   from typing import Optional, Callable
   
   @dataclass
   class PreprocessingConfig:
       target_fs: int = 256
       bandpass: tuple[float, float] = (0.5, 120.0)  
       notch_freq: float = 60.0
       z_score: bool = True
   
   class PreprocessingPipeline:
       def __init__(self, config: PreprocessingConfig):
           self.config = config
           
       def __call__(self, data: np.ndarray, fs: float) -> np.ndarray:
           # Modular preprocessing chain
   ```

#### Success Criteria:
- [ ] All dataset loaders work consistently
- [ ] Preprocessing produces identical outputs to wu_2025
- [ ] Data validation catches edge cases
- [ ] Memory usage optimized for large files
- [ ] Integration tests pass

### **Phase 4: Evaluation System Enhancement**
**Duration**: 4-6 days  
**Priority**: Medium (Builds on existing work)

#### Tasks:
1. **Metrics Unification**
   ```python
   # evaluation/metrics/clinical.py
   class ClinicalMetrics:
       @staticmethod
       def false_alarms_per_24h(
           predictions: np.ndarray, 
           labels: np.ndarray,
           fs: int = 256
       ) -> float:
           # Standardized FA/24h calculation
   
       @staticmethod  
       def sensitivity(predictions: np.ndarray, labels: np.ndarray) -> float:
           # Clinical sensitivity metric
   ```

2. **NEDC Integration Enhancement**  
   ```python
   # evaluation/scorers/nedc.py
   from pathlib import Path
   from typing import Dict, Any
   
   class NEDCScorer:
       def __init__(self, nedc_root: Path):
           self.nedc_root = nedc_root
           
       def score_predictions(
           self, 
           predictions: Dict[str, np.ndarray],
           ground_truth: Dict[str, list],
           output_dir: Path
       ) -> Dict[str, float]:
           # Enhanced NEDC scoring with better error handling
   ```

#### Success Criteria:
- [ ] Metrics match existing evaluation pipeline  
- [ ] NEDC integration more robust
- [ ] Clinical assessment automated
- [ ] Results reproducible
- [ ] Performance tracking integrated

### **Phase 5: CLI & Production Interface**
**Duration**: 2-3 days
**Priority**: Low (Polish & usability)

#### Tasks:
1. **Command-Line Interface**
   ```python
   # cli/predict.py
   import click
   from pathlib import Path
   
   @click.command()
   @click.argument('input_file', type=click.Path(exists=True))
   @click.argument('output_file', type=click.Path())
   @click.option('--config', type=click.Path(), help='Configuration file')
   def predict(input_file: str, output_file: str, config: Optional[str]):
       """Predict seizures from EDF file"""
       # Clean CLI interface
   ```

2. **Configuration Files**
   ```yaml
   # config/default.yaml
   model:
     in_channels: 19
     in_samples: 15360
     drop_rate: 0.1
     
   preprocessing:
     target_fs: 256
     bandpass: [0.5, 120.0]
     notch_freq: 60.0
     
   inference:
     batch_size: 1
     device: auto
     
   postprocessing:
     threshold: 0.8
     kernel_size: 5
     min_duration_sec: 2.0
   ```

#### Success Criteria:
- [ ] CLI matches wu_2025 functionality
- [ ] Configuration system works
- [ ] Help documentation complete
- [ ] Error messages user-friendly
- [ ] Backwards compatibility maintained

---

## 🧪 **TESTING STRATEGY**

### Test Categories
```python
# Unit Tests (Fast, Isolated)
tests/unit/
├── test_models.py          # Model architecture tests
├── test_preprocessing.py   # Signal processing tests  
├── test_inference.py       # Inference engine tests
└── test_metrics.py         # Metric calculation tests

# Integration Tests (Realistic Workflows)  
tests/integration/
├── test_end_to_end.py      # Full pipeline tests
├── test_data_loading.py    # Dataset loading tests
└── test_evaluation.py      # Evaluation pipeline tests

# Fixtures (Reusable Test Data)
tests/fixtures/
├── data/
│   ├── sample.edf          # Small test EDF file
│   ├── sample.csv_bi       # Ground truth labels
│   └── corrupt.edf         # Error handling test
├── models/
│   └── test_weights.pth    # Minimal model weights
└── expected/
    └── outputs.pkl         # Expected inference results
```

### Testing Requirements
- **Coverage Target**: 85% minimum
- **Performance Tests**: Inference time benchmarks  
- **Memory Tests**: Memory usage validation
- **GPU Tests**: CUDA functionality (if available)
- **Error Tests**: Graceful failure handling

---

## 🚦 **SUCCESS CRITERIA**

### Functional Requirements
- [ ] **Accuracy**: Outputs match wu_2025 within 0.001% tolerance
- [ ] **Performance**: Inference time within 110% of original
- [ ] **Memory**: Memory usage within 120% of original  
- [ ] **Robustness**: Handles malformed inputs gracefully
- [ ] **Compatibility**: Works with existing evaluation pipeline

### Code Quality Requirements
- [ ] **Type Safety**: 100% mypy compliance
- [ ] **Code Style**: 100% ruff compliance
- [ ] **Test Coverage**: 85% minimum coverage
- [ ] **Documentation**: All public APIs documented
- [ ] **Error Handling**: Comprehensive exception hierarchy

### Integration Requirements  
- [ ] **Drop-in Replacement**: Can replace wu_2025 with minimal changes
- [ ] **Configuration**: Fully configurable without code changes
- [ ] **Extensibility**: Easy to add new datasets/models
- [ ] **Monitoring**: Built-in performance/error monitoring
- [ ] **Deployment**: Production-ready packaging

---

## 🔄 **ROLLOUT STRATEGY**

### Development Workflow
```bash
# 1. Start feature work
git checkout feature/integrate-wu-transformer

# 2. Implement phase (with tests)
make test        # Must pass
make lint        # Must pass  
make typecheck   # Must pass

# 3. Integration testing
python -m seizure_transformer.cli.predict tests/fixtures/data/sample.edf output.tsv
python -m seizure_transformer.cli.evaluate --config tests/fixtures/config/test.yaml

# 4. Performance validation
python tests/benchmarks/compare_wu2025.py

# 5. Merge to development
git checkout development
git merge feature/integrate-wu-transformer

# 6. Final validation on development  
make check-all
python tests/integration/test_end_to_end.py

# 7. Merge to main (when ready)
git checkout main  
git merge development
```

### Rollback Strategy
- **Keep wu_2025 intact** until full validation complete
- **Feature flags** to switch between implementations
- **Performance benchmarks** to detect regressions  
- **Automated testing** to catch breaking changes

---

## 📊 **RISK ASSESSMENT**

### High Risk
- **Weight Loading**: Model weights may not transfer correctly
  - *Mitigation*: Extensive numerical validation tests
- **Preprocessing Differences**: Subtle signal processing variations
  - *Mitigation*: Bit-exact comparison with wu_2025 outputs
- **Performance Regression**: Refactored code may be slower
  - *Mitigation*: Continuous benchmarking during development

### Medium Risk  
- **API Compatibility**: Breaking changes to existing evaluation code
  - *Mitigation*: Comprehensive integration tests
- **Configuration Complexity**: Over-engineering configuration system
  - *Mitigation*: Start simple, add complexity only when needed
- **Testing Overhead**: Test suite becomes too slow
  - *Mitigation*: Separate fast/slow tests, parallel execution

### Low Risk
- **Documentation Debt**: Insufficient documentation  
  - *Mitigation*: Documentation as part of definition-of-done
- **Dependency Conflicts**: New dependencies conflict with existing
  - *Mitigation*: UV lock files, container-based testing

---

## 📅 **TIMELINE & MILESTONES**

| Phase | Duration | Milestone | Deliverables |
|-------|----------|-----------|--------------|
| **Phase 1** | 3-5 days | Foundation Complete | Project structure, configs, test infrastructure |
| **Phase 2** | 4-6 days | Model Integration | Refactored model, weight loading, inference engine |
| **Phase 3** | 3-5 days | Data Pipeline | Unified data loading, preprocessing pipeline |
| **Phase 4** | 4-6 days | Enhanced Evaluation | Improved metrics, NEDC integration |
| **Phase 5** | 2-3 days | Production Polish | CLI interfaces, documentation |
| **Total** | **16-25 days** | **Full Integration** | **Production-ready seizure detection system** |

---

## 🎯 **SIGN-OFF REQUIREMENTS**

This plan requires approval on:

### Technical Architecture
- [ ] **Package Structure**: Directory layout and module organization
- [ ] **Configuration System**: YAML configs + Pydantic validation  
- [ ] **Testing Strategy**: Unit/integration tests + fixtures
- [ ] **Type Safety**: Full mypy compliance strategy
- [ ] **Error Handling**: Exception hierarchy and error recovery

### Quality Standards
- [ ] **Code Coverage**: 85% minimum coverage target
- [ ] **Performance**: 110% of wu_2025 performance maximum  
- [ ] **Documentation**: All public APIs documented
- [ ] **Backwards Compatibility**: Drop-in replacement for wu_2025
- [ ] **Deployment**: Production-ready packaging

### Timeline & Resources
- [ ] **Estimated Duration**: 16-25 days acceptable
- [ ] **Milestone Deliverables**: Phase deliverables appropriate
- [ ] **Risk Mitigation**: Risk assessment and mitigation strategies approved
- [ ] **Rollback Strategy**: Rollback plan approved
- [ ] **Success Criteria**: Functional and quality requirements approved

---

**SENIOR SIGN-OFF**: _________________________ **DATE**: _____________

**READY TO PROCEED**: ◯ YES ◯ NO ◯ REVISIONS REQUIRED

---

*This document will be updated as implementation progresses and requirements evolve.*
