import sqlite3
from pathlib import Path
from datetime import datetime, timezone


DATABASE_PATH = Path("data/ransomtrap.db")


def get_connection():
    """Return a connection to the local RansomTrap SQLite database."""

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """Create all RansomTrap database tables if they do not exist."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            file_path TEXT,
            process_id INTEGER,
            process_name TEXT,
            status TEXT NOT NULL DEFAULT 'new',
            details TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS process_tree (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_id INTEGER NOT NULL,
            pid INTEGER NOT NULL,
            parent_pid INTEGER,
            process_name TEXT,
            executable TEXT,
            FOREIGN KEY (alert_id) REFERENCES alerts(id)
        )
    """)

    connection.commit()
    connection.close()


def log_alert(
    alert_type,
    severity,
    file_path=None,
    process_id=None,
    process_name=None,
    status="new",
    details=None,
):
    """Insert an alert and return its database ID."""

    connection = get_connection()
    cursor = connection.cursor()

    timestamp = datetime.now(timezone.utc).isoformat()

    cursor.execute(
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
            status,
            details,
        ),
    )

    alert_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return alert_id


def log_process_tree(alert_id, process_tree):
    """Store process-tree information for an alert."""

    if not process_tree:
        return

    connection = get_connection()
    cursor = connection.cursor()

    for process in process_tree:
        cursor.execute(
            """
            INSERT INTO process_tree (
                alert_id,
                pid,
                parent_pid,
                process_name,
                executable
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                alert_id,
                process.get("pid"),
                process.get("parent_pid"),
                process.get("name"),
                process.get("exe"),
            ),
        )

    connection.commit()
    connection.close()


def update_alert_process(alert_id, process_id, process_name):
    """Attach process information to an existing alert."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE alerts
        SET process_id = ?,
            process_name = ?
        WHERE id = ?
        """,
        (
            process_id,
            process_name,
            alert_id,
        ),
    )

    connection.commit()
    connection.close()


def update_alert_status(alert_id, status):
    """Update the status of an alert."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE alerts
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            alert_id,
        ),
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()

    test_alert_id = log_alert(
        alert_type="database_test",
        severity="low",
        details="RansomTrap database test alert.",
    )

    print(f"[+] Database initialized successfully.")
    print(f"[+] Test alert created: ID={test_alert_id}")