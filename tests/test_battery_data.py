# Tests for BatteryData and CycleData core data structures.

import os
import pytest

from batteryml.data.battery_data import BatteryData, CycleData, CyclingProtocol


class TestCycleData:
    """Tests for the CycleData dataclass."""

    def test_creation_and_attributes(self, sample_cycle_data):
        """CycleData stores all required fields and they are accessible."""
        cd = sample_cycle_data
        assert cd.cycle_number == 0
        assert isinstance(cd.voltage_in_V, list)
        assert isinstance(cd.current_in_A, list)
        assert isinstance(cd.discharge_capacity_in_Ah, list)
        assert len(cd.voltage_in_V) == len(cd.current_in_A)
        assert cd.internal_resistance_in_ohm is not None

    def test_to_dict_round_trip(self, sample_cycle_data):
        """CycleData.to_dict() produces a dict that can recreate the object."""
        cd = sample_cycle_data
        d = cd.to_dict()
        assert isinstance(d, dict)
        assert d["cycle_number"] == cd.cycle_number
        # Recreate from dict
        cd2 = CycleData(**d)
        assert cd2.cycle_number == cd.cycle_number
        assert cd2.voltage_in_V == cd.voltage_in_V

    def test_additional_data(self):
        """Extra keyword arguments are stored in additional_data."""
        cd = CycleData(cycle_number=5, custom_field=[1, 2, 3])
        assert cd.additional_data["custom_field"] == [1, 2, 3]
        d = cd.to_dict()
        assert d["custom_field"] == [1, 2, 3]


class TestBatteryData:
    """Tests for the BatteryData container."""

    def test_creation_and_attributes(self, sample_battery_data):
        """BatteryData stores metadata and cycle data correctly."""
        bd = sample_battery_data
        assert bd.cell_id == "test_cell_001"
        assert bd.nominal_capacity_in_Ah == 1.1
        assert len(bd.cycle_data) == 250
        assert bd.form_factor == "cylindrical"

    def test_print_description(self, sample_battery_data, capsys):
        """print_description runs without error and includes cell_id."""
        sample_battery_data.print_description()
        captured = capsys.readouterr()
        assert "test_cell_001" in captured.out

    def test_to_dict(self, sample_battery_data):
        """to_dict returns a serializable dictionary."""
        d = sample_battery_data.to_dict()
        assert isinstance(d, dict)
        assert d["cell_id"] == "test_cell_001"
        assert isinstance(d["cycle_data"], list)
        assert isinstance(d["cycle_data"][0], dict)
        assert isinstance(d["charge_protocol"], list)

    def test_dump_load_round_trip(self, sample_battery_data, tmp_data_dir):
        """dump() then load() produces an equivalent BatteryData object."""
        path = os.path.join(tmp_data_dir, "cell.pkl")
        sample_battery_data.dump(path)
        loaded = BatteryData.load(path)

        assert loaded.cell_id == sample_battery_data.cell_id
        assert loaded.nominal_capacity_in_Ah == sample_battery_data.nominal_capacity_in_Ah
        assert len(loaded.cycle_data) == len(sample_battery_data.cycle_data)

        # Spot-check a cycle
        orig_c = sample_battery_data.cycle_data[10]
        load_c = loaded.cycle_data[10]
        assert orig_c.cycle_number == load_c.cycle_number
        assert orig_c.voltage_in_V == load_c.voltage_in_V

    def test_empty_cycle_data(self):
        """BatteryData can be created with an empty cycle_data list."""
        bd = BatteryData(cell_id="empty_cell", cycle_data=[])
        assert bd.cell_id == "empty_cell"
        assert len(bd.cycle_data) == 0
        d = bd.to_dict()
        assert d["cycle_data"] == []

    def test_missing_optional_fields(self):
        """BatteryData created with only cell_id has None for optional fields."""
        bd = BatteryData(cell_id="minimal")
        assert bd.cell_id == "minimal"
        assert bd.form_factor is None
        assert bd.nominal_capacity_in_Ah is None
        assert bd.cycle_data is None

    def test_dump_load_empty_cycles(self, tmp_data_dir):
        """dump/load round-trip works for a battery with zero cycles."""
        bd = BatteryData(cell_id="empty", cycle_data=[])
        path = os.path.join(tmp_data_dir, "empty.pkl")
        bd.dump(path)
        loaded = BatteryData.load(path)
        assert loaded.cell_id == "empty"
        assert len(loaded.cycle_data) == 0
