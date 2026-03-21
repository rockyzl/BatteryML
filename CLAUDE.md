# BatteryML — AI Assistant Guide

BatteryML is an open-source machine learning platform for **battery degradation prediction** (RUL and SOH), published at ICLR 2024 by Microsoft. This guide covers everything an AI assistant needs to understand the codebase, contribute effectively, and follow project conventions.

---

## Project Overview

Battery cells degrade over cycling. This platform:
1. **Preprocesses** raw cycler data from 7+ public datasets into a unified `BatteryData` format
2. **Extracts features** from cycling patterns (voltage, capacity, variance metrics)
3. **Annotates labels** — Remaining Useful Life (RUL) or State of Health (SOH)
4. **Trains and evaluates** 15 models ranging from linear regression to Transformers
5. **Benchmarks** results across datasets with RMSE metrics

---

## Repository Structure

```
BatteryML/
├── batteryml/               # Main Python package
│   ├── data/                # Core data models (BatteryData, CycleData, DataBundle)
│   ├── feature/             # Feature extractors
│   ├── label/               # Label annotators (RUL, SOH)
│   ├── models/              # ML/DL model implementations
│   │   ├── rul_predictors/  # 15 RUL models
│   │   └── soh_predictors/  # SOH models
│   ├── preprocess/          # Dataset-specific preprocessors
│   ├── train_test_split/    # Dataset splitting strategies
│   ├── utils/               # Registry, config loading utilities
│   ├── visualization/       # Plotting helpers
│   ├── builders.py          # Registry definitions (MODELS, FEATURE_EXTRACTORS, etc.)
│   ├── pipeline.py          # Main training/evaluation orchestration
│   └── task.py              # DataBundle construction from config
├── bin/
│   └── batteryml.py         # CLI entry point
├── configs/
│   ├── baselines/
│   │   ├── sklearn/         # Config files for sklearn-based models
│   │   └── nn_models/       # Config files for neural network models
│   ├── cyclers/             # Cycler device mapping configs (ARBIN, NEWARE, etc.)
│   └── soh/                 # SOH task configs
├── data/                    # (git-ignored) Processed battery cell data (.pkl files)
├── workspaces/              # (git-ignored) Training checkpoints and predictions
├── baseline.ipynb           # Example: RUL prediction walkthrough
├── soh_example.ipynb        # Example: SOH prediction walkthrough
├── result.ipynb             # Example: Results analysis and visualization
├── run_all_rul_baseline.sh  # Script to run all RUL baseline configurations
├── requirements.txt         # Python dependencies
├── setup.py                 # Package configuration
├── dataprepare.md           # Dataset download and preparation guide
└── .flake8                  # Flake8 linting configuration
```

---

## Core Data Models

Located in `batteryml/data/battery_data.py`.

```python
CyclingProtocol          # Charge/discharge protocol spec
  rate_in_C, current_in_A, voltage_in_V, power_in_W
  start/end_voltage, start/end_soc

CycleData                # Single charge/discharge cycle
  cycle_number: int
  voltage_in_V: List[float]
  current_in_A: List[float]
  charge_capacity_in_Ah: List[float]
  discharge_capacity_in_Ah: List[float]
  time_in_s: List[float]
  temperature_in_C: List[float]
  internal_resistance_in_ohm: float
  additional_data: dict   # Extensible custom fields

BatteryData              # Single battery cell
  cell_id: str
  cycle_data: List[CycleData]
  nominal_capacity_in_Ah: float
  anode/cathode/electrolyte_material: str
  form_factor: str
  charge_protocol / discharge_protocol: List[CyclingProtocol]
  reference, description: str
```

`DataBundle` (in `batteryml/data/databundle.py`) wraps train/test splits:
```python
DataBundle
  train_data: Dataset      # (feature_tensor, label_tensor)
  test_data: Dataset
  feature_transformation   # Optional ZScore/LogScale transformation
  label_transformation     # Optional transformation
```

---

## Registry Pattern (Extension Points)

BatteryML uses a `Registry` class (`batteryml/utils/registry.py`) for a plugin architecture. All major components are registered and instantiated dynamically from YAML configs.

**Registries defined in `batteryml/builders.py`:**

| Registry | Base Class | Location |
|---|---|---|
| `MODELS` | `BaseModel` | `batteryml/models/` |
| `PREPROCESSORS` | `BasePreprocessor` | `batteryml/preprocess/` |
| `FEATURE_EXTRACTORS` | `BaseFeatureExtractor` | `batteryml/feature/` |
| `LABEL_ANNOTATORS` | `BaseLabelAnnotator` | `batteryml/label/` |
| `TRAIN_TEST_SPLITTERS` | `BaseTrainTestSplitter` | `batteryml/train_test_split/` |
| `DATA_TRANSFORMATIONS` | `BaseDataTransformation` | `batteryml/data/transformation/` |

**To add a new component:**
1. Create a class inheriting from the appropriate base class
2. Decorate with `@REGISTRY_NAME.register()` (e.g., `@MODELS.register()`)
3. Import it in the relevant `__init__.py` so it registers at startup
4. Reference it by class name in YAML configs

---

## Configuration System

All experiments are driven by YAML config files. Example structure:

```yaml
model:
    name: 'LinearRegressionRULPredictor'   # Registry name
train_test_split:
    name: 'MATRPrimaryTestTrainTestSplitter'
    cell_data_path: 'data/processed/MATR'  # Path to preprocessed data
feature:
    name: 'VarianceModelFeatureExtractor'
    interp_dims: 1000
    critical_cycles: [2, 9, 99]
    use_precalculated_qdlin: True
label:
    name: 'RULLabelAnnotator'
feature_transformation:
    name: 'ZScoreDataTransformation'
label_transformation:
    name: 'SequentialDataTransformation'
    transformations:
        - name: 'LogScaleDataTransformation'
        - name: 'ZScoreDataTransformation'
```

Config files live in `configs/baselines/sklearn/` and `configs/baselines/nn_models/` and use the pattern: `<model_variant>/<dataset_split>.yaml`.

---

## CLI Usage

The `batteryml` CLI (defined in `bin/batteryml.py`) has three commands:

### Download
```bash
batteryml download <dataset> <output_dir>
# dataset: MATR, CALCE, HUST, HNEI, RWTH, SNL, UL_PUR
```

### Preprocess
```bash
batteryml preprocess <input_type> <raw_dir> <output_dir> [--config CONFIG]
# input_type: MATR, CALCE, HUST, HNEI, RWTH, SNL, UL_PUR  (public datasets)
#             ARBIN, BATTERYARCHIVE, BIOLOGIC, INDIGO, LANDT, MACCOR, NEWARE, NOVONIX  (cycler formats)
```

### Run (Train/Eval)
```bash
batteryml run <config.yaml> \
    --workspace ./workspaces \
    --device cpu \          # or cuda:0
    --train \
    --eval \
    --metric RMSE,MAE \
    --seed 0 \
    --epochs 100 \
    --skip_if_executed True
```

---

## Available Models

### RUL Predictors (`batteryml/models/rul_predictors/`)

| Model | Class Name | Type |
|---|---|---|
| Dummy Regressor | `DummyRULPredictor` | Baseline |
| Linear Regression | `LinearRegressionRULPredictor` | Linear |
| Ridge | `RidgeRULPredictor` | Linear |
| Elastic Net | `ElasticNetRULPredictor` | Linear |
| PCR | `PCRRULPredictor` | Linear |
| PLSR | `PLSRRULPredictor` | Linear |
| Gaussian Process | `GaussianProcessRULPredictor` | Statistical |
| SVM | `SVMRULPredictor` | Statistical |
| Random Forest | `RandomForestRULPredictor` | Tree |
| XGBoost | `XGBRULPredictor` | Tree |
| MLP | `MLPRULPredictor` | Neural Net |
| CNN | `CNNRULPredictor` | Neural Net |
| LSTM | `LSTMRULPredictor` | Neural Net |
| Transformer | `TransformerRULPredictor` | Neural Net |

### Feature Extractors (`batteryml/feature/`)

| Class | Description |
|---|---|
| `VarianceModelFeatureExtractor` | Variance of discharge capacity across cycles |
| `DischargeModelFeatureExtractor` | Discharge profile statistics |
| `FullModelFeatureExtractor` | Combined variance + discharge features |
| `VoltageCapacityMatrixFeatureExtractor` | 2D voltage-capacity matrix per cycle |
| `SeversonFeatureExtractor` | Base class for Severson-style features |

### Label Annotators (`batteryml/label/`)

| Class | Description |
|---|---|
| `RULLabelAnnotator` | Cycles remaining until 80% SOH (default threshold) |
| `SOHLabelAnnotator` | State-of-health as fraction of nominal capacity |

---

## Available Datasets

| Dataset | Chemistry | Cells | Notes |
|---|---|---|---|
| MATR | LFP/graphite | 180 | 4 batches, primary and secondary test splits |
| HUST | LFP/graphite | 77 | Various discharge protocols |
| CALCE | LCO/graphite | 13 | CSV/Excel format |
| RWTH | NMC/carbon | 48 | ZIP archive |
| SNL | NCA, NMC, LFP | 61 | Battery Archive CSV |
| UL_PUR | NCA/graphite | 10 | Battery Archive CSV |
| HNEI | NMC_LCO/graphite | 14 | CSV format |

**Combined datasets:** CRUH (CALCE+RWTH+UL_PUR+HNEI), CRUSH (adds SNL), MIX (all)

---

## Development Conventions

### Code Style
- **PEP 8** enforced by flake8 (see `.flake8`)
- Unused imports allowed in `__init__.py` files (F401 ignored)
- Long lines allowed in `scripts/download.py`

### Naming
- **Classes:** CamelCase (e.g., `VarianceModelFeatureExtractor`)
- **Methods/functions:** snake_case (e.g., `process_cell`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `EOL_SOH`)
- **Config keys:** snake_case (e.g., `cell_data_path`, `interp_dims`)

### License Headers
All source files must include the Microsoft MIT license header:
```python
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
```

### Abstract Base Classes
Every major component type has a base class in `base.py` within its directory. Always inherit from the appropriate base:
- Feature extractors → `BaseFeatureExtractor` (must implement `process_cell`)
- Label annotators → `BaseLabelAnnotator` (must implement `process_cell`)
- Models → `BaseModel` or `SklearnModel`/`NNModel` (must implement `fit`, `predict`)
- Preprocessors → `BasePreprocessor`
- Splitters → `BaseTrainTestSplitter` (must implement `split`)
- Transformations → `BaseDataTransformation` (must implement `fit`, `transform`)

### Data Units
Always use SI base units as encoded in attribute names:
- Voltage: `_in_V` (volts)
- Current: `_in_A` (amperes)
- Capacity: `_in_Ah` (ampere-hours)
- Time: `_in_s` (seconds)
- Temperature: `_in_C` (Celsius)
- Resistance: `_in_ohm` (ohms)

---

## Key Implementation Details

### Pipeline Flow (`batteryml/pipeline.py`)

1. Load config (YAML → Python dict via `addict.Dict`)
2. Build `DataBundle` via `Task` class — loads preprocessed `.pkl` files, applies feature extraction, label annotation, and train/test splitting
3. Apply feature/label transformations (fit on train, apply to both)
4. Call `model.fit(train_data)`
5. Call `model.predict(test_data)` and compute metrics (RMSE, MAE, MAPE)
6. Save predictions as `.pkl` in workspace directory

### Neural Network Training (`batteryml/models/nn_model.py`)
- Uses PyTorch `DataLoader` with configurable batch size
- Supports `--device` flag for CPU/GPU selection
- Checkpoint saving/loading via `torch.save`/`torch.load`
- Resume training via `--ckpt-to-resume`

### Preprocessing Pattern
Each dataset preprocessor in `batteryml/preprocess/preprocess_<DATASET>.py`:
- Reads raw files (CSV, .mat, Excel, HDF5)
- Creates `CycleData` objects for each cycle
- Creates `BatteryData` object with all cycles
- Saves as pickle: `<output_dir>/<cell_id>.pkl`

### Config Loading (`batteryml/utils/config.py`)
- Supports both `.yaml` and `.py` config files
- YAML configs parsed via PyYAML
- Python configs loaded as modules

---

## Testing and Validation

There is no formal test suite. Validation is done via:
- Jupyter notebooks (`baseline.ipynb`, `soh_example.ipynb`, `result.ipynb`)
- Shell script `run_all_rul_baseline.sh` to reproduce all baseline results

When modifying code, verify by:
1. Running the relevant notebook end-to-end
2. Running a representative config: `batteryml run configs/baselines/sklearn/variance_model/matr_1.yaml --workspace /tmp/test --train --eval`

---

## Common Tasks

### Adding a New Model

```python
# batteryml/models/rul_predictors/my_model.py
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from ..base import BaseModel
from ..builders import MODELS

@MODELS.register()
class MyModelRULPredictor(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # initialize model

    def fit(self, dataset):
        # train on dataset.feature, dataset.label
        pass

    def predict(self, dataset):
        # return torch.Tensor of predictions
        pass
```

Then import in `batteryml/models/rul_predictors/__init__.py`.

### Adding a New Dataset Preprocessor

```python
# batteryml/preprocess/preprocess_MYDATA.py
from .base import BasePreprocessor
from ..builders import PREPROCESSORS

@PREPROCESSORS.register()
class MYDATAPreprocessor(BasePreprocessor):
    def process(self, input_dir, output_dir):
        # read raw files, create BatteryData objects, save as .pkl
        pass
```

Register in `batteryml/preprocess/__init__.py` and add to CLI in `bin/batteryml.py`.

### Running Benchmarks

```bash
# Run all sklearn baselines on MATR
bash run_all_rul_baseline.sh

# Run a single config
batteryml run configs/baselines/sklearn/variance_model/matr_1.yaml \
    --workspace workspaces/variance_matr \
    --train --eval --seed 0
```

---

## Dependencies

Key packages and their purposes:

| Package | Purpose |
|---|---|
| `numpy>=1.24,<2.0.0` | Numerical arrays (pinned <2.0.0 for API compatibility) |
| `pandas` | Data manipulation for CSV/Excel preprocessing |
| `scipy` | Interpolation, statistical functions |
| `scikit-learn` | Classical ML models + preprocessing |
| `xgboost` | Gradient boosting models |
| `torch` | Neural network models (optional) |
| `addict` | Attribute-style dict access for configs |
| `pyyaml` | YAML config file parsing |
| `numba` | JIT compilation for performance-critical feature extraction |
| `h5py` | Reading HDF5/MATLAB data files |
| `openpyxl` | Reading Excel files |
| `tqdm` | Progress bars in preprocessing |
| `matplotlib` | Visualization |

Install: `pip install -r requirements.txt && pip install -e .`
