# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Tests for label annotators."""
import math
import pytest
import torch
from batteryml.label.rul import RULLabelAnnotator
from batteryml.label.soh import SOHLabelAnnotator


class TestRULLabelAnnotator:
    def test_output_is_tensor(self, sample_battery_data):
        """RULLabelAnnotator.process_cell returns a torch.Tensor."""
        annotator = RULLabelAnnotator()
        result = annotator.process_cell(sample_battery_data)
        assert isinstance(result, torch.Tensor)

    def test_rul_is_scalar(self, sample_battery_data):
        """process_cell returns a scalar (0-dim) tensor."""
        annotator = RULLabelAnnotator()
        result = annotator.process_cell(sample_battery_data)
        assert result.dim() == 0

    def test_rul_is_non_negative_or_nan(self, sample_battery_data):
        """RUL value is either non-negative or NaN (when below min_rul_limit)."""
        annotator = RULLabelAnnotator()
        result = annotator.process_cell(sample_battery_data)
        if not torch.isnan(result):
            assert result.item() >= 0

    def test_rul_with_low_min_limit(self, sample_battery_data):
        """With min_rul_limit=0 the annotator always returns a finite value."""
        annotator = RULLabelAnnotator(min_rul_limit=0.0)
        result = annotator.process_cell(sample_battery_data)
        assert not torch.isnan(result)
        assert result.item() >= 0

    def test_rul_eol_soh_threshold(self, sample_battery_data):
        """Lower eol_soh threshold means cell reaches EOL later (higher RUL)."""
        annotator_strict = RULLabelAnnotator(eol_soh=0.9, min_rul_limit=0.0)
        annotator_lenient = RULLabelAnnotator(eol_soh=0.7, min_rul_limit=0.0)
        rul_strict = annotator_strict.process_cell(sample_battery_data).item()
        rul_lenient = annotator_lenient.process_cell(sample_battery_data).item()
        # Stricter threshold (higher eol_soh) triggers EOL sooner => lower RUL
        assert rul_strict <= rul_lenient

    def test_batch_call_returns_1d_tensor(self, sample_battery_data):
        """Calling annotator on a list produces a 1-D float tensor."""
        annotator = RULLabelAnnotator()
        result = annotator([sample_battery_data, sample_battery_data])
        assert isinstance(result, torch.Tensor)
        assert result.dim() == 1
        assert result.shape[0] == 2
        assert result.dtype == torch.float32

    def test_pad_eol_false_gives_nan_when_no_eol(self):
        """With pad_eol=False, cells that never reach EOL are labelled NaN."""
        from tests.conftest import make_cycle
        from batteryml.data.battery_data import BatteryData

        # Cell that never fades below 80% within 50 cycles
        cycles = [make_cycle(i, capacity_fade=0.0) for i in range(50)]
        cell = BatteryData(
            cell_id='no_eol_cell',
            cycle_data=cycles,
            nominal_capacity_in_Ah=1.1,
        )
        annotator = RULLabelAnnotator(eol_soh=0.8, pad_eol=False,
                                      min_rul_limit=0.0)
        result = annotator.process_cell(cell)
        assert torch.isnan(result)


class TestSOHLabelAnnotator:
    def test_output_is_tensor(self, sample_battery_data):
        """SOHLabelAnnotator.process_cell returns a torch.Tensor."""
        annotator = SOHLabelAnnotator()
        result = annotator.process_cell(sample_battery_data)
        assert isinstance(result, torch.Tensor)

    def test_soh_is_scalar(self, sample_battery_data):
        """process_cell returns a scalar (0-dim) tensor."""
        annotator = SOHLabelAnnotator()
        result = annotator.process_cell(sample_battery_data)
        assert result.dim() == 0

    def test_soh_relative_mode_range(self, sample_battery_data):
        """SOH in relative mode is in a physically plausible range (0, 1.5]."""
        annotator = SOHLabelAnnotator(cycle_index=100, mode='relative')
        result = annotator.process_cell(sample_battery_data)
        if not torch.isnan(result):
            assert 0.0 < result.item() <= 1.5

    def test_soh_nan_when_not_enough_cycles(self, small_battery_data):
        """SOH is NaN when the cell has fewer cycles than cycle_index."""
        # small_battery_data has 20 cycles; default cycle_index=100
        annotator = SOHLabelAnnotator(cycle_index=100)
        result = annotator.process_cell(small_battery_data)
        assert torch.isnan(result)

    def test_soh_absolute_mode(self, sample_battery_data):
        """SOH in absolute mode returns a capacity value in Ah."""
        annotator = SOHLabelAnnotator(cycle_index=100, mode='absolute')
        result = annotator.process_cell(sample_battery_data)
        if not torch.isnan(result):
            # Should be a positive capacity value
            assert result.item() > 0.0

    def test_soh_early_cycle_index(self, small_battery_data):
        """SOH is finite when cycle_index is within available cycle count."""
        annotator = SOHLabelAnnotator(cycle_index=10, mode='relative')
        result = annotator.process_cell(small_battery_data)
        assert not torch.isnan(result)
        assert result.item() > 0.0

    def test_batch_call_returns_1d_tensor(self, sample_battery_data):
        """Calling annotator on a list produces a 1-D float tensor."""
        annotator = SOHLabelAnnotator(cycle_index=50)
        result = annotator([sample_battery_data, sample_battery_data])
        assert isinstance(result, torch.Tensor)
        assert result.dim() == 1
        assert result.shape[0] == 2
        assert result.dtype == torch.float32
