# Licensed under the MIT License.
# Copyright (c) Microsoft Corporation.

"""Hyperparameter tuning utilities for BatteryML.

This sub-package provides integration with Optuna for automated
hyperparameter optimization. Optuna must be installed separately::

    pip install optuna
"""

from batteryml.tuning.optuna_tuner import OptunaTuner

__all__ = ['OptunaTuner']
