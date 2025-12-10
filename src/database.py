"""
Database module for managing SQLite database operations.
Handles users, sessions, messages, and user profiles.
"""

import sqlite3
import hashlib
import json
from datetime import datetime
from typing import Optional, Dict, List, Any


class Database:
    def __init__(self, db_path: str = "chat_agent.db"):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """Create a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Initialize database tables."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        """)

        # User profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY,
                profile_json TEXT NOT NULL,
                emotional_state_json TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_emotional_check TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        conn.commit()
        conn.close()

    def hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username: str, password: str) -> Dict[str, Any]:
        """Create a new user."""
        conn = self.get_connection()
        cursor = conn.cursor()

        password_hash = self.hash_password(password)

        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid

            # Create default session for new user
            cursor.execute(
                "INSERT INTO sessions (user_id, session_name) VALUES (?, ?)",
                (user_id, "Default Session")
            )
            conn.commit()

            conn.close()
            return {"success": True, "user_id": user_id, "username": username}
        except sqlite3.IntegrityError:
            conn.close()
            return {"success": False, "error": "Username already exists"}

    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate a user."""
        conn = self.get_connection()
        cursor = conn.cursor()

        password_hash = self.hash_password(password)

        cursor.execute(
            "SELECT id, username FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            return {"success": True, "user_id": user["id"], "username": user["username"]}
        else:
            return {"success": False, "error": "Invalid credentials"}

    def create_session(self, user_id: int, session_name: str) -> int:
        """Create a new chat session."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO sessions (user_id, session_name) VALUES (?, ?)",
            (user_id, session_name)
        )
        conn.commit()
        session_id = cursor.lastrowid
        conn.close()

        return session_id

    def get_user_sessions(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all sessions for a user."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT id, session_name, created_at, updated_at
               FROM sessions
               WHERE user_id = ?
               ORDER BY updated_at DESC""",
            (user_id,)
        )

        sessions = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return sessions

    def get_user_id_from_session(self, session_id: int) -> Optional[int]:
        """Get user_id from session_id."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT user_id FROM sessions WHERE id = ?",
            (session_id,)
        )

        row = cursor.fetchone()
        conn.close()

        return row["user_id"] if row else None

    def add_message(self, session_id: int, role: str, content: str) -> int:
        """Add a message to a session."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content)
        )
        conn.commit()
        message_id = cursor.lastrowid

        # Update session's updated_at timestamp
        cursor.execute(
            "UPDATE sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (session_id,)
        )
        conn.commit()
        conn.close()

        return message_id

    def get_session_messages(self, session_id: int, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all messages for a session."""
        conn = self.get_connection()
        cursor = conn.cursor()

        query = """SELECT id, role, content, created_at
                   FROM messages
                   WHERE session_id = ?
                   ORDER BY created_at ASC"""

        if limit:
            query += f" LIMIT {limit}"

        cursor.execute(query, (session_id,))

        messages = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return messages

    def delete_session(self, session_id: int, user_id: int) -> bool:
        """Delete a session and all its messages."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Verify session belongs to user
        cursor.execute(
            "SELECT id FROM sessions WHERE id = ? AND user_id = ?",
            (session_id, user_id)
        )

        if not cursor.fetchone():
            conn.close()
            return False

        # Delete messages first
        cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))

        # Delete session
        cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))

        conn.commit()
        conn.close()

        return True

    def get_user_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user profile."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT profile_json, emotional_state_json, last_updated FROM user_profiles WHERE user_id = ?",
            (user_id,)
        )

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        profile = json.loads(row["profile_json"])
        if row["emotional_state_json"]:
            profile["emotional_state"] = json.loads(row["emotional_state_json"])
        profile["last_updated"] = row["last_updated"]

        return profile

    def create_user_profile(self, user_id: int, profile_data: Dict[str, Any]) -> bool:
        """Create initial user profile."""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO user_profiles (user_id, profile_json) VALUES (?, ?)",
                (user_id, json.dumps(profile_data))
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    def update_user_profile(self, user_id: int, profile_data: Dict[str, Any]) -> bool:
        """Update user profile."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """UPDATE user_profiles
               SET profile_json = ?, last_updated = CURRENT_TIMESTAMP
               WHERE user_id = ?""",
            (json.dumps(profile_data), user_id)
        )

        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()

        return rows_affected > 0

    def update_emotional_state(self, user_id: int, emotional_state: Dict[str, Any]) -> bool:
        """Update user's emotional state analysis."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """UPDATE user_profiles
               SET emotional_state_json = ?, last_emotional_check = CURRENT_TIMESTAMP
               WHERE user_id = ?""",
            (json.dumps(emotional_state), user_id)
        )

        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()

        return rows_affected > 0
