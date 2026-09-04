import time
import threading

from agent.trap_manager import create_trap_files, get_user_folders
from agent.file_monitor import start_monitor
from agent.database import initialize_database
from agent.entropy_monitor import scan_folder


ENTROPY_EXTENSIONS = [
    ".txt",
    ".doc",
    ".xls",
]


def start_entropy_monitor():
    """Run periodic entropy scans in the background."""

    def entropy_scan_loop():
        while True:
            try:
                for folder in get_user_folders():
                    if folder.exists():
                        scan_folder(
                            folder,
                            extensions=ENTROPY_EXTENSIONS,
                        )

            except Exception as e:
                print(f"[ENTROPY] Scan error: {e}")

            time.sleep(30)

    thread = threading.Thread(
        target=entropy_scan_loop,
        daemon=True,
    )

    thread.start()

    return thread


def main():
    print("=" * 50)
    print("        RANSOMTRAP SECURITY AGENT")
    print("=" * 50)

    # Initialize local SQLite database
    initialize_database()
    print("[+] SQLite database initialized.")

    # Create decoy/trap files
    trap_files = create_trap_files()

    print(f"[+] Trap files ready: {len(trap_files)}")

    for path in trap_files:
        print(f"    {path}")

    # Start trap-file filesystem monitoring
    observer = start_monitor()

    # Start entropy monitoring
    start_entropy_monitor()

    print("[+] Entropy monitoring ACTIVE.")
    print("[+] RansomTrap protection is ACTIVE.")
    print("[+] Press Ctrl+C to stop the agent.")
    print()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[+] Stopping RansomTrap...")

        observer.stop()
        observer.join()

        print("[+] RansomTrap stopped safely.")


if __name__ == "__main__":
    main()