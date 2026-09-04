import sqlite3
from pathlib import Path
from datetime import datetime, timezone


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "ransomtrap.db"


def get_connection():
    """Create a connection to the local RansomTrap SQLite database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create RansomTrap database tables if they do not exist."""

    connection = get_connection()

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS traps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active'
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            file_path TEXT,
            process_id INTEGER,
            process_name TEXT,
            status TEXT NOT NULL DEFAULT 'detected',
            details TEXT
        );

        CREATE TABLE IF NOT EXISTS process_tree (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_id INTEGER NOT NULL,
            pid INTEGER NOT NULL,
            parent_pid INTEGER,
            process_name TEXT,
            executable TEXT,
            FOREIGN KEY (alert_id) REFERENCES alerts(id)
        );
        """
    )

    connection.commit()
    connection.close()


def log_alert(
    alert_type,
    severity,
    file_path=None,
    process_id=None,
    process_name=None,
    details=None,
):
    """Store a security alert in SQLite."""

    timestamp = datetime.now(timezone.utc).isoformat()

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO alerts (
            timestamp,
            alert_type,
            severity,
            file_path,
            process_id,
            process_name,
            status,
            details
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            timestamp,
            alert_type,
            severity,
            file_path,
            process_id,
            process_name,
            "detected",
            details,
        ),
    )

    alert_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return alert_id


if __name__ == "__main__":
    initialize_database()

    alert_id = log_alert(
        alert_type="trap_modified",
        severity="high",
        file_path=r"C:\Test\RansomTrap_Document.docx",
        details="Test alert generated during database verification.",
    )

    print(f"[+] Database initialized: {DB_PATH}")
    print(f"[+] Test alert created with ID: {alert_id}")