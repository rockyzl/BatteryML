# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import torch
import numpy as np
from scipy.signal import savgol_filter
from scipy.stats import skew

from batteryml.builders import FEATURE_EXTRACTORS
from batteryml.data.battery_data import BatteryData
from batteryml.feature.base import BaseFeatureExtractor


@FEATURE_EXTRACTORS.register()
class dQdVFeatureExtractor(BaseFeatureExtractor):
    """
    Differential capacity (dQ/dV) feature extractor.

    dQ/dV peaks correspond to phase transitions in electrode materials.
    Peak position shifts and area changes indicate LAM (Loss of Active
    Material) and LLI (Loss of Lithium Inventory).
    """

    def __init__(self, interp_dim=1000, sg_window=51, sg_polyorder=3,
                 ref_cycle=9, eval_cycle=99, **kwargs):
        super().__init__(**kwargs)
        self.interp_dim = interp_dim
        self.sg_window = sg_window
        self.sg_polyorder = sg_polyorder
        self.ref_cycle = ref_cycle
        self.eval_cycle = eval_cycle

    def _compute_dqdv(self, voltage, capacity):
        """Compute smoothed dQ/dV curve for a single cycle.

        Args:
            voltage: array of voltage values (V)
            capacity: array of discharge capacity values (Ah)

        Returns:
            Tuple of (dqdv, voltage_interp) arrays, or (None, None) if
            insufficient data.
        """
        voltage = np.array(voltage, dtype=np.float64)
        capacity = np.array(capacity, dtype=np.float64)

        # Filter out NaN/Inf values
        valid_mask = np.isfinite(voltage) & np.isfinite(capacity)
        voltage = voltage[valid_mask]
        capacity = capacity[valid_mask]

        if len(voltage) < 10:
            return None, None

        # Sort by voltage (discharge curves may be descending)
        sort_idx = np.argsort(voltage)
        voltage = voltage[sort_idx]
        capacity = capacity[sort_idx]

        # Remove duplicate voltage values
        _, unique_idx = np.unique(voltage, return_index=True)
        voltage = voltage[unique_idx]
        capacity = capacity[unique_idx]

        if len(voltage) < 10:
            return None, None

        v_min = voltage.min()
        v_max = voltage.max()

        if v_max - v_min < 1e-6:
            return None, None

        # Interpolate capacity onto uniform voltage grid
        voltage_interp = np.linspace(v_min, v_max, self.interp_dim)
        capacity_interp = np.interp(voltage_interp, voltage, capacity)

        # Smooth with Savitzky-Golay filter
        # Ensure window length doesn't exceed data length and is odd
        window = min(self.sg_window, len(capacity_interp))
        if window % 2 == 0:
            window -= 1
        polyorder = min(self.sg_polyorder, window - 1)

        if window < polyorder + 2:
            return None, None

        capacity_smooth = savgol_filter(capacity_interp, window, polyorder)

        # Numerical differentiation: dQ/dV
        dv = np.diff(voltage_interp)
        dq = np.diff(capacity_smooth)

        # Avoid division by near-zero
        dv = np.where(np.abs(dv) < 1e-10, 1e-10, dv)
        dqdv = dq / dv

        # Voltage midpoints corresponding to dQ/dV values
        voltage_mid = 0.5 * (voltage_interp[:-1] + voltage_interp[1:])

        return dqdv, voltage_mid

    def _extract_peak_features(self, dqdv, voltage_interp):
        """Extract peak position, height, FWHM, and area from dQ/dV curve.

        Args:
            dqdv: array of dQ/dV values
            voltage_interp: array of voltage midpoints

        Returns:
            dict with keys: peak_voltage, peak_height, peak_fwhm, peak_area
        """
        zero_features = {
            'peak_voltage': 0.0,
            'peak_height': 0.0,
            'peak_fwhm': 0.0,
            'peak_area': 0.0,
        }

        if dqdv is None or len(dqdv) == 0:
            return zero_features

        peak_idx = int(np.argmax(dqdv))
        peak_height = float(dqdv[peak_idx])
        peak_voltage = float(voltage_interp[peak_idx])

        # Half-maximum threshold
        half_max = peak_height / 2.0

        # Find left boundary (first crossing of half_max going left from peak)
        left_idx = peak_idx
        for i in range(peak_idx, -1, -1):
            if dqdv[i] <= half_max:
                left_idx = i
                break

        # Find right boundary (first crossing of half_max going right from peak)
        right_idx = peak_idx
        for i in range(peak_idx, len(dqdv)):
            if dqdv[i] <= half_max:
                right_idx = i
                break

        peak_fwhm = float(voltage_interp[right_idx] - voltage_interp[left_idx])

        # Peak area: trapezoid integration over the FWHM region
        peak_area = float(
            np.trapz(dqdv[left_idx:right_idx + 1],
                     voltage_interp[left_idx:right_idx + 1])
        )

        return {
            'peak_voltage': peak_voltage,
            'peak_height': peak_height,
            'peak_fwhm': abs(peak_fwhm),
            'peak_area': abs(peak_area),
        }

    def process_cell(self, cell_data: BatteryData) -> torch.Tensor:
        """Extract dQ/dV features from a battery cell.

        Features extracted:
            0: peak_voltage (ref cycle)
            1: peak_height (ref cycle)
            2: peak_fwhm (ref cycle)
            3: peak_area (ref cycle)
            4: peak_voltage (eval cycle)
            5: peak_height (eval cycle)
            6: peak_fwhm (eval cycle)
            7: peak_area (eval cycle)
            8: delta_peak_voltage (eval - ref)
            9: delta_peak_height (eval - ref)
            10: dqdv_variance (eval cycle)
            11: dqdv_skewness (eval cycle)

        Returns:
            torch.Tensor of shape (1, 12)
        """
        num_features = 12
        zero_features = [0.0] * num_features

        num_cycles = len(cell_data.cycle_data)

        # Helper to safely get dQ/dV for a given cycle index
        def get_cycle_features(cycle_idx):
            if cycle_idx >= num_cycles:
                return None, None
            cycle = cell_data.cycle_data[cycle_idx]
            voltage = cycle.voltage_in_V
            capacity = cycle.discharge_capacity_in_Ah
            if voltage is None or capacity is None:
                return None, None
            return self._compute_dqdv(voltage, capacity)

        # Reference cycle features
        ref_dqdv, ref_voltage = get_cycle_features(self.ref_cycle)
        ref_peaks = self._extract_peak_features(ref_dqdv, ref_voltage)

        # Eval cycle features
        eval_dqdv, eval_voltage = get_cycle_features(self.eval_cycle)
        eval_peaks = self._extract_peak_features(eval_dqdv, eval_voltage)

        # Delta features
        delta_peak_voltage = eval_peaks['peak_voltage'] - ref_peaks['peak_voltage']
        delta_peak_height = eval_peaks['peak_height'] - ref_peaks['peak_height']

        # Statistical features on eval dQ/dV curve
        if eval_dqdv is not None and len(eval_dqdv) > 1:
            dqdv_variance = float(np.var(eval_dqdv))
            dqdv_skewness = float(skew(eval_dqdv))
            if not np.isfinite(dqdv_skewness):
                dqdv_skewness = 0.0
        else:
            dqdv_variance = 0.0
            dqdv_skewness = 0.0

        features = [
            ref_peaks['peak_voltage'],
            ref_peaks['peak_height'],
            ref_peaks['peak_fwhm'],
            ref_peaks['peak_area'],
            eval_peaks['peak_voltage'],
            eval_peaks['peak_height'],
            eval_peaks['peak_fwhm'],
            eval_peaks['peak_area'],
            delta_peak_voltage,
            delta_peak_height,
            dqdv_variance,
            dqdv_skewness,
        ]

        # Replace any remaining NaN/Inf with 0
        features = [f if np.isfinite(f) else 0.0 for f in features]

        return torch.tensor(features, dtype=torch.float32).unsqueeze(0)
