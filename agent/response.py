import psutil
from datetime import datetime, timezone


def get_process_snapshot(pid):
    """Capture basic forensic information before containment."""

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
    """Safely suspend a process by PID."""

    try:
        process = psutil.Process(pid)
        process.suspend()

        print(f"[CONTAINMENT] Process suspended: PID={pid}")
        return True

    except psutil.NoSuchProcess:
        print(f"[!] Process no longer exists: PID={pid}")

    except psutil.AccessDenied:
        print(f"[!] Access denied while suspending PID={pid}")

    except psutil.ZombieProcess:
        print(f"[!] Zombie process: PID={pid}")

    except Exception as error:
        print(f"[!] Failed to suspend PID={pid}: {error}")

    return False


def terminate_process(pid):
    """Terminate a process after explicit confirmation from the caller."""

    try:
        process = psutil.Process(pid)

        print(f"[RESPONSE] Terminating PID={pid} ({process.name()})")

        process.terminate()
        process.wait(timeout=5)

        print(f"[RESPONSE] Process terminated: PID={pid}")
        return True

    except psutil.NoSuchProcess:
        print(f"[!] Process already exited: PID={pid}")

    except psutil.AccessDenied:
        print(f"[!] Access denied while terminating PID={pid}")

    except psutil.TimeoutExpired:
        print(f"[!] Process did not terminate within timeout: PID={pid}")

    except psutil.ZombieProcess:
        print(f"[!] Zombie process: PID={pid}")

    except Exception as error:
        print(f"[!] Failed to terminate PID={pid}: {error}")

    return False


if __name__ == "__main__":
    current_process = psutil.Process()

    print("[+] Response module test")
    print(f"[+] Current PID: {current_process.pid}")

    snapshot = get_process_snapshot(current_process.pid)

    if snapshot:
        print("[+] Forensic snapshot:")
        print(f"    Name: {snapshot['name']}")
        print(f"    PID: {snapshot['pid']}")
        print(f"    Parent PID: {snapshot['parent_pid']}")
        print(f"    Executable: {snapshot['exe']}")
        print(f"    Command: {snapshot['cmdline']}")

    print("[+] Snapshot test successful.")
    print("[+] No process was suspended or terminated.")