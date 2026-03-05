"""Player registration and login with SQLite backend."""

import hashlib
import os
import sqlite3


class AuthManager:
    """Manages player registration and authentication using SQLite."""

    def __init__(self, db_path: str = "tournament.db") -> None:
        """Initialize the auth manager and create the users table if needed."""
        self.db_path = db_path
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "  username TEXT UNIQUE NOT NULL,"
            "  password_hash TEXT NOT NULL,"
            "  salt TEXT NOT NULL"
            ")"
        )
        self._conn.commit()

    def register(self, username: str, password: str) -> tuple[bool, str]:
        """Register a new user. Returns (success, message)."""
        if not username or not username.strip():
            return False, "Username cannot be empty"
        if not password:
            return False, "Password cannot be empty"

        username = username.strip()
        salt = os.urandom(16).hex()
        password_hash = hashlib.sha256((salt + password).encode()).hexdigest()

        try:
            self._conn.execute(
                "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                (username, password_hash, salt),
            )
            self._conn.commit()
            return True, "Registration successful"
        except sqlite3.IntegrityError:
            return False, "Username already exists"

    def login(self, username: str, password: str) -> tuple[bool, str]:
        """Verify credentials. Returns (success, message)."""
        if not username or not username.strip():
            return False, "Username cannot be empty"
        if not password:
            return False, "Password cannot be empty"

        username = username.strip()
        row = self._conn.execute(
            "SELECT password_hash, salt FROM users WHERE username = ?",
            (username,),
        ).fetchone()

        if row is None:
            return False, "User not found"

        stored_hash, salt = row
        password_hash = hashlib.sha256((salt + password).encode()).hexdigest()

        if password_hash == stored_hash:
            return True, "Login successful"
        return False, "Wrong password"

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()
