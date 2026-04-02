# Licensed under the MIT License.
# Copyright (c) Microsoft Corporation.

import torch
import pickle

from typing import Dict, List, Optional, Union

from batteryml.data.transformation.base import BaseDataTransformation


class Dataset:
    def __init__(self, feature: torch.Tensor, label: torch.Tensor):
        assert len(feature) == len(label), (len(feature), len(label))

        self.label = label
        self.feature = feature

    def __len__(self):
        return len(self.label)

    def __getitem__(self, item: int):
        return {
            'feature': self.feature[item],
            'label': self.label[item]
        }

    @property
    def device(self):
        return self.label.device

    def to(self, device: str):
        self.label = self.label.to(device)
        self.feature = self.feature.to(device)
        return self


class DataBundle:
    def __init__(self,
                 train_feature: torch.Tensor,
                 train_label: torch.Tensor,
                 test_feature: torch.Tensor,
                 test_label: torch.Tensor,
                 feature_transformation: BaseDataTransformation = None,
                 label_transformation: BaseDataTransformation = None):
        # Convert the dtype
        train_feature = train_feature.float()
        train_label = train_label.float()
        test_feature = test_feature.float()
        test_label = test_label.float()

        self.feature_transformation = feature_transformation
        self.label_transformation = label_transformation

        # Fit the stateful transformations
        if feature_transformation is not None:
            self.feature_transformation.fit(train_feature)
            train_feature = self.feature_transformation.transform(train_feature)
            test_feature = self.feature_transformation.transform(test_feature)
        if label_transformation is not None:
            self.label_transformation.fit(train_label)
            train_label = self.label_transformation.transform(train_label)
            test_label = self.label_transformation.transform(test_label)

        # Build datasets
        self.train_data = Dataset(train_feature, train_label)
        self.test_data = Dataset(test_feature, test_label)

    def to(self, device: str):
        self.train_data = self.train_data.to(device)
        self.test_data = self.test_data.to(device)
        if self.feature_transformation is not None:
            self.feature_transformation = self.feature_transformation.to(device)
        if self.label_transformation is not None:
            self.label_transformation = self.label_transformation.to(device)
        return self

    @property
    def device(self):
        return self.train_data.feature.device

    @torch.no_grad()
    def evaluate(
        self,
        prediction: torch.Tensor,
        metric: Union[str, List[str]] = 'RMSE',
        data_type: str = 'test',
        metrics: Optional[List[str]] = None,
    ) -> Union[float, Dict[str, float]]:
        """Evaluate predictions against ground truth.

        Args:
            prediction: Model predictions.
            metric: Single metric name (for backward compatibility).
            data_type: 'test' or 'train'.
            metrics: List of metric names. If provided, returns a dict
                of {metric_name: score}. Supports new metrics from
                batteryml.evaluation.metrics.

        Returns:
            float if a single metric string is used (backward compat),
            Dict[str, float] if metrics list is provided.
        """
        if data_type == 'train':
            target = self.train_data.label
        else:
            target = self.test_data.label

        if self.label_transformation is not None:
            target = self.label_transformation.inverse_transform(target)
            prediction = (
                self.label_transformation
                .inverse_transform(prediction)
            )

        # New multi-metric path
        if metrics is not None:
            from batteryml.evaluation.metrics import get_metric
            return {m: get_metric(m)(target, prediction) for m in metrics}

        return self._evaluate_score(target, prediction, metric)

    @torch.no_grad()
    def evaluate_all(
        self,
        prediction: torch.Tensor,
        data_type: str = 'test',
    ) -> Dict[str, float]:
        """Evaluate predictions with all available metrics.

        使用所有可用指标评估预测结果。

        Args:
            prediction: Model predictions.
            data_type: 'test' or 'train'.

        Returns:
            Dict[str, float]: All metric scores.
        """
        from batteryml.evaluation.metrics import METRIC_REGISTRY

        if data_type == 'train':
            target = self.train_data.label
        else:
            target = self.test_data.label

        if self.label_transformation is not None:
            lt = self.label_transformation
            target = lt.inverse_transform(target)
            prediction = lt.inverse_transform(prediction)

        results = {}
        for name, func in METRIC_REGISTRY.items():
            try:
                results[name] = func(target, prediction)
            except ValueError:
                results[name] = float('nan')
        return results

    @staticmethod
    def _evaluate_score(
        target: torch.Tensor,
        prediction: torch.Tensor,
        metric: str
    ) -> float:
        assert metric in ['RMSE', 'MAE', 'MAPE'], metric
        if metric == 'RMSE':
            score = torch.mean((target - prediction) ** 2) ** 0.5
        elif metric == 'MAE':
            score = torch.mean((target - prediction).abs())
        else:
            nonzero = target != 0
            if not nonzero.any():
                return float('inf')
            score = torch.abs(
                (target[nonzero] - prediction[nonzero]) / target[nonzero]
            ).mean()

        return float(score)

    @staticmethod
    def load(path: str):
        with open(path, 'rb') as f:
            return pickle.load(f)

    def dump(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self, f)
