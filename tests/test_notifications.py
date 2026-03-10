# test_notifications.py
# Unit tests for email sending and report encryption (NotificationService)

# TODO: import unittest
# TODO: from unittest.mock import patch, MagicMock
# TODO: from src.notifications.email_service import NotificationService


class TestNotificationService:
    """Tests for report building, encryption, and email delivery."""

    def test_build_report_returns_string(self):
        """
        buildReport() should return a non-empty string containing the server URL.
        # TODO: create mock server, history, failure objects
        #        call ns.buildReport(server, history, failure)
        #        assert isinstance(result, str) and server.url in result
        """
        pass

    def test_encrypt_report_creates_zip(self):
        """
        encryptReport() should create a .zip file and delete the original .txt.
        # TODO: write a temp .txt file
        #        call ns.encryptReport(path)
        #        assert .zip exists and original .txt is gone
        """
        pass

    def test_send_email_calls_smtp(self):
        """
        sendEmail() should connect to SMTP and send one message.
        # TODO: mock smtplib.SMTP as context manager
        #        call ns.sendEmail(to, subject, body, attachmentPath)
        #        assert smtp.sendmail was called once
        """
        pass

    def test_notify_failure_orchestrates_all_steps(self):
        """
        notifyFailure() should call buildReport, encryptReport, and sendEmail in order.
        # TODO: mock all three sub-methods
        #        call notifyFailure and assert all three were called
        """
        pass
