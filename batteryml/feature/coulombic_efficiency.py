# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import torch
import numpy as np
from scipy import stats

from batteryml.builders import FEATURE_EXTRACTORS
from batteryml.data.battery_data import BatteryData
from batteryml.feature.base import BaseFeatureExtractor


@FEATURE_EXTRACTORS.register()
class CoulombicEfficiencyFeatureExtractor(BaseFeatureExtractor):
    """
    Feature extractor based on Coulombic Efficiency (CE) per cycle.
    CE = discharge_capacity / charge_capacity
    Early CE convergence is a strong predictor of SEI stability and battery longevity.
    """

    def __init__(self, early_cycles_n=5, reference_cycle=9, **kwargs):
        super().__init__(**kwargs)
        self.early_cycles_n = early_cycles_n
        self.reference_cycle = reference_cycle

    def _compute_ce_series(self, cell_data: BatteryData):
        """Compute per-cycle Coulombic Efficiency values, skipping invalid cycles."""
        ce_values = []
        for cycle in cell_data.cycle_data:
            charge_cap = cycle.charge_capacity_in_Ah
            discharge_cap = cycle.discharge_capacity_in_Ah
            if charge_cap is None or discharge_cap is None:
                continue
            q_charge = max(charge_cap) if hasattr(charge_cap, '__iter__') else charge_cap
            q_discharge = max(discharge_cap) if hasattr(discharge_cap, '__iter__') else discharge_cap
            if q_charge is None or np.isnan(q_charge) or q_charge == 0:
                continue
            if q_discharge is None or np.isnan(q_discharge):
                continue
            ce = q_discharge / q_charge
            ce_values.append(ce)
        return np.array(ce_values, dtype=np.float64)

    def process_cell(self, cell_data: BatteryData) -> torch.Tensor:
        ce_series = self._compute_ce_series(cell_data)

        n = self.early_cycles_n
        early_ce = ce_series[:n] if len(ce_series) >= n else ce_series

        # Feature 1: ce_mean_early
        ce_mean_early = float(np.mean(early_ce)) if len(early_ce) > 0 else 0.0

        # Feature 2: ce_slope_early — linear fit slope over early window
        if len(early_ce) >= 2:
            x = np.arange(len(early_ce), dtype=np.float64)
            slope, _, _, _, _ = stats.linregress(x, early_ce)
            ce_slope_early = float(slope)
        else:
            ce_slope_early = 0.0

        # Feature 3: ce_std_early — standard deviation of early CE
        ce_std_early = float(np.std(early_ce)) if len(early_ce) > 1 else 0.0

        # Feature 4: ce_convergence_cycle — first cycle index where CE >= 0.999
        convergence_threshold = 0.999
        convergence_indices = np.where(ce_series >= convergence_threshold)[0]
        if len(convergence_indices) > 0:
            ce_convergence_cycle = float(convergence_indices[0])
        else:
            ce_convergence_cycle = float(len(ce_series))

        # Feature 5: ce_at_cycle_n — CE at the reference cycle index
        ref_idx = self.reference_cycle
        if ref_idx < len(ce_series):
            ce_at_cycle_n = float(ce_series[ref_idx])
        elif len(ce_series) > 0:
            ce_at_cycle_n = float(ce_series[-1])
        else:
            ce_at_cycle_n = 0.0

        # Feature 6: ce_delta_early — ce_at_cycle_n minus ce_mean_early
        ce_delta_early = ce_at_cycle_n - ce_mean_early

        features = [
            ce_mean_early,
            ce_slope_early,
            ce_std_early,
            ce_convergence_cycle,
            ce_at_cycle_n,
            ce_delta_early,
        ]

        feature_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
        # Replace NaN and Inf with 0
        feature_tensor = torch.where(
            torch.isnan(feature_tensor) | torch.isinf(feature_tensor),
            torch.zeros_like(feature_tensor),
            feature_tensor,
        )
        return feature_tensor
