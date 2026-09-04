from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import sqlite3
import time
import json

from trap_manager import get_user_folders, TRAP_FILE_NAMES
from entropy_analyzer import analyze_file


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "dashboard" / "backend" / "ransotrap.db"
ENTROPY_STATUS_PATH = BASE_DIR / "agent" / "entropy_status.json"


def save_entropy_status(file_path, entropy_result):
    """Save latest entropy analysis result for dashboard."""

    try:
        status_data = {
            "file": str(file_path),
            "entropy": entropy_result.get("entropy"),
            "threshold": entropy_result.get("threshold"),
            "status": entropy_result.get("status"),
            "suspicious": entropy_result.get("suspicious"),
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(ENTROPY_STATUS_PATH, "w", encoding="utf-8") as file:
            json.dump(status_data, file, indent=4)

        print("[+] Latest entropy status saved.")

    except Exception as error:
        print(f"[ERROR] Failed to save entropy status: {error}")


def simulate_containment(file_path):
    """Simulate ransomware containment response."""

    print("\n[RESPONSE] Initiating threat containment...")
    print(f"[RESPONSE] Isolating suspicious activity near: {file_path}")

    time.sleep(1)

    print("[OK] Threat containment completed (simulation).\n")

    return {
        "status": "CONTAINED",
        "process_name": "Unknown Process",
        "action": "Suspicious activity isolated (simulation)"
    }


def save_alert(event_type, file_path, containment, entropy_result=None):
    """Save detected trap file activity into database."""

    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        severity = "HIGH"
        entropy_info = "Entropy analysis unavailable"

        if entropy_result:
            entropy_value = entropy_result.get("entropy")
            entropy_status = entropy_result.get("status")

            entropy_info = (
                f"Entropy: {entropy_value} | "
                f"Status: {entropy_status}"
            )

            if entropy_result.get("suspicious"):
                severity = "CRITICAL"

        action_message = (
            f"Trap file {event_type}: {file_path} | "
            f"{entropy_info} | "
            f"{containment['action']}"
        )

        cursor.execute("""
            INSERT INTO alerts
            (timestamp, severity, detector, process_pid,
             process_name, status, action)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            severity,
            "Trap File Monitor + Entropy Analysis",
            0,
            containment["process_name"],
            containment["status"],
            action_message
        ))

        connection.commit()
        connection.close()

        print("[+] Security alert saved to database.")

    except Exception as error:
        print(f"[ERROR] Failed to save alert: {error}")


class TrapEventHandler(FileSystemEventHandler):

    def _is_trap_file(self, path):
        return Path(path).name in TRAP_FILE_NAMES

    def handle_trap_event(self, event_type, path):

        print(f"\n[THREAT DETECTED] Trap file {event_type}: {path}")

        entropy_result = None

        # Entropy analysis only when file exists
        if event_type in ["MODIFIED", "CREATED"]:

            print("[+] Running entropy analysis...")

            entropy_result = analyze_file(path)

            # Save latest entropy result for dashboard
            save_entropy_status(path, entropy_result)

            if entropy_result.get("entropy") is not None:

                print(
                    f"[+] Entropy Score: "
                    f"{entropy_result['entropy']}"
                )

                print(
                    f"[+] Entropy Status: "
                    f"{entropy_result['status']}"
                )

                if entropy_result.get("suspicious"):
                    print(
                        "[ALERT] HIGH ENTROPY DETECTED - "
                        "Possible encryption activity!"
                    )
                else:
                    print("[OK] Entropy level appears normal.")

            else:
                print("[!] Entropy analysis could not read the file.")

        else:
            print("[INFO] Entropy analysis skipped.")

        containment = simulate_containment(path)

        save_alert(
            event_type,
            path,
            containment,
            entropy_result
        )

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

    observer = Observer()
    handler = TrapEventHandler()

    monitored_folders = []

    for folder in get_user_folders():
        if folder.exists():
            observer.schedule(handler, str(folder), recursive=False)
            monitored_folders.append(folder)

    observer.start()

    print("[+] RansomTrap file monitor started.")
    print("[+] Entropy Analysis Engine: ACTIVE")
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