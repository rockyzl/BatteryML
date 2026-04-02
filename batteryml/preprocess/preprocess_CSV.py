# Licensed under the MIT License.
# Copyright (c) Microsoft Corporation.

import logging
from pathlib import Path
from typing import Dict, List, Optional

from tqdm import tqdm

from batteryml import BatteryData
from batteryml.builders import PREPROCESSORS
from batteryml.preprocess.base import BasePreprocessor
from batteryml.preprocess.csv_importer import CSVBatteryImporter


logger = logging.getLogger(__name__)


@PREPROCESSORS.register()
class CSVPreprocessor(BasePreprocessor):
    """Preprocessor that wraps :class:`CSVBatteryImporter` for CLI / YAML use.

    This allows importing arbitrary CSV/Excel battery data via the standard
    BatteryML preprocessing pipeline, driven entirely by configuration rather
    than custom code.

    YAML configuration example::

        preprocessor:
          type: CSVPreprocessor
          output_dir: ./processed
          column_mapping:
            cycle: Cycle_Number
            voltage: Voltage(V)
            current: Current(A)
            charge_capacity: Charge_Capacity(Ah)
            discharge_capacity: Discharge_Capacity(Ah)
            time: Test_Time(s)
            temperature: Temperature(C)
          cell_id_column: Cell_ID          # optional
          file_pattern: "*.csv"            # optional, default *.csv
          metadata:                        # optional
            form_factor: cylindrical
            anode_material: graphite
            cathode_material: NMC

    Parameters
    ----------
    output_dir : str
        Directory to write processed ``.pkl`` files.
    column_mapping : dict
        See :class:`CSVBatteryImporter`.
    cell_id_column : str, optional
        See :class:`CSVBatteryImporter`.
    file_pattern : str
        Glob pattern to match input files (default ``'*.csv'``).
    metadata : dict, optional
        Extra metadata forwarded to ``BatteryData``.
    silent : bool
        Suppress progress output.
    """

    def __init__(
        self,
        output_dir: str,
        column_mapping: Dict[str, str],
        cell_id_column: Optional[str] = None,
        file_pattern: str = '*.csv',
        metadata: Optional[Dict] = None,
        silent: bool = False,
    ):
        super().__init__(output_dir=output_dir, silent=silent)
        self.column_mapping = column_mapping
        self.cell_id_column = cell_id_column
        self.file_pattern = file_pattern
        self.metadata = metadata or {}

    def process(self, parentdir: str, **kwargs) -> List[BatteryData]:
        """Import CSV/Excel files from *parentdir*.

        Parameters
        ----------
        parentdir : str or Path
            Directory containing the source data files.

        Returns
        -------
        tuple of (int, int)
            (processed_count, skipped_count)
        """
        path = Path(parentdir)
        if not path.is_dir():
            raise FileNotFoundError(
                f"Source directory not found: '{path}'"
            )

        importer = CSVBatteryImporter(
            column_mapping=self.column_mapping,
            cell_id_column=self.cell_id_column,
            metadata=self.metadata,
        )

        raw_files = sorted(path.glob(self.file_pattern))
        if not raw_files:
            logger.warning(
                "No files matching '%s' in '%s'.", self.file_pattern, path
            )
            return 0, 0

        process_batteries_num = 0
        skip_batteries_num = 0

        files_iter = raw_files
        if not self.silent:
            files_iter = tqdm(raw_files, desc='Processing CSV files')

        for raw_file in files_iter:
            try:
                batteries = importer.load(raw_file)
            except Exception as exc:
                logger.error("Failed to load '%s': %s", raw_file, exc)
                continue

            for battery in batteries:
                if self.check_processed_file(battery.cell_id):
                    skip_batteries_num += 1
                    continue

                self.dump_single_file(battery)
                process_batteries_num += 1

                if not self.silent:
                    tqdm.write(
                        f'File: {battery.cell_id} dumped to pkl file'
                    )

        return process_batteries_num, skip_batteries_num
