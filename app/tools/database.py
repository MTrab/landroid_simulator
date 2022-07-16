"""Database handler"""

from enum import Enum

import os
from pathlib import Path
import sqlite3
from typing import Any


class DatabaseTypes(Enum):
    """Database types."""

    USERS = {
        "file": "landroid_simulator.db",
        "scheme": """
CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY,
    email text NOT NULL,
    password text NOT NULL,
    fullname text
);
INSERT INTO users (email,password,fullname)
VALUES ("none@none.none","f3812cd46d0efc3da4f5998bbab3ab70","Admin");
""",
    }


class Database:
    """User database handler."""

    def __init__(
        self,
        storage: str = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "/databases"
        ),
    ) -> None:
        """Initialize the database object."""
        self._conn: sqlite3.Connection
        self._db_store = storage

    def connect(
        self, database: DatabaseTypes = DatabaseTypes.USERS
    ) -> sqlite3.Connection:
        """Connect to the database."""

        db = os.path.join(self._db_store, database.value["file"])
        path = Path(db)

        if path.is_file():
            self._conn = sqlite3.connect(db)
        else:
            self._conn = sqlite3.connect(db)
            self._init_database(database)

        return self._conn

    def _init_database(self, database: DatabaseTypes = DatabaseTypes.USERS) -> None:
        """Initialize the database if it was not found."""
        cursor = self._conn.cursor()
        cursor.execute(database.value["scheme"])
