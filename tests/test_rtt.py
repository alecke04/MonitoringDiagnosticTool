# test_rtt.py
# Unit tests for RTT measurement logic (MonitoringSystem.measureRTT)

# TODO: import unittest
# TODO: from unittest.mock import patch
# TODO: from src.monitoring.rtt import measure
# TODO: from src.models.results import RTTResult
import unittest
from unittest.mock import patch
from src.monitoring.rtt import measure
from src.models.results import RTTResult


class TestRTT:
    """Tests for RTT measurement and statistics calculation."""

    def test_returns_correct_sample_count(self):
        """
        measureRTT with samples=10 should return an RTTResult with count=10.
        # TODO: mock requests.get to return instantly
        #        call measure(url, sample_path, samples=10)
        #        assert result.count == 10
        """
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200  # Simulate successful response
            result = measure("http://34.133.77.191", "/test", samples=10)
            assert result.count == 10
        pass

    def test_average_is_computed_correctly(self):
        """
        RTTResult.average should equal the mean of all measurements.
        # TODO: inject known RTT values and verify average = sum / count
        """
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            # Simulate 5 samples with RTTs of 100ms, 200ms, 300ms, 400ms, 500ms
            with patch("time.time", side_effect=[0, 0.1, 0.1, 0.3, 0.3, 0.6, 0.6, 1.0, 1.0, 1.5]):
                result = measure("http://34.133.77.191", "/test", samples=5)
                expected_average = (100 + 200 + 300 + 400 + 500) / 5
                assert abs(result.average - expected_average) < 1e-6
        pass

    def test_median_is_computed_correctly(self):
        """
        RTTResult.median should equal the middle value of sorted measurements.
        # TODO: inject odd-count measurements and verify median
        """
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            # Simulate 5 samples with RTTs of 100ms, 200ms, 300ms, 400ms, 500ms
            with patch("time.time", side_effect=[0, 0.1, 0.1, 0.3, 0.3, 0.6, 0.6, 1.0, 1.0, 1.5]):
                result = measure("http://34.133.77.191", "/test", samples=5)
                expected_median = 300
                assert abs(result.median - expected_median) < 1e-6
        pass

    def test_confidence_interval_is_calculated(self):
        """
        After calculateConfidenceInterval(), confidence90Interval should be
        a tuple (lower, upper) with lower <= average <= upper.
        # TODO: call calculateConfidenceInterval and assert tuple shape
        """
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            # Simulate 5 samples with RTTs of 100ms, 200ms, 300ms, 400ms, 500ms
            with patch("time.time", side_effect=[0, 0.1, 0.1, 0.3, 0.3, 0.6, 0.6, 1.0, 1.0, 1.5]):
                result = measure("http://34.133.77.191", "/test", samples=5)
                result.calculateConfidenceInterval()
                assert isinstance(result.confidence90Interval, tuple) and len(result.confidence90Interval) == 2
                lower, upper = result.confidence90Interval
                assert lower <= result.average <= upper
        pass
