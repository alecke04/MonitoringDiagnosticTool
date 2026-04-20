# test_ssl.py
# Unit tests for SSL certificate validation (MonitoringSystem.checkSSL)

# TODO: import unittest
# TODO: from unittest.mock import patch
# TODO: from src.monitoring.ssl_check import check
# TODO: from src.models.results import SSLResult
import ssl
import unittest
from unittest.mock import patch
from src.monitoring.ssl_check import check
from src.models.results import SSLResult

class TestSSL:
    """Tests for SSL certificate retrieval and validation logic."""

    def test_valid_cert_returns_isValid_true(self):
        """
        When the cert exists and expiry is in the future, isValid should be True.
        # TODO: mock TLS_GET_CERTIFICATE to return a future expiry date
        #        assert result.isValid == True
        """
        mock_cert = {
            "notAfter": "Dec 31 23:59:59 2099 GMT"
        }
        with patch("ssl.create_default_context") as mock_ssl_context:
            mock_context = mock_ssl_context.return_value
            mock_socket = mock_context.wrap_socket.return_value.__enter__.return_value
            mock_socket.getpeercert.return_value = mock_cert
            result = check("http://34.133.77.191")
            assert result.isValid == True and result.expirationDate == "Dec 31 23:59:59 2099 GMT"
        pass

    def test_expired_cert_returns_isValid_false(self):
        """
        When the cert expiry date is in the past, isValid should be False.
        # TODO: mock cert with a past expiry date
        #        assert result.isValid == False
        """
        mock_cert = {
            "notAfter": "Jan 1 00:00:00 2000 GMT"
        }
        with patch("ssl.create_default_context") as mock_ssl_context:
            mock_context = mock_ssl_context.return_value
            mock_socket = mock_context.wrap_socket.return_value.__enter__.return_value
            mock_socket.getpeercert.return_value = mock_cert
            result = check("http://34.133.77.191")
            assert result.isValid == False and result.expirationDate == "Jan 1 00:00:00 2000 GMT"
        pass

    def test_ssl_error_returns_isValid_false_unknown_date(self):
        """
        When an SSLError is raised, result should be isValid=False, expirationDate="Unknown".
        # TODO: mock ssl to raise ssl.SSLError
        #        assert result.isValid == False and result.expirationDate == "Unknown"
        """
        with patch("ssl.create_default_context") as mock_ssl_context:
            mock_context = mock_ssl_context.return_value
            mock_socket = mock_context.wrap_socket.return_value.__enter__.return_value
            mock_socket.getpeercert.side_effect = ssl.SSLError("SSL error occurred")
            result = check("http://34.133.77.191")
            assert result.isValid == False and result.expirationDate == "Unknown"
        pass
