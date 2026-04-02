# BatteryML Product Roadmap / 产品路线图

## Vision / 愿景

**Make BatteryML the world's leading open-source platform for intelligent battery lifecycle management, bridging the gap between battery science and machine learning.**

将BatteryML打造为全球领先的开源电池全生命周期智能管理平台，连接电池科学与机器学习的桥梁。

## Current Status: v0.0.1 Alpha

BatteryML is currently in its alpha stage, published at ICLR 2024. The platform provides:

- **8 public datasets** — CALCE, MATR, HUST, HNEI, RWTH, SNL, UL_PUR, and OX, plus combined sets (CRUH, CRUSH, MIX)
- **15+ models** — From dummy baselines and linear models (Ridge, PCR, PLSR, ElasticNet, SVM) to tree-based methods (XGBoost, Random Forest) and deep learning architectures (MLP, CNN, LSTM, Transformer)
- **Feature engineering** — Built-in feature extractors including Variance, Discharge, Full, Severson, and Voltage-Capacity Matrix models
- **CLI tool** — `batteryml` command for downloading, preprocessing, training, and evaluation
- **Cycler support** — ARBIN and NEWARE data format processing with configurable field mappings

## Roadmap

### v0.5 — Foundation (Target: Q2 2026)

**Theme: Improve software quality and user experience / 提升软件质量和用户体验**

- [x] pytest test framework with coverage target of 30%
- [x] GitHub Actions CI/CD pipeline (lint, test, build)
- [ ] Google Colab one-click demo notebooks
- [x] CSV/Excel universal data importer for custom datasets
- [x] Multi-dimensional evaluation metrics (MAE / MAPE / R² / MedAE)
- [x] Improved error messages and user-friendly exception handling
- [ ] Bilingual tutorials in English and Chinese / 中英文双语教程
- [ ] Type hints across core modules
- [ ] Automated code formatting with `black` and `isort`

### v1.0 — Core Complete (Target: Q4 2026)

**Theme: Complete core ML functionality and visualization / 完善核心ML功能和可视化**

- [x] Optuna hyperparameter auto-tuning integration
- [x] SHAP model interpretability and feature importance analysis
- [ ] K-Fold cross-validation framework
- [ ] Streamlit Web visualization dashboard
- [ ] MkDocs official documentation site
- [ ] Online Benchmark Leaderboard
- [x] Learning rate schedulers and early stopping mechanisms
- [x] Automated data quality report generation
- [ ] SOH (State of Health) prediction model library expansion
- [ ] Biologic, LANDT, and Indigo cycler support completion

### v2.0 — Enterprise Ready (Target: Q2 2027)

**Theme: Build enterprise-grade capabilities / 构建企业级能力**

- [ ] RESTful online inference API
- [ ] Pack-level battery analysis framework (cell-to-pack modeling)
- [ ] ONNX model export for edge deployment
- [ ] Calendar aging data support
- [ ] Safety early-warning model (thermal runaway, overcharge detection)
- [ ] Maccor cycler support
- [ ] Solid-state battery and sodium-ion battery material support / 固态电池/钠离子电池材料支持
- [ ] Multi-GPU distributed training support
- [ ] Role-based access control for enterprise deployment

### v3.0 — Platform (Target: 2028)

**Theme: Platform ecosystem and next-generation capabilities / 平台化与生态建设**

- [ ] Battery Digital Twin platform / 电池数字孪生平台
- [ ] Federated learning framework for privacy-preserving collaboration / 联邦学习框架
- [ ] Battery Passport compliance (EU regulation) / 电池护照合规
- [ ] Battery Foundation Model (pre-trained on multi-source degradation data) / 电池基础模型
- [ ] Real-time online learning and model updating / 实时在线学习
- [ ] Plugin marketplace for community extensions
- [ ] Integration with battery management system (BMS) hardware

## User Personas / 目标用户

| Priority | Persona | Description |
|----------|---------|-------------|
| **P0** | **Battery Researcher / 电池研究人员** | Academic researchers studying battery degradation mechanisms. Need quick access to public datasets, reproducible benchmarks, and state-of-the-art models to validate hypotheses. |
| **P0** | **ML Engineer / 机器学习工程师** | Data scientists applying ML techniques to battery problems. Need clean APIs, extensible model interfaces, and easy experimentation with hyperparameters and architectures. |
| **P1** | **Battery Test Engineer / 电池测试工程师** | Engineers at battery manufacturers who collect cycling data from test equipment (ARBIN, NEWARE, etc.). Need seamless data import, quality reports, and degradation predictions. |
| **P2** | **EV/ESS Product Manager / 电动汽车/储能产品经理** | Decision-makers who need battery lifetime forecasts and safety assessments to plan warranty policies and maintenance schedules. Need dashboards and interpretable results. |

## How to Contribute / 如何参与

We welcome contributions of all kinds! Please read our [Contributing Guide](./CONTRIBUTING.md) to get started.

Whether you want to fix a bug, add a new model, improve documentation, or propose a new feature, your help is valued. Check out the roadmap items above for inspiration on where to contribute.

For questions and discussions, please use [GitHub Issues](https://github.com/microsoft/BatteryML/issues) and [GitHub Discussions](https://github.com/microsoft/BatteryML/discussions).
