# Tests for data transformation classes (ZScore, LogScale, Sequential).

import pytest
import torch

from batteryml.data.transformation.z_score import ZScoreDataTransformation
from batteryml.data.transformation.log_scale import LogScaleDataTransformation
from batteryml.data.transformation.sequential import SequentialDataTransformation


class TestZScoreDataTransformation:
    """Tests for ZScoreDataTransformation fit/transform/inverse_transform."""

    def test_round_trip(self):
        """fit -> transform -> inverse_transform recovers the original data."""
        data = torch.randn(20, 5)
        t = ZScoreDataTransformation()
        t.fit(data)
        transformed = t.transform(data)
        recovered = t.inverse_transform(transformed)
        assert torch.allclose(data, recovered, atol=1e-5)

    def test_transformed_statistics(self):
        """After z-score transform, data should have ~zero mean and ~unit std."""
        data = torch.randn(100, 3) * 5 + 10
        t = ZScoreDataTransformation()
        t.fit(data)
        transformed = t.transform(data)
        assert torch.allclose(transformed.mean(0), torch.zeros(3), atol=1e-5)
        assert torch.allclose(transformed.std(0), torch.ones(3), atol=0.15)

    def test_assert_fitted_raises(self):
        """transform before fit raises AssertionError."""
        t = ZScoreDataTransformation()
        with pytest.raises(AssertionError, match="not fitted"):
            t.transform(torch.tensor([1.0]))

    def test_all_zeros_input(self):
        """All-zero input does not produce NaN (std is clamped)."""
        data = torch.zeros(10, 3)
        t = ZScoreDataTransformation()
        t.fit(data)
        transformed = t.transform(data)
        assert not torch.isnan(transformed).any()

    def test_single_value_input(self):
        """Single-element tensor: ZScore std is NaN due to Bessel correction.

        This is expected behavior — torch.std on a single sample returns NaN.
        We only verify fit/transform/inverse_transform do not raise exceptions.
        """
        data = torch.tensor([[42.0]])
        t = ZScoreDataTransformation()
        t.fit(data)
        transformed = t.transform(data)
        # NaN is expected for single-value due to Bessel-corrected std
        t.inverse_transform(transformed)

    def test_two_samples_roundtrip(self):
        """Two-sample input should round-trip correctly."""
        data = torch.tensor([[42.0], [44.0]])
        t = ZScoreDataTransformation()
        t.fit(data)
        transformed = t.transform(data)
        recovered = t.inverse_transform(transformed)
        assert torch.allclose(data, recovered, atol=1e-5)


class TestLogScaleDataTransformation:
    """Tests for LogScaleDataTransformation."""

    def test_round_trip_natural_log(self):
        """Natural log transform -> inverse recovers the original data."""
        data = torch.rand(20, 5) + 0.1  # positive values
        t = LogScaleDataTransformation()
        transformed = t.transform(data)
        recovered = t.inverse_transform(transformed)
        assert torch.allclose(data, recovered, atol=1e-5)

    def test_round_trip_base10(self):
        """Base-10 log transform -> inverse recovers the original data."""
        data = torch.rand(20, 5) + 0.1
        t = LogScaleDataTransformation(base=10.0)
        transformed = t.transform(data)
        recovered = t.inverse_transform(transformed)
        assert torch.allclose(data, recovered, atol=1e-4)

    def test_transform_values(self):
        """Log transform produces correct values for known inputs."""
        data = torch.tensor([[1.0, 2.718281828]])
        t = LogScaleDataTransformation()  # natural log
        transformed = t.transform(data)
        assert abs(transformed[0, 0].item()) < 1e-5  # ln(1) == 0
        assert abs(transformed[0, 1].item() - 1.0) < 1e-4  # ln(e) ~ 1

    def test_single_value(self):
        """Single positive value transforms and inverts correctly."""
        data = torch.tensor([[5.0]])
        t = LogScaleDataTransformation()
        recovered = t.inverse_transform(t.transform(data))
        assert torch.allclose(data, recovered, atol=1e-5)


class TestSequentialDataTransformation:
    """Tests for SequentialDataTransformation (composing transforms)."""

    def test_round_trip(self):
        """Sequential(LogScale, ZScore) round-trips correctly."""
        data = torch.rand(30, 4) + 0.1
        log_t = LogScaleDataTransformation()
        z_t = ZScoreDataTransformation()
        seq = SequentialDataTransformation(transformations=[log_t, z_t])
        seq.fit(data)
        transformed = seq.transform(data)
        recovered = seq.inverse_transform(transformed)
        assert torch.allclose(data, recovered, atol=1e-4)

    def test_single_transform_sequential(self):
        """Sequential with a single ZScore behaves like ZScore alone."""
        data = torch.randn(20, 3)
        z = ZScoreDataTransformation()
        seq = SequentialDataTransformation(transformations=[z])
        seq.fit(data)
        transformed = seq.transform(data)
        recovered = seq.inverse_transform(transformed)
        assert torch.allclose(data, recovered, atol=1e-5)
