import math
from pathlib import Path
from collections import Counter


def calculate_entropy(file_path):
    """
    Calculate Shannon entropy of a file.

    Entropy range:
    0.0 = very predictable data
    8.0 = highly random data
    """

    try:
        file_path = Path(file_path)

        if not file_path.exists():
            return None

        data = file_path.read_bytes()

        if not data:
            return 0.0

        byte_counts = Counter(data)
        file_size = len(data)

        entropy = 0.0

        for count in byte_counts.values():
            probability = count / file_size
            entropy -= probability * math.log2(probability)

        return round(entropy, 4)

    except Exception as error:
        print(f"[ERROR] Entropy calculation failed: {error}")
        return None


def analyze_file(file_path, threshold=7.5):
    """
    Analyze whether a file has suspiciously high entropy.
    """

    entropy = calculate_entropy(file_path)

    if entropy is None:
        return {
            "file": str(file_path),
            "entropy": None,
            "status": "ERROR",
            "suspicious": False
        }

    suspicious = entropy >= threshold

    return {
        "file": str(file_path),
        "entropy": entropy,
        "threshold": threshold,
        "status": "HIGH_ENTROPY" if suspicious else "NORMAL",
        "suspicious": suspicious
    }


if __name__ == "__main__":

    print("\n[+] RansomTrap Entropy Analysis Engine")

    test_file = input("Enter file path to analyze: ").strip()

    result = analyze_file(test_file)

    print("\n--- Analysis Result ---")
    print(f"File: {result['file']}")
    print(f"Entropy: {result['entropy']}")
    print(f"Status: {result['status']}")
    print(f"Suspicious: {result['suspicious']}")