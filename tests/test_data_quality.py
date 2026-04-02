# Tests for the data quality detection module.

import pytest

from batteryml.data.quality import DataQualityChecker, QualityReport


class TestDataQualityChecker:
    """Tests for the data quality checker on sample battery data."""

    def test_checker_runs_without_error(self, sample_battery_data):
        """The quality checker should run on sample data without raising."""
        checker = DataQualityChecker()
        report = checker.check(sample_battery_data)
        assert report is not None
        assert isinstance(report, QualityReport)

    def test_quality_report_has_score(self, sample_battery_data):
        """The quality report should contain a score between 0 and 100."""
        checker = DataQualityChecker()
        report = checker.check(sample_battery_data)
        assert 0 <= report.score <= 100

    def test_quality_report_summary(self, sample_battery_data):
        """Generating a text summary from the report should not raise."""
        checker = DataQualityChecker()
        report = checker.check(sample_battery_data)
        summary = report.summary()
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert report.cell_id in summary

    def test_anomaly_detection_clean_data(self, sample_battery_data):
        """Clean simulated data should have no error-level anomalies."""
        checker = DataQualityChecker()
        report = checker.check(sample_battery_data)
        errors = report.get_issues(severity='error')
        assert len(errors) == 0

    def test_missing_data_detection(self, sample_battery_data):
        """The sample fixture has all fields populated, so no missing errors."""
        checker = DataQualityChecker()
        report = checker.check(sample_battery_data)
        missing_issues = [
            i for i in report.get_issues()
            if i.get('category') == 'missing_data'
            and i.get('severity') == 'error'
        ]
        assert len(missing_issues) == 0
