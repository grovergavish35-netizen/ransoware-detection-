import subprocess
import sys
import time
from pathlib import Path

from agent.database import initialize_database, log_alert
from agent.response import handle_process_response


DEMO_FILE = Path("data") / "demo_document.txt"


def create_demo_file():
    """Create a harmless file for the recovery snapshot test."""

    DEMO_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    DEMO_FILE.write_text(
        "RansomTrap controlled E2E demonstration file.\n",
        encoding="utf-8",
    )

    print(f"[DEMO] Test file created: {DEMO_FILE}")


def start_controlled_process():
    """Start a harmless long-running child process."""

    command = [
        sys.executable,
        "-c",
        "import time; time.sleep(600)",
    ]

    process = subprocess.Popen(command)

    print(
        f"[DEMO] Controlled test process started: "
        f"PID={process.pid}"
    )

    return process


def verify_process_stopped(pid):
    """Check whether the controlled process has exited."""

    try:
        process = subprocess.Popen(
            [
                sys.executable,
                "-c",
                (
                    "import psutil, sys; "
                    f"sys.exit(0 if psutil.pid_exists({pid}) else 1)"
                ),
            ]
        )

        process.wait(timeout=5)

        return process.returncode != 0

    except Exception:
        return False


def main():
    print("=" * 55)
    print("       RANSOMTRAP SAFE E2E RESPONSE DEMO")
    print("=" * 55)

    initialize_database()

    print("[+] SQLite initialized.")

    create_demo_file()

    process = start_controlled_process()

    time.sleep(1)

    alert_id = log_alert(
        alert_type="demo_ransomware_detection",
        severity="high",
        file_path=str(DEMO_FILE),
        process_id=process.pid,
        process_name="controlled-demo-process",
        details=(
            "Controlled RansomTrap demonstration. "
            "No malicious activity is performed."
        ),
    )

    print(
        f"[DEMO] SQLite alert created: ID={alert_id}"
    )

    print()
    print("[DEMO] Starting response pipeline...")

    success = handle_process_response(
        alert_id=alert_id,
        pid=process.pid,
        file_path=DEMO_FILE,
    )

    print()

    if success:
        print("[+] E2E response workflow completed successfully.")
    else:
        print("[!] E2E response workflow reported a failure.")

    print()
    print("[DEMO] Cleaning up demo file...")

    if DEMO_FILE.exists():
        DEMO_FILE.unlink()

    print("[+] Demo cleanup completed.")

    print()
    print("[+] Safe E2E demonstration finished.")


if __name__ == "__main__":
    main()