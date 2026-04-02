# Licensed under the MIT License.
# Copyright (c) Microsoft Corporation.

import torch
import numpy as np

from typing import Union

ArrayLike = Union[torch.Tensor, np.ndarray]


def _to_numpy(arr: ArrayLike) -> np.ndarray:
    """Convert input to numpy array, handling torch tensors.

    将输入转换为 numpy 数组，支持 torch.Tensor。
    """
    if isinstance(arr, torch.Tensor):
        return arr.detach().cpu().numpy()
    return np.asarray(arr, dtype=np.float64)


def _validate_inputs(y_true: ArrayLike, y_pred: ArrayLike):
    """Validate inputs: check for empty arrays and matching shapes.

    验证输入：检查空数组和形状是否匹配。

    Raises:
        ValueError: If inputs are empty or have mismatched shapes.
    """
    y_true = _to_numpy(y_true)
    y_pred = _to_numpy(y_pred)

    if y_true.size == 0 or y_pred.size == 0:
        raise ValueError(
            "Input arrays must not be empty. "
            "输入数组不能为空。")

    if y_true.shape != y_pred.shape:
        raise ValueError(
            f"Shape mismatch: y_true {y_true.shape} vs y_pred {y_pred.shape}. "
            f"形状不匹配：y_true {y_true.shape} 与 y_pred {y_pred.shape}。")

    return y_true, y_pred


def _filter_nan(y_true: np.ndarray, y_pred: np.ndarray):
    """Remove entries where either y_true or y_pred is NaN.

    移除 y_true 或 y_pred 中包含 NaN 的条目。

    Raises:
        ValueError: If all entries are NaN.
    """
    mask = ~(np.isnan(y_true) | np.isnan(y_pred))
    y_true = y_true[mask]
    y_pred = y_pred[mask]

    if y_true.size == 0:
        raise ValueError(
            "All entries are NaN after filtering. "
            "过滤后所有条目均为 NaN。")

    return y_true, y_pred


def rmse(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    """Root Mean Squared Error (RMSE).

    均方根误差。

    RMSE = sqrt(mean((y_true - y_pred)^2))

    Args:
        y_true: Ground truth values. 真实值。
        y_pred: Predicted values. 预测值。

    Returns:
        float: RMSE score.
    """
    y_true, y_pred = _validate_inputs(y_true, y_pred)
    y_true, y_pred = _filter_nan(y_true, y_pred)
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def mae(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    """Mean Absolute Error (MAE).

    平均绝对误差。

    MAE = mean(|y_true - y_pred|)

    Args:
        y_true: Ground truth values. 真实值。
        y_pred: Predicted values. 预测值。

    Returns:
        float: MAE score.
    """
    y_true, y_pred = _validate_inputs(y_true, y_pred)
    y_true, y_pred = _filter_nan(y_true, y_pred)
    return float(np.mean(np.abs(y_true - y_pred)))


def mape(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    """Mean Absolute Percentage Error (MAPE).

    平均绝对百分比误差。处理零值时会跳过 y_true == 0 的条目。

    MAPE = mean(|y_true - y_pred| / |y_true|) * 100

    Args:
        y_true: Ground truth values. 真实值。
        y_pred: Predicted values. 预测值。

    Returns:
        float: MAPE score as a percentage.

    Raises:
        ValueError: If all y_true values are zero.
    """
    y_true, y_pred = _validate_inputs(y_true, y_pred)
    y_true, y_pred = _filter_nan(y_true, y_pred)

    # Filter out zero values in y_true to avoid division by zero
    nonzero_mask = y_true != 0
    if not np.any(nonzero_mask):
        raise ValueError(
            "All y_true values are zero; MAPE is undefined. "
            "所有 y_true 值均为零，MAPE 无定义。")

    y_true = y_true[nonzero_mask]
    y_pred = y_pred[nonzero_mask]

    return float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100)


def r2_score(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    """R² (coefficient of determination) score.

    R² 决定系数。

    R² = 1 - SS_res / SS_tot
    where SS_res = sum((y_true - y_pred)^2)
          SS_tot = sum((y_true - mean(y_true))^2)

    Args:
        y_true: Ground truth values. 真实值。
        y_pred: Predicted values. 预测值。

    Returns:
        float: R² score. Best possible score is 1.0.
    """
    y_true, y_pred = _validate_inputs(y_true, y_pred)
    y_true, y_pred = _filter_nan(y_true, y_pred)

    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)

    if ss_tot == 0:
        # All y_true values are the same
        return 0.0 if ss_res > 0 else 1.0

    return float(1 - ss_res / ss_tot)


def medae(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    """Median Absolute Error (MedAE).

    中位绝对误差。

    MedAE = median(|y_true - y_pred|)

    Args:
        y_true: Ground truth values. 真实值。
        y_pred: Predicted values. 预测值。

    Returns:
        float: MedAE score.
    """
    y_true, y_pred = _validate_inputs(y_true, y_pred)
    y_true, y_pred = _filter_nan(y_true, y_pred)
    return float(np.median(np.abs(y_true - y_pred)))


def max_error(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    """Maximum Absolute Error.

    最大绝对误差。

    max_error = max(|y_true - y_pred|)

    Args:
        y_true: Ground truth values. 真实值。
        y_pred: Predicted values. 预测值。

    Returns:
        float: Maximum absolute error.
    """
    y_true, y_pred = _validate_inputs(y_true, y_pred)
    y_true, y_pred = _filter_nan(y_true, y_pred)
    return float(np.max(np.abs(y_true - y_pred)))


def explained_variance(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    """Explained Variance Score.

    解释方差分数。

    EV = 1 - Var(y_true - y_pred) / Var(y_true)

    Args:
        y_true: Ground truth values. 真实值。
        y_pred: Predicted values. 预测值。

    Returns:
        float: Explained variance score. Best possible score is 1.0.
    """
    y_true, y_pred = _validate_inputs(y_true, y_pred)
    y_true, y_pred = _filter_nan(y_true, y_pred)

    var_true = np.var(y_true)
    if var_true < 1e-15:
        residual_var = np.var(y_true - y_pred)
        return 0.0 if residual_var > 0 else 1.0

    return float(1 - np.var(y_true - y_pred) / var_true)


# Registry mapping metric names to functions
METRIC_REGISTRY = {
    'rmse': rmse,
    'mae': mae,
    'mape': mape,
    'r2': r2_score,
    'r2_score': r2_score,
    'medae': medae,
    'max_error': max_error,
    'explained_variance': explained_variance,
}


def get_metric(name: str):
    """Get a metric function by name.

    根据名称获取指标函数。

    Args:
        name: Metric name (case-insensitive). 指标名称（不区分大小写）。

    Returns:
        Callable: The metric function.

    Raises:
        ValueError: If the metric name is not recognized.
    """
    key = name.lower()
    if key not in METRIC_REGISTRY:
        avail = list(METRIC_REGISTRY.keys())
        raise ValueError(
            f"Unknown metric '{name}'. Available: {avail}. "
            f"未知指标 '{name}'。可用指标：{avail}。")
    return METRIC_REGISTRY[key]
