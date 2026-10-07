import sys
from pathlib import Path
from datetime import datetime

# Project root ko Python path mein add karo
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from agent.trap_manager import get_user_folders, TRAP_FILE_NAMES
from services.database import initialize_database, insert_trap


def sync_traps():
    """Find existing trap files and save them to SQLite."""

    initialize_database()

    synced_count = 0

    for folder in get_user_folders():
        if not folder.exists():
            continue

        for filename in TRAP_FILE_NAMES:
            trap_path = folder / filename

            if trap_path.exists():
                created_time = datetime.fromtimestamp(
                    trap_path.stat().st_ctime
                ).strftime("%Y-%m-%d %H:%M:%S")

                insert_trap(
                    str(trap_path),
                    filename,
                    created_time,
                    "ACTIVE"
                )

                print(f"[+] Synced: {trap_path}")
                synced_count += 1

    print(f"\n[+] Total trap files synced: {synced_count}")


if __name__ == "__main__":
    sync_traps()