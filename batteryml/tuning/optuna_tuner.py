# Licensed under the MIT License.
# Copyright (c) Microsoft Corporation.

"""Optuna-based hyperparameter auto-tuning for BatteryML models.

This module provides the OptunaTuner class which integrates Optuna's
hyperparameter optimization framework with BatteryML's Pipeline to
enable automated search for optimal model hyperparameters.
"""

from __future__ import annotations

import copy
import shutil
import tempfile
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

import yaml

try:
    import optuna
    from optuna.pruners import MedianPruner
except ImportError:
    raise ImportError(
        "Optuna is required for hyperparameter tuning but is not installed. "
        "Please install it with: pip install optuna\n"
        "Optionally install optuna-dashboard for visualization: "
        "pip install optuna-dashboard"
    )

from batteryml.pipeline import Pipeline

logger = logging.getLogger(__name__)


class OptunaTuner:
    """Optuna-based hyperparameter auto-tuning for BatteryML models.

    Wraps Optuna's study API to search over hyperparameters defined in a
    search space, evaluating each trial by training and evaluating a
    BatteryML Pipeline.

    Args:
        config_path: Path to a BatteryML YAML configuration file.
        search_space: Dictionary mapping dotted parameter paths to search
            space definitions. Each value is a tuple of
            ``(type, *args)`` where type is one of:

            - ``('float', low, high)``: Uniform float sampling.
            - ``('log_uniform', low, high)``: Log-uniform float sampling.
            - ``('int', low, high)``: Uniform integer sampling.
            - ``('categorical', [choices])``: Categorical sampling.
        metric: Evaluation metric name (e.g. ``'RMSE'``, ``'MAE'``).
        direction: Optimization direction, ``'minimize'`` or ``'maximize'``.
        n_trials: Number of optimization trials to run.
        n_jobs: Number of parallel jobs (1 = sequential).
        seed: Random seed for reproducibility.

    Example::

        tuner = OptunaTuner(
            config_path='configs/baselines/sklearn/variance_model/matr_1.yaml',
            search_space={
                'model.learning_rate': ('log_uniform', 1e-5, 1e-1),
                'model.batch_size': ('categorical', [16, 32, 64, 128]),
                'model.epochs': ('int', 10, 200),
                'model.hidden_dim': ('int', 32, 512),
            },
            metric='RMSE',
            direction='minimize',
            n_trials=50,
        )
        best_params = tuner.run()
        tuner.save_best_config('best_config.yaml')
    """

    # Mapping from user-facing type names to Optuna suggest methods
    _SUGGEST_MAP = {
        'float': 'suggest_float',
        'log_uniform': 'suggest_float',
        'int': 'suggest_int',
        'categorical': 'suggest_categorical',
    }

    def __init__(
        self,
        config_path: Union[str, Path],
        search_space: Dict[str, tuple],
        metric: str = 'RMSE',
        direction: str = 'minimize',
        n_trials: int = 50,
        n_jobs: int = 1,
        seed: int = 42,
    ):
        self.config_path = Path(config_path)
        self.search_space = search_space
        self.metric = metric
        self.direction = direction
        self.n_trials = n_trials
        self.n_jobs = n_jobs
        self.seed = seed

        # Validate search space
        for key, spec in self.search_space.items():
            if not isinstance(spec, (tuple, list)) or len(spec) < 2:
                raise ValueError(
                    f"Invalid search space spec for '{key}': {spec}. "
                    "Expected (type, *args), e.g. ('float', 0.1, 1.0)."
                )
            stype = spec[0]
            if stype not in self._SUGGEST_MAP:
                raise ValueError(
                    f"Unknown search space type '{stype}' for '{key}'. "
                    f"Supported types: {list(self._SUGGEST_MAP.keys())}."
                )

        # Will be set after run()
        self._study: Optional[optuna.Study] = None
        self._base_config: Optional[dict] = None
        self._tmp_dirs: List[Path] = []

    def _suggest_params(
        self,
        trial: optuna.Trial,
        search_space: Dict[str, tuple],
    ) -> Dict[str, Any]:
        """Sample hyperparameters from the search space using an Optuna trial.

        Args:
            trial: An Optuna trial object used for parameter suggestion.
            search_space: The search space dictionary (same format as
                ``__init__``).

        Returns:
            A flat dictionary mapping dotted parameter paths to sampled
            values.
        """
        params: Dict[str, Any] = {}
        for key, spec in search_space.items():
            spec = list(spec)
            stype = spec[0]

            if stype == 'float':
                low, high = spec[1], spec[2]
                params[key] = trial.suggest_float(key, low, high)
            elif stype == 'log_uniform':
                low, high = spec[1], spec[2]
                params[key] = trial.suggest_float(key, low, high, log=True)
            elif stype == 'int':
                low, high = spec[1], spec[2]
                params[key] = trial.suggest_int(key, low, high)
            elif stype == 'categorical':
                choices = spec[1]
                params[key] = trial.suggest_categorical(key, choices)

        return params

    @staticmethod
    def _set_nested(config: dict, dotted_key: str, value: Any) -> None:
        """Set a value in a nested dict using a dotted key path.

        For example, ``_set_nested(cfg, 'model.lr', 0.01)`` sets
        ``cfg['model']['lr'] = 0.01``.

        Args:
            config: The configuration dictionary to modify.
            dotted_key: Dot-separated path to the target key.
            value: The value to set.
        """
        keys = dotted_key.split('.')
        d = config
        for k in keys[:-1]:
            if k not in d:
                d[k] = {}
            d = d[k]
        d[keys[-1]] = value

    def _load_base_yaml(self) -> dict:
        """Load the raw YAML config as a plain dict.

        Returns:
            The parsed YAML configuration dictionary.
        """
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _create_objective(self) -> Callable[[optuna.Trial], float]:
        """Create an Optuna objective function.

        The returned callable takes an ``optuna.Trial``, applies the
        sampled hyperparameters to a copy of the base config, trains and
        evaluates the model via a BatteryML ``Pipeline``, and returns
        the evaluation score.

        Returns:
            A callable suitable for ``optuna.Study.optimize``.
        """
        base_yaml = self._load_base_yaml()
        self._base_config = copy.deepcopy(base_yaml)

        def objective(trial: optuna.Trial) -> float:
            # Sample parameters
            params = self._suggest_params(trial, self.search_space)

            # Apply sampled params to a fresh copy of the config
            trial_yaml = copy.deepcopy(base_yaml)
            for dotted_key, value in params.items():
                self._set_nested(trial_yaml, dotted_key, value)

            # Write trial config to a temporary file
            trial_dir = tempfile.mkdtemp(
                prefix=f'optuna_trial_{trial.number}_'
            )
            self._tmp_dirs.append(Path(trial_dir))
            trial_config_path = Path(trial_dir) / 'trial_config.yaml'
            with open(trial_config_path, 'w', encoding='utf-8') as f:
                yaml.dump(trial_yaml, f, allow_unicode=True)

            # Create a pipeline with a trial-specific workspace
            trial_workspace = Path(trial_dir) / 'workspace'
            trial_workspace.mkdir(exist_ok=True)

            try:
                pipeline = Pipeline(
                    config_path=trial_config_path,
                    workspace=str(trial_workspace),
                )

                # Train
                result = pipeline.train(
                    seed=self.seed,
                    skip_if_executed=False,
                )
                if result is None:
                    raise RuntimeError("Training returned None")
                model, dataset = result

                # Evaluate
                prediction = model.predict(dataset)
                score = dataset.evaluate(prediction, self.metric)

                logger.info(
                    "Trial %d: %s = %.6f, params = %s",
                    trial.number, self.metric, score, params,
                )
                return float(score)

            except Exception as e:
                logger.warning(
                    "Trial %d failed with error: %s", trial.number, e
                )
                raise optuna.TrialPruned(f"Trial failed: {e}")

        return objective

    def run(
        self, workspace: Optional[Union[str, Path]] = None,
    ) -> Dict[str, Any]:
        """Run the hyperparameter optimization.

        Creates an Optuna study and optimizes the objective over the
        configured number of trials.

        Args:
            workspace: Optional base directory for trial workspaces.
                If not provided, temporary directories are used.

        Returns:
            A dictionary of the best hyperparameters found.
        """
        sampler = optuna.samplers.TPESampler(seed=self.seed)
        pruner = MedianPruner(
            n_startup_trials=5,
            n_warmup_steps=0,
        )

        self._study = optuna.create_study(
            direction=self.direction,
            sampler=sampler,
            pruner=pruner,
            study_name='batteryml_tuning',
        )

        objective = self._create_objective()

        self._study.optimize(
            objective,
            n_trials=self.n_trials,
            n_jobs=self.n_jobs,
            show_progress_bar=True,
        )

        best = self._study.best_params
        logger.info("Best parameters: %s", best)
        logger.info(
            "Best %s: %.6f", self.metric, self._study.best_value
        )

        return best

    def save_best_config(self, output_path: Union[str, Path]) -> None:
        """Save the best configuration found to a YAML file.

        Merges the best hyperparameters back into the original config
        and writes the result.

        Args:
            output_path: Destination path for the YAML config file.

        Raises:
            RuntimeError: If ``run()`` has not been called yet.
        """
        if self._study is None or self._base_config is None:
            raise RuntimeError(
                "No study results available. Call run() first."
            )

        best_config = copy.deepcopy(self._base_config)
        for dotted_key, value in self._study.best_params.items():
            self._set_nested(best_config, dotted_key, value)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(
                best_config, f,
                allow_unicode=True,
                default_flow_style=False,
            )

        logger.info("Best config saved to %s", output_path)

    def get_study_summary(self) -> str:
        """Return a text summary of the optimization study.

        Includes the number of completed/pruned/failed trials, the best
        value and parameters, and the top 5 trials.

        Returns:
            A formatted multi-line string summarizing the study.

        Raises:
            RuntimeError: If ``run()`` has not been called yet.
        """
        if self._study is None:
            raise RuntimeError(
                "No study results available. Call run() first."
            )

        study = self._study
        completed = [
            t for t in study.trials
            if t.state == optuna.trial.TrialState.COMPLETE
        ]
        pruned = [
            t for t in study.trials
            if t.state == optuna.trial.TrialState.PRUNED
        ]
        failed = [
            t for t in study.trials
            if t.state == optuna.trial.TrialState.FAIL
        ]

        lines = [
            "=" * 60,
            "Optuna Hyperparameter Optimization Summary",
            "=" * 60,
            f"Study name:        {study.study_name}",
            f"Direction:         {self.direction}",
            f"Metric:            {self.metric}",
            f"Total trials:      {len(study.trials)}",
            f"  Completed:       {len(completed)}",
            f"  Pruned:          {len(pruned)}",
            f"  Failed:          {len(failed)}",
            "",
        ]

        if completed:
            lines.extend([
                f"Best trial:        #{study.best_trial.number}",
                f"Best {self.metric}:  {study.best_value:.6f}",
                "Best parameters:",
            ])
            for k, v in study.best_params.items():
                lines.append(f"  {k}: {v}")
            lines.append("")

            # Top 5 trials
            sorted_trials = sorted(
                completed,
                key=lambda t: t.value,
                reverse=(self.direction == 'maximize'),
            )
            lines.append("Top 5 trials:")
            for t in sorted_trials[:5]:
                lines.append(
                    f"  Trial #{t.number}: {self.metric} = {t.value:.6f}"
                )
        else:
            lines.append("No completed trials.")

        lines.append("=" * 60)
        return "\n".join(lines)

    def get_importance(self) -> Dict[str, float]:
        """Return hyperparameter importance scores.

        Uses Optuna's ``get_param_importances`` to rank how much each
        hyperparameter contributes to the objective value.

        Returns:
            A dictionary mapping parameter names to importance scores
            (floats between 0 and 1), sorted from most to least
            important.

        Raises:
            RuntimeError: If ``run()`` has not been called yet.
        """
        if self._study is None:
            raise RuntimeError(
                "No study results available. Call run() first."
            )

        try:
            importances = optuna.importance.get_param_importances(
                self._study
            )
        except Exception as e:
            logger.warning(
                "Could not compute parameter importances: %s", e
            )
            importances = {}

        return importances

    def __del__(self) -> None:
        """Ensure temporary directories are cleaned up on deletion."""
        self.cleanup()

    def cleanup(self) -> None:
        """Remove all temporary directories created during optimization.

        Call this after optimization is complete and results have been
        saved if you want to free disk space used by trial workspaces.
        """
        for tmp_dir in self._tmp_dirs:
            if tmp_dir.exists():
                shutil.rmtree(tmp_dir, ignore_errors=True)
        self._tmp_dirs.clear()
