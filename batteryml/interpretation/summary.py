# Licensed under the MIT License.
# Copyright (c) Microsoft Corporation.

from typing import Dict, List, Optional

from batteryml.interpretation.explainer import ModelExplainer


class InterpretabilitySummary:
    """Generate a comprehensive interpretability report for a model.

    为模型生成全面的可解释性报告，包括排列重要性、内置重要性以及
    可选的SHAP值分析结果。

    Usage:
        explainer = ModelExplainer(model, data_bundle)
        summary = InterpretabilitySummary(explainer)
        print(summary.generate())
        report = summary.to_dict()
    """

    def __init__(
        self,
        explainer: ModelExplainer,
        feature_names: Optional[List[str]] = None,
    ):
        """Initialize the summary generator.

        Args:
            explainer: A ``ModelExplainer`` instance bound to a model and
                data bundle.
            feature_names: Optional human-readable feature names.
        """
        self.explainer = explainer
        self.feature_names = feature_names

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self, top_k: int = 10) -> str:
        """Generate a text summary of model interpretability analysis.

        生成模型可解释性分析的文本摘要。

        The report includes:
        - Permutation importance (always computed).
        - Built-in importance (if available).
        - SHAP-based importance (if the ``shap`` library is installed
          and the model is supported).

        Args:
            top_k: Number of top features to highlight per method.

        Returns:
            A formatted multi-line string report.
        """
        lines: List[str] = []
        lines.append('=' * 60)
        lines.append('  Model Interpretability Report')
        lines.append('=' * 60)
        lines.append('')
        lines.append(f'Model type   : {type(self.explainer.model).__name__}')
        lines.append(f'Data split   : {self.explainer.data_type}')
        lines.append(f'Metric       : {self.explainer.metric}')
        lines.append(f'Num features : {self.explainer.n_features}')
        lines.append(f'Num samples  : {self.explainer._features_2d.shape[0]}')
        lines.append('')

        # Permutation importance (always available)
        lines.append('-' * 60)
        lines.append('  Permutation Importance')
        lines.append('-' * 60)
        perm = self.explainer.permutation_importance(
            feature_names=self.feature_names
        )
        lines.extend(self._format_importance(perm, top_k))
        lines.append('')

        # Built-in importance
        builtin = self.explainer.builtin_importance(
            feature_names=self.feature_names
        )
        if builtin is not None:
            lines.append('-' * 60)
            lines.append('  Built-in Feature Importance')
            lines.append('-' * 60)
            lines.extend(self._format_importance(builtin, top_k))
            lines.append('')

        # SHAP importance
        shap_vals = self.explainer.shap_values(
            feature_names=self.feature_names
        )
        if shap_vals is not None:
            import numpy as np
            names = self.explainer._feature_names(self.feature_names)
            mean_abs = np.abs(shap_vals).mean(axis=0)
            shap_imp = {n: float(v) for n, v in zip(names, mean_abs)}
            lines.append('-' * 60)
            lines.append('  SHAP Feature Importance (mean |SHAP value|)')
            lines.append('-' * 60)
            lines.extend(self._format_importance(shap_imp, top_k))
            lines.append('')

        lines.append('=' * 60)
        lines.append('  End of Report')
        lines.append('=' * 60)

        return '\n'.join(lines)

    def to_dict(self, top_k: int = 10) -> Dict:
        """Export the interpretability analysis as a dictionary.

        将可解释性分析导出为字典，便于序列化或进一步处理。

        Args:
            top_k: Number of top features to include per method.

        Returns:
            Dictionary with keys for each available method, plus metadata.
        """
        result: Dict = {
            'model_type': type(self.explainer.model).__name__,
            'data_type': self.explainer.data_type,
            'metric': self.explainer.metric,
            'n_features': self.explainer.n_features,
            'n_samples': int(self.explainer._features_2d.shape[0]),
        }

        # Permutation importance
        perm = self.explainer.permutation_importance(
            feature_names=self.feature_names
        )
        result['permutation_importance'] = self._top_k(perm, top_k)

        # Built-in importance
        builtin = self.explainer.builtin_importance(
            feature_names=self.feature_names
        )
        if builtin is not None:
            result['builtin_importance'] = self._top_k(builtin, top_k)

        # SHAP importance
        shap_vals = self.explainer.shap_values(
            feature_names=self.feature_names
        )
        if shap_vals is not None:
            import numpy as np
            names = self.explainer._feature_names(self.feature_names)
            mean_abs = np.abs(shap_vals).mean(axis=0)
            shap_imp = {n: float(v) for n, v in zip(names, mean_abs)}
            result['shap_importance'] = self._top_k(shap_imp, top_k)

        return result

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _format_importance(
        importance: Dict[str, float], top_k: int
    ) -> List[str]:
        """Format an importance dictionary as ranked text lines.

        Args:
            importance: Feature name to importance mapping.
            top_k: Number of top features to include.

        Returns:
            List of formatted strings.
        """
        sorted_items = sorted(
            importance.items(), key=lambda x: abs(x[1]), reverse=True
        )[:top_k]

        lines = []
        for rank, (name, value) in enumerate(sorted_items, 1):
            lines.append(f'  {rank:>3}. {name:<30s} {value:>12.6f}')
        return lines

    @staticmethod
    def _top_k(importance: Dict[str, float], top_k: int) -> Dict[str, float]:
        """Return the top-k features by absolute importance.

        Args:
            importance: Feature name to importance mapping.
            top_k: Number of top features to keep.

        Returns:
            Filtered dictionary with only the top-k entries.
        """
        sorted_items = sorted(
            importance.items(), key=lambda x: abs(x[1]), reverse=True
        )[:top_k]
        return dict(sorted_items)
