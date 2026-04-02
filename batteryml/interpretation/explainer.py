# Licensed under the MIT License.
# Copyright (c) Microsoft Corporation.

import warnings
import numpy as np
import torch
import matplotlib.pyplot as plt

from typing import Dict, List, Optional, Tuple

from batteryml.models.base import BaseModel
from batteryml.models.sklearn_model import SklearnModel
from batteryml.data.databundle import DataBundle


class ModelExplainer:
    """Model interpretability and feature importance analysis.

    模型可解释性和特征重要性分析工具。
    支持SHAP值分析、排列重要性(Permutation Importance)和内置特征重要性。

    This class provides multiple methods to analyze which features are most
    important for a model's predictions:
    - Permutation Importance: always available, no extra dependencies.
    - SHAP values: requires the optional ``shap`` library.
    - Built-in importance: for tree-based models that expose
      ``feature_importances_``.

    Usage:
        explainer = ModelExplainer(model, data_bundle)
        importance = explainer.permutation_importance()
        explainer.plot_importance(top_k=10, save_path='importance.png')
    """

    def __init__(
        self,
        model: BaseModel,
        data_bundle: DataBundle,
        data_type: str = 'test',
        metric: str = 'RMSE',
    ):
        """Initialize the explainer.

        Args:
            model: A trained BatteryML model.
            data_bundle: The DataBundle used for evaluation.
            data_type: Which split to use for explanations ('test' or 'train').
            metric: Evaluation metric used to measure performance changes.
                Must be one of 'RMSE', 'MAE', or 'MAPE'.
        """
        self.model = model
        self.data_bundle = data_bundle
        self.data_type = data_type
        self.metric = metric

        # Cache feature / label tensors
        if data_type == 'test':
            self._features = data_bundle.test_data.feature.clone()
            self._labels = data_bundle.test_data.label.clone()
        else:
            self._features = data_bundle.train_data.feature.clone()
            self._labels = data_bundle.train_data.label.clone()

        # Flatten features to 2-D (n_samples, n_features) as sklearn models do
        self._features_2d = self._features.view(len(self._features), -1)
        self.n_features = self._features_2d.shape[1]

        # Cached results
        self._perm_importance: Optional[Dict[str, float]] = None
        self._shap_values: Optional[np.ndarray] = None
        self._builtin_importance: Optional[Dict[str, float]] = None

    # ------------------------------------------------------------------
    # Helper: compute score for a given feature tensor
    # ------------------------------------------------------------------

    def _score(self, features_2d: torch.Tensor) -> float:
        """Compute the evaluation score for a feature matrix.

        A *lower* RMSE/MAE/MAPE is better, so a score
        *increase* after permutation means the feature
        was important.

        Args:
            features_2d: Feature tensor (n_samples, n_features).

        Returns:
            The scalar evaluation score.
        """
        # Temporarily replace the features in the data bundle
        if self.data_type == 'test':
            original = self.data_bundle.test_data.feature
            self.data_bundle.test_data.feature = features_2d.view(
                original.shape
            )
        else:
            original = self.data_bundle.train_data.feature
            self.data_bundle.train_data.feature = features_2d.view(
                original.shape
            )

        try:
            preds = self.model.predict(
                self.data_bundle,
                data_type=self.data_type,
            )
            score = self.data_bundle.evaluate(
                preds,
                metric=self.metric,
                data_type=self.data_type,
            )
        finally:
            # Restore original features
            if self.data_type == 'test':
                self.data_bundle.test_data.feature = original
            else:
                self.data_bundle.train_data.feature = original

        return float(score)

    # ------------------------------------------------------------------
    # Feature name helpers
    # ------------------------------------------------------------------

    def _feature_names(
        self, feature_names: Optional[List[str]] = None,
    ) -> List[str]:
        """Return feature names, generating defaults if needed.

        Args:
            feature_names: Explicit list of feature names. If ``None``,
                names are generated as ``feature_0``, ``feature_1``, etc.

        Returns:
            List of feature name strings.
        """
        if feature_names is not None:
            if len(feature_names) != self.n_features:
                raise ValueError(
                    f"Expected {self.n_features} feature names, "
                    f"got {len(feature_names)}."
                )
            return feature_names
        return [f'feature_{i}' for i in range(self.n_features)]

    # ------------------------------------------------------------------
    # Permutation Importance
    # ------------------------------------------------------------------

    def permutation_importance(
        self,
        n_repeats: int = 10,
        seed: int = 42,
        feature_names: Optional[List[str]] = None,
    ) -> Dict[str, float]:
        """Compute permutation feature importance.

        计算排列特征重要性。
        对每个特征，随机打乱其值后观察模型性能下降程度。
        下降越多 = 该特征越重要。

        This method does not require any additional libraries beyond NumPy
        and PyTorch (already required by BatteryML).

        Args:
            n_repeats: Number of times to permute each feature.
            seed: Random seed for reproducibility.
            feature_names: Optional list of human-readable feature names.

        Returns:
            Dictionary mapping feature names to importance scores (mean
            increase in the evaluation metric after permutation).
        """
        rng = np.random.RandomState(seed)
        names = self._feature_names(feature_names)
        baseline_score = self._score(self._features_2d)

        importances: Dict[str, float] = {}
        n_samples = self._features_2d.shape[0]

        for feat_idx in range(self.n_features):
            scores = []
            for _ in range(n_repeats):
                permuted = self._features_2d.clone()
                perm_idx = torch.from_numpy(
                    rng.permutation(n_samples)
                ).long()
                permuted[:, feat_idx] = permuted[perm_idx, feat_idx]
                scores.append(self._score(permuted))

            # Importance = mean score increase (higher metric = worse)
            importances[names[feat_idx]] = float(
                np.mean(scores) - baseline_score
            )

        self._perm_importance = importances
        return importances

    # ------------------------------------------------------------------
    # SHAP values (optional dependency)
    # ------------------------------------------------------------------

    def shap_values(
        self,
        max_samples: int = 100,
        feature_names: Optional[List[str]] = None,
    ) -> Optional[np.ndarray]:
        """Compute SHAP values. Requires the optional ``shap`` library.

        计算SHAP值。需要安装shap库。
        如果shap未安装，返回None并打印友好提示。

        For sklearn-compatible models a ``shap.Explainer`` is used
        automatically. Neural-network models are not currently supported.

        Args:
            max_samples: Maximum number of samples used for the SHAP
                background dataset (sub-sampled for speed).
            feature_names: Optional list of human-readable feature names.

        Returns:
            SHAP values as a numpy array of shape (n_samples, n_features),
            or ``None`` if the ``shap`` library is not installed or the model
            type is not supported.
        """
        try:
            import shap  # noqa: F401
        except ImportError:
            warnings.warn(
                "The 'shap' library is not installed. "
                "Install it with: pip install shap\n"
                "SHAP analysis is unavailable; returning None. "
                "You can still use permutation_importance() which has "
                "no extra dependencies."
            )
            return None

        if not isinstance(self.model, SklearnModel):
            warnings.warn(
                "SHAP analysis is currently only supported for sklearn-based "
                "models (SklearnModel). Returning None."
            )
            return None

        features_np = self._features_2d.numpy()
        n = min(max_samples, len(features_np))
        background = shap.sample(features_np, n)

        explainer = shap.Explainer(
            self.model.model.predict,
            background,
            feature_names=self._feature_names(feature_names),
        )
        shap_result = explainer(features_np)
        self._shap_values = shap_result.values
        return self._shap_values

    # ------------------------------------------------------------------
    # Built-in importance (tree-based models)
    # ------------------------------------------------------------------

    def builtin_importance(
        self,
        feature_names: Optional[List[str]] = None,
    ) -> Optional[Dict[str, float]]:
        """Retrieve the model's built-in feature importance.

        获取模型内置的特征重要性（如RandomForest / XGBoost的
        ``feature_importances_``）。对不支持的模型返回None。

        Args:
            feature_names: Optional list of human-readable feature names.

        Returns:
            Dictionary mapping feature names to importance values, or
            ``None`` if the underlying model does not expose
            ``feature_importances_``.
        """
        if not isinstance(self.model, SklearnModel):
            return None

        inner = self.model.model
        if not hasattr(inner, 'feature_importances_'):
            return None

        names = self._feature_names(feature_names)
        imp = inner.feature_importances_
        result = {name: float(val) for name, val in zip(names, imp)}
        self._builtin_importance = result
        return result

    # ------------------------------------------------------------------
    # Visualization
    # ------------------------------------------------------------------

    def _get_importance(
        self,
        method: str,
        feature_names: Optional[List[str]] = None,
    ) -> Dict[str, float]:
        """Return importance dict for a given method, computing if needed.

        Args:
            method: One of 'permutation', 'builtin', or 'shap'.
            feature_names: Optional feature names.

        Returns:
            Dictionary mapping feature names to importance scores.

        Raises:
            ValueError: If the method is unknown or unavailable.
        """
        if method == 'permutation':
            if self._perm_importance is not None:
                return self._perm_importance
            return self.permutation_importance(feature_names=feature_names)
        elif method == 'builtin':
            result = self.builtin_importance(feature_names=feature_names)
            if result is None:
                raise ValueError(
                    "Built-in importance is not available "
                    "for this model. Use 'permutation'."
                )
            return result
        elif method == 'shap':
            vals = self.shap_values(feature_names=feature_names)
            if vals is None:
                raise ValueError(
                    "SHAP values are not available. Make sure the 'shap' "
                    "library is installed and the model is sklearn-based."
                )
            names = self._feature_names(feature_names)
            mean_abs = np.abs(vals).mean(axis=0)
            return {n: float(v) for n, v in zip(names, mean_abs)}
        else:
            raise ValueError(
                f"Unknown method '{method}'. "
                "Choose from 'permutation', 'builtin', or 'shap'."
            )

    def plot_importance(
        self,
        method: str = 'permutation',
        top_k: int = 15,
        feature_names: Optional[List[str]] = None,
        save_path: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 6),
    ):
        """Plot feature importance as a horizontal bar chart.

        绘制特征重要性条形图。

        Args:
            method: Importance method ('permutation', 'builtin', or 'shap').
            top_k: Number of top features to display.
            feature_names: Optional list of human-readable feature names.
            save_path: If provided, save the figure to this path.
            figsize: Figure size as ``(width, height)``.
        """
        importance = self._get_importance(method, feature_names)

        # Sort by absolute importance descending, take top_k
        sorted_items = sorted(
            importance.items(), key=lambda x: abs(x[1]), reverse=True
        )[:top_k]
        sorted_items.reverse()  # smallest at top for horizontal bar chart

        names = [item[0] for item in sorted_items]
        values = [item[1] for item in sorted_items]

        fig, ax = plt.subplots(figsize=figsize)
        colors = plt.cm.viridis(
            np.linspace(0.3, 0.9, len(names))
        )
        ax.barh(names, values, color=colors)
        ax.set_xlabel('Importance')
        ax.set_title(f'Feature Importance ({method})')
        ax.grid(axis='x', alpha=0.3)
        fig.tight_layout()

        if save_path is not None:
            fig.savefig(save_path, dpi=150, bbox_inches='tight')

        plt.close(fig)
        return fig

    def plot_importance_comparison(
        self,
        methods: Optional[List[str]] = None,
        top_k: int = 10,
        feature_names: Optional[List[str]] = None,
        save_path: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 5),
    ):
        """Plot side-by-side importance comparison.

        并排对比不同方法的特征重要性。

        Args:
            methods: List of methods to compare. If ``None``, automatically
                selects all available methods.
            top_k: Number of top features to display per method.
            feature_names: Optional list of human-readable feature names.
            save_path: If provided, save the figure to this path.
            figsize: Figure size as ``(width, height)``.
        """
        if methods is None:
            methods = self._available_methods()

        if len(methods) == 0:
            raise ValueError("No importance methods are available.")

        fig, axes = plt.subplots(1, len(methods), figsize=figsize)
        if len(methods) == 1:
            axes = [axes]

        for ax, method in zip(axes, methods):
            try:
                importance = self._get_importance(method, feature_names)
            except ValueError:
                ax.set_title(f'{method}\n(unavailable)')
                ax.set_visible(False)
                continue

            sorted_items = sorted(
                importance.items(), key=lambda x: abs(x[1]), reverse=True
            )[:top_k]
            sorted_items.reverse()

            names = [item[0] for item in sorted_items]
            values = [item[1] for item in sorted_items]

            colors = plt.cm.viridis(
                np.linspace(0.3, 0.9, len(names))
            )
            ax.barh(names, values, color=colors)
            ax.set_xlabel('Importance')
            ax.set_title(f'{method}')
            ax.grid(axis='x', alpha=0.3)

        fig.suptitle(
            'Feature Importance Comparison',
            fontsize=14, y=1.02,
        )
        fig.tight_layout()

        if save_path is not None:
            fig.savefig(
                save_path, dpi=150, bbox_inches='tight',
            )

        plt.close(fig)
        return fig

    def _available_methods(self) -> List[str]:
        """Return a list of importance methods available for the current model.

        Returns:
            List of method name strings.
        """
        methods = ['permutation']  # Always available

        # Check built-in
        if isinstance(self.model, SklearnModel):
            inner = self.model.model
            if hasattr(inner, 'feature_importances_'):
                methods.append('builtin')

        # Check SHAP
        try:
            import shap  # noqa: F401
            if isinstance(self.model, SklearnModel):
                methods.append('shap')
        except ImportError:
            pass

        return methods
