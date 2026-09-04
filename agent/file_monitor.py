from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from trap_manager import get_user_folders, TRAP_FILE_NAMES
from database import initialize_database, log_alert


class TrapEventHandler(FileSystemEventHandler):
    """Handle filesystem activity involving RansomTrap trap files."""

    def _is_trap_file(self, path):
        return Path(path).name in TRAP_FILE_NAMES

    def _record_alert(self, event_type, path):
        alert_id = log_alert(
            alert_type=f"trap_{event_type}",
            severity="high",
            file_path=str(path),
            details=f"RansomTrap detected {event_type} activity on a trap file.",
        )

        print(
            f"[ALERT] Trap file {event_type}: {path} "
            f"(Alert ID: {alert_id})"
        )

    def on_modified(self, event):
        if event.is_directory:
            return

        if self._is_trap_file(event.src_path):
            self._record_alert("modified", event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return

        if self._is_trap_file(event.src_path):
            self._record_alert("created", event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return

        if self._is_trap_file(event.src_path):
            self._record_alert("deleted", event.src_path)


def start_monitor():
    """Start monitoring folders containing trap files."""

    initialize_database()

    observer = Observer()
    handler = TrapEventHandler()

    monitored_folders = []

    for folder in get_user_folders():
        if folder.exists():
            observer.schedule(
                handler,
                str(folder),
                recursive=False,
            )
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
            pass

    except KeyboardInterrupt:
        print("\n[+] Stopping monitor...")
        observer.stop()

    observer.join()