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
        with sqlite3.connect(self.dbPath) as conn:
            cursor = conn.cursor() #connect to sqlite
            cursor.execute(""" INSERT INTO monitored_runs (target_id, timestamp, reachable, http_status, error_code, ssl_expiration, avg_rtt, median_rtt) #inserts into these columns
            VALUES (?, ?, ?, ?, ?, ?, ?, ?) """, (server, availability.timestamp, availability.reachable, availability.http_status, availability.error_code, ssl, statistics.mean(rtt), statistics.median(rtt))) #values inserted
            run_id = cursor.lastrowid #use last rowid as current 
            if rtt is not None:
                samples = [(run_id, value) for value in rtt] #attaches run id for each rtt value
                cursor.executemany("""INSERT INTO monitored_runs (rtt)
                                    VALUES rtt  """)
            conn.commit() #commit
            return run_id 
        

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
