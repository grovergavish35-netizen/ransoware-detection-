from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import sqlite3
import time

from trap_manager import get_user_folders, TRAP_FILE_NAMES


# Database path
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "dashboard" / "backend" / "ransotrap.db"


def simulate_containment(file_path):
    """
    Simulate ransomware containment response.
    No real process is terminated.
    """

    print("\n[🛡️ RESPONSE] Initiating threat containment...")
    print(f"[🛡️ RESPONSE] Isolating suspicious activity near: {file_path}")

    time.sleep(1)

    print("[✓] Threat containment completed (simulation).\n")

    return {
        "status": "CONTAINED",
        "process_name": "Unknown Process",
        "action": "Suspicious activity isolated (simulation)"
    }


def save_alert(event_type, file_path, containment):
    """Save detected trap file activity into the database."""

    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO alerts
            (timestamp, severity, detector, process_pid,
             process_name, status, action)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "HIGH",
            "Trap File Monitor",
            0,
            containment["process_name"],
            containment["status"],
            f"Trap file {event_type}: {file_path} | "
            f"{containment['action']}"
        ))

        connection.commit()
        connection.close()

        print("[+] Security alert saved to database.")

    except Exception as error:
        print(f"[ERROR] Failed to save alert: {error}")


class TrapEventHandler(FileSystemEventHandler):
    """Handle filesystem activity involving RansomTrap files."""

    def _is_trap_file(self, path):
        return Path(path).name in TRAP_FILE_NAMES

    def handle_trap_event(self, event_type, path):
        """Handle detected trap file activity."""

        print(f"\n[🚨 THREAT DETECTED] Trap file {event_type}: {path}")

        # Automatic containment simulation
        containment = simulate_containment(path)

        # Save final threat status to database
        save_alert(event_type, path, containment)

        print("[!] Threat detection and response completed.\n")

    def on_modified(self, event):
        if event.is_directory:
            return

        if self._is_trap_file(event.src_path):
            self.handle_trap_event("MODIFIED", event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return

        if self._is_trap_file(event.src_path):
            self.handle_trap_event("CREATED", event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return

        if self._is_trap_file(event.src_path):
            self.handle_trap_event("DELETED", event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return

        if self._is_trap_file(event.src_path):
            self.handle_trap_event(
                "RENAMED/MOVED",
                f"{event.src_path} -> {event.dest_path}"
            )

        elif self._is_trap_file(event.dest_path):
            self.handle_trap_event(
                "MOVED TO TRAP NAME",
                f"{event.src_path} -> {event.dest_path}"
            )


def start_monitor():
    """Start monitoring folders containing trap files."""

    observer = Observer()
    handler = TrapEventHandler()

    monitored_folders = []

    for folder in get_user_folders():
        if folder.exists():
            observer.schedule(handler, str(folder), recursive=False)
            monitored_folders.append(folder)

    observer.start()

    print("[+] RansomTrap file monitor started.")
    print("[+] Monitoring:")

    for folder in monitored_folders:
        print(f"    {folder}")

    return observer


if __name__ == "__main__":
    observer = start_monitor()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[+] Stopping monitor...")
        observer.stop()

    observer.join()