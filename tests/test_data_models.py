# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Tests for core BatteryData and CycleData models."""
import pytest
from batteryml.data.battery_data import BatteryData, CycleData


class TestCycleData:
    def test_cycle_data_creation(self):
        """CycleData can be created with required fields."""
        cycle = CycleData(
            cycle_number=1,
            voltage_in_V=[3.6, 3.5, 3.4],
            current_in_A=[-1.0, -1.0, -1.0],
            discharge_capacity_in_Ah=[0.0, 0.5, 1.0],
            charge_capacity_in_Ah=[0.0, 0.5, 1.02],
            time_in_s=[0.0, 1800.0, 3600.0],
            temperature_in_C=[25.0, 25.1, 25.2],
            internal_resistance_in_ohm=0.05,
        )
        assert cycle.cycle_number == 1
        assert cycle.voltage_in_V == [3.6, 3.5, 3.4]
        assert cycle.current_in_A == [-1.0, -1.0, -1.0]
        assert cycle.internal_resistance_in_ohm == pytest.approx(0.05)

    def test_cycle_data_empty_lists(self):
        """CycleData handles empty measurement lists."""
        cycle = CycleData(
            cycle_number=0,
            voltage_in_V=[],
            current_in_A=[],
            discharge_capacity_in_Ah=[],
            charge_capacity_in_Ah=[],
        )
        assert cycle.cycle_number == 0
        assert cycle.voltage_in_V == []
        assert cycle.discharge_capacity_in_Ah == []

    def test_cycle_data_defaults_to_none(self):
        """CycleData optional fields default to None."""
        cycle = CycleData(cycle_number=5)
        assert cycle.voltage_in_V is None
        assert cycle.current_in_A is None
        assert cycle.temperature_in_C is None
        assert cycle.internal_resistance_in_ohm is None

    def test_cycle_data_additional_data(self):
        """CycleData stores extra keyword arguments in additional_data dict."""
        cycle = CycleData(cycle_number=1, custom_field=42.0)
        assert 'custom_field' in cycle.additional_data
        assert cycle.additional_data['custom_field'] == 42.0

    def test_cycle_data_to_dict(self):
        """CycleData.to_dict() returns a dict with all standard keys."""
        cycle = CycleData(
            cycle_number=3,
            voltage_in_V=[3.5],
            current_in_A=[-1.0],
        )
        d = cycle.to_dict()
        assert isinstance(d, dict)
        assert d['cycle_number'] == 3
        assert 'voltage_in_V' in d
        assert 'current_in_A' in d


class TestBatteryData:
    def test_battery_data_creation(self, sample_battery_data):
        """BatteryData can be created and has correct cycle count."""
        assert len(sample_battery_data.cycle_data) == 150

    def test_battery_data_cell_id(self, sample_battery_data):
        """BatteryData has expected cell_id."""
        assert sample_battery_data.cell_id == 'test_cell_001'

    def test_battery_data_nominal_capacity(self, sample_battery_data):
        """BatteryData has expected nominal capacity."""
        assert sample_battery_data.nominal_capacity_in_Ah == pytest.approx(1.1)

    def test_battery_data_material_fields(self, sample_battery_data):
        """BatteryData stores cathode and anode material strings."""
        assert sample_battery_data.cathode_material == 'LFP'
        assert sample_battery_data.anode_material == 'graphite'

    def test_battery_data_default_protocols_empty(self):
        """BatteryData charge/discharge protocols default to empty lists."""
        cell = BatteryData(cell_id='minimal_cell')
        assert cell.charge_protocol == []
        assert cell.discharge_protocol == []

    def test_battery_data_cycle_data_none_by_default(self):
        """BatteryData cycle_data is None when not provided."""
        cell = BatteryData(cell_id='no_cycles')
        assert cell.cycle_data is None

    def test_battery_data_small_fixture(self, small_battery_data):
        """small_battery_data fixture has 20 cycles."""
        assert len(small_battery_data.cycle_data) == 20
        assert small_battery_data.cell_id == 'test_cell_small'

    def test_battery_data_capacity_fade(self, sample_battery_data):
        """Discharge capacity decreases over cycles (degradation is modelled)."""
        first_cycle_cap = max(
            sample_battery_data.cycle_data[0].discharge_capacity_in_Ah)
        last_cycle_cap = max(
            sample_battery_data.cycle_data[-1].discharge_capacity_in_Ah)
        assert last_cycle_cap < first_cycle_cap

    def test_battery_data_to_dict_roundtrip(self, sample_battery_data):
        """BatteryData.to_dict() contains expected top-level keys."""
        d = sample_battery_data.to_dict()
        assert isinstance(d, dict)
        assert 'cell_id' in d
        assert 'cycle_data' in d
        assert isinstance(d['cycle_data'], list)
        assert len(d['cycle_data']) == 150
