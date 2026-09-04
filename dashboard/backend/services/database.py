import sqlite3
from pathlib import Path


# Database file location
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "ransotrap.db"


def get_connection():
    """Create and return a SQLite database connection."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create development tables if they do not exist."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            severity TEXT,
            detector TEXT,
            process_pid INTEGER,
            process_name TEXT,
            status TEXT,
            action TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT,
            filename TEXT,
            created_at TEXT,
            status TEXT
        )
    """)

    connection.commit()
    connection.close()


def insert_sample_alert():
    """Insert one sample alert for dashboard development."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO alerts (
            timestamp,
            severity,
            detector,
            process_pid,
            process_name,
            status,
            action
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "2026-09-04 15:20:00",
        "HIGH",
        "Trap File Monitor",
        1234,
        "sample_process.exe",
        "CONTAINED",
        "Process terminated (simulation)"
    ))

    connection.commit()
    connection.close()


def insert_trap(path, filename, created_at, status="ACTIVE"):
    """Insert a trap file record into the database."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO traps (
            path,
            filename,
            created_at,
            status
        )
        VALUES (?, ?, ?, ?)
    """, (
        path,
        filename,
        created_at,
        status
    ))

    connection.commit()
    connection.close()