from database.db_class import DbClass
from datetime import datetime
import sqlite3

class TestEntry(DbClass):
    @classmethod
    def get_table_structure(cls) -> dict[str, str]:
        return {
        "url": "TEXT NOT NULL",
        "date": "TEXT NOT NULL",
        "excText": "TEXT",
        "mean": "REAL",
        "median": "REAL",
        "std_dev": "REAL",
        "ci_low": "REAL",
        "ci_high": "REAL, PRIMARY KEY (url, date)",
    }

    def __init__(self, url, date, mean, median, std_dev, ci_low, ci_high, exc_text):
        self.url = url
        self.date = date
        self.mean = mean
        self.median = median
        self.std_dev = std_dev
        self.ci_low = ci_low
        self.ci_high = ci_high
        self.exc_text = exc_text

    @classmethod
    def from_raw_data(cls, server:str, result:tuple[bool, Exception] | tuple[bool, list[float]]):
        if result[0]:
            data_list = result[1]
            return TestEntry(server, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data_list[0], data_list[1], data_list[2], data_list[3], data_list[4], "")
        else:
            return TestEntry(server, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, 0, 0, 0, 0, str(result[1]))

    def save(self, conn):
        """Stores the instance using an existing connection object."""
        cursor = conn.cursor()

        query = f'''
            INSERT INTO {type(self).__name__} (url, date, mean, median, std_dev, ci_low, ci_high, excText)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''

        values = (self.url, self.date, self.mean, self.median, self.std_dev, self.ci_low, self.ci_high, self.exc_text)

        cursor.execute(query, values)
        conn.commit()

    @classmethod
    def load(cls, conn, url, date):
        """Creates a new instance using an existing connection object."""
        # Set row_factory locally to ensure we can access by column name
        original_factory = conn.row_factory
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {cls.__name__} WHERE url = ? AND date = ?", (url, date))
        row = cursor.fetchone()

        # Reset factory to original state to avoid side effects elsewhere
        conn.row_factory = original_factory

        if row:
            return TestEntry(
                row['url'],
                row['date'],
                row['mean'],
                row['median'],
                row['std_dev'],
                row['ci_low'],
                row['ci_high'],
                row['excText'],
            )
        return None

    def __repr__(self):
        if len(self.exc_text) != 0:
            return f"Test for server {self.url} failed at {self.date}, with {self.exc_text}"
        else:
            return f"Test for server {self.url} succeeded at {self.date}, with mean {self.mean}, median {self.std_dev}, std_dev {self.std_dev} ci_low {self.ci_low} ci_high {self.ci_high}"