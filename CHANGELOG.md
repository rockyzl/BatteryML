# Changelog / 变更日志

All notable changes to BatteryML will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Product roadmap (`ROADMAP.md`) with milestones through v3.0
- Contributing guide (`CONTRIBUTING.md`) with development setup and conventions
- This changelog (`CHANGELOG.md`)

### Changed
- (Planned) pytest test framework targeting 30% coverage
- (Planned) GitHub Actions CI/CD pipeline
- (Planned) Multi-dimensional evaluation metrics (MAE / MAPE / R² / MedAE)

### Fixed
- (Pending) Improved error messages and exception handling

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
