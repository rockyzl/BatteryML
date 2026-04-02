# Tests for train/test splitting utilities.

import os
import pytest

from batteryml.data.battery_data import BatteryData
from batteryml.train_test_split.random_split import RandomTrainTestSplitter


class TestRandomTrainTestSplitter:
    """Tests for RandomTrainTestSplitter."""

    def test_split_produces_non_empty_sets(self, sample_battery_data_list,
                                           tmp_data_dir):
        """Both train and test sets are non-empty after splitting."""
        # Dump batteries to pkl files so the splitter can discover them
        for bat in sample_battery_data_list:
            path = os.path.join(tmp_data_dir, f"{bat.cell_id}.pkl")
            bat.dump(path)

        splitter = RandomTrainTestSplitter(
            cell_data_path=tmp_data_dir,
            seed=42,
            train_test_split_ratio=0.6,
        )
        train, test = splitter.split()
        assert len(train) > 0, "Train set should not be empty"
        assert len(test) > 0, "Test set should not be empty"

    def test_no_overlap(self, sample_battery_data_list, tmp_data_dir):
        """Train and test sets should have no common elements."""
        for bat in sample_battery_data_list:
            path = os.path.join(tmp_data_dir, f"{bat.cell_id}.pkl")
            bat.dump(path)

        splitter = RandomTrainTestSplitter(
            cell_data_path=tmp_data_dir,
            seed=42,
            train_test_split_ratio=0.6,
        )
        train, test = splitter.split()
        assert set(train).isdisjoint(set(test)), \
            "Train and test sets must not overlap"

    def test_union_equals_total(self, sample_battery_data_list, tmp_data_dir):
        """Train + test should cover all data files."""
        for bat in sample_battery_data_list:
            path = os.path.join(tmp_data_dir, f"{bat.cell_id}.pkl")
            bat.dump(path)

        splitter = RandomTrainTestSplitter(
            cell_data_path=tmp_data_dir,
            seed=42,
            train_test_split_ratio=0.6,
        )
        train, test = splitter.split()
        assert len(train) + len(test) == len(sample_battery_data_list)

    def test_deterministic_with_seed(self, sample_battery_data_list,
                                     tmp_data_dir):
        """Same seed produces the same split."""
        for bat in sample_battery_data_list:
            path = os.path.join(tmp_data_dir, f"{bat.cell_id}.pkl")
            bat.dump(path)

        s1 = RandomTrainTestSplitter(cell_data_path=tmp_data_dir, seed=7,
                                     train_test_split_ratio=0.6)
        s2 = RandomTrainTestSplitter(cell_data_path=tmp_data_dir, seed=7,
                                     train_test_split_ratio=0.6)
        assert s1.split() == s2.split()
