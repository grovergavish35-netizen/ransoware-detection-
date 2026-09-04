from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from trap_manager import get_user_folders, TRAP_FILE_NAMES


class TrapEventHandler(FileSystemEventHandler):
    """Handle filesystem activity involving RansomTrap files."""

    def _is_trap_file(self, path):
        return Path(path).name in TRAP_FILE_NAMES

    def on_modified(self, event):
        if event.is_directory:
            return

        if self._is_trap_file(event.src_path):
            print(f"[ALERT] Trap file modified: {event.src_path}")

    def on_created(self, event):
        if event.is_directory:
            return

        if self._is_trap_file(event.src_path):
            print(f"[ALERT] Trap file created: {event.src_path}")

    def on_deleted(self, event):
        if event.is_directory:
            return

        if self._is_trap_file(event.src_path):
            print(f"[ALERT] Trap file deleted: {event.src_path}")

    def on_moved(self, event):
        if event.is_directory:
            return

        if self._is_trap_file(event.src_path):
            print(
                f"[ALERT] Trap file renamed/moved: "
                f"{event.src_path} -> {event.dest_path}"
            )

        elif self._is_trap_file(event.dest_path):
            print(
                f"[ALERT] File moved to trap name: "
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
            pass
    except KeyboardInterrupt:
        print("\n[+] Stopping monitor...")
        observer.stop()

    observer.join()