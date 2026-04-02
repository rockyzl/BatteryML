# Changelog / 变更日志

All notable changes to BatteryML will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Product roadmap (`ROADMAP.md`) with milestones through v3.0
- Contributing guide (`CONTRIBUTING.md`) with development setup and conventions
- This changelog (`CHANGELOG.md`)
- Multi-dimensional evaluation metrics module (`batteryml/evaluation/`): RMSE, MAE, MAPE, R², MedAE, Max Error, Explained Variance with `EvaluationReport` class
- Optuna hyperparameter auto-tuning integration (`batteryml/tuning/`): `OptunaTuner` with configurable search spaces, TPE sampler, and MedianPruner
- Model interpretability module (`batteryml/interpretation/`): `ModelExplainer` with permutation importance, optional SHAP values, built-in tree importance, and `InterpretabilitySummary` report
- Data quality checker (`batteryml/data/quality/`): `DataQualityChecker` with 5 check categories (basic stats, missing data, anomaly detection, consistency, noise estimation) and weighted `QualityReport`
- CSV/Excel universal data importer (`batteryml/preprocess/csv_importer.py`): `CSVBatteryImporter` with auto column detection
- Learning rate schedulers (cosine, step, plateau, onecycle) and early stopping for neural network models
- Gradient clipping support for `NNModel`
- Training history recording in `NNModel.fit()`
- pytest test suite with 12 test files (65+ tests)
- GitHub Actions CI/CD pipeline (lint, test matrix, build)
- Multi-role agent analysis system (`batteryml/agents/`)

### Changed
- `DataBundle.evaluate()` extended with multi-metric support (backward compatible)
- `DataBundle.evaluate_all()` method added for all-metrics evaluation
- `NNModel.predict()` now supports `data_type` parameter

### Fixed
- MAPE division by zero in `DataBundle._evaluate_score()` when target contains zeros
- NaN loss handling in `NNModel.fit()` (now catches both inf and NaN)
- OneCycleLR validation for empty DataLoader
- Redundant capacity check in data quality checker
- Floating-point precision in `explained_variance()` zero-variance check
- Memory leak prevention in `OptunaTuner` via `__del__` cleanup
- Unused imports removed across new modules (flake8 compliance)
- Typo fix: "Traning" -> "Training" in progress bar

## [0.0.1] — 2024-03-14

Initial public release at ICLR 2024.

### Added
- **Core framework** — `BatteryData` unified data format for battery cycling data
- **CLI tool** — `batteryml` command with `download`, `preprocess`, and `run` subcommands
- **8 public datasets** — CALCE, MATR, HUST, HNEI, RWTH, SNL, UL_PUR, OX with download and preprocessing scripts
- **Combined datasets** — CRUH, CRUSH, and MIX for cross-dataset evaluation
- **15 RUL prediction models:**
  - Dummy regressor baseline
  - Linear models: Ridge, Linear Regression, ElasticNet, PCR, PLSR
  - Traditional ML: Gaussian Process, XGBoost, Random Forest, SVM
  - Deep learning: MLP, CNN, LSTM, Transformer
- **5 feature extractors** — Variance model, Discharge model, Full model, Severson features, Voltage-Capacity Matrix
- **Cycler support** — ARBIN and NEWARE data format processing with configurable YAML mappings
- **Config-driven training** — YAML configuration files for reproducible experiments
- **Benchmark results** — Comprehensive RUL prediction benchmarks across all datasets
- **Jupyter notebooks** — `baseline.ipynb`, `result.ipynb`, `soh_example.ipynb` for interactive exploration
- MIT License

[Unreleased]: https://github.com/microsoft/BatteryML/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/microsoft/BatteryML/releases/tag/v0.0.1
