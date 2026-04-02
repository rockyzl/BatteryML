# Tests for the evaluation module (metrics and reports).

import math
import pytest
import numpy as np

from batteryml.evaluation.metrics import (
    rmse, mae, mape, r2_score, get_metric, _validate_inputs,
)
from batteryml.evaluation.report import EvaluationReport


class TestMetricsKnownValues:
    """Verify metric computations against hand-calculated results."""

    def test_rmse_known_values(self):
        """RMSE of [1,2,3] vs [1,2,3] is 0; [1,2,3] vs [4,5,6] is 3."""
        assert rmse(np.array([1, 2, 3]), np.array([1, 2, 3])) == 0.0

        # diff = [3, 3, 3], squared = [9, 9, 9], mean = 9, sqrt = 3
        result = rmse(np.array([1, 2, 3]), np.array([4, 5, 6]))
        assert math.isclose(result, 3.0, abs_tol=1e-9)

    def test_mae_known_values(self):
        """MAE of [1,2,3] vs [2,3,5] is mean([1,1,2]) = 4/3."""
        result = mae(np.array([1, 2, 3]), np.array([2, 3, 5]))
        assert math.isclose(result, 4.0 / 3.0, abs_tol=1e-9)

    def test_mape_known_values(self):
        """MAPE of [100,200] vs [110,190] = mean([10/100, 10/200])*100."""
        y_true = np.array([100.0, 200.0])
        y_pred = np.array([110.0, 190.0])
        expected = (0.1 + 0.05) / 2 * 100  # 7.5%
        result = mape(y_true, y_pred)
        assert math.isclose(result, expected, abs_tol=1e-9)

    def test_r2_perfect_prediction(self):
        """R² should be 1.0 when predictions equal true values."""
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        assert math.isclose(r2_score(y, y), 1.0, abs_tol=1e-9)

    def test_r2_mean_prediction(self):
        """R² should be 0.0 when prediction is the mean of y_true."""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.full_like(y_true, y_true.mean())
        assert math.isclose(r2_score(y_true, y_pred), 0.0, abs_tol=1e-9)


class TestMetricsEdgeCases:
    """Edge cases and input validation for metrics."""

    def test_metrics_torch_numpy_consistency(self):
        """torch.Tensor and numpy inputs should produce the same results."""
        torch = pytest.importorskip("torch")
        y_true_np = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred_np = np.array([1.1, 2.2, 2.9, 4.1])
        y_true_t = torch.tensor(y_true_np)
        y_pred_t = torch.tensor(y_pred_np)

        assert math.isclose(rmse(y_true_np, y_pred_np),
                            rmse(y_true_t, y_pred_t), abs_tol=1e-9)
        assert math.isclose(mae(y_true_np, y_pred_np),
                            mae(y_true_t, y_pred_t), abs_tol=1e-9)
        assert math.isclose(r2_score(y_true_np, y_pred_np),
                            r2_score(y_true_t, y_pred_t), abs_tol=1e-9)

    def test_metrics_empty_input_raises(self):
        """Empty arrays should raise ValueError."""
        with pytest.raises(ValueError):
            rmse(np.array([]), np.array([]))
        with pytest.raises(ValueError):
            mae(np.array([]), np.array([]))

    def test_get_metric_case_insensitive(self):
        """get_metric should look up metrics case-insensitively."""
        assert get_metric('RMSE') is get_metric('rmse')
        assert get_metric('Mae') is get_metric('mae')
        assert get_metric('R2') is get_metric('r2')

        with pytest.raises(ValueError):
            get_metric('nonexistent_metric')


class TestEvaluationReport:
    """Tests for the EvaluationReport class."""

    def test_evaluation_report_summary(self):
        """Report summary generation should not raise and include key info."""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.1, 2.1, 2.9, 4.2, 4.8])
        report = EvaluationReport(
            y_true, y_pred,
            model_name='test_model',
            dataset_name='test_dataset',
        )
        summary = report.summary()
        assert isinstance(summary, str)
        assert 'test_model' in summary
        assert 'test_dataset' in summary

        metrics = report.compute_all_metrics()
        assert 'rmse' in metrics
        assert 'mae' in metrics
        assert 'r2_score' in metrics

    def test_evaluation_report_compare(self):
        """Comparing two reports should not raise and return differences."""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred_a = np.array([1.1, 2.1, 2.9, 4.2, 4.8])
        y_pred_b = np.array([1.5, 2.5, 3.5, 3.5, 5.5])

        report_a = EvaluationReport(y_true, y_pred_a, model_name='model_a')
        report_b = EvaluationReport(y_true, y_pred_b, model_name='model_b')

        comparison = report_a.compare(report_b)
        assert 'metrics' in comparison
        assert 'self_model' in comparison
        assert comparison['self_model'] == 'model_a'
        assert comparison['other_model'] == 'model_b'
        # model_a should have lower RMSE (better)
        assert comparison['metrics']['rmse']['improved'] is True
