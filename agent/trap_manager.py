from pathlib import Path


TRAP_FILE_NAMES = [
    "RansomTrap_Document.docx",
    "RansomTrap_Important.xlsx",
    "RansomTrap_Photos.zip",
]


def get_user_folders():
    """Return common Windows user folders."""
    home = Path.home()

    return [
        home / "Desktop",
        home / "Documents",
        home / "Downloads",
    ]


def create_trap_files():
    """Create harmless decoy files in existing user folders."""
    created_files = []

    for folder in get_user_folders():
        if not folder.exists():
            continue

        for filename in TRAP_FILE_NAMES:
            trap_path = folder / filename

            if not trap_path.exists():
                trap_path.write_text(
                    "RansomTrap decoy file.\n"
                    "This file is used for ransomware detection testing.\n",
                    encoding="utf-8",
                )

            created_files.append(str(trap_path))

    return created_files


if __name__ == "__main__":
    files = create_trap_files()

    print("RansomTrap trap files:")
    for file_path in files:
        print(f"  {file_path}")