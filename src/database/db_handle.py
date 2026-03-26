# DatabaseHandle — all SQLite read/write operations
# Single class responsible for every interaction with monitor.db

import sqlite3, os, statistics
from src.models import WebServer, MonitorHistory, MonitorRun



class DatabaseHandle:
    """
    Wraps all SQLite database operations for the monitoring tool.

    Attributes:
        dbPath (str): Absolute or relative path to the SQLite .db file
    """

    def __init__(self, dbPath: str):
        self.dbPath = dbPath #Calls path for database
        self._init_db() #calls table creation if not exists
        pass

    def _init_db(self) -> None:
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql") #Finds location of schema.sql to avoid duplication 
        conn = sqlite3.connect(self.dbPath) #creates database file
        with open(schema_path, "r") as f: #reads schema.sql
            contents = f.read()
        cursor = conn.cursor()
        cursor.executescript(contents) #executes contents of script
        conn.close()

    def saveResult(self, server, availability, rtt, ssl) -> int:
        """
        Inserts one complete monitoring cycle into the DB:
          - One row in monitored_runs
          - Up to 100 rows in rtt_samples (if rtt is not None)

        Returns the run_id of the newly inserted monitored_runs row.

        # TODO:  INSERT INTO monitored_runs with all fields from availability/rtt/ssl
        #        get lastrowid as runId
        #        if rtt is not None: INSERT each measurement into rtt_samples
        #        commit and return runId
        """
        monitored_runs_query = """
        INSERT INTO monitored_runs (target_id, timestamp, availability.isUp, availability.httpCode, 
        rtt_average, rtt_median, ssl_valid) VALUES (?, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)
        """
        
        rtt_samples_query = """
        INSERT INTO rtt_samples (run_id, sample_value) VALUES (?, ?)
        """
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        rtt_average = rtt['average'] if rtt else None
        rtt_median = rtt['median'] if rtt else None
        ssl_valid = ssl['valid'] if ssl else None
        cursor.execute(monitored_runs_query, (server.id, availability.isUp, availability.httpCode, 
                                              rtt_average, rtt_median, ssl_valid))
        run_id = cursor.lastrowid
        if rtt:
            for sample in rtt['samples']:
                cursor.execute(rtt_samples_query, (run_id, sample))
        conn.commit()
        conn.close()
        return run_id
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
        query = """
        SELECT run_id, target_id, timestamp, availability.isUp, availability.httpCode, rtt_average, rtt_median, ssl_valid
        FROM monitored_runs
        WHERE target_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        cursor.execute(query, (server.id, number))
        rows = cursor.fetchall()
        conn.close()
        monitor_runs = []
        for row in rows:
            run_id, target_id, timestamp, isUp, httpCode, rtt_average, rtt_median, ssl_valid = row
            monitor_run = MonitorRun(run_id, target_id, timestamp, isUp, httpCode, rtt_average, rtt_median, ssl_valid)
            monitor_runs.append(monitor_run)
        return monitor_runs
        pass

    def getRunsInTimeframe(self, server, start: str, end: str) -> list:
        """
        Retrieves all runs for a server between `start` and `end` timestamps.

        Returns a list of MonitorRun objects.
        # TODO: SELECT from monitored_runs WHERE target_id = server.id
        #        AND timestamp BETWEEN start AND end
        """
        query = """
        SELECT run_id, target_id, timestamp, availability.isUp, availability.httpCode, rtt_average, rtt_median, ssl_valid
        FROM monitored_runs
        WHERE target_id = ?
        AND timestamp BETWEEN ? AND ?
        ORDER BY timestamp DESC
        """
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        cursor.execute(query, (server.id, start, end))
        rows = cursor.fetchall()
        conn.close()
        monitor_runs = []
        for row in rows:
            run_id, target_id, timestamp, isUp, httpCode, rtt_average, rtt_median, ssl_valid = row
            monitor_run = MonitorRun(run_id, target_id, timestamp, isUp, httpCode, rtt_average, rtt_median, ssl_valid)
            monitor_runs.append(monitor_run)
        return monitor_runs
        pass

    def updateNotificationStatus(self, runId: int, status: str) -> None:
        """
        Updates the sent_status field in the notifications table for a given run.
        Status must be one of: 'PENDING', 'SENT', 'FAILED'

        # TODO: UPDATE notifications SET sent_status = status WHERE run_id = runId
        #        commit the change
        """
        query = """
        UPDATE notifications
        SET sent_status = ?
        WHERE run_id = ?
        """
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        cursor.execute(query, (status, runId))
        conn.commit()
        conn.close()
        pass

    def addTarget(self, server) -> int:
        """
        Inserts a new server into monitored_targets.
        Returns the new target_id.
        # TODO: INSERT INTO monitored_targets and return lastrowid
        """
        query = """
        INSERT INTO monitored_targets (url, sample_path, check_ssl) VALUES (?, ?, ?)
        """
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        cursor.execute(query, (server.url, server.sample_path, server.check_ssl))
        target_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return target_id
        pass

    def removeTarget(self, targetId: int) -> None:
        """
        Deletes a server from monitored_targets by target_id.
        # TODO: DELETE FROM monitored_targets WHERE target_id = targetId
        """
        query = """
        DELETE FROM monitored_targets
        WHERE target_id = ?
        """
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        cursor.execute(query, (targetId,))
        conn.commit()
        conn.close()
        pass

    def getAllTargets(self) -> list:
        """
        Returns all rows from monitored_targets as a list of WebServer objects.
        # TODO: SELECT * FROM monitored_targets and map to WebServer objects
        """
        query = """
        SELECT target_id, url, sample_path, check_ssl
        FROM monitored_targets
        """
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        servers = []
        for row in rows:
            target_id, url, sample_path, check_ssl = row
            server = WebServer(target_id, url, sample_path, check_ssl)
            servers.append(server)
        return servers
        pass
