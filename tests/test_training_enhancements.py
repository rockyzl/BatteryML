# Tests for Phase 2 training enhancements (scheduler, early stopping,
# gradient clipping, training history) on the NNModel base class.

import pytest
import torch
import torch.nn as nn

from batteryml.models.nn_model import NNModel


# ---------------------------------------------------------------------------
# Minimal concrete NNModel subclass for testing (NNModel is abstract).
# ---------------------------------------------------------------------------

class _DummyNNModel(NNModel):
    """Minimal concrete subclass so we can instantiate and inspect NNModel."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._linear = nn.Linear(1, 1)

    # Implement abstract methods with stubs
    def process_data(self, dataset):  # noqa: D401
        return dataset

    def build_model(self):
        pass

    def predict(self, dataset):
        return []

    def loss_func(self, *args, **kwargs):
        return torch.tensor(0.0)


class TestNNModelBackwardCompat:
    """Ensure new parameters do not break existing behaviour."""

    def test_nn_model_backward_compat(self):
        """Creating NNModel without new params should work as before."""
        model = _DummyNNModel(epochs=5, batch_size=8)
        assert model.train_epochs == 5
        assert model.train_batch_size == 8

    def test_nn_model_with_scheduler(self):
        """Passing scheduler='cosine' should not raise."""
        model = _DummyNNModel(epochs=5, scheduler='cosine')
        assert model.scheduler == 'cosine'

    def test_nn_model_with_early_stopping(self):
        """Passing early_stopping=True should not raise."""
        model = _DummyNNModel(epochs=5, early_stopping=True)
        assert model.early_stopping is True

    def test_nn_model_with_gradient_clipping(self):
        """Passing gradient_clip_val=1.0 should not raise."""
        model = _DummyNNModel(epochs=5, gradient_clip_val=1.0)
        assert model.gradient_clip_val == 1.0

    def test_nn_model_training_history(self):
        """training_history property should exist and be a list."""
        model = _DummyNNModel(epochs=5)
        history = model.training_history
        assert isinstance(history, list)
