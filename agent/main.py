from trap_manager import create_trap_files
from file_monitor import start_monitor
import time


def main():
    print("=" * 50)
    print("       RansomTrap Security Agent")
    print("=" * 50)

    print("\n[+] Creating trap files...")
    trap_files = create_trap_files()

    for file_path in trap_files:
        print(f"    Created/verified: {file_path}")

    print("\n[+] Starting file monitor...")
    observer = start_monitor()

    print("\n[+] RansomTrap Agent is ACTIVE")
    print("[+] Press Ctrl+C to stop\n")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[+] Stopping RansomTrap Agent...")
        observer.stop()

    observer.join()
    print("[+] Agent stopped successfully.")


if __name__ == "__main__":
    main()