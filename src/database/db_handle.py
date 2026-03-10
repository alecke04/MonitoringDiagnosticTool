# DatabaseHandle — all SQLite read/write operations
# Single class responsible for every interaction with monitor.db

# TODO: import sqlite3, os
# TODO: from src.models import WebServer, MonitorHistory, MonitorRun


class DatabaseHandle:
    """
    Wraps all SQLite database operations for the monitoring tool.

    Attributes:
        dbPath (str): Absolute or relative path to the SQLite .db file
    """

    def __init__(self, dbPath: str):
        # TODO: assign self.dbPath = dbPath
        # TODO: call self._init_db() to create tables if they don't exist
        pass

    def _init_db(self) -> None:
        """
        Reads and executes schema.sql to initialize all tables
        if the database file doesn't already exist.
        # TODO: open connection, read schema.sql, executescript, close
        """
        pass

    def saveResult(self, server, availability, rtt, ssl) -> int:
        """
        Inserts one complete monitoring cycle into the DB:
          - One row in monitored_runs
          - Up to 100 rows in rtt_samples (if rtt is not None)

        Returns the run_id of the newly inserted monitored_runs row.

        # TODO: INSERT INTO monitored_runs with all fields from availability/rtt/ssl
        #        get lastrowid as runId
        #        if rtt is not None: INSERT each measurement into rtt_samples
        #        commit and return runId
        """
        pass

    def getRecent(self, number: int, server) -> list:
        """
        Retrieves the `number` most recent MonitorRun rows for a given server,
        ordered by timestamp descending.

        Returns a list of MonitorRun objects.
        # TODO: SELECT from monitored_runs WHERE target_id = server.id
        #        ORDER BY timestamp DESC LIMIT number
        #        map rows to MonitorRun objects and return
        """
        pass

    def getRunsInTimeframe(self, server, start: str, end: str) -> list:
        """
        Retrieves all runs for a server between `start` and `end` timestamps.

        Returns a list of MonitorRun objects.
        # TODO: SELECT from monitored_runs WHERE target_id = server.id
        #        AND timestamp BETWEEN start AND end
        """
        pass

    def updateNotificationStatus(self, runId: int, status: str) -> None:
        """
        Updates the sent_status field in the notifications table for a given run.
        Status must be one of: 'PENDING', 'SENT', 'FAILED'

        # TODO: UPDATE notifications SET sent_status = status WHERE run_id = runId
        #        commit the change
        """
        pass

    def addTarget(self, server) -> int:
        """
        Inserts a new server into monitored_targets.
        Returns the new target_id.
        # TODO: INSERT INTO monitored_targets and return lastrowid
        """
        pass

    def removeTarget(self, targetId: int) -> None:
        """
        Deletes a server from monitored_targets by target_id.
        # TODO: DELETE FROM monitored_targets WHERE target_id = targetId
        """
        pass

    def getAllTargets(self) -> list:
        """
        Returns all rows from monitored_targets as a list of WebServer objects.
        # TODO: SELECT * FROM monitored_targets and map to WebServer objects
        """
        pass
