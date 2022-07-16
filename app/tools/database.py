"""Database handler"""

from enum import Enum
import logging

import os
from pathlib import Path
import sqlite3
from typing import Any

_LOGGER = logging.getLogger(__name__)


class DatabaseTypes(Enum):
    """Database types."""

    USERS = {
        "file": "landroid_simulator.db",
        "scheme": """
CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY,
    email text NOT NULL,
    password text NOT NULL,
    fullname text,
    admin tinyint(1) NOT NULL DEFAULT 0,

);
""",
        "default": """
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
    ) -> sqlite3.Connection | None:
        """Connect to the database."""

        db = os.path.join(self._db_store, database.value["file"])
        path = Path(db)

        try:
            if path.is_file():
                self._conn = sqlite3.connect(db, 5)
            else:
                self._conn = sqlite3.connect(db, 5)
                self._init_database(database)

            return self._conn
        except sqlite3.OperationalError:
            _LOGGER.error("Error reading database from %s", db)

            return None

    def cursor(self) -> sqlite3.Cursor:
        """Return a SQLite cursor."""
        return self._conn.cursor()

    def _init_database(self, database: DatabaseTypes = DatabaseTypes.USERS) -> None:
        """Initialize the database if it was not found."""
        _LOGGER.warning("Database was not found, initializing now.")
        cursor = self._conn.cursor()
        cursor.execute(database.value["scheme"])
        if not isinstance(database.value["default"], type(None)):
            _LOGGER.info(
                "Adding default data to the database. %s", database.value["default"]
            )
            cursor.execute(database.value["default"])

        self._conn.commit()
