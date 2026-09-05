from flask import Flask, jsonify
from flask_cors import CORS
from pathlib import Path
from datetime import datetime
import sqlite3
import psutil
import sys
import json


# ==========================================
# PATH SETUP
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent.parent
AGENT_DIR = PROJECT_DIR / "agent"

if str(AGENT_DIR) not in sys.path:
    sys.path.append(str(AGENT_DIR))


# ==========================================
# IMPORT PROJECT MODULES
# ==========================================

try:
    from trap_manager import get_user_folders, TRAP_FILE_NAMES
except ImportError as error:
    print("[WARNING] Could not import trap_manager:", error)

    def get_user_folders():
        return []

    TRAP_FILE_NAMES = []


try:
    from risk_engine import calculate_risk
except ImportError as error:
    print("[WARNING] Could not import risk_engine:", error)

    def calculate_risk(
        trap_triggered=False,
        high_entropy=False,
        suspicious_processes=0
    ):
        return {
            "risk_score": 0,
            "severity": "UNKNOWN",
            "recommended_action": "RISK ENGINE ERROR",
            "signals": [],
            "analyzed_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)
CORS(app)

DB_PATH = BASE_DIR / "ransotrap.db"


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

def init_database():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            severity TEXT,
            detector TEXT,
            process_pid INTEGER,
            process_name TEXT,
            status TEXT,
            action TEXT
        )
    """)

    connection.commit()
    connection.close()

    print("[+] Database initialized successfully.")


# ==========================================
# HOME API
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "RansomTrap Backend Running",
        "message": "Backend API is active"
    })


# ==========================================
# API: GET TRAP FILES
# ==========================================

@app.route("/api/traps", methods=["GET"])
def get_traps():

    traps = []

    try:

        folders = get_user_folders()

        for folder in folders:

            if folder.exists():

                for file in folder.iterdir():

                    if (
                        file.is_file()
                        and file.name in TRAP_FILE_NAMES
                    ):

                        traps.append({
                            "name": file.name,
                            "path": str(file),
                            "status": "ACTIVE"
                        })

    except Exception as error:

        print("[ERROR] Trap API:", error)

    return jsonify(traps)


# ==========================================
# API: GET SECURITY ALERTS
# ==========================================

@app.route("/api/alerts", methods=["GET"])
def get_alerts():

    try:

        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM alerts
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        connection.close()

        alerts = []

        for row in rows:
            alerts.append(dict(row))

        return jsonify(alerts)

    except Exception as error:

        print("[ERROR] Alerts API:", error)

        return jsonify({
            "error": str(error)
        }), 500


# ==========================================
# API: PROCESS COUNT
# ==========================================

@app.route("/api/processes", methods=["GET"])
def get_processes():

    try:

        count = len(
            list(psutil.process_iter())
        )

        return jsonify({
            "count": count
        })

    except Exception as error:

        print("[ERROR] Process Count:", error)

        return jsonify({
            "count": 0
        })


# ==========================================
# API: SUSPICIOUS PROCESS DETECTION
# ==========================================

@app.route("/api/suspicious-processes", methods=["GET"])
def suspicious_processes():

    suspicious = []

    suspicious_keywords = [
        "ransom",
        "encrypt",
        "locker",
        "crypt"
    ]

    try:

        for process in psutil.process_iter(
            ["pid", "name"]
        ):

            try:

                process_name = (
                    process.info["name"] or ""
                ).lower()

                for keyword in suspicious_keywords:

                    if keyword in process_name:

                        suspicious.append({
                            "pid": process.info["pid"],
                            "name": process.info["name"],
                            "reason": (
                                f"Suspicious keyword detected: {keyword}"
                            ),
                            "severity": "HIGH"
                        })

                        break

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                continue

    except Exception as error:

        print("[ERROR] Process Monitor:", error)

    return jsonify({
        "processes": suspicious
    })


# ==========================================
# API: ENTROPY STATUS
# ==========================================

@app.route("/api/entropy-status", methods=["GET"])
def entropy_status():

    entropy_file = AGENT_DIR / "entropy_status.json"

    if entropy_file.exists():

        try:

            with open(
                entropy_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            return jsonify(data)

        except Exception as error:

            print(
                "[ERROR] Entropy Status:",
                error
            )

    return jsonify({
        "status": "WAITING",
        "entropy": None,
        "threshold": 7.5,
        "suspicious": False,
        "analyzed_at": None,
        "file": None
    })


# ==========================================
# API: RISK SCORE ENGINE
# ==========================================

@app.route("/api/risk-score", methods=["GET"])
def risk_score():

    try:

        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM alerts
            ORDER BY id DESC
            LIMIT 10
        """)

        recent_alerts = cursor.fetchall()
        connection.close()

        trap_triggered = False

        for alert in recent_alerts:

            detector = (
                alert["detector"] or ""
            ).lower()

            if (
                "trap" in detector
                or "attack simulation" in detector
            ):
                trap_triggered = True
                break


        entropy_file = AGENT_DIR / "entropy_status.json"
        high_entropy = False

        if entropy_file.exists():

            try:

                with open(
                    entropy_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    entropy_data = json.load(file)

                high_entropy = entropy_data.get(
                    "suspicious",
                    False
                )

            except Exception as error:

                print(
                    "[WARNING] Entropy read error:",
                    error
                )


        suspicious_count = 0

        suspicious_keywords = [
            "ransom",
            "encrypt",
            "locker",
            "crypt"
        ]

        for process in psutil.process_iter(["name"]):

            try:

                process_name = (
                    process.info["name"] or ""
                ).lower()

                if any(
                    keyword in process_name
                    for keyword in suspicious_keywords
                ):
                    suspicious_count += 1

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                continue


        result = calculate_risk(
            trap_triggered=trap_triggered,
            high_entropy=high_entropy,
            suspicious_processes=suspicious_count
        )

        return jsonify(result)


    except Exception as error:

        print("[ERROR] Risk Engine:", error)

        return jsonify({
            "risk_score": 0,
            "severity": "UNKNOWN",
            "recommended_action": "ERROR",
            "signals": [],
            "error": str(error)
        }), 500


# ==========================================
# API: SAFE ATTACK SIMULATION
# ==========================================

@app.route("/api/simulate-attack", methods=["POST"])
def simulate_attack():

    try:

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
            INSERT INTO alerts (
                timestamp,
                severity,
                detector,
                process_pid,
                process_name,
                status,
                action
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            "CRITICAL",
            "Attack Simulation",
            9999,
            "demo_simulation.exe",
            "CONTAINED",
            "Simulated ransomware activity detected and safely contained"
        ))

        connection.commit()
        connection.close()

        print(
            "[SIMULATION] Attack simulation completed safely."
        )

        return jsonify({
            "success": True,
            "message": "Simulated attack detected and safely contained"
        })

    except Exception as error:

        print("[ERROR] Simulation:", error)

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ==========================================
# API: THREAT RESPONSE CENTER
# ==========================================

@app.route("/api/threat-response", methods=["GET"])
def threat_response():

    try:

        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM alerts
            ORDER BY id DESC
            LIMIT 1
        """)

        latest_alert = cursor.fetchone()
        connection.close()

        response = {
            "status": "MONITORING",
            "threat_detected": False,
            "recommended_action": "SYSTEM NORMAL",
            "response_action": "NO ACTION REQUIRED",
            "latest_threat": None
        }

        if latest_alert:

            severity = (
                latest_alert["severity"] or "LOW"
            )

            detector = (
                latest_alert["detector"] or "Unknown"
            )

            alert_status = (
                latest_alert["status"] or "UNKNOWN"
            )

            if severity.upper() == "CRITICAL":

                response = {
                    "status": "THREAT CONTAINED",
                    "threat_detected": True,
                    "recommended_action": (
                        "ISOLATE AND INVESTIGATE"
                    ),
                    "response_action": (
                        "AUTOMATIC CONTAINMENT ACTIVATED"
                    ),
                    "latest_threat": {
                        "severity": severity,
                        "detector": detector,
                        "status": alert_status,
                        "timestamp": latest_alert["timestamp"]
                    }
                }

            elif severity.upper() == "HIGH":

                response = {
                    "status": "HIGH RISK DETECTED",
                    "threat_detected": True,
                    "recommended_action": (
                        "INVESTIGATE IMMEDIATELY"
                    ),
                    "response_action": (
                        "MONITORING SUSPICIOUS ACTIVITY"
                    ),
                    "latest_threat": {
                        "severity": severity,
                        "detector": detector,
                        "status": alert_status,
                        "timestamp": latest_alert["timestamp"]
                    }
                }

        return jsonify(response)

    except Exception as error:

        print("[ERROR] Threat Response:", error)

        return jsonify({
            "status": "ERROR",
            "threat_detected": False,
            "recommended_action": "CHECK BACKEND",
            "response_action": "FAILED"
        }), 500


# ==========================================
# API: MANUAL THREAT CONTAINMENT
# ==========================================

@app.route("/api/contain-threat", methods=["POST"])
def contain_threat():

    try:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO alerts (
                timestamp,
                severity,
                detector,
                process_pid,
                process_name,
                status,
                action
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            "CRITICAL",
            "Manual Threat Response",
            0,
            "User Initiated",
            "CONTAINED",
            "Manual containment action activated"
        ))

        connection.commit()
        connection.close()

        print(
            "[RESPONSE] Manual containment activated."
        )

        return jsonify({
            "success": True,
            "message": "Threat containment action completed"
        })

    except Exception as error:

        print("[ERROR] Containment:", error)

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# ==========================================
# API: THREAT ACTIVITY TIMELINE
# ==========================================

@app.route("/api/threat-timeline", methods=["GET"])
def threat_timeline():

    try:

        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Latest 10 security events
        cursor.execute("""
            SELECT
                id,
                timestamp,
                severity,
                detector,
                status,
                action,
                process_name
            FROM alerts
            ORDER BY id DESC
            LIMIT 10
        """)

        rows = cursor.fetchall()
        connection.close()

        timeline = []

        # Reverse so oldest -> newest
        for row in reversed(rows):

            event = {
                "id": row["id"],
                "timestamp": row["timestamp"],
                "severity": row["severity"],
                "title": row["detector"],
                "status": row["status"],
                "action": row["action"],
                "process": row["process_name"]
            }

            timeline.append(event)


        return jsonify({
            "total_events": len(timeline),
            "events": timeline,
            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        })

    except Exception as error:

        print("[ERROR] Threat Timeline:", error)

        return jsonify({
            "total_events": 0,
            "events": [],
            "error": str(error)
        }), 500


# ==========================================
# API: SYSTEM STATUS
# ==========================================

@app.route("/api/status", methods=["GET"])
def system_status():

    try:

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM alerts"
        )

        alert_count = cursor.fetchone()[0]
        connection.close()

        return jsonify({
            "system": "PROTECTED",
            "alerts": alert_count,
            "backend": "ACTIVE"
        })

    except Exception as error:

        return jsonify({
            "system": "UNKNOWN",
            "error": str(error)
        })


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    init_database()

    print("\n========================================")
    print("      RANSOMTRAP BACKEND STARTED")
    print("========================================")
    print("Backend URL: http://127.0.0.1:5000")
    print("Dashboard API: ACTIVE")
    print("Risk Score Engine: ACTIVE")
    print("Threat Response Center: ACTIVE")
    print("Threat Activity Timeline: ACTIVE")
    print("Attack Simulation API: ACTIVE")
    print("========================================\n")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )