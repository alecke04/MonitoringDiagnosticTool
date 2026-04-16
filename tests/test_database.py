# test_database.py
# Unit tests for SQLite database operations (DatabaseHandle)

# TODO: import unittest, os, tempfile
# TODO: from src.database.db_handle import DatabaseHandle
# TODO: from src.models import WebServer, MonitorRun
import unittest
import os
import tempfile
from unittest.mock import MagicMock
from src.database.db_handle import DatabaseHandle
from src.models import WebServer, MonitorRun


class TestDatabaseHandle:
    """Tests for all DatabaseHandle CRUD operations."""

    def setup_method(self):
        """
        Creates a fresh in-memory or temp-file SQLite DB before each test.
        # TODO: create a temp db file path and instantiate DatabaseHandle
        #        this ensures tests don't share state
        """
        self.db_path = tempfile.NamedTemporaryFile(delete=False).name
        self.db = DatabaseHandle(db_path=self.db_path)
        pass

    def teardown_method(self):
        """
        Removes the temp DB file after each test.
        # TODO: os.remove(self.db_path) if it exists
        """
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        pass

    def test_save_result_returns_run_id(self):
        """
        saveResult() should insert a row and return a positive integer run_id.
        # TODO: create mock server, availability, rtt, ssl objects
        #        call db.saveResult(...)
        #        assert isinstance(run_id, int) and run_id > 0
        """
        mock_server = WebServer(id=1, url="http://34.133.77.191", email="immyowngrandpa03@gmail.com")
        mock_availability = MagicMock()
        mock_rtt = MagicMock()
        mock_ssl = MagicMock()
        run_id = self.db.saveResult(mock_server, mock_availability, mock_rtt, mock_ssl)
        assert isinstance(run_id, int) and run_id > 0
        pass

    def test_get_recent_returns_correct_count(self):
        """
        getRecent(number=3) should return at most 3 MonitorRun objects.
        # TODO: insert 5 runs, call getRecent(3, server), assert len == 3
        """
        mock_server = WebServer(id=1, url="http://34.133.77.191", email="immyowngrandpa03@gmail.com")
        for i in range(5):
            mock_availability = MagicMock()
            mock_rtt = MagicMock()
            mock_ssl = MagicMock()
            self.db.saveResult(mock_server, mock_availability, mock_rtt, mock_ssl)
        recent_runs = self.db.getRecent(number=3, server=mock_server)
        assert len(recent_runs) == 3
        pass

    def test_update_notification_status(self):
        """
        After calling updateNotificationStatus(runId, 'SENT'),
        the notifications table should reflect 'SENT'.
        # TODO: insert a run and notification, update status, query and assert
        """
        mock_server = WebServer(id=1, url="http://34.133.77.191", email="immyowngrandpa03@gmail.com")
        mock_availability = MagicMock()
        mock_rtt = MagicMock()
        mock_ssl = MagicMock()
        run_id = self.db.saveResult(mock_server, mock_availability, mock_rtt, mock_ssl)
        self.db.recordNotification(run_id, filename="test.zip", status="PENDING")
        self.db.updateNotificationStatus(run_id, "SENT")
        # Query the notifications table to verify the update
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT status FROM notifications WHERE run_id = ?", (run_id,))
        result = cursor.fetchone()
        assert result[0] == "SENT"
        pass

    def test_add_and_remove_target(self):
        """
        addTarget() should insert a server; removeTarget() should delete it.
        # TODO: add a WebServer, assert it appears in getAllTargets()
        #        remove it, assert it no longer appears
        """
        mock_server = WebServer(id=1, url="http://34.133.77.191", email="immyowngrandpa03@gmail.com")
        self.db.addTarget(mock_server)
        all_targets = self.db.getAllTargets()
        assert mock_server in all_targets
        self.db.removeTarget(mock_server)
        all_targets = self.db.getAllTargets()
        assert mock_server not in all_targets
        pass
