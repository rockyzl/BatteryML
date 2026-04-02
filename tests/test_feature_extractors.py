# Smoke tests for feature extractors.

import pytest
import torch

from batteryml.feature.variance_model import VarianceModelFeatureExtractor
from batteryml.feature.discharge_model import DischargeModelFeatureExtractor
from batteryml.feature.full_model import FullModelFeatureExtractor
from batteryml.feature.voltage_capacity_matrix import (
    VoltageCapacityMatrixFeatureExtractor,
)


class TestVarianceModelFeatureExtractor:
    """Smoke tests for VarianceModelFeatureExtractor."""

    def test_runs_without_error(self, sample_battery_data):
        """Extractor produces output on valid battery data."""
        ext = VarianceModelFeatureExtractor()
        features = ext([sample_battery_data])
        assert isinstance(features, torch.Tensor)

    def test_output_shape_and_values(self, sample_battery_data):
        """Output tensor is non-empty and contains no NaN."""
        ext = VarianceModelFeatureExtractor()
        features = ext([sample_battery_data])
        assert features.numel() > 0
        assert not torch.isnan(features).any()


class TestDischargeModelFeatureExtractor:
    """Smoke tests for DischargeModelFeatureExtractor."""

    def test_runs_without_error(self, sample_battery_data):
        """Extractor produces output on valid battery data."""
        ext = DischargeModelFeatureExtractor()
        features = ext([sample_battery_data])
        assert isinstance(features, torch.Tensor)

    def test_output_shape_and_values(self, sample_battery_data):
        """Output tensor is non-empty and contains no NaN."""
        ext = DischargeModelFeatureExtractor()
        features = ext([sample_battery_data])
        assert features.numel() > 0
        assert not torch.isnan(features).any()


class TestFullModelFeatureExtractor:
    """Smoke tests for FullModelFeatureExtractor."""

    def test_runs_without_error(self, sample_battery_data):
        """Extractor produces output on valid battery data."""
        ext = FullModelFeatureExtractor()
        features = ext([sample_battery_data])
        assert isinstance(features, torch.Tensor)

    def test_output_shape_and_values(self, sample_battery_data):
        """Output tensor is non-empty and contains no NaN."""
        ext = FullModelFeatureExtractor()
        features = ext([sample_battery_data])
        assert features.numel() > 0
        assert not torch.isnan(features).any()


class TestVoltageCapacityMatrixFeatureExtractor:
    """Smoke tests for VoltageCapacityMatrixFeatureExtractor."""

    def test_runs_without_error(self, sample_battery_data):
        """Extractor produces output on valid battery data."""
        ext = VoltageCapacityMatrixFeatureExtractor()
        features = ext([sample_battery_data])
        assert isinstance(features, torch.Tensor)

    def test_output_shape_and_values(self, sample_battery_data):
        """Output tensor is non-empty and contains no NaN."""
        ext = VoltageCapacityMatrixFeatureExtractor()
        features = ext([sample_battery_data])
        assert features.numel() > 0
        assert not torch.isnan(features).any()
