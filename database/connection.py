"""SQLite connection, bound to the same database for all modules."""
import sqlite3
from core.config import DATABASE_PATH
class Database:
    def get_connection(self):
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(str(DATABASE_PATH), timeout=10)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys = ON')
        db.execute('PRAGMA busy_timeout = 5000')
        return db
