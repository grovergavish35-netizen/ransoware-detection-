import math
from collections import Counter
from pathlib import Path


def calculate_entropy(data):
    """Calculate Shannon entropy for bytes."""

    if not data:
        return 0.0

    counts = Counter(data)
    length = len(data)

    entropy = 0.0

    for count in counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy


def calculate_file_entropy(file_path, sample_size=1024 * 1024):
    """
    Calculate entropy using up to the first 1 MB of a file.
    Returns None if the file cannot be read.
    """

    path = Path(file_path)

    try:
        with path.open("rb") as file:
            data = file.read(sample_size)

        return calculate_entropy(data)

    except (OSError, PermissionError):
        return None


def is_high_entropy(file_path, threshold=7.5):
    """Return True when file entropy exceeds the configured threshold."""

    entropy = calculate_file_entropy(file_path)

    if entropy is None:
        return False

    return entropy >= threshold


if __name__ == "__main__":
    test_file = Path("data") / "entropy_test.txt"

    test_file.write_text(
        "This is a normal RansomTrap entropy test file. " * 100,
        encoding="utf-8",
    )

    entropy = calculate_file_entropy(test_file)

    print(f"[+] Test file: {test_file}")
    print(f"[+] Entropy: {entropy:.4f}")

    if is_high_entropy(test_file):
        print("[!] High entropy detected")
    else:
        print("[+] Entropy is within normal range")

    test_file.unlink(missing_ok=True)