# test_notifications.py
# Unit tests for email sending and report encryption (NotificationService)

# TODO: import unittest
# TODO: from unittest.mock import patch, MagicMock
# TODO: from src.notifications.email_service import NotificationService
import os
import unittest
from unittest.mock import patch, MagicMock
from src.notifications.email_service import NotificationService

class TestNotificationService:
    """Tests for report building, encryption, and email delivery."""

    def test_build_report_returns_string(self):
        """
        buildReport() should return a non-empty string containing the server URL.
        # TODO: create mock server, history, failure objects
        #        call ns.buildReport(server, history, failure)
        #        assert isinstance(result, str) and server.url in result
        """
        ns = NotificationService()
        mock_server = MagicMock()
        mock_server.url = "http://34.133.77.191"
        mock_history = MagicMock()
        mock_failure = MagicMock()
        result = ns.build_report(mock_server, mock_history, mock_failure)
        assert isinstance(result, str) and mock_server.url in result
        pass

    def test_encrypt_report_creates_zip(self):
        """
        encryptReport() should create a .zip file and delete the original .txt.
        # TODO: write a temp .txt file
        #        call ns.encryptReport(path)
        #        assert .zip exists and original .txt is gone
        """
        ns = NotificationService(reportPassword="testpassword", senderEmail="immyowngrandpa03@gmail.com")
        # Create a temp .txt file
        temp_txt_path = "temp_report.txt"   
        with open(temp_txt_path, "w") as f:
            f.write("This is a test report.")
        # Call encrypt_report
        zip_path = ns.encrypt_report(temp_txt_path, password="testpassword")
        assert os.path.exists(zip_path) and not os.path.exists(temp_txt_path)
        # Clean up the created zip file        
        if os.path.exists(zip_path):
            os.remove(zip_path)
        pass

    def test_send_email_calls_smtp(self):
        """
        sendEmail() should connect to SMTP and send one message.
        # TODO: mock smtplib.SMTP as context manager
        #        call ns.sendEmail(to, subject, body, attachmentPath)
        #        assert smtp.sendmail was called once
        """
        ns = NotificationService(senderEmail="immyowngrandpa03@gmail.com")
        with patch("smtplib.SMTP") as mock_smtp_class:
            mock_smtp_instance = MagicMock()
            mock_smtp_class.return_value.__enter__.return_value = mock_smtp_instance
            ns.sendEmail("immyowngrandpa03@gmail.com", "Test Subject", "Test Body", None)
            mock_smtp_instance.sendmail.assert_called_once()
        pass

    def test_notify_failure_orchestrates_all_steps(self):
        """
        notifyFailure() should call buildReport, encryptReport, and sendEmail in order.
        # TODO: mock all three sub-methods
        #        call notifyFailure and assert all three were called
        """
        ns = NotificationService(reportPassword="testpassword", senderEmail="immyowngrandpa03@gmail.com")
        with patch.object(ns, 'build_report', return_value="report content") as mock_build_report:
            with patch.object(ns, 'encrypt_report', return_value="encrypted_report.zip") as mock_encrypt_report:
                with patch.object(ns, 'sendEmail') as mock_send_email:
                    ns.notify_failure(server=MagicMock(), history=MagicMock(), run_id=123)
                    mock_build_report.assert_called_once()
                    mock_encrypt_report.assert_called_once()
                    mock_send_email.assert_called_once()
        pass
