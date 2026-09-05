import os
import shutil
from datetime import datetime


BACKUP_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "secure_backups"
)


def initialize_backup_folder():
    """Create secure backup directory if it does not exist."""

    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)


def backup_file(file_path):
    """Create a safe backup copy of a file."""

    initialize_backup_folder()

    if not os.path.exists(file_path):
        return {
            "success": False,
            "message": "File not found"
        }

    file_name = os.path.basename(file_path)

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_name = f"{timestamp}_{file_name}"

    backup_path = os.path.join(
        BACKUP_FOLDER,
        backup_name
    )

    shutil.copy2(
        file_path,
        backup_path
    )

    return {
        "success": True,
        "backup_name": backup_name,
        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }


def get_backup_status():
    """Return available backup information."""

    initialize_backup_folder()

    backups = []

    for file_name in os.listdir(BACKUP_FOLDER):

        file_path = os.path.join(
            BACKUP_FOLDER,
            file_name
        )

        if os.path.isfile(file_path):

            backups.append({
                "name": file_name,
                "size": os.path.getsize(file_path),
                "created_at": datetime.fromtimestamp(
                    os.path.getctime(file_path)
                ).strftime("%Y-%m-%d %H:%M:%S")
            })

    return {
        "total_backups": len(backups),
        "backups": backups
    }