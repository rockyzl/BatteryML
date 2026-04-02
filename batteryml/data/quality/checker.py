"""Automated data quality checker for battery cycling data.

自动化电池循环数据质量检测器。检测缺失值、异常循环、数据一致性和传感器噪声。
"""

import logging
from typing import Any, Dict, List, Optional

import numpy as np

from batteryml.data.quality.report import QualityReport

logger = logging.getLogger(__name__)


class DataQualityChecker:
    """Automated data quality checker for battery cycling data.

    Runs a suite of checks on a BatteryData object and produces a
    QualityReport with scored findings and actionable issues.

    Usage:
        checker = DataQualityChecker()
        report = checker.check(battery_data)
        print(report.summary())
        issues = report.get_issues(severity='warning')
    """

    def __init__(
        self,
        capacity_jump_threshold: float = 0.20,
        capacity_recovery_threshold: float = 0.05,
        noise_std_threshold: float = 0.01,
    ):
        """Initialize the checker with configurable thresholds.

        Args:
            capacity_jump_threshold: Relative capacity change between
                adjacent cycles to flag as anomaly (default 20%).
            capacity_recovery_threshold: Capacity increase threshold
                to flag unexpected recovery (default 5%).
            noise_std_threshold: Voltage noise std threshold in V.
        """
        self.capacity_jump_threshold = capacity_jump_threshold
        self.capacity_recovery_threshold = capacity_recovery_threshold
        self.noise_std_threshold = noise_std_threshold

    def check(self, battery_data) -> QualityReport:
        """Run all quality checks on a BatteryData object.

        Args:
            battery_data: A BatteryData instance.

        Returns:
            QualityReport with all check results.
        """
        results = {}
        results['basic_stats'] = self._check_basic_stats(battery_data)
        results['missing_data'] = self._check_missing_data(battery_data)
        results['anomaly_detection'] = self._check_anomalies(battery_data)
        results['consistency'] = self._check_consistency(battery_data)
        results['noise_estimation'] = self._check_noise(battery_data)

        return QualityReport(
            cell_id=getattr(battery_data, 'cell_id', 'unknown'),
            checks_results=results,
        )

    def check_batch(self, battery_data_list: list) -> List[QualityReport]:
        """Run checks on multiple BatteryData objects.

        Args:
            battery_data_list: List of BatteryData instances.

        Returns:
            List of QualityReport objects.
        """
        return [self.check(bd) for bd in battery_data_list]

    # ------------------------------------------------------------------
    # Individual check implementations
    # ------------------------------------------------------------------

    def _check_basic_stats(self, bd) -> Dict[str, Any]:
        """Compute basic statistics for the battery data."""
        issues: List[Dict] = []
        cycles = getattr(bd, 'cycle_data', []) or []
        n_cycles = len(cycles)

        if n_cycles == 0:
            issues.append({
                'severity': 'error',
                'message': 'No cycle data found.',
            })
            return {'score': 0.0, 'issues': issues, 'n_cycles': 0}

        # Data points per cycle
        points_per_cycle = []
        for c in cycles:
            v = getattr(c, 'voltage_in_V', None) or []
            points_per_cycle.append(len(v))

        stats = {
            'n_cycles': n_cycles,
            'points_per_cycle_mean': float(np.mean(points_per_cycle)) if points_per_cycle else 0,
            'points_per_cycle_min': int(np.min(points_per_cycle)) if points_per_cycle else 0,
            'points_per_cycle_max': int(np.max(points_per_cycle)) if points_per_cycle else 0,
        }

        empty_cycles = sum(1 for p in points_per_cycle if p == 0)
        if empty_cycles > 0:
            issues.append({
                'severity': 'warning',
                'message': f'{empty_cycles} cycle(s) have zero data points.',
            })

        score = max(0.0, 100.0 - (empty_cycles / max(n_cycles, 1)) * 100)
        return {'score': score, 'issues': issues, **stats}

    def _check_missing_data(self, bd) -> Dict[str, Any]:
        """Check for missing data fields in cycle data."""
        issues: List[Dict] = []
        cycles = getattr(bd, 'cycle_data', []) or []
        if not cycles:
            return {'score': 100.0, 'issues': issues}

        fields = [
            'voltage_in_V', 'current_in_A',
            'charge_capacity_in_Ah', 'discharge_capacity_in_Ah',
            'time_in_s', 'temperature_in_C',
        ]

        missing_counts = {f: 0 for f in fields}
        for c in cycles:
            for f in fields:
                val = getattr(c, f, None)
                if val is None or (isinstance(val, (list, np.ndarray)) and len(val) == 0):
                    missing_counts[f] += 1

        n = len(cycles)
        for f, count in missing_counts.items():
            if count > 0:
                pct = count / n * 100
                severity = 'error' if pct > 50 else 'warning' if pct > 10 else 'info'
                issues.append({
                    'severity': severity,
                    'message': f'{f}: missing in {count}/{n} cycles ({pct:.1f}%)',
                })

        total_missing = sum(missing_counts.values())
        total_possible = n * len(fields)
        score = max(0.0, 100.0 - (total_missing / max(total_possible, 1)) * 100)
        return {'score': score, 'issues': issues}

    def _check_anomalies(self, bd) -> Dict[str, Any]:
        """Detect anomalous cycles (capacity jumps, zero capacity, etc.)."""
        issues: List[Dict] = []
        cycles = getattr(bd, 'cycle_data', []) or []
        if len(cycles) < 2:
            return {'score': 100.0, 'issues': issues}

        # Extract discharge capacities
        capacities = []
        for c in cycles:
            dc = getattr(c, 'discharge_capacity_in_Ah', None) or []
            if isinstance(dc, (list, np.ndarray)) and len(dc) > 0:
                capacities.append(float(dc[-1]) if len(dc) > 0 else 0.0)
            else:
                capacities.append(None)

        anomaly_count = 0
        n_valid = sum(1 for c in capacities if c is not None and c > 0)

        for i in range(1, len(capacities)):
            prev, curr = capacities[i - 1], capacities[i]
            if prev is None or curr is None or prev == 0:
                continue

            change = abs(curr - prev) / abs(prev)
            if change > self.capacity_jump_threshold:
                anomaly_count += 1
                if anomaly_count <= 5:  # Limit reported issues
                    issues.append({
                        'severity': 'warning',
                        'message': (
                            f'Capacity jump at cycle {i}: '
                            f'{prev:.4f} -> {curr:.4f} ({change*100:.1f}% change)'
                        ),
                    })

            # Unexpected recovery
            if curr > prev * (1 + self.capacity_recovery_threshold):
                if anomaly_count <= 10:
                    issues.append({
                        'severity': 'info',
                        'message': (
                            f'Capacity recovery at cycle {i}: '
                            f'{prev:.4f} -> {curr:.4f}'
                        ),
                    })

        if anomaly_count > 5:
            issues.append({
                'severity': 'warning',
                'message': f'Total {anomaly_count} capacity anomalies detected '
                           f'(showing first 5).',
            })

        # Zero capacity cycles
        zero_caps = sum(1 for c in capacities if c is not None and c == 0)
        if zero_caps > 0:
            issues.append({
                'severity': 'error',
                'message': f'{zero_caps} cycle(s) with zero discharge capacity.',
            })

        n_total = len(capacities)
        score = max(0.0, 100.0 - (anomaly_count + zero_caps) / max(n_total, 1) * 100)
        return {'score': score, 'issues': issues}

    def _check_consistency(self, bd) -> Dict[str, Any]:
        """Check data consistency (cycle numbering, voltage limits, etc.)."""
        issues: List[Dict] = []
        cycles = getattr(bd, 'cycle_data', []) or []
        if not cycles:
            return {'score': 100.0, 'issues': issues}

        # Check cycle numbering continuity
        cycle_numbers = [
            getattr(c, 'cycle_number', None) for c in cycles
        ]
        cycle_numbers = [n for n in cycle_numbers if n is not None]

        if cycle_numbers:
            gaps = []
            for i in range(1, len(cycle_numbers)):
                if cycle_numbers[i] != cycle_numbers[i - 1] + 1:
                    gaps.append(i)
            if gaps:
                issues.append({
                    'severity': 'info',
                    'message': f'Cycle numbering has {len(gaps)} gap(s).',
                })

        # Check voltage within limits
        v_min_limit = getattr(bd, 'min_voltage_limit_in_V', None)
        v_max_limit = getattr(bd, 'max_voltage_limit_in_V', None)
        violations = 0

        if v_min_limit is not None or v_max_limit is not None:
            for c in cycles:
                v = getattr(c, 'voltage_in_V', None) or []
                if not v:
                    continue
                v_arr = np.array(v, dtype=float)
                if v_min_limit is not None and np.any(v_arr < v_min_limit - 0.1):
                    violations += 1
                if v_max_limit is not None and np.any(v_arr > v_max_limit + 0.1):
                    violations += 1

        if violations > 0:
            issues.append({
                'severity': 'warning',
                'message': f'{violations} cycle(s) have voltage outside nominal limits.',
            })

        score = max(0.0, 100.0 - len(issues) * 10)
        return {'score': score, 'issues': issues}

    def _check_noise(self, bd) -> Dict[str, Any]:
        """Estimate sensor noise levels."""
        issues: List[Dict] = []
        cycles = getattr(bd, 'cycle_data', []) or []
        if not cycles:
            return {'score': 100.0, 'issues': issues}

        noise_levels = []
        for c in cycles[:50]:  # Sample first 50 cycles for speed
            v = getattr(c, 'voltage_in_V', None) or []
            if len(v) > 10:
                v_arr = np.array(v, dtype=float)
                diffs = np.diff(v_arr)
                noise_levels.append(float(np.std(diffs)))

        if noise_levels:
            avg_noise = float(np.mean(noise_levels))
            if avg_noise > self.noise_std_threshold:
                issues.append({
                    'severity': 'warning',
                    'message': (
                        f'High voltage noise detected: avg std of '
                        f'first differences = {avg_noise:.6f} V'
                    ),
                })
            score = max(0.0, 100.0 - max(0, avg_noise - self.noise_std_threshold) * 10000)
        else:
            score = 100.0

        return {'score': score, 'issues': issues}
