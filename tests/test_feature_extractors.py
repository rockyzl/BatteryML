# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Tests for feature extractors."""
import pytest
import torch
from batteryml.feature.variance_model import VarianceModelFeatureExtractor


class TestVarianceModelFeatureExtractor:
    def test_output_is_tensor(self, sample_battery_data):
        """VarianceModelFeatureExtractor returns a torch.Tensor."""
        extractor = VarianceModelFeatureExtractor()
        result = extractor.process_cell(sample_battery_data)
        assert isinstance(result, torch.Tensor)

    def test_output_shape(self, sample_battery_data):
        """Output is a 1-D tensor with one feature value (Variance)."""
        extractor = VarianceModelFeatureExtractor()
        result = extractor.process_cell(sample_battery_data)
        # get_features returns a 1-D tensor; Variance model produces 1 feature
        assert result.dim() == 1
        assert result.shape[0] == 1

    def test_output_finite(self, sample_battery_data):
        """Output contains no NaN or Inf values."""
        extractor = VarianceModelFeatureExtractor()
        result = extractor.process_cell(sample_battery_data)
        assert torch.isfinite(result).all()

    def test_different_cells_give_different_features(
            self, sample_battery_data, small_battery_data):
        """Two batteries with different degradation levels yield different features.

        small_battery_data has only 20 cycles, which is fewer than the default
        critical_cycles=[1, 9, 99], so this test uses a custom extractor that
        only needs cycles up to index 10.
        """
        extractor = VarianceModelFeatureExtractor(
            critical_cycles=[1, 5, 10])
        result_large = extractor.process_cell(sample_battery_data)
        result_small = extractor.process_cell(small_battery_data)
        # The two fixtures have different capacity-fade profiles
        assert not torch.allclose(result_large, result_small)

    def test_batch_call_stacks_correctly(self, sample_battery_data):
        """Calling the extractor on a list of cells stacks into (N, F) tensor."""
        extractor = VarianceModelFeatureExtractor()
        result = extractor([sample_battery_data, sample_battery_data])
        assert isinstance(result, torch.Tensor)
        assert result.shape[0] == 2
        assert result.dim() == 2

    def test_custom_critical_cycles(self, sample_battery_data):
        """VarianceModelFeatureExtractor respects custom critical_cycles."""
        extractor_default = VarianceModelFeatureExtractor()
        extractor_custom = VarianceModelFeatureExtractor(
            critical_cycles=[2, 10, 110])
        result_default = extractor_default.process_cell(sample_battery_data)
        result_custom = extractor_custom.process_cell(sample_battery_data)
        # Different reference cycles should yield different variance values
        assert not torch.allclose(result_default, result_custom)


class TestCoulombicEfficiencyFeatureExtractor:
    """Placeholder tests — will be populated when CE extractor is implemented."""

    def test_import(self):
        """CoulombicEfficiencyFeatureExtractor can be imported."""
        try:
            from batteryml.feature.coulombic_efficiency import (
                CoulombicEfficiencyFeatureExtractor,
            )
            assert CoulombicEfficiencyFeatureExtractor is not None
        except ImportError:
            pytest.skip("CoulombicEfficiencyFeatureExtractor not yet implemented")


class TestdQdVFeatureExtractor:
    """Placeholder tests for dQ/dV extractor."""

    def test_import(self):
        """dQdVFeatureExtractor can be imported."""
        try:
            from batteryml.feature.dqdv import dQdVFeatureExtractor
            assert dQdVFeatureExtractor is not None
        except ImportError:
            pytest.skip("dQdVFeatureExtractor not yet implemented")
