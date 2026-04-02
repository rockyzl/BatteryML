# Licensed under the MIT License.
# Copyright (c) Microsoft Corporation.

import numpy as np

from typing import Dict, Optional, Union

from batteryml.evaluation.metrics import (
    rmse, mae, mape, r2_score, medae, max_error, explained_variance,
    ArrayLike, _to_numpy, _validate_inputs, _filter_nan,
)


class EvaluationReport:
    """Model evaluation report generator.

    模型评估报告生成器。

    Args:
        y_true: Ground truth values. 真实值。
        y_pred: Predicted values. 预测值。
        model_name: Optional model name for the report. 可选的模型名称。
        dataset_name: Optional dataset name for the report. 可选的数据集名称。
    """

    # All metric functions to compute
    _METRIC_FUNCS = {
        'rmse': rmse,
        'mae': mae,
        'mape': mape,
        'r2_score': r2_score,
        'medae': medae,
        'max_error': max_error,
        'explained_variance': explained_variance,
    }

    def __init__(
        self,
        y_true: ArrayLike,
        y_pred: ArrayLike,
        model_name: Optional[str] = None,
        dataset_name: Optional[str] = None,
    ):
        self.y_true = _to_numpy(y_true)
        self.y_pred = _to_numpy(y_pred)
        self.model_name = model_name
        self.dataset_name = dataset_name
        self._metrics: Optional[Dict[str, float]] = None

    def compute_all_metrics(self) -> Dict[str, float]:
        """Compute all available metrics and cache the results.

        计算所有可用指标并缓存结果。

        Returns:
            Dict[str, float]: A dictionary mapping metric names to values.
        """
        if self._metrics is not None:
            return dict(self._metrics)

        results = {}
        for name, func in self._METRIC_FUNCS.items():
            try:
                results[name] = func(self.y_true, self.y_pred)
            except ValueError:
                results[name] = float('nan')

        self._metrics = results
        return dict(results)

    def summary(self) -> str:
        """Generate a text summary of the evaluation results.

        生成评估结果的文本摘要。

        Returns:
            str: Formatted summary string.
        """
        metrics = self.compute_all_metrics()
        lines = []
        lines.append('=' * 50)
        lines.append('Evaluation Report / 评估报告')
        lines.append('=' * 50)

        if self.model_name:
            lines.append(f'Model / 模型:     {self.model_name}')
        if self.dataset_name:
            lines.append(f'Dataset / 数据集: {self.dataset_name}')

        lines.append(f'Samples / 样本数: {len(self.y_true)}')
        lines.append('-' * 50)

        for name, value in metrics.items():
            lines.append(f'  {name:<24s}: {value:.6f}')

        lines.append('=' * 50)
        return '\n'.join(lines)

    def to_dict(self) -> Dict:
        """Convert the report to a dictionary.

        将报告转为字典。

        Returns:
            Dict: Dictionary containing all report information.
        """
        metrics = self.compute_all_metrics()
        return {
            'model_name': self.model_name,
            'dataset_name': self.dataset_name,
            'num_samples': len(self.y_true),
            'metrics': metrics,
        }

    def compare(self, other: 'EvaluationReport') -> Dict:
        """Compare this report with another report.

        将本报告与另一个报告进行对比。

        For error metrics (rmse, mae, mape, medae, max_error), negative
        difference means improvement (lower is better).
        For score metrics (r2_score, explained_variance), positive
        difference means improvement (higher is better).

        Args:
            other: Another EvaluationReport to compare against.

        Returns:
            Dict: Comparison results with differences and improvements.
        """
        self_metrics = self.compute_all_metrics()
        other_metrics = other.compute_all_metrics()

        # Metrics where lower is better
        lower_is_better = {'rmse', 'mae', 'mape', 'medae', 'max_error'}

        comparison = {}
        for name in self_metrics:
            self_val = self_metrics[name]
            other_val = other_metrics.get(name, float('nan'))
            diff = self_val - other_val

            if name in lower_is_better:
                improved = diff < 0
            else:
                improved = diff > 0

            comparison[name] = {
                'self': self_val,
                'other': other_val,
                'diff': diff,
                'improved': improved,
            }

        return {
            'self_model': self.model_name,
            'other_model': other.model_name,
            'metrics': comparison,
        }
