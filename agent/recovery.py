from pathlib import Path
import shutil
from datetime import datetime


BACKUP_ROOT = Path("data") / "recovery"


def create_snapshot(file_path):
    """
    Create a local recovery copy of a file.

    Returns the backup path if successful, otherwise None.
    """

    source = Path(file_path)

    if not source.exists() or not source.is_file():
        print(f"[RECOVERY] File not found: {source}")
        return None

    try:
        BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        backup_name = f"{source.stem}_{timestamp}{source.suffix}"
        backup_path = BACKUP_ROOT / backup_name

        shutil.copy2(source, backup_path)

        print(f"[RECOVERY] Snapshot created: {backup_path}")

        return backup_path

    except Exception as e:
        print(f"[RECOVERY] Snapshot failed: {e}")
        return None


def restore_snapshot(snapshot_path, destination_path):
    """
    Restore a recovery snapshot to its destination.
    """

    snapshot = Path(snapshot_path)
    destination = Path(destination_path)

    if not snapshot.exists() or not snapshot.is_file():
        print(f"[RECOVERY] Snapshot not found: {snapshot}")
        return False

    try:
        destination.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(snapshot, destination)

        print(f"[RECOVERY] File restored: {destination}")

        return True

    except Exception as e:
        print(f"[RECOVERY] Restore failed: {e}")
        return False


if __name__ == "__main__":
    print("[+] Recovery module test")

    test_file = Path("data") / "recovery_test.txt"
    test_file.parent.mkdir(parents=True, exist_ok=True)

    test_file.write_text(
        "RansomTrap recovery test file.",
        encoding="utf-8",
    )

    snapshot = create_snapshot(test_file)

    if snapshot:
        restored_file = Path("data") / "recovery_restored.txt"

        if restore_snapshot(snapshot, restored_file):
            print("[+] Recovery test successful.")

        if restored_file.exists():
            restored_file.unlink()

        snapshot.unlink()

    if test_file.exists():
        test_file.unlink()

    print("[+] Recovery module test completed.")