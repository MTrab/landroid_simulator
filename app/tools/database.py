"""Database handler"""

import hashlib
import logging
import os
import sqlite3
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from dataclasses_json import DataClassJsonMixin

_LOGGER = logging.getLogger(__name__)


@dataclass
class UserInfo(DataClassJsonMixin):
    """Holds userinformation"""

    user_id: int
    email: str
    fullname: str
    admin: bool = False


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
    admin tinyint(1) NOT NULL DEFAULT 0
);
""",
        "default": """
INSERT INTO users (email,password,fullname,admin)
VALUES ("none@none.none","f3812cd46d0efc3da4f5998bbab3ab70","Admin",1);
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

    def get_userinfo(self, email: str) -> str:
        """Returns UserInfo object holding users information."""
        db = self.connect(DatabaseTypes.USERS)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        data = cursor.fetchone()
        user = UserInfo(
            user_id=int(data[0]),
            email=data[1],
            fullname=data[3],
            admin=bool(data[4]),
        )
        cursor.close()
        db.close()
        return user.to_json()

    def user_exist(self, email: str) -> bool:
        """Check if user exists in database

        Args:
            email (str): User email

        Returns:
            bool: Returns True if the email is found in the database
        """
        db = self.connect(DatabaseTypes.USERS)
        cursor = db.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM users WHERE email=?",
            (email,),
        )
        data = cursor.fetchone()[0]
        cursor.close()
        db.close()

        return bool(data)

    def save_user(self, user_data: dict) -> bool:
        """Save user in database."""
        try:
            db = self.connect(DatabaseTypes.USERS)
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users (email,password,fullname,admin) VALUES (?,?,?,0)",
                (
                    user_data["email"],
                    self.hash_password(user_data["password"]),
                    user_data["name"],
                ),
            )
            self._conn.commit()
            cursor.close()
            db.close()
            return True
        except:  # pylint: disable=bare-except
            return False

    def hash_password(self, password) -> str:
        """Hash password for database encryption."""
        return hashlib.md5(password.encode("utf-8")).hexdigest()

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
        cursor.close()
