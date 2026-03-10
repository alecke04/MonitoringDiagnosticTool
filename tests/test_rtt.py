# test_rtt.py
# Unit tests for RTT measurement logic (MonitoringSystem.measureRTT)

# TODO: import unittest
# TODO: from unittest.mock import patch
# TODO: from src.monitoring.rtt import measure
# TODO: from src.models.results import RTTResult


class TestRTT:
    """Tests for RTT measurement and statistics calculation."""

    def test_returns_correct_sample_count(self):
        """
        measureRTT with samples=10 should return an RTTResult with count=10.
        # TODO: mock requests.get to return instantly
        #        call measure(url, sample_path, samples=10)
        #        assert result.count == 10
        """
        pass

    def test_average_is_computed_correctly(self):
        """
        RTTResult.average should equal the mean of all measurements.
        # TODO: inject known RTT values and verify average = sum / count
        """
        pass

    def test_median_is_computed_correctly(self):
        """
        RTTResult.median should equal the middle value of sorted measurements.
        # TODO: inject odd-count measurements and verify median
        """
        pass

    def test_confidence_interval_is_calculated(self):
        """
        After calculateConfidenceInterval(), confidence90Interval should be
        a tuple (lower, upper) with lower <= average <= upper.
        # TODO: call calculateConfidenceInterval and assert tuple shape
        """
        pass
