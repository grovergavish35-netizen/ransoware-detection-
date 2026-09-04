from pathlib import Path

from agent.entropy_detector import calculate_file_entropy
from agent.database import log_alert


DEFAULT_THRESHOLD = 7.5


def scan_file(file_path, threshold=DEFAULT_THRESHOLD):
    """
    Calculate file entropy and create an alert if entropy is unusually high.
    """

    path = Path(file_path)

    if not path.exists() or not path.is_file():
        return None

    try:
        entropy = calculate_file_entropy(path)

        if entropy >= threshold:
            alert_id = log_alert(
                alert_type="high_entropy",
                severity="medium",
                file_path=str(path),
                details=(
                    f"High entropy detected: {entropy:.2f} "
                    f"(threshold: {threshold:.2f})"
                ),
            )

            print(
                f"[ENTROPY ALERT] {path} "
                f"entropy={entropy:.2f} "
                f"(Alert ID: {alert_id})"
            )

            return alert_id

    except Exception as e:
        print(f"[ENTROPY] Failed to scan {path}: {e}")

    return None


def scan_folder(folder_path, extensions=None, threshold=DEFAULT_THRESHOLD):
    """
    Scan files directly inside a folder.

    extensions can be used to limit scanning, for example:
    ['.docx', '.xlsx', '.zip']
    """

    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        return

    for file_path in folder.iterdir():

        if not file_path.is_file():
            continue

        if extensions:
            if file_path.suffix.lower() not in extensions:
                continue

        scan_file(file_path, threshold)


if __name__ == "__main__":
    print("[+] Entropy monitor test")

    test_folder = Path("data")

    if test_folder.exists():
        scan_folder(test_folder)
        print("[+] Entropy scan completed.")
    else:
        print("[!] data folder not found.")