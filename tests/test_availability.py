# test_availability.py
# Unit tests for HTTP availability checking logic (MonitoringSystem.checkAvailability)

# TODO: import unittest
# TODO: from unittest.mock import patch, MagicMock
# TODO: from src.monitoring.availability import check
# TODO: from src.models.results import AvailResult
import unittest
from unittest.mock import patch, MagicMock

import requests
from src.monitoring.availability import check
from src.models.results import AvailResult


class TestAvailability:
    """Tests for the HTTP availability check function."""

    def test_server_up_returns_isUp_true(self):
        """
        When the server returns HTTP 200, AvailResult.isUp should be True
        and httpCode should be 200.
        # TODO: mock requests.get to return a mock response with status_code=200
        #        call check(url, timeout)
        #        assert result.isUp == True and result.httpCode == 200
        """
        if server_response := MagicMock():
            server_response.status_code = 200
            server_response.reason = "OK"
            with patch("requests.get", return_value=server_response):
                result = check("http://34.133.77.191", timeout=5)
                assert result.isUp == True and result.httpCode == 200
        pass

    def test_server_down_404_returns_isUp_false(self):
        """
        When the server returns HTTP 404, AvailResult.isUp should be False.
        # TODO: mock requests.get to return status_code=404
        #        assert result.isUp == False
        """
        if server_response := MagicMock():
            server_response.status_code = 404
            server_response.reason = "Not Found"
            with patch("requests.get", return_value=server_response):
                result = check("http://34.133.77.191/nonexistent", timeout=5)
                assert result.isUp == False and result.httpCode == 404
        pass

    def test_timeout_returns_isUp_false_code_zero(self):
        """
        When requests raises a Timeout exception, result should have
        isUp=False and httpCode=0.
        # TODO: mock requests.get to raise requests.exceptions.Timeout
        #        assert result.isUp == False and result.httpCode == 0
        """
        with patch("requests.get", side_effect=requests.exceptions.Timeout):
            result = check("http://34.133.77.191", timeout=5)
            assert result.isUp == False and result.httpCode == 0
        pass

    def test_connection_error_returns_isUp_false(self):
        """
        When requests raises a ConnectionError, result should have isUp=False.
        # TODO: mock requests.get to raise requests.exceptions.ConnectionError
        """
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
            result = check("http://34.133.77.191", timeout=5)
            assert result.isUp == False and result.httpCode == 0
