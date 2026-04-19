# DatabaseHandle — all SQLite read/write operations
# Single class responsible for every interaction with monitor.db

import sqlite3, os, statistics

from database.test_entry import TestEntry
from filelock import FileLock


class DatabaseHandle:
    """
    Wraps all SQLite database operations for the monitoring tool.

    Attributes:
        db_path (str): Absolute or relative path to the SQLite .db file
    """

    def __init__(self, db_path: str):
        self.db_path = db_path #Calls path for database
        self.lock = FileLock("./data.lock")
        self._init_db() #calls table creation if not exists
        pass

    def _init_db(self) -> None:
        with self.lock:
            conn = sqlite3.connect(self.db_path) #creates database file
            cursor = conn.cursor()

            create_query = TestEntry.get_table_creation_string()
            cursor.executescript(create_query)

            conn.close()

    def save_result(self, server:str, result:tuple[bool, Exception] | tuple[bool, list[float]]) -> bool:
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)

                test_entry = TestEntry.from_raw_data(server, result)
                test_entry.save(conn)

                conn.close()

                return True
            except Exception as e:
                print("Encountered error during save_result in DatabaseHandle error:"+str(e))
                return False

    def get_recent(self, number: int, server: str) -> list:
        with self.lock:
            conn = sqlite3.connect(self.db_path)

            query = f"SELECT url, date FROM {TestEntry.__name__} ORDER BY date DESC LIMIT ?"

            cursor = conn.cursor()
            cursor.execute(query, (number,))
            rows = cursor.fetchall()

            for row in rows:
                url, date = row
                print(TestEntry.load(conn, url, date))

'''
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
        with self.lock:
            try:
                with sqlite3.connect(self.dbPath) as conn:
                    query =

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
'''