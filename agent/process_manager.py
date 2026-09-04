import psutil


def get_process_info(pid):
    """Return basic information about a process."""

    try:
        process = psutil.Process(pid)

        try:
            executable = process.exe()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            executable = None

        try:
            name = process.name()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            name = None

        return {
            "pid": process.pid,
            "name": name,
            "exe": executable,
            "parent_pid": process.ppid(),
        }

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess,
    ):
        return None


def get_parent_chain(pid):
    """Return the target process and all available parents."""

    chain = []
    current_pid = pid
    visited = set()

    while current_pid and current_pid not in visited:
        visited.add(current_pid)

        info = get_process_info(current_pid)

        if info is None:
            break

        chain.append(info)

        parent_pid = info["parent_pid"]

        if not parent_pid or parent_pid == current_pid:
            break

        current_pid = parent_pid

    return chain


def get_child_processes(pid):
    """Return all recursive child processes."""

    try:
        process = psutil.Process(pid)

        children = []

        for child in process.children(recursive=True):
            info = get_process_info(child.pid)

            if info:
                children.append(info)

        return children

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess,
    ):
        return []


def get_full_process_tree(pid):
    """
    Return a combined process tree containing:
    - target process
    - parent chain
    - recursive children
    """

    processes = []
    seen_pids = set()

    # Add target + parents
    for process in get_parent_chain(pid):
        if process["pid"] not in seen_pids:
            processes.append(process)
            seen_pids.add(process["pid"])

    # Add recursive children
    for process in get_child_processes(pid):
        if process["pid"] not in seen_pids:
            processes.append(process)
            seen_pids.add(process["pid"])

    return processes


def print_process_tree(pid):
    """Print the complete process tree information."""

    info = get_process_info(pid)

    if info is None:
        print(f"[PROCESS] PID {pid} not found.")
        return

    print("[PROCESS] Target process:")
    print(f"    PID: {info['pid']}")
    print(f"    Name: {info['name']}")
    print(f"    EXE: {info['exe']}")
    print(f"    Parent PID: {info['parent_pid']}")

    print()
    print("[PROCESS] Parent chain:")

    parent_chain = get_parent_chain(pid)

    for process in parent_chain:
        print(
            f"    PID={process['pid']} "
            f"PPID={process['parent_pid']} "
            f"Name={process['name']}"
        )

    print()
    print("[PROCESS] Child processes:")

    children = get_child_processes(pid)

    if not children:
        print("    None")
    else:
        for child in children:
            print(
                f"    PID={child['pid']} "
                f"PPID={child['parent_pid']} "
                f"Name={child['name']}"
            )

    print()
    print("[PROCESS] Combined process tree:")

    full_tree = get_full_process_tree(pid)

    for process in full_tree:
        print(
            f"    PID={process['pid']} "
            f"PPID={process['parent_pid']} "
            f"Name={process['name']}"
        )


if __name__ == "__main__":
    current_pid = psutil.Process().pid

    print(
        f"[+] Testing Process Tree v2 "
        f"with current PID: {current_pid}"
    )

    print_process_tree(current_pid)

    print()
    print("[+] Process Tree v2 test completed.")