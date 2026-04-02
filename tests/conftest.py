# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""
Shared pytest fixtures for BatteryML tests.
"""
import pytest
import numpy as np
from batteryml.data.battery_data import BatteryData, CycleData


def make_cycle(cycle_number, n_points=100, capacity_fade=0.0):
    """Create a synthetic CycleData for testing."""
    # Discharge curve: voltage drops from 3.6V to 2.5V
    voltage = np.linspace(3.6, 2.5, n_points).tolist()
    current = [-1.0] * n_points  # constant current discharge
    time = np.linspace(0, 3600, n_points).tolist()
    # Discharge capacity fades gradually with cycle number
    base_capacity = 1.1 * (1.0 - capacity_fade)
    discharge_cap = np.linspace(0, base_capacity, n_points).tolist()
    charge_cap = np.linspace(0, base_capacity / 0.98, n_points).tolist()  # CE ~0.98
    temperature = [25.0] * n_points

    return CycleData(
        cycle_number=cycle_number,
        voltage_in_V=voltage,
        current_in_A=current,
        time_in_s=time,
        discharge_capacity_in_Ah=discharge_cap,
        charge_capacity_in_Ah=charge_cap,
        temperature_in_C=temperature,
        internal_resistance_in_ohm=0.05 + cycle_number * 0.0001,
    )


@pytest.fixture
def sample_battery_data():
    """A synthetic BatteryData with 150 cycles showing gradual degradation.

    min/max voltage limits are set so that VarianceModelFeatureExtractor
    can compute interpolated Qdlin curves without hitting NaN issues.
    """
    cycles = []
    for i in range(150):
        fade = min(i / 200.0, 0.3)  # max 30% fade
        cycles.append(make_cycle(i, capacity_fade=fade))

    return BatteryData(
        cell_id='test_cell_001',
        cycle_data=cycles,
        nominal_capacity_in_Ah=1.1,
        form_factor='cylindrical',
        cathode_material='LFP',
        anode_material='graphite',
        min_voltage_limit_in_V=2.5,
        max_voltage_limit_in_V=3.6,
    )


@pytest.fixture
def small_battery_data():
    """A small BatteryData with only 20 cycles (for early-cycle testing)."""
    cycles = [make_cycle(i, capacity_fade=i / 100.0) for i in range(20)]
    return BatteryData(
        cell_id='test_cell_small',
        cycle_data=cycles,
        nominal_capacity_in_Ah=1.1,
        cathode_material='NMC',
        anode_material='graphite',
        min_voltage_limit_in_V=2.5,
        max_voltage_limit_in_V=3.6,
    )
