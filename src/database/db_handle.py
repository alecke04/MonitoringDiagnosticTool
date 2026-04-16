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
        INSERT INTO monitored_runs (target_id, timestamp, reachable, http_status, error_code, 
        ssl_expiration, avg_rtt, median_rtt) VALUES (?, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?)
        """
        
        rtt_samples_query = """
        INSERT INTO rtt_samples (run_id, rtt_value) VALUES (?, ?)
        """
        try:
            with sqlite3.connect(self.dbPath) as conn:
                cursor = conn.cursor()
                rtt_average = rtt['average'] if rtt else None
                rtt_median = rtt['median'] if rtt else None
                ssl_expiration = ssl['expirationDate'] if ssl else None
                error_code = None if availability.isUp else availability.httpDescript
                
                cursor.execute(monitored_runs_query, (server.id, int(availability.isUp), availability.httpCode, 
                                                      error_code, ssl_expiration, rtt_average, rtt_median))
                run_id = cursor.lastrowid
                
                if rtt and 'measurements' in rtt:
                    for sample in rtt['measurements']:
                        cursor.execute(rtt_samples_query, (run_id, sample))
                
                conn.commit()
                return run_id
        except sqlite3.Error as e:
            raise Exception(f"Database error in saveResult: {e}")

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
        SELECT run_id, timestamp, reachable, http_status, error_code, ssl_expiration, avg_rtt, median_rtt
        FROM monitored_runs
        WHERE target_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """
        try:
            with sqlite3.connect(self.dbPath) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (server.id, number))
                rows = cursor.fetchall()
            
            monitor_runs = []
            for row in rows:
                run_id, timestamp, reachable, http_status, error_code, ssl_expiration, avg_rtt, median_rtt = row
                confidence_interval = self._calculate_confidence_interval(run_id) if avg_rtt else (None, None)
                monitor_run = MonitorRun(run_id, timestamp, bool(reachable), http_status, error_code or "", 
                                        ssl_expiration is not None, ssl_expiration or "", avg_rtt, median_rtt, confidence_interval)
                monitor_runs.append(monitor_run)
            return monitor_runs
        except sqlite3.Error as e:
            raise Exception(f"Database error in getRecent: {e}")

    def getRunById(self, run_id: int):
        """
        Retrieves a single monitoring run by its run_id.
        Returns a MonitorRun object or None if not found.
        """
        query = """
        SELECT run_id, timestamp, reachable, http_status, error_code, ssl_expiration, avg_rtt, median_rtt
        FROM monitored_runs
        WHERE run_id = ?
        """
        try:
            with sqlite3.connect(self.dbPath) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (run_id,))
                row = cursor.fetchone()
            
            if not row:
                return None
            
            run_id, timestamp, reachable, http_status, error_code, ssl_expiration, avg_rtt, median_rtt = row
            confidence_interval = self._calculate_confidence_interval(run_id) if avg_rtt else (None, None)
            monitor_run = MonitorRun(run_id, timestamp, bool(reachable), http_status, error_code or "", 
                                    ssl_expiration is not None, ssl_expiration or "", avg_rtt, median_rtt, confidence_interval)
            return monitor_run
        except sqlite3.Error as e:
            raise Exception(f"Database error in getRunById: {e}")

    def getRunsInTimeframe(self, server, start: str, end: str) -> list:
        """
        Retrieves all runs for a server between `start` and `end` timestamps.

        Returns a list of MonitorRun objects.
        # TODO: SELECT from monitored_runs WHERE target_id = server.id
        #        AND timestamp BETWEEN start AND end
        """
        query = """
        SELECT run_id, timestamp, reachable, http_status, error_code, ssl_expiration, avg_rtt, median_rtt
        FROM monitored_runs
        WHERE target_id = ?
        AND timestamp BETWEEN ? AND ?
        ORDER BY timestamp DESC
        """
        try:
            with sqlite3.connect(self.dbPath) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (server.id, start, end))
                rows = cursor.fetchall()
            
            monitor_runs = []
            for row in rows:
                run_id, timestamp, reachable, http_status, error_code, ssl_expiration, avg_rtt, median_rtt = row
                confidence_interval = self._calculate_confidence_interval(run_id) if avg_rtt else (None, None)
                monitor_run = MonitorRun(run_id, timestamp, bool(reachable), http_status, error_code or "", 
                                        ssl_expiration is not None, ssl_expiration or "", avg_rtt, median_rtt, confidence_interval)
                monitor_runs.append(monitor_run)
            return monitor_runs
        except sqlite3.Error as e:
            raise Exception(f"Database error in getRunsInTimeframe: {e}")

    def updateNotificationStatus(self, runId: int, status: str) -> None:
        """
        Updates the sent_status field in the notifications table for a given run.
        Status must be one of: 'PENDING', 'SENT', 'FAILED'
        """
        if status not in ('PENDING', 'SENT', 'FAILED'):
            raise ValueError(f"Invalid status: {status}. Must be one of: PENDING, SENT, FAILED")
        
        query = """
        UPDATE notifications
        SET sent_status = ?
        WHERE run_id = ?
        """
        try:
            with sqlite3.connect(self.dbPath) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (status, runId))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database error in updateNotificationStatus: {e}")

    def hasRecentNotification(self, server_id: int, minutes_threshold: int = 15) -> bool:
        """
        Checks if a notification was recently sent for this server.
        Returns True if a SENT notification exists within the last N minutes.
        
        Used to prevent duplicate alert emails for transient failures.
        """
        query = """
        SELECT COUNT(*)
        FROM notifications n
        JOIN monitored_runs mr ON n.run_id = mr.run_id
        WHERE mr.target_id = ?
        AND n.sent_status = 'SENT'
        AND datetime(n.time_sent) > datetime('now', '-' || ? || ' minutes')
        """
        try:
            with sqlite3.connect(self.dbPath) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (server_id, minutes_threshold))
                count = cursor.fetchone()[0]
            return count > 0
        except sqlite3.Error as e:
            raise Exception(f"Database error in hasRecentNotification: {e}")

    def recordNotification(self, run_id: int, filename: str = None, status: str = 'SENT') -> int:
        """
        Records that a notification was sent for a specific monitoring run.
        Returns the notification_id.
        
        Args:
            run_id: The monitored_runs row this notification is for
            filename: Name of the encrypted report ZIP file (optional)
            status: 'PENDING', 'SENT', or 'FAILED'
        """
        query = """
        INSERT INTO notifications (run_id, sent_status, filename, time_sent)
        VALUES (?, ?, ?, datetime('now'))
        """
        try:
            with sqlite3.connect(self.dbPath) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (run_id, status, filename))
                conn.commit()
                notification_id = cursor.lastrowid
            return notification_id
        except sqlite3.Error as e:
            raise Exception(f"Database error in recordNotification: {e}")

    def addTarget(self, server, email_recipient: str, interval: int = 300, 
                   timeout: int = 10, retry_count: int = 3) -> int:
        """
        Inserts a new server into monitored_targets.
        Returns the new target_id.
        """
        query = """
        INSERT INTO monitored_targets (url, sample_path, email_recipient, interval, timeout, retry_count) 
        VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            with sqlite3.connect(self.dbPath) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (server.url, server.sample, email_recipient, interval, timeout, retry_count))
                target_id = cursor.lastrowid
                conn.commit()
                return target_id
        except sqlite3.Error as e:
            raise Exception(f"Database error in addTarget: {e}")

    def removeTarget(self, targetId: int) -> None:
        """
        Deletes a server from monitored_targets by target_id.
        # TODO: DELETE FROM monitored_targets WHERE target_id = targetId
        """
        query = """
        DELETE FROM monitored_targets
        WHERE target_id = ?
        """
        try:
            with sqlite3.connect(self.dbPath) as conn:
                cursor = conn.cursor()
                cursor.execute(query, (targetId,))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database error in removeTarget: {e}")

    def getAllTargets(self) -> list:
        """
        Returns all rows from monitored_targets as a list of WebServer objects.
        """
        query = """
        SELECT target_id, url, email_recipient, sample_path
        FROM monitored_targets
        """
        try:
            with sqlite3.connect(self.dbPath) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
            
            servers = []
            for row in rows:
                target_id, url, email_recipient, sample_path = row
                server = WebServer(target_id, url, email_recipient, sample_path)
                servers.append(server)
            return servers
        except sqlite3.Error as e:
            raise Exception(f"Database error in getAllTargets: {e}")
    
    def _calculate_confidence_interval(self, run_id: int) -> tuple:
        """
        Helper method: calculates 90% confidence interval from RTT samples for a run.
        Returns (lower, upper) tuple or (None, None) if no samples.
        """
        try:
            with sqlite3.connect(self.dbPath) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT rtt_value FROM rtt_samples WHERE run_id = ?", (run_id,))
                rows = cursor.fetchall()
            
            if not rows:
                return (None, None)
            
            samples = [row[0] for row in rows]
            mean = sum(samples) / len(samples)
            stddev = (sum((x - mean) ** 2 for x in samples) / max(1, len(samples) - 1)) ** 0.5
            z_score = 1.645  # 90% confidence
            margin_of_error = z_score * (stddev / (len(samples) ** 0.5))
            
            return (mean - margin_of_error, mean + margin_of_error)
        except sqlite3.Error:
            return (None, None)
