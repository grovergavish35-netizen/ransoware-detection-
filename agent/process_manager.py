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
    """
    Build the parent chain for a process.

    Returns a list starting from the target process
    and moving upward through its parents.
    """

    tree = []
    current_pid = pid

    while current_pid:

        info = get_process_info(current_pid)

        if info is None:
            break

        tree.append(info)

        parent_pid = info["parent_pid"]

        if parent_pid == current_pid:
            break

        current_pid = parent_pid

    return tree


def get_child_processes(pid):
    """Return direct child processes of the given PID."""

    try:
        process = psutil.Process(pid)

        children = []

        for child in process.children(recursive=True):
            info = get_process_info(child.pid)

            if info:
                children.append(info)

        return children

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return []


def print_process_tree(pid):
    """Print parent and child process information."""

    info = get_process_info(pid)

    if info is None:
        print(f"[PROCESS] PID {pid} not found.")
        return

    print("[PROCESS] Target process:")
    print(f"    PID: {info['pid']}")
    print(f"    Name: {info['name']}")
    print(f"    EXE: {info['exe']}")
    print(f"    Parent PID: {info['parent_pid']}")

    print("[PROCESS] Parent chain:")

    for process in get_process_tree(pid):
        print(
            f"    PID={process['pid']} "
            f"PPID={process['parent_pid']} "
            f"Name={process['name']}"
        )

    print("[PROCESS] Child processes:")

    for child in get_child_processes(pid):
        print(
            f"    PID={child['pid']} "
            f"PPID={child['parent_pid']} "
            f"Name={child['name']}"
        )


if __name__ == "__main__":
    current_pid = psutil.Process().pid

    print(f"[+] Testing process manager with current PID: {current_pid}")
    print_process_tree(current_pid)