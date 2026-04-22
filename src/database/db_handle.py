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

            query = f"SELECT url, date FROM {TestEntry.__name__}  WHERE url = ? ORDER BY date DESC LIMIT ?"

            cursor = conn.cursor()
            cursor.execute(query, (server, number))
            rows = cursor.fetchall()

            data = []

            for row in rows:
                url, date = row
                test_entry = TestEntry.load(conn, url, date)
                data.append(test_entry)

            return data