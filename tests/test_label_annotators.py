# Tests for RUL and SOH label annotators.

import math
import pytest
import torch

from batteryml.label.rul import RULLabelAnnotator
from batteryml.label.soh import SOHLabelAnnotator
from batteryml.data.battery_data import BatteryData, CycleData


class TestRULLabelAnnotator:
    """Tests for RULLabelAnnotator."""

    def test_basic_rul(self, sample_battery_data):
        """RUL annotator returns a finite positive tensor for degrading battery."""
        annotator = RULLabelAnnotator(eol_soh=0.8)
        label = annotator.process_cell(sample_battery_data)
        assert isinstance(label, torch.Tensor)
        # The battery degrades to ~75% by cycle 250, so EOL should be found
        assert not torch.isnan(label)
        assert label.item() > 0

    def test_rul_label_via_call(self, sample_battery_data_list):
        """Calling the annotator on a list returns a 1-D tensor of length N."""
        annotator = RULLabelAnnotator(eol_soh=0.8)
        labels = annotator(sample_battery_data_list)
        assert labels.shape == (len(sample_battery_data_list),)
        assert labels.dtype == torch.float32

    def test_no_degradation_battery(self):
        """Battery that never reaches EOL gets a padded label (not NaN by default)."""
        cycles = []
        for i in range(300):
            cycles.append(CycleData(
                cycle_number=i,
                discharge_capacity_in_Ah=[1.1] * 10,
                voltage_in_V=[3.5] * 10,
                current_in_A=[-1.0] * 10,
            ))
        bd = BatteryData(
            cell_id="no_degrade",
            cycle_data=cycles,
            nominal_capacity_in_Ah=1.1,
        )
        annotator = RULLabelAnnotator(eol_soh=0.8, pad_eol=True)
        label = annotator.process_cell(bd)
        # pad_eol=True means it should return a number, not NaN
        assert not torch.isnan(label)
        assert label.item() > 0


class TestSOHLabelAnnotator:
    """Tests for SOHLabelAnnotator."""

    def test_basic_soh_relative(self, sample_battery_data):
        """SOH annotator returns a value between 0 and 1 in relative mode."""
        annotator = SOHLabelAnnotator(cycle_index=100, mode="relative")
        label = annotator.process_cell(sample_battery_data)
        assert isinstance(label, torch.Tensor)
        assert not torch.isnan(label)
        # At cycle 100 the capacity should still be > 0.8 of nominal
        assert 0 < label.item() <= 1.1

    def test_soh_absolute_mode(self, sample_battery_data):
        """SOH annotator in absolute mode returns capacity in Ah."""
        annotator = SOHLabelAnnotator(cycle_index=100, mode="absolute")
        label = annotator.process_cell(sample_battery_data)
        assert not torch.isnan(label)
        # Should be near nominal capacity
        assert 0.5 < label.item() < 1.5

    def test_soh_label_via_call(self, sample_battery_data_list):
        """Calling the annotator on a list returns a 1-D tensor of length N."""
        annotator = SOHLabelAnnotator(cycle_index=100)
        labels = annotator(sample_battery_data_list)
        assert labels.shape == (len(sample_battery_data_list),)

    def test_cycle_index_beyond_data(self):
        """If cycle_index exceeds available cycles, return NaN."""
        cycles = [CycleData(
            cycle_number=0,
            discharge_capacity_in_Ah=[1.0] * 10,
            voltage_in_V=[3.5] * 10,
            current_in_A=[-1.0] * 10,
        )]
        bd = BatteryData(cell_id="short", cycle_data=cycles,
                         nominal_capacity_in_Ah=1.0)
        annotator = SOHLabelAnnotator(cycle_index=100)
        label = annotator.process_cell(bd)
        assert torch.isnan(label)

    def test_no_degradation_soh(self):
        """Battery without degradation gets SOH close to 1.0 in relative mode."""
        cycles = []
        for i in range(200):
            cycles.append(CycleData(
                cycle_number=i,
                discharge_capacity_in_Ah=[1.1] * 10,
                voltage_in_V=[3.5] * 10,
                current_in_A=[-1.0] * 10,
            ))
        bd = BatteryData(
            cell_id="healthy",
            cycle_data=cycles,
            nominal_capacity_in_Ah=1.1,
        )
        annotator = SOHLabelAnnotator(cycle_index=100, mode="relative")
        label = annotator.process_cell(bd)
        assert abs(label.item() - 1.0) < 0.05
