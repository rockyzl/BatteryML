# Licensed under the MIT License.
# Copyright (c) Microsoft Corporation.

import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from batteryml import BatteryData, CycleData


logger = logging.getLogger(__name__)


# Common column name patterns used by auto_detect_columns.
# Each key is a CycleData field; values are regex patterns that match
# commonly seen column headers (case-insensitive).
_COLUMN_PATTERNS: Dict[str, List[str]] = {
    'cycle': [
        r'^cycle[_\s]*(number|index|id|num|no|#)?$',
        r'^cycle$',
        r'^cyc$',
    ],
    'voltage': [
        r'^voltage.*$',
        r'^v$',
        r'^volt$',
        r'^ecell.*$',
        r'^voltage[_\s]*\(?v\)?$',
    ],
    'current': [
        r'^current.*$',
        r'^i$',
        r'^curr$',
        r'^current[_\s]*\(?a\)?$',
    ],
    'charge_capacity': [
        r'^charge[_\s]*capacity.*$',
        r'^q[_\s]*charge.*$',
        r'^qc$',
        r'^capacity[_\s]*charge.*$',
        r'^chg[_\s]*cap.*$',
    ],
    'discharge_capacity': [
        r'^discharge[_\s]*capacity.*$',
        r'^q[_\s]*discharge.*$',
        r'^qd$',
        r'^capacity[_\s]*discharge.*$',
        r'^dchg[_\s]*cap.*$',
        r'^dch[_\s]*cap.*$',
    ],
    'time': [
        r'^(test[_\s]*)?time.*$',
        r'^t$',
        r'^elapsed[_\s]*time.*$',
        r'^step[_\s]*time.*$',
    ],
    'temperature': [
        r'^temp.*$',
        r'^temperature.*$',
        r'^t[_\s]*cell.*$',
        r'^cell[_\s]*temp.*$',
    ],
}


class CSVBatteryImporter:
    """Universal CSV/Excel battery data importer.

    Imports battery cycling data from CSV or Excel files into BatteryML's
    standard ``BatteryData`` format using a simple column-name mapping.

    Parameters
    ----------
    column_mapping : dict
        Mapping from BatteryML field names to the column names present in the
        source file.  Recognised keys:

        - ``'cycle'`` (required) -- cycle number column
        - ``'voltage'`` -- voltage column (V)
        - ``'current'`` -- current column (A)
        - ``'charge_capacity'`` -- charge capacity column (Ah)
        - ``'discharge_capacity'`` -- discharge capacity column (Ah)
        - ``'time'`` -- time column (s)
        - ``'temperature'`` -- temperature column (deg C)

    cell_id_column : str, optional
        Column that distinguishes different cells when a single file contains
        data from more than one cell.  When *None*, the filename stem is used
        as the cell ID.
    metadata : dict, optional
        Extra keyword arguments forwarded to every ``BatteryData`` constructor
        (e.g. ``form_factor``, ``anode_material``, ``nominal_capacity_in_Ah``).

    Examples
    --------
    >>> importer = CSVBatteryImporter(
    ...     column_mapping={
    ...         'cycle': 'Cycle_Number',
    ...         'voltage': 'Voltage(V)',
    ...         'current': 'Current(A)',
    ...         'charge_capacity': 'Charge_Capacity(Ah)',
    ...         'discharge_capacity': 'Discharge_Capacity(Ah)',
    ...         'time': 'Test_Time(s)',
    ...         'temperature': 'Temperature(C)',
    ...     },
    ...     cell_id_column='Cell_ID',
    ... )
    >>> battery_data_list = importer.load('my_data.csv')
    >>> battery_data_list = importer.load('my_data.xlsx')
    """

    # Fields that map directly to CycleData constructor kwargs.
    _FIELD_TO_CYCLE_KWARG = {
        'voltage': 'voltage_in_V',
        'current': 'current_in_A',
        'charge_capacity': 'charge_capacity_in_Ah',
        'discharge_capacity': 'discharge_capacity_in_Ah',
        'time': 'time_in_s',
        'temperature': 'temperature_in_C',
    }

    _VALID_MAPPING_KEYS = {'cycle', 'voltage', 'current', 'charge_capacity',
                           'discharge_capacity', 'time', 'temperature'}

    def __init__(
        self,
        column_mapping: Dict[str, str],
        cell_id_column: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ):
        if not column_mapping:
            raise ValueError(
                "column_mapping must be a non-empty dict. "
                "At minimum, 'cycle' must be provided."
            )
        if 'cycle' not in column_mapping:
            raise ValueError(
                "column_mapping must contain a 'cycle' key that maps to the "
                "cycle-number column in your data."
            )
        unknown_keys = set(column_mapping) - self._VALID_MAPPING_KEYS
        if unknown_keys:
            raise ValueError(
                f"Unrecognised keys in column_mapping: {unknown_keys}. "
                f"Valid keys are: {sorted(self._VALID_MAPPING_KEYS)}"
            )

        self.column_mapping = column_mapping
        self.cell_id_column = cell_id_column
        self.metadata = metadata or {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self, filepath: str) -> List[BatteryData]:
        """Load battery data from a single CSV or Excel file.

        Parameters
        ----------
        filepath : str or Path
            Path to a ``.csv``, ``.xlsx``, or ``.xls`` file.

        Returns
        -------
        list of BatteryData
            One ``BatteryData`` per cell found in the file.

        Raises
        ------
        FileNotFoundError
            If *filepath* does not exist.
        ValueError
            If required columns are missing or the file is empty.
        """
        filepath = Path(filepath)
        self._check_file_exists(filepath)

        df = self._read_file(filepath)
        if df.empty:
            raise ValueError(
                f"The file '{filepath}' is empty or contains no data rows."
            )

        self._validate_columns(df, filepath)
        self._coerce_numeric(df, filepath)

        return self._build_battery_data(df, filepath)

    def load_directory(
        self, dirpath: str, pattern: str = '*.csv'
    ) -> List[BatteryData]:
        """Batch-import all matching files from a directory.

        Parameters
        ----------
        dirpath : str or Path
            Directory to scan.
        pattern : str
            Glob pattern for files to load (default ``'*.csv'``).

        Returns
        -------
        list of BatteryData
        """
        dirpath = Path(dirpath)
        if not dirpath.is_dir():
            raise FileNotFoundError(
                f"Directory not found: '{dirpath}'"
            )

        files = sorted(dirpath.glob(pattern))
        if not files:
            logger.warning(
                "No files matching pattern '%s' found in '%s'.",
                pattern, dirpath,
            )
            return []

        results: List[BatteryData] = []
        for f in files:
            try:
                results.extend(self.load(f))
            except Exception as exc:
                logger.error("Failed to load '%s': %s", f, exc)
        return results

    def validate(self, filepath: str) -> Dict:
        """Validate a file without fully loading it.

        Returns a dict with keys:

        - ``valid`` (bool)
        - ``errors`` (list of str)
        - ``stats`` (dict) -- row_count, cell_count, cycle_range, columns

        Parameters
        ----------
        filepath : str or Path

        Returns
        -------
        dict
        """
        filepath = Path(filepath)
        result: Dict = {'valid': True, 'errors': [], 'stats': {}}

        # Check existence
        if not filepath.exists():
            result['valid'] = False
            result['errors'].append(f"File not found: '{filepath}'")
            return result

        # Try reading
        try:
            df = self._read_file(filepath)
        except Exception as exc:
            result['valid'] = False
            result['errors'].append(f"Cannot read file: {exc}")
            return result

        if df.empty:
            result['valid'] = False
            result['errors'].append("File is empty or has no data rows.")
            return result

        # Column check
        missing = self._missing_columns(df)
        if missing:
            result['valid'] = False
            result['errors'].append(
                f"Missing columns: {missing}. "
                f"Available columns in file: {list(df.columns)}"
            )

        # Stats
        cycle_col = self.column_mapping.get('cycle')
        stats: Dict = {
            'row_count': len(df),
            'columns': list(df.columns),
        }
        if cycle_col and cycle_col in df.columns:
            stats['cycle_range'] = (
                int(df[cycle_col].min()), int(df[cycle_col].max())
            )
        if self.cell_id_column and self.cell_id_column in df.columns:
            stats['cell_count'] = int(df[self.cell_id_column].nunique())
        else:
            stats['cell_count'] = 1
        result['stats'] = stats

        return result

    @classmethod
    def auto_detect_columns(cls, filepath: str) -> Dict[str, str]:
        """Heuristically detect column mapping for a file.

        Reads the header row and matches column names against common patterns
        for battery cycling data.

        Parameters
        ----------
        filepath : str or Path

        Returns
        -------
        dict
            Suggested ``column_mapping`` dict. Keys that could not be detected
            are omitted.
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: '{filepath}'")

        # Read just the header
        suffix = filepath.suffix.lower()
        if suffix == '.csv':
            df = pd.read_csv(filepath, nrows=0)
        elif suffix in ('.xlsx', '.xls'):
            df = pd.read_excel(filepath, nrows=0)
        else:
            raise ValueError(
                f"Unsupported file format '{suffix}'. "
                "Use .csv, .xlsx, or .xls."
            )

        columns = list(df.columns)
        mapping: Dict[str, str] = {}

        for field, patterns in _COLUMN_PATTERNS.items():
            for col in columns:
                col_clean = col.strip()
                for pat in patterns:
                    if re.match(pat, col_clean, re.IGNORECASE):
                        mapping[field] = col
                        break
                if field in mapping:
                    break

        return mapping

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _check_file_exists(filepath: Path) -> None:
        """Raise FileNotFoundError with a friendly message."""
        if not filepath.exists():
            raise FileNotFoundError(
                f"File not found: '{filepath}'. "
                "Please check that the path is correct."
            )

    @staticmethod
    def _read_file(filepath: Path) -> pd.DataFrame:
        """Read a CSV or Excel file into a DataFrame."""
        suffix = filepath.suffix.lower()
        if suffix == '.csv':
            return pd.read_csv(filepath)
        elif suffix in ('.xlsx', '.xls'):
            return pd.read_excel(filepath)
        else:
            raise ValueError(
                f"Unsupported file format '{suffix}'. "
                "Supported formats: .csv, .xlsx, .xls"
            )

    def _missing_columns(self, df: pd.DataFrame) -> List[str]:
        """Return list of mapped columns not present in *df*."""
        missing = []
        for key, col_name in self.column_mapping.items():
            if col_name not in df.columns:
                missing.append(f"{key} -> '{col_name}'")
        if self.cell_id_column and self.cell_id_column not in df.columns:
            missing.append(f"cell_id_column -> '{self.cell_id_column}'")
        return missing

    def _validate_columns(self, df: pd.DataFrame, filepath: Path) -> None:
        """Raise ValueError if any mapped columns are missing."""
        missing = self._missing_columns(df)
        if missing:
            raise ValueError(
                f"Column mapping mismatch in '{filepath.name}'.\n"
                f"  Missing columns: {missing}\n"
                f"  Available columns in file: {list(df.columns)}"
            )

    def _coerce_numeric(self, df: pd.DataFrame, filepath: Path) -> None:
        """Convert mapped columns to numeric types in-place.

        Non-numeric values are coerced to NaN and a warning is emitted with
        details about problematic rows.
        """
        for field, col_name in self.column_mapping.items():
            if col_name not in df.columns:
                continue
            if not pd.api.types.is_numeric_dtype(df[col_name]):
                original = df[col_name].copy()
                df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
                bad_mask = original.notna() & df[col_name].isna()
                n_bad = bad_mask.sum()
                if n_bad > 0:
                    bad_rows = list(df.index[bad_mask][:5])
                    logger.warning(
                        "Column '%s' (field='%s') in '%s' has %d non-numeric "
                        "values (first bad rows: %s). They have been set to "
                        "NaN.",
                        col_name, field, filepath.name, n_bad, bad_rows,
                    )

    def _build_battery_data(
        self, df: pd.DataFrame, filepath: Path
    ) -> List[BatteryData]:
        """Group rows and construct BatteryData objects."""
        if self.cell_id_column:
            groups = df.groupby(self.cell_id_column)
        else:
            # Treat the entire file as a single cell.
            cell_id = filepath.stem
            groups = [(cell_id, df)]

        results: List[BatteryData] = []
        for cell_id, cell_df in groups:
            cell_id = str(cell_id)
            cycle_col = self.column_mapping['cycle']
            cycles: List[CycleData] = []

            for cycle_num, cycle_df in cell_df.groupby(cycle_col, sort=True):
                kwargs = {}
                for field, kwarg_name in self._FIELD_TO_CYCLE_KWARG.items():
                    col_name = self.column_mapping.get(field)
                    if col_name and col_name in cycle_df.columns:
                        values = cycle_df[col_name].values
                        kwargs[kwarg_name] = np.where(
                            np.isnan(values), 0.0, values
                        ).tolist()

                cycles.append(CycleData(
                    cycle_number=int(cycle_num),
                    **kwargs,
                ))

            battery = BatteryData(
                cell_id=cell_id,
                cycle_data=cycles,
                **self.metadata,
            )
            results.append(battery)

        return results
