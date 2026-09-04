import psutil
from datetime import datetime, timezone

from agent.recovery import create_snapshot
from agent.process_manager import get_process_tree
from agent.database import (
    log_process_tree,
    update_alert_process,
    update_alert_status,
)


def get_process_snapshot(pid):
    """Capture forensic information about a process."""

    try:
        process = psutil.Process(pid)

        return {
            "pid": process.pid,
            "name": process.name(),
            "exe": process.exe(),
            "cmdline": process.cmdline(),
            "parent_pid": process.ppid(),
            "username": process.username(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess,
    ):
        return None


def suspend_process(pid):
    """Suspend a process for containment."""

    try:
        process = psutil.Process(pid)
        process.suspend()

        print(f"[CONTAINMENT] Process suspended: PID={pid}")
        return True

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess,
    ) as e:
        print(f"[CONTAINMENT] Failed to suspend PID={pid}: {e}")
        return False


def terminate_process(pid):
    """Terminate a process after containment."""

    try:
        process = psutil.Process(pid)
        process.terminate()
        process.wait(timeout=5)

        print(f"[CONTAINMENT] Process terminated: PID={pid}")
        return True

    except psutil.TimeoutExpired:
        print(
            f"[CONTAINMENT] Process did not terminate "
            f"within timeout: PID={pid}"
        )
        return False

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess,
    ) as e:
        print(f"[CONTAINMENT] Failed to terminate PID={pid}: {e}")
        return False


def handle_process_response(alert_id, pid, file_path=None):
    """
    Perform the forensic and containment workflow for a known PID.

    IMPORTANT:
    The PID must come from a trusted process-attribution mechanism.
    This function does not guess which process caused a filesystem event.
    """

    print()
    print("[RESPONSE] Starting response workflow...")
    print(f"[RESPONSE] Alert ID: {alert_id}")
    print(f"[RESPONSE] Target PID: {pid}")

    # 1. Capture forensic snapshot
    snapshot = get_process_snapshot(pid)

    if snapshot is None:
        print("[FORENSICS] Unable to capture process snapshot.")
        update_alert_status(alert_id, "process_unavailable")
        return False

    print("[FORENSICS] Process snapshot captured.")

    # 2. Attach process information to alert
    update_alert_process(
        alert_id,
        snapshot["pid"],
        snapshot["name"],
    )

    # 3. Capture process tree
    process_tree = get_process_tree(pid)

    if process_tree:
        log_process_tree(
            alert_id,
            process_tree,
        )

        print(
            f"[FORENSICS] Process tree recorded: "
            f"{len(process_tree)} process(es)"
        )

    # 4. Create recovery snapshot if file exists
    if file_path:
        recovery_path = create_snapshot(file_path)

        if recovery_path:
            print(
                f"[RECOVERY] Snapshot available: "
                f"{recovery_path}"
            )

    # 5. Suspend first
    if not suspend_process(pid):
        update_alert_status(alert_id, "containment_failed")
        return False

    update_alert_status(alert_id, "suspended")

    # 6. Terminate after successful suspension
    if not terminate_process(pid):
        update_alert_status(alert_id, "termination_failed")
        return False

    update_alert_status(alert_id, "contained")

    print("[RESPONSE] Threat containment completed.")
    return True


def print_snapshot(snapshot):
    """Print a forensic process snapshot."""

    if not snapshot:
        print("[FORENSICS] Process snapshot unavailable.")
        return

    print("[FORENSICS] Process snapshot:")
    print(f"    PID: {snapshot['pid']}")
    print(f"    Name: {snapshot['name']}")
    print(f"    EXE: {snapshot['exe']}")
    print(f"    Parent PID: {snapshot['parent_pid']}")
    print(f"    Username: {snapshot['username']}")
    print(f"    Command Line: {snapshot['cmdline']}")
    print(f"    Timestamp: {snapshot['timestamp']}")


if __name__ == "__main__":
    current_pid = psutil.Process().pid

    print(
        f"[+] Testing response module with current PID: "
        f"{current_pid}"
    )

    snapshot = get_process_snapshot(current_pid)

    print_snapshot(snapshot)

    print("[+] Response module test completed safely.")