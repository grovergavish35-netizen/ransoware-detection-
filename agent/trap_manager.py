from pathlib import Path

from agent.database import initialize_database, get_connection


TRAP_FILE_NAMES = {
    "RansomTrap_Document.docx",
    "RansomTrap_Important.xlsx",
    "RansomTrap_Photos.zip",
}


def get_user_folders():
    home = Path.home()

    return [
        home / "Desktop",
        home / "Documents",
        home / "Downloads",
    ]


def register_trap(trap_path):
    initialize_database()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO traps (path, created_at, status)
        VALUES (?, datetime('now'), 'active')
        ON CONFLICT(path) DO UPDATE SET
            status = 'active'
        """,
        (str(trap_path),),
    )

    connection.commit()
    connection.close()


def create_trap_file(folder, file_name):
    folder.mkdir(parents=True, exist_ok=True)

    trap_path = folder / file_name

    if not trap_path.exists():
        trap_path.write_bytes(
            b"RansomTrap harmless decoy file."
        )

        print(f"[TRAP] Created: {trap_path}")
    else:
        print(f"[TRAP] Already exists: {trap_path}")

    register_trap(trap_path)

    return trap_path


def create_trap_files():
    trap_files = []

    for folder in get_user_folders():
        if not folder.exists():
            continue

        for file_name in sorted(TRAP_FILE_NAMES):
            trap_path = create_trap_file(
                folder,
                file_name,
            )

            trap_files.append(trap_path)

    return trap_files


if __name__ == "__main__":
    print("[+] RansomTrap trap manager test")

    trap_files = create_trap_files()

    print()
    print(f"[+] Trap files ready: {len(trap_files)}")

    for trap in trap_files:
        print(f"    {trap}")

    print("[+] Trap registration completed.")