# Licensed under the MIT License.
# End-to-end integration smoke tests for the BatteryML pipeline.

import pytest
import torch

from batteryml.data.databundle import DataBundle
from batteryml.data.transformation.z_score import ZScoreDataTransformation
from batteryml.feature.variance_model import VarianceModelFeatureExtractor
from batteryml.label.rul import RULLabelAnnotator


@pytest.mark.slow
class TestPipelineIntegration:
    """Lightweight smoke test for BatteryData -> features -> labels -> DataBundle."""

    def test_full_pipeline_no_error(self, sample_battery_data_list):
        """The complete pipeline from BatteryData to DataBundle should execute without errors."""
        cells = sample_battery_data_list  # 5 batteries

        # Step 1: Extract features
        extractor = VarianceModelFeatureExtractor()
        features = extractor(cells)
        assert isinstance(features, torch.Tensor)
        assert features.shape[0] == len(cells)

        # Step 2: Annotate labels
        annotator = RULLabelAnnotator(eol_soh=0.8, min_rul_limit=1.0)
        labels = annotator(cells)
        assert isinstance(labels, torch.Tensor)
        assert labels.shape[0] == len(cells)

        # Step 3: Split into train/test (manual split for integration test)
        train_features = features[:3]
        train_labels = labels[:3]
        test_features = features[3:]
        test_labels = labels[3:]

        # Step 4: Create DataBundle with transformation
        bundle = DataBundle(
            train_feature=train_features,
            train_label=train_labels,
            test_feature=test_features,
            test_label=test_labels,
            feature_transformation=ZScoreDataTransformation(),
        )
        assert len(bundle.train_data) == 3
        assert len(bundle.test_data) == 2

    def test_databundle_evaluate(self, sample_battery_data_list):
        """DataBundle.evaluate should return a valid score for dummy predictions."""
        cells = sample_battery_data_list

        extractor = VarianceModelFeatureExtractor()
        features = extractor(cells)

        annotator = RULLabelAnnotator(eol_soh=0.8, min_rul_limit=1.0)
        labels = annotator(cells)

        bundle = DataBundle(
            train_feature=features[:3],
            train_label=labels[:3],
            test_feature=features[3:],
            test_label=labels[3:],
        )

        # Create dummy predictions (same as test labels for near-zero error)
        predictions = bundle.test_data.label.clone()
        rmse = bundle.evaluate(predictions, metric='RMSE')
        assert isinstance(rmse, float)
        assert rmse >= 0
