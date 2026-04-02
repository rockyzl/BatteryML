# Shared pytest fixtures for BatteryML tests.

import math
import pytest
import tempfile
import numpy as np

from batteryml.data.battery_data import BatteryData, CycleData, CyclingProtocol


def _make_cycle(cycle_number, nominal_cap=1.1, degradation=0.0, n_points=50):
    """Helper: create a realistic CycleData with slight degradation applied."""
    cap = nominal_cap * (1.0 - degradation)
    t = np.linspace(0, 3600, n_points).tolist()
    voltage = np.linspace(3.0, 4.2, n_points).tolist()
    current_charge = [1.0] * n_points
    current_discharge = [-1.0] * n_points
    # Combine charge/discharge into one series (simplified)
    current = (current_charge[: n_points // 2]
               + current_discharge[n_points // 2:])
    charge_cap = np.linspace(0, cap, n_points).tolist()
    discharge_cap = np.linspace(0, cap, n_points).tolist()
    temperature = np.linspace(25.0, 35.0, n_points).tolist()

    return CycleData(
        cycle_number=cycle_number,
        voltage_in_V=voltage,
        current_in_A=current,
        charge_capacity_in_Ah=charge_cap,
        discharge_capacity_in_Ah=discharge_cap,
        time_in_s=t,
        temperature_in_C=temperature,
        internal_resistance_in_ohm=0.02 + degradation * 0.1,
    )


@pytest.fixture
def sample_cycle_data():
    """A single CycleData object with reasonable simulated data."""
    return _make_cycle(cycle_number=0, nominal_cap=1.1)


@pytest.fixture
def sample_battery_data():
    """A BatteryData object with 250 cycles simulating capacity fade.

    The nominal capacity is 1.1 Ah and the discharge capacity degrades
    linearly so that by cycle 250 it has dropped to about 80% of nominal.
    """
    n_cycles = 250
    cycles = []
    for i in range(n_cycles):
        # Linear degradation from 0% to ~25% over 250 cycles
        degradation = 0.25 * i / (n_cycles - 1)
        cycles.append(_make_cycle(cycle_number=i,
                                  nominal_cap=1.1,
                                  degradation=degradation))

    return BatteryData(
        cell_id="test_cell_001",
        cycle_data=cycles,
        nominal_capacity_in_Ah=1.1,
        form_factor="cylindrical",
        anode_material="graphite",
        cathode_material="NMC",
        min_voltage_limit_in_V=3.0,
        max_voltage_limit_in_V=4.2,
        charge_protocol=[CyclingProtocol(rate_in_C=1.0)],
        discharge_protocol=[CyclingProtocol(rate_in_C=1.0)],
    )


@pytest.fixture
def sample_battery_data_list(sample_battery_data):
    """A list of 5 BatteryData objects with varying degradation profiles."""
    import copy
    batteries = []
    for idx in range(5):
        bat = copy.deepcopy(sample_battery_data)
        bat.cell_id = f"test_cell_{idx:03d}"
        batteries.append(bat)
    return batteries


@pytest.fixture
def tmp_data_dir():
    """Provide a temporary directory for file I/O tests."""
    with tempfile.TemporaryDirectory() as d:
        yield d
