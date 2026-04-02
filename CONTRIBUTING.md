# Contributing to BatteryML / 贡献指南

Thank you for your interest in contributing to BatteryML! This guide will help you get started.

感谢您对BatteryML的关注！本指南将帮助您开始贡献。

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Code Style](#code-style)
- [Branch Naming Convention](#branch-naming-convention)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)
- [How to Add a New Model](#how-to-add-a-new-model)
- [How to Add a New Dataset Preprocessor](#how-to-add-a-new-dataset-preprocessor)
- [How to Add a New Feature Extractor](#how-to-add-a-new-feature-extractor)
- [Issues and Discussions](#issues-and-discussions)
- [Code of Conduct](#code-of-conduct)

## Development Environment Setup

1. **Fork and clone the repository:**

   ```bash
   git clone https://github.com/<your-username>/BatteryML.git
   cd BatteryML
   ```

2. **Create a virtual environment (Python 3.8+ recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies and the package in development mode:**

   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Install PyTorch** (required for deep learning models):

   Follow the official instructions at [pytorch.org](https://pytorch.org/get-started/locally/) to install the version matching your CUDA setup.

5. **Install development tools:**

   ```bash
   pip install flake8 pytest pytest-cov black isort
   ```

6. **Verify the installation:**

   ```bash
   batteryml --help
   ```

## Code Style

We follow [PEP 8](https://peps.python.org/pep-0008/) conventions, enforced by **flake8**.

- **Linting:** Run `flake8 batteryml/` before submitting a PR.
- **Line length:** Maximum 120 characters.
- **Formatting (recommended):** Use `black` with default settings and `isort` for import sorting.
- **Docstrings:** Use Google-style docstrings for all public classes and functions.
- **Type hints:** Encouraged for all new code.

Example:

```python
def predict_rul(
    model: BaseModel,
    battery_data: BatteryData,
    n_cycles: int = 100
) -> float:
    """Predict remaining useful life for a battery.

    Args:
        model: A trained prediction model.
        battery_data: Input battery cycling data.
        n_cycles: Number of early cycles to use for prediction.

    Returns:
        Predicted remaining useful life in cycles.
    """
    ...
```

## Branch Naming Convention

Use the following prefixes for your branches:

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New features | `feature/optuna-tuning` |
| `fix/` | Bug fixes | `fix/matr-download-timeout` |
| `docs/` | Documentation updates | `docs/add-colab-tutorial` |
| `refactor/` | Code refactoring | `refactor/model-base-class` |
| `test/` | Adding or updating tests | `test/feature-extractor-unit` |

Always branch from the latest `main`:

```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

## Pull Request Process

1. **Before submitting:**
   - Ensure your code passes `flake8 batteryml/` with no errors.
   - Run existing tests with `pytest` and confirm they pass.
   - Add tests for any new functionality (see [Testing Requirements](#testing-requirements)).
   - Update documentation if your change affects user-facing behavior.

2. **PR description should include:**
   - A clear summary of what the PR does and why.
   - Related issue number (e.g., `Fixes #42` or `Relates to #42`).
   - How to test the changes (steps or commands).
   - Screenshots or output samples if applicable.

3. **PR review:**
   - At least one maintainer approval is required before merging.
   - Address all review comments before requesting re-review.
   - Keep PRs focused — one feature or fix per PR.

4. **After approval:**
   - Squash and merge is the preferred merge strategy.
   - Delete your branch after merging.

## Testing Requirements

- **All new features must include tests.** PRs without tests for new functionality will not be merged.
- **Bug fixes should include a regression test** that verifies the fix.
- Place test files under a `tests/` directory mirroring the source structure:

  ```
  batteryml/models/rul_predictors/ridge.py
  tests/models/rul_predictors/test_ridge.py
  ```

- Run tests:

  ```bash
  pytest tests/                    # Run all tests
  pytest tests/ --cov=batteryml    # Run with coverage report
  pytest tests/models/ -v          # Run specific test directory
  ```

## How to Add a New Model

1. **Choose the appropriate directory:**
   - RUL prediction: `batteryml/models/rul_predictors/`
   - SOH prediction: `batteryml/models/soh_predictors/`

2. **Create a new Python file** (e.g., `my_model.py`) and implement your model by inheriting from the appropriate base class:

   ```python
   # For sklearn-based models, inherit from SklearnModel
   from batteryml.models.sklearn_model import SklearnModel

   class MyModel(SklearnModel):
       def _get_model(self):
           # Return your sklearn model instance
           ...
   ```

   ```python
   # For deep learning models, inherit from NNModel
   from batteryml.models.nn_model import NNModel

   class MyModel(NNModel):
       def __init__(self, ...):
           super().__init__(...)
           # Define your architecture
           ...

       def forward(self, batch):
           # Implement forward pass
           ...
   ```

3. **Register your model** in the corresponding `__init__.py`.

4. **Create a config file** under `configs/` for reproducibility.

5. **Add tests** for your model under `tests/models/`.

6. **Update documentation** with model description and benchmark results if available.

## How to Add a New Dataset Preprocessor

1. **Create a new preprocessor file** at `batteryml/preprocess/preprocess_<DATASET>.py`.

2. **Implement the preprocessing function** following the existing pattern (see `preprocess_MATR.py` as a reference):

   ```python
   def preprocess_<DATASET>(raw_data_path, output_path, ...):
       """Preprocess <DATASET> raw data into BatteryData format.

       Args:
           raw_data_path: Path to the raw data directory.
           output_path: Path to save processed BatteryData files.
       """
       ...
   ```

3. **Register the preprocessor** in `batteryml/preprocess/__init__.py`.

4. **If a download script is needed**, add the download logic and register it so `batteryml download <DATASET>` works.

5. **Add a config file** under `configs/cycler/` if the dataset comes from a specific cycler format.

6. **Test your preprocessor** with sample data and add tests under `tests/preprocess/`.

## How to Add a New Feature Extractor

1. **Create a new feature extractor** at `batteryml/feature/<feature_name>.py`.

2. **Inherit from the base class** in `batteryml/feature/base.py`:

   ```python
   from batteryml.feature.base import BaseFeature

   class MyFeature(BaseFeature):
       def extract(self, battery_data):
           """Extract features from battery data.

           Args:
               battery_data: A BatteryData instance.

           Returns:
               Extracted feature vector (numpy array).
           """
           ...
   ```

3. **Register the feature extractor** in `batteryml/feature/__init__.py`.

4. **Add tests** under `tests/feature/`.

5. **Document the feature** — describe what physical or statistical properties it captures and reference any relevant papers.

## Issues and Discussions

### When to open an Issue

- Bug reports (include steps to reproduce, environment info, and error messages)
- Feature requests with clear use cases
- Data format compatibility problems

### When to use Discussions

- General questions about BatteryML usage
- Ideas for future development (before writing a formal proposal)
- Sharing your research results or use cases
- Asking for help with battery data or model selection

### Issue templates

When opening an issue, please use the appropriate template and include:

- **Bug report:** Environment (OS, Python version, BatteryML version), steps to reproduce, expected vs. actual behavior, error logs.
- **Feature request:** Problem description, proposed solution, alternatives considered.

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). Please review the full text in [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

By participating in this project, you agree to abide by its terms. If you experience or witness unacceptable behavior, please report it to [opencode@microsoft.com](mailto:opencode@microsoft.com).

---

Thank you for contributing to BatteryML! Together we can accelerate battery research and innovation.

感谢您为BatteryML做出贡献！让我们共同加速电池研究与创新。
