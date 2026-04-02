# Sprint 1 Status Board

> Sprint: Physical Feature Augmentation + Test Infrastructure
> Period: 2026-04-02 — 2026-04-30
> Team: ML Engineers, DevOps

---

## Kanban Board

### DONE

*(No tasks completed yet — sprint just started)*

---

### IN PROGRESS

*(No tasks currently in progress)*

---

### TODO

#### TASK-101 — `CoulombicEfficiencyFeatureExtractor`
- [ ] Implement CE computation per cycle (`Q_discharge / Q_charge`)
- [ ] Add mean, std, slope, and per-cycle CE features
- [ ] Handle edge cases (zero charge, missing cycles)
- [ ] Register in `FEATURE_EXTRACTORS` registry
- [ ] Write unit tests (`tests/feature/test_coulombic_efficiency.py`)
- [ ] Create example YAML config (`configs/baselines/sklearn/coulombic_efficiency/matr_1.yaml`)

**Owner:** ML Engineer
**Estimate:** 3 days
**Target:** 2026-04-09

---

#### TASK-102 — `dQdVFeatureExtractor`
- [ ] Implement voltage interpolation onto uniform grid
- [ ] Apply Savitzky-Golay smoothing to dQ/dV curve
- [ ] Extract peak positions, amplitudes, and FWHM via `scipy.signal.find_peaks`
- [ ] Ensure fixed-length feature vector (zero-pad if fewer peaks found)
- [ ] Register in `FEATURE_EXTRACTORS` registry
- [ ] Write unit tests (`tests/feature/test_dqdv.py`)
- [ ] Create example YAML config (`configs/baselines/sklearn/dqdv/matr_1.yaml`)

**Owner:** ML Engineer
**Estimate:** 4 days
**Target:** 2026-04-11

---

#### TASK-103 — pytest Test Suite Setup
- [ ] Create `tests/` directory structure (`__init__.py` files)
- [ ] Write `tests/conftest.py` with `sample_battery_data` and `sample_databundle` fixtures
- [ ] Write smoke tests for `VarianceModelFeatureExtractor`
- [ ] Write fit/predict roundtrip tests for `LinearRegressionRULPredictor`
- [ ] Write `BatteryData` serialization tests
- [ ] Add `pytest.ini` configuration
- [ ] Add `pytest` and `pytest-cov` to `requirements-dev.txt`
- [ ] Verify `pytest tests/` runs under 30 seconds

**Owner:** ML Engineer / DevOps
**Estimate:** 2 days
**Target:** 2026-04-07
**Note:** This task should be started first as other tasks depend on it.

---

#### TASK-104 — GitHub Actions CI/CD
- [ ] Create `.github/workflows/ci.yml`
- [ ] Add lint job (flake8 with existing `.flake8` config)
- [ ] Add test job (pytest with coverage upload)
- [ ] Add build validation job (`pip install -e .`)
- [ ] Configure Python matrix: 3.9, 3.10, 3.11
- [ ] Set up pip dependency caching
- [ ] Add CI status badge to README (if present)

**Owner:** DevOps Engineer
**Estimate:** 1 day
**Target:** 2026-04-10
**Blocked by:** TASK-103 (tests must exist first)

---

#### TASK-105 — Update Module Imports (`__init__.py`)
- [ ] Add `CoulombicEfficiencyFeatureExtractor` import to `batteryml/feature/__init__.py`
- [ ] Add `dQdVFeatureExtractor` import to `batteryml/feature/__init__.py`
- [ ] Verify both classes appear in `FEATURE_EXTRACTORS` at runtime
- [ ] Confirm no circular import errors

**Owner:** ML Engineer
**Estimate:** 0.5 days
**Target:** 2026-04-14
**Blocked by:** TASK-101, TASK-102

---

## Sprint 1 Timeline

```
Week 1 (Apr 02–06)   Week 2 (Apr 07–11)   Week 3 (Apr 14–17)   Week 4 (Apr 22–30)
|                    |                    |                    |
TASK-103 ████████    |                    |                    |
TASK-101       ██████████████             |                    |
TASK-102          ██████████████████      |                    |
TASK-104             |       ████████     |                    |
TASK-105             |                ████|                    |
                     |                    Buffer / Polish      |
```

---

## Sprint 1 Definition of Done

A Sprint 1 task is considered DONE when:

1. Code is implemented and follows project conventions (PEP 8, Microsoft license header, snake_case)
2. The component is registered in its registry and importable from the package
3. Unit tests pass (`pytest tests/` exits with code 0)
4. An end-to-end test with a YAML config on MATR dataset succeeds
5. Code is merged to `master` via a reviewed pull request
6. CI/CD pipeline passes on the merged commit

---

## Sprint 1 Metrics

| Metric | Target |
|--------|--------|
| Tasks completed | 5 / 5 |
| Test coverage (batteryml) | >= 60% |
| CI build time | <= 5 minutes |
| New feature extractors | 2 |
| Open bugs introduced | 0 |

---

## Notes & Blockers

- TASK-103 (pytest setup) is the critical path dependency for TASK-101, TASK-102, and TASK-104. It should be started and completed first.
- No blockers identified at sprint start.
- Real battery data (MATR dataset) is required for end-to-end validation; ensure `data/processed/MATR` is available on the development machine.

---

## Upcoming: Sprint 2 Preview

| Task | Description | Planned Start |
|------|-------------|---------------|
| TASK-201 | `EarlyCycleFeatureExtractor` | 2026-05-01 |
| TASK-202 | MC Dropout uncertainty quantification | 2026-05-05 |
| TASK-203 | MAPIE conformal prediction intervals | 2026-05-14 |
