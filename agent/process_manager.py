import psutil


def get_process_info(pid):
    """Return basic information about a process."""

    try:
        process = psutil.Process(pid)

        return {
            "pid": process.pid,
            "name": process.name(),
            "exe": process.exe(),
            "parent_pid": process.ppid(),
        }

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None


def get_process_tree(pid):
    """Return the process and its parent chain."""

    tree = []

    try:
        process = psutil.Process(pid)

        while process:
            try:
                tree.append(
                    {
                        "pid": process.pid,
                        "name": process.name(),
                        "exe": process.exe(),
                        "parent_pid": process.ppid(),
                    }
                )

                parent = process.parent()

                if parent is None:
                    break

                process = parent

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                break

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess,
    ):
        pass

    return tree


def print_process_tree(pid):
    """Print a process tree for debugging."""

    tree = get_process_tree(pid)

    if not tree:
        print(f"[!] Could not inspect process {pid}")
        return

    print("[+] Process tree:")

    for process in tree:
        print(
            f"    PID={process['pid']} "
            f"Name={process['name']} "
            f"Parent={process['parent_pid']}"
        )


if __name__ == "__main__":
    current_pid = psutil.Process().pid

    print(f"[+] Testing process manager with PID {current_pid}")
    print_process_tree(current_pid)