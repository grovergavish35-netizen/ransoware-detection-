import psutil


# Demo suspicious process keywords
SUSPICIOUS_KEYWORDS = [
    "ransomware",
    "encryptor",
    "malware",
    "locker",
    "crypt"
]


def get_running_processes():
    """
    Get information about currently running processes.
    """

    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "status"]
    ):
        try:
            processes.append({
                "pid": process.info["pid"],
                "name": process.info["name"],
                "status": process.info["status"]
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            pass

    return processes


def get_process_count():
    """Return total running process count."""
    return len(get_running_processes())


def detect_suspicious_processes():
    """
    Detect processes with suspicious names.
    """

    suspicious_processes = []

    for process in psutil.process_iter(["pid", "name", "status"]):
        try:
            process_name = process.info["name"] or ""
            process_name_lower = process_name.lower()

            for keyword in SUSPICIOUS_KEYWORDS:
                if keyword in process_name_lower:
                    suspicious_processes.append({
                        "pid": process.info["pid"],
                        "name": process_name,
                        "status": process.info["status"],
                        "reason": f"Suspicious keyword detected: {keyword}",
                        "severity": "HIGH"
                    })
                    break

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            pass

    return suspicious_processes


def simulate_containment(pid, process_name):
    """
    Safe containment simulation for SIH demo.
    Does NOT terminate any real process.
    """

    return {
        "pid": pid,
        "process": process_name,
        "action": "CONTAINMENT_SIMULATED",
        "status": "BLOCKED",
        "message": "Suspicious process isolated successfully"
    }


if __name__ == "__main__":

    processes = get_running_processes()

    print("\n[+] RansomTrap Process Monitor Started")
    print(f"[+] Total running processes: {len(processes)}")

    suspicious = detect_suspicious_processes()

    print(f"[+] Suspicious processes found: {len(suspicious)}")

    if suspicious:
        print("\n[!] Suspicious Processes:")

        for process in suspicious:
            print(
                f"PID: {process['pid']} | "
                f"Name: {process['name']} | "
                f"Reason: {process['reason']}"
            )
    else:
        print("\n[✓] No suspicious processes detected.")