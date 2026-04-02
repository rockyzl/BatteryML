# BatteryML Project Task Tracking

> Last Updated: 2026-04-02
> Project: BatteryML — Battery Degradation Prediction Platform (ICLR 2024, Microsoft)

---

## Table of Contents

1. [Sprint Overview](#sprint-overview)
2. [Sprint 1 — Physical Feature Augmentation + Test Infrastructure](#sprint-1)
3. [Sprint 2 — Early-Cycle Prediction + Uncertainty Quantification](#sprint-2)
4. [Sprint 3 — Usability & Integration](#sprint-3)
5. [Dependency Graph](#dependency-graph)
6. [Risk Register](#risk-register)

---

## Sprint Overview

| Sprint | Focus | Status | Target Completion |
|--------|-------|--------|-------------------|
| Sprint 1 | Physical Feature Augmentation + Test Infrastructure | In Progress | 2026-04-30 |
| Sprint 2 | Early-Cycle Prediction + Uncertainty Quantification | Planned | 2026-05-31 |
| Sprint 3 | Usability & Integration | Planned | 2026-06-30 |

---

## Sprint 1

### Goal
Strengthen the feature extraction pipeline with physically meaningful metrics (Coulombic Efficiency, dQ/dV) and establish a formal test infrastructure with CI/CD.

---

### TASK-101: Implement `CoulombicEfficiencyFeatureExtractor`

| Field | Value |
|-------|-------|
| **Owner Role** | ML Engineer |
| **Status** | TODO |
| **Priority** | High |
| **Estimate** | 3 days |

**Description**
Coulombic efficiency (CE) is the ratio of charge extracted during discharge to charge delivered during charge in each cycle. CE is a sensitive early indicator of lithium plating and side reactions, making it valuable for RUL prediction.

**File Paths**
- Implementation: `batteryml/feature/coulombic_efficiency.py`
- Registration: `batteryml/feature/__init__.py`
- Test: `tests/feature/test_coulombic_efficiency.py`
- Example config: `configs/baselines/sklearn/coulombic_efficiency/matr_1.yaml`

**Interface Design**
```python
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from .base import BaseFeatureExtractor
from ..builders import FEATURE_EXTRACTORS

@FEATURE_EXTRACTORS.register()
class CoulombicEfficiencyFeatureExtractor(BaseFeatureExtractor):
    """
    Extracts Coulombic Efficiency features from battery cycling data.

    CE_n = Q_discharge_n / Q_charge_n

    Features extracted per cell:
      - mean_CE: mean CE across all cycles
      - std_CE: standard deviation of CE
      - CE_slope: linear trend slope of CE over cycles
      - CE_at_cycle_k: CE value at specific cycles (configurable)
      - CE_variance_window: rolling variance of CE (window configurable)
    """
    def __init__(
        self,
        critical_cycles: list = None,
        window_size: int = 10,
        **kwargs
    ):
        ...

    def process_cell(self, battery_data: BatteryData) -> np.ndarray:
        ...
```

**Acceptance Criteria**
- [ ] CE computed as `sum(discharge_capacity) / sum(charge_capacity)` per cycle
- [ ] Handles edge cases: zero charge capacity, missing cycles
- [ ] Features include mean, std, slope, and per-critical-cycle CE values
- [ ] Registered as `CoulombicEfficiencyFeatureExtractor` in `FEATURE_EXTRACTORS`
- [ ] Unit tests cover: normal operation, edge cases, correct shape of output
- [ ] Works end-to-end with a YAML config on MATR dataset

**Dependencies**
- TASK-105 (pytest setup) — tests should be written alongside implementation

---

### TASK-102: Implement `dQdVFeatureExtractor`

| Field | Value |
|-------|-------|
| **Owner Role** | ML Engineer |
| **Status** | TODO |
| **Priority** | High |
| **Estimate** | 4 days |

**Description**
The differential capacity (dQ/dV) curve reveals electrochemical phase transitions in the electrode materials. Peak positions and amplitudes shift as the cell degrades. Extracting features from dQ/dV provides interpretable, physics-grounded signals for degradation models.

**File Paths**
- Implementation: `batteryml/feature/dqdv.py`
- Registration: `batteryml/feature/__init__.py`
- Test: `tests/feature/test_dqdv.py`
- Example config: `configs/baselines/sklearn/dqdv/matr_1.yaml`

**Interface Design**
```python
@FEATURE_EXTRACTORS.register()
class dQdVFeatureExtractor(BaseFeatureExtractor):
    """
    Extracts features from the differential capacity (dQ/dV) curve.

    dQ/dV is computed by numerical differentiation of Q w.r.t. V,
    then smoothed with a Savitzky-Golay or Gaussian filter.

    Features extracted:
      - Peak positions (voltage at max dQ/dV per cycle)
      - Peak amplitudes
      - Peak width (FWHM)
      - Area under dQ/dV curve in configurable voltage windows
      - Shift of peak positions relative to cycle 2 (reference)
    """
    def __init__(
        self,
        voltage_range: tuple = (2.0, 3.6),
        n_interp_points: int = 1000,
        smoothing_method: str = 'savgol',  # 'savgol' or 'gaussian'
        smoothing_window: int = 21,
        critical_cycles: list = None,
        **kwargs
    ):
        ...

    def process_cell(self, battery_data: BatteryData) -> np.ndarray:
        ...
```

**Acceptance Criteria**
- [ ] dQ/dV computed via `numpy.gradient` or `scipy.signal` after interpolation onto uniform voltage grid
- [ ] Smoothing applied before peak detection to avoid noise artifacts
- [ ] `scipy.signal.find_peaks` used for peak detection with configurable prominence
- [ ] Feature vector has consistent, documented dimension regardless of number of peaks found (zero-padded if fewer peaks)
- [ ] Registered as `dQdVFeatureExtractor` in `FEATURE_EXTRACTORS`
- [ ] Unit tests cover: smooth curve, noisy curve, missing voltage range data
- [ ] Works end-to-end with a YAML config on MATR dataset

**Dependencies**
- TASK-105 (pytest setup)
- `scipy>=1.9` already in requirements

---

### TASK-103: Set Up pytest Test Suite

| Field | Value |
|-------|-------|
| **Owner Role** | DevOps / ML Engineer |
| **Status** | TODO |
| **Priority** | High |
| **Estimate** | 2 days |

**Description**
The project currently has no formal test suite. This task establishes the pytest infrastructure, shared fixtures, and initial smoke tests for existing components.

**File Paths**
- `tests/__init__.py`
- `tests/conftest.py` — shared fixtures (sample BatteryData, DataBundle)
- `tests/feature/__init__.py`
- `tests/feature/test_variance_model.py` — smoke tests for existing extractor
- `tests/models/__init__.py`
- `tests/models/test_sklearn_models.py` — fit/predict roundtrip tests
- `tests/data/__init__.py`
- `tests/data/test_battery_data.py` — data model serialization tests
- `pytest.ini` or `pyproject.toml` — pytest configuration

**Acceptance Criteria**
- [ ] `pytest tests/` runs without errors from repository root
- [ ] `conftest.py` provides `sample_battery_data` fixture with at least 10 synthetic cycles
- [ ] `conftest.py` provides `sample_databundle` fixture with train/test split
- [ ] Smoke tests exist for `VarianceModelFeatureExtractor`, `LinearRegressionRULPredictor`
- [ ] Tests run in under 30 seconds on a standard laptop (no real data required)
- [ ] `pytest --cov=batteryml` produces a coverage report
- [ ] `pytest-cov` and `pytest` added to `requirements-dev.txt`

**Dependencies**
- None (foundational task)

---

### TASK-104: Configure GitHub Actions CI/CD

| Field | Value |
|-------|-------|
| **Owner Role** | DevOps Engineer |
| **Status** | TODO |
| **Priority** | Medium |
| **Estimate** | 1 day |

**Description**
Automate linting, testing, and build validation on every pull request and push to `master`.

**File Paths**
- `.github/workflows/ci.yml`

**Workflow Design**
```yaml
# Triggers: push to master, all pull requests
# Jobs:
#   lint:    flake8 --config .flake8
#   test:    pytest tests/ --cov=batteryml --cov-report=xml
#   build:   pip install -e . && python -c "import batteryml"
# Matrix: Python 3.9, 3.10, 3.11
# Caching: pip dependency cache keyed on requirements hash
```

**Acceptance Criteria**
- [ ] CI triggers on push to `master` and all PRs targeting `master`
- [ ] Lint job runs `flake8` using existing `.flake8` config
- [ ] Test job runs `pytest tests/` and uploads coverage to Codecov (or equivalent)
- [ ] Build job validates `pip install -e .` succeeds and package imports correctly
- [ ] Matrix covers Python 3.9, 3.10, 3.11
- [ ] Workflow completes in under 5 minutes on GitHub-hosted runners
- [ ] Badge added to `README.md` (if README exists) showing CI status

**Dependencies**
- TASK-103 (tests must exist before CI can run them)

---

### TASK-105: Update Module Imports (`__init__.py`)

| Field | Value |
|-------|-------|
| **Owner Role** | ML Engineer |
| **Status** | TODO |
| **Priority** | Medium |
| **Estimate** | 0.5 days |

**Description**
After implementing new feature extractors, ensure they are imported in the package `__init__.py` so they register with the `FEATURE_EXTRACTORS` registry at startup.

**File Paths**
- `batteryml/feature/__init__.py`

**Changes Required**
```python
# Add to batteryml/feature/__init__.py:
from .coulombic_efficiency import CoulombicEfficiencyFeatureExtractor
from .dqdv import dQdVFeatureExtractor
```

**Acceptance Criteria**
- [ ] `from batteryml.feature import CoulombicEfficiencyFeatureExtractor` works after install
- [ ] `from batteryml.feature import dQdVFeatureExtractor` works after install
- [ ] Both classes appear in `FEATURE_EXTRACTORS` registry at runtime
- [ ] No circular import errors

**Dependencies**
- TASK-101 (CoulombicEfficiencyFeatureExtractor must exist)
- TASK-102 (dQdVFeatureExtractor must exist)

---

## Sprint 2

### Goal
Enable early-cycle RUL prediction using limited cycling data, and quantify prediction uncertainty using ensemble methods.

---

### TASK-201: Implement `EarlyCycleFeatureExtractor`

| Field | Value |
|-------|-------|
| **Owner Role** | ML Engineer |
| **Status** | PLANNED |
| **Priority** | High |
| **Estimate** | 3 days |

**Description**
Severson et al. (2019) demonstrated that features from just the first 100 cycles can predict RUL with high accuracy. This extractor formalizes early-cycle feature extraction as a configurable component, supporting `n_cycles` (e.g., 10, 20, 50, 100) as a parameter.

**File Paths**
- Implementation: `batteryml/feature/early_cycle.py`
- Registration: `batteryml/feature/__init__.py`
- Test: `tests/feature/test_early_cycle.py`
- Config example: `configs/baselines/sklearn/early_cycle/matr_1.yaml`

**Interface Design**
```python
@FEATURE_EXTRACTORS.register()
class EarlyCycleFeatureExtractor(BaseFeatureExtractor):
    def __init__(
        self,
        n_cycles: int = 100,
        feature_types: list = ['variance', 'slope', 'intercept', 'discharge_mean'],
        reference_cycle: int = 10,
        **kwargs
    ):
        ...
```

**Acceptance Criteria**
- [ ] Only uses data from cycles 1..n_cycles (configurable)
- [ ] Raises warning (not error) if a cell has fewer than `n_cycles` cycles
- [ ] Feature types are configurable via YAML
- [ ] Validated on MATR dataset; RMSE should be competitive with published baselines at 100 cycles
- [ ] Unit tests cover cells with fewer cycles than `n_cycles`

**Dependencies**
- TASK-103 (pytest infrastructure)
- TASK-105 (import registration pattern established)

---

### TASK-202: Uncertainty Quantification — MC Dropout

| Field | Value |
|-------|-------|
| **Owner Role** | ML Engineer (Deep Learning) |
| **Status** | PLANNED |
| **Priority** | High |
| **Estimate** | 4 days |

**Description**
Add MC Dropout support to neural network models (`MLPRULPredictor`, `LSTMRULPredictor`, `TransformerRULPredictor`) so that prediction intervals can be estimated by running forward passes with dropout enabled at inference time.

**File Paths**
- Modified: `batteryml/models/nn_model.py`
- Modified: `batteryml/models/rul_predictors/mlp.py`
- Modified: `batteryml/models/rul_predictors/lstm.py`
- Modified: `batteryml/models/rul_predictors/transformer.py`
- New: `batteryml/uncertainty/__init__.py`
- New: `batteryml/uncertainty/mc_dropout.py`
- Test: `tests/uncertainty/test_mc_dropout.py`

**Interface Design**
```python
class MCDropoutMixin:
    """Mixin to add MC Dropout uncertainty estimation to any NNModel."""
    def predict_with_uncertainty(
        self,
        dataset,
        n_samples: int = 100
    ) -> tuple[np.ndarray, np.ndarray]:
        """Returns (mean_predictions, std_predictions)."""
        ...
```

**Acceptance Criteria**
- [ ] `predict_with_uncertainty` returns `(mean, std)` both of shape `(n_samples,)`
- [ ] Dropout is enabled during inference (model.train() mode selectively)
- [ ] `n_samples` configurable via YAML config `uncertainty.mc_samples`
- [ ] Confidence intervals visualizable via existing `batteryml/visualization/` utilities
- [ ] Unit tests confirm std > 0 when dropout_rate > 0

**Dependencies**
- TASK-103 (pytest infrastructure)
- Existing NN models must be stable

---

### TASK-203: Uncertainty Quantification — MAPIE Conformal Prediction

| Field | Value |
|-------|-------|
| **Owner Role** | ML Engineer |
| **Status** | PLANNED |
| **Priority** | Medium |
| **Estimate** | 3 days |

**Description**
MAPIE (Model Agnostic Prediction Interval Estimator) provides distribution-free prediction intervals using conformal prediction. This integrates MAPIE as a wrapper compatible with all `SklearnModel` subclasses.

**File Paths**
- New: `batteryml/uncertainty/conformal.py`
- Modified: `batteryml/models/sklearn_model.py`
- Test: `tests/uncertainty/test_conformal.py`

**Interface Design**
```python
@MODELS.register()
class ConformalRULPredictor(BaseModel):
    """
    Wraps any registered SklearnModel with MAPIE conformal intervals.

    Config example:
      model:
        name: ConformalRULPredictor
        base_model: LinearRegressionRULPredictor
        alpha: 0.1   # 90% coverage
    """
    def predict_interval(self, dataset, alpha: float = 0.1):
        """Returns (lower_bound, upper_bound) arrays."""
        ...
```

**Acceptance Criteria**
- [ ] `mapie` added to `requirements.txt`
- [ ] Works with any `SklearnModel` subclass via config `base_model` field
- [ ] Empirical coverage on MATR test set >= `1 - alpha` (validated in test)
- [ ] Intervals exported to workspace predictions `.pkl` alongside point estimates
- [ ] Unit tests validate coverage guarantee on synthetic data

**Dependencies**
- TASK-103 (pytest infrastructure)
- TASK-202 design patterns inform consistent UQ API

---

## Sprint 3

### Goal
Lower the barrier to entry for new users and enable production deployment via REST API and automated reporting.

---

### TASK-301: CSV/Excel Data Import Wizard

| Field | Value |
|-------|-------|
| **Owner Role** | Software Engineer |
| **Status** | PLANNED |
| **Priority** | High |
| **Estimate** | 5 days |

**Description**
Many researchers have data in CSV or Excel format from custom test benches. This wizard provides an interactive CLI and a programmatic API to map arbitrary column names to the `BatteryData` schema.

**File Paths**
- New: `batteryml/preprocess/preprocess_CSV.py`
- New: `batteryml/preprocess/wizard.py`
- New: `configs/cyclers/CSV_TEMPLATE.yaml`
- Test: `tests/preprocess/test_csv_import.py`

**Interface Design**
```python
@PREPROCESSORS.register()
class CSVPreprocessor(BasePreprocessor):
    """
    Preprocessor for arbitrary CSV/Excel files.

    Requires a column mapping config:
      columns:
        voltage: "Voltage(V)"
        current: "Current(A)"
        capacity: "Capacity(Ah)"
        cycle_number: "Cycle_Index"
        time: "Test_Time(s)"
        temperature: "Temperature (C)"   # optional
    """
    def __init__(self, column_mapping: dict, **kwargs):
        ...
```

**Acceptance Criteria**
- [ ] Supports `.csv` and `.xlsx`/`.xls` files
- [ ] Column mapping specified via YAML config
- [ ] Interactive wizard (`batteryml preprocess CSV --wizard`) prompts user to map columns
- [ ] Handles files with multiple sheets (Excel) and multiple cycle files per cell
- [ ] Produces valid `BatteryData` `.pkl` files compatible with all downstream pipeline steps
- [ ] Unit tests use synthetic CSV data (no external files required)

**Dependencies**
- TASK-103 (pytest infrastructure)

---

### TASK-302: FastAPI REST Interface

| Field | Value |
|-------|-------|
| **Owner Role** | Backend Engineer |
| **Status** | PLANNED |
| **Priority** | High |
| **Estimate** | 6 days |

**Description**
Expose BatteryML's prediction pipeline as a REST API so it can be integrated into external systems (BMS firmware, cloud dashboards, lab automation).

**File Paths**
- New: `batteryml/api/__init__.py`
- New: `batteryml/api/app.py`
- New: `batteryml/api/schemas.py`
- New: `batteryml/api/endpoints/predict.py`
- New: `batteryml/api/endpoints/health.py`
- New: `configs/api/default.yaml`
- Test: `tests/api/test_endpoints.py`

**API Endpoints**
```
GET  /health              — liveness probe
POST /predict/rul         — predict RUL from cycle data payload
POST /predict/soh         — predict SOH from cycle data payload
POST /predict/batch       — batch predictions
GET  /models              — list available registered models
```

**Acceptance Criteria**
- [ ] `fastapi` and `uvicorn` added to `requirements.txt` (optional install group)
- [ ] Server starts with `batteryml serve --config configs/api/default.yaml --port 8000`
- [ ] `POST /predict/rul` accepts JSON payload with cycle data, returns `{"rul": float, "confidence_interval": [float, float]}`
- [ ] OpenAPI docs available at `/docs`
- [ ] Authentication support via API key header (configurable, disabled by default)
- [ ] Integration tests use `httpx.AsyncClient` (no live server required)
- [ ] Docker-compose file provided for containerized deployment

**Dependencies**
- TASK-202 (uncertainty output for confidence intervals)
- TASK-203 (conformal intervals as alternative CI method)

---

### TASK-303: Excel/PDF Report Export

| Field | Value |
|-------|-------|
| **Owner Role** | Software Engineer |
| **Status** | PLANNED |
| **Priority** | Medium |
| **Estimate** | 4 days |

**Description**
Generate automated experiment reports containing model performance metrics, prediction plots, and configuration summaries. Useful for sharing results with non-technical stakeholders.

**File Paths**
- New: `batteryml/reporting/__init__.py`
- New: `batteryml/reporting/excel_report.py`
- New: `batteryml/reporting/pdf_report.py`
- New: `batteryml/reporting/templates/`
- CLI addition: `batteryml report <workspace_dir> --format excel|pdf`

**Acceptance Criteria**
- [ ] Excel report: separate sheets for metrics table, predictions vs. actuals, configuration
- [ ] PDF report: title page, metrics summary, per-cell prediction plots, config appendix
- [ ] Supports all metrics computed by pipeline (RMSE, MAE, MAPE)
- [ ] `openpyxl` (already in requirements) used for Excel; `reportlab` or `weasyprint` for PDF
- [ ] CLI command `batteryml report` added to `bin/batteryml.py`
- [ ] Works on any workspace directory produced by `batteryml run`

**Dependencies**
- TASK-302 is independent; no hard dependency
- Visualization utilities in `batteryml/visualization/` reused for plots

---

## Dependency Graph

```
Sprint 1:
  TASK-103 (pytest setup)
      ↑
  TASK-101 (CoulombicEfficiency) ──→ TASK-105 (update __init__.py)
  TASK-102 (dQdV)               ──↗
      ↑
  TASK-104 (CI/CD) ← depends on TASK-103

Sprint 2:
  TASK-103 (pytest, Sprint 1)
      ↑
  TASK-201 (EarlyCycle)
  TASK-202 (MC Dropout)    ──→ TASK-302 (REST API, Sprint 3)
  TASK-203 (MAPIE Conformal) ──↗

Sprint 3:
  TASK-301 (CSV Import)    — independent
  TASK-302 (REST API)      ← TASK-202, TASK-203
  TASK-303 (Reports)       — largely independent, reuses visualization
```

---

## Risk Register

| Risk ID | Description | Likelihood | Impact | Mitigation |
|---------|-------------|------------|--------|------------|
| R-01 | dQ/dV feature extraction is numerically unstable for noisy voltage data from certain cyclers | Medium | High | Implement robust smoothing (Savitzky-Golay); add voltage monotonicity check; unit-test with synthetic noisy data |
| R-02 | MC Dropout requires changes to existing NN model training loops; may introduce regressions | Medium | High | Use mixin pattern to avoid modifying core training code; add regression tests comparing predictions before/after |
| R-03 | MAPIE library version conflicts with existing scikit-learn pin | Low | Medium | Test in isolated environment; consider vendoring or version-pinning `mapie` alongside `scikit-learn` |
| R-04 | CSV Import Wizard cannot handle all possible column naming conventions from arbitrary instruments | High | Medium | Focus on top-5 most common cycler formats; provide clear error messages guiding users to edit the mapping YAML |
| R-05 | FastAPI REST API introduces a new optional dependency that complicates the install story | Low | Low | Use optional dependency group `pip install batteryml[api]`; keep API code isolated from core package |
| R-06 | CI/CD on GitHub Actions may be slow due to heavy ML dependencies (torch, scipy, etc.) | Medium | Low | Cache pip dependencies; use lightweight test fixtures that don't require loading real data |
| R-07 | Coulombic efficiency edge cases (e.g., zero charge delivered in a cycle) may cause division-by-zero | Medium | Medium | Guard with `np.where(charge > 0, discharge/charge, np.nan)`; propagate NaN gracefully through feature vector |
| R-08 | Sprint 2 UQ features may not generalize well across datasets with different degradation patterns | Medium | High | Validate coverage on MATR, HUST, and CALCE; document dataset-specific calibration requirements |
