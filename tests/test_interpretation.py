# Tests for the model interpretation / explainability module (Phase 2).

import pytest
import numpy as np


class TestExplainerImport:
    """Verify the interpretation module can be imported."""

    def test_explainer_import(self):
        """Importing the interpretation module should not crash."""
        try:
            import batteryml.interpretation  # noqa: F401
        except ImportError:
            pytest.skip(
                "batteryml.interpretation module not yet implemented")
        except Exception as exc:
            pytest.fail(
                f"Unexpected error importing batteryml.interpretation: {exc}")


class TestPermutationImportance:
    """Tests for permutation-based feature importance."""

    def test_permutation_importance(self):
        """permutation_importance should return a dict of feature->score."""
        try:
            from batteryml.interpretation import permutation_importance
        except ImportError:
            pytest.skip(
                "batteryml.interpretation.permutation_importance "
                "not yet available")

        # Build a trivial sklearn model for testing
        sklearn = pytest.importorskip("sklearn")
        from sklearn.ensemble import RandomForestRegressor

        rng = np.random.RandomState(42)
        X = rng.randn(100, 3)
        y = X[:, 0] * 2 + X[:, 1] * 0.5 + rng.randn(100) * 0.1
        feature_names = ['feat_a', 'feat_b', 'feat_c']

        model = RandomForestRegressor(n_estimators=10, random_state=42)
        model.fit(X, y)

        result = permutation_importance(
            model, X, y, feature_names=feature_names)
        assert isinstance(result, dict)
        assert len(result) == 3
        for name in feature_names:
            assert name in result


class TestBuiltinImportance:
    """Tests for extracting built-in feature importance from sklearn models."""

    def test_builtin_importance_sklearn(self):
        """Built-in importance from a RandomForest should be a dict."""
        try:
            from batteryml.interpretation import builtin_importance
        except ImportError:
            pytest.skip(
                "batteryml.interpretation.builtin_importance "
                "not yet available")

        sklearn = pytest.importorskip("sklearn")
        from sklearn.ensemble import RandomForestRegressor

        rng = np.random.RandomState(42)
        X = rng.randn(100, 3)
        y = X[:, 0] * 2 + rng.randn(100) * 0.1
        feature_names = ['a', 'b', 'c']

        model = RandomForestRegressor(n_estimators=10, random_state=42)
        model.fit(X, y)

        result = builtin_importance(model, feature_names=feature_names)
        assert isinstance(result, dict)
        assert len(result) == 3
        # Feature 'a' should have the highest importance
        assert result['a'] > result['b']
        assert result['a'] > result['c']


class TestPlotImportance:
    """Tests for importance visualization."""

    def test_plot_importance_no_error(self):
        """Plotting feature importance should not raise (Agg backend)."""
        try:
            from batteryml.interpretation import plot_importance
        except ImportError:
            pytest.skip(
                "batteryml.interpretation.plot_importance not yet available")

        import matplotlib
        matplotlib.use('Agg')

        importances = {'feat_a': 0.5, 'feat_b': 0.3, 'feat_c': 0.2}
        # Should not raise
        fig = plot_importance(importances)
        assert fig is not None
