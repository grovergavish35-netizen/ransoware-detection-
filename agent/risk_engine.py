from datetime import datetime


def calculate_risk(
    trap_triggered=False,
    high_entropy=False,
    suspicious_processes=0
):
    """
    Calculate ransomware threat risk score
    based on multiple detection signals.
    """

    score = 0
    signals = []

    # Trap file activity
    if trap_triggered:
        score += 40
        signals.append({
            "signal": "Trap File Activity",
            "score": 40,
            "status": "DETECTED"
        })

    # High entropy detection
    if high_entropy:
        score += 30
        signals.append({
            "signal": "High File Entropy",
            "score": 30,
            "status": "DETECTED"
        })

    # Suspicious process detection
    if suspicious_processes > 0:
        score += 30
        signals.append({
            "signal": "Suspicious Process",
            "score": 30,
            "status": f"{suspicious_processes} DETECTED"
        })

    # Ensure score never exceeds 100
    score = min(score, 100)

    # Determine severity
    if score >= 80:
        severity = "CRITICAL"
        action = "CONTAIN IMMEDIATELY"

    elif score >= 50:
        severity = "HIGH"
        action = "INVESTIGATE AND ISOLATE"

    elif score >= 20:
        severity = "MEDIUM"
        action = "MONITOR ACTIVITY"

    else:
        severity = "LOW"
        action = "SYSTEM NORMAL"

    return {
        "risk_score": score,
        "severity": severity,
        "recommended_action": action,
        "signals": signals,
        "analyzed_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }