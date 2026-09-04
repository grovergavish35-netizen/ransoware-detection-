from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import json
from pathlib import Path

from services.database import (
    initialize_database,
    get_connection,
    insert_sample_alert
)

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parents[2]

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Entropy status file path
ENTROPY_STATUS_PATH = BASE_DIR / "agent" / "entropy_status.json"


from agent.process_monitor import (
    get_process_count,
    detect_suspicious_processes
)

from agent.entropy_analyzer import analyze_file


app = Flask(__name__)
CORS(app)

# Create database tables when backend starts
initialize_database()


# Health API
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    })


# Get security alerts
@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM alerts
        ORDER BY id DESC
    """)

    alerts = [dict(row) for row in cursor.fetchall()]
    connection.close()

    return jsonify(alerts)


# Get trap files
@app.route("/api/traps", methods=["GET"])
def get_traps():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM traps
        ORDER BY id DESC
    """)

    traps = [dict(row) for row in cursor.fetchall()]
    connection.close()

    return jsonify(traps)


# Get real running process count
@app.route("/api/processes", methods=["GET"])
def get_processes():
    try:
        process_count = get_process_count()

        return jsonify({
            "count": process_count,
            "status": "active"
        })

    except Exception as error:
        return jsonify({
            "count": 0,
            "status": "error",
            "error": str(error)
        }), 500


# Detect suspicious processes
@app.route("/api/suspicious-processes", methods=["GET"])
def get_suspicious_processes():
    try:
        suspicious_processes = detect_suspicious_processes()

        return jsonify({
            "count": len(suspicious_processes),
            "processes": suspicious_processes
        })

    except Exception as error:
        return jsonify({
            "count": 0,
            "processes": [],
            "error": str(error)
        }), 500


# Analyze a file manually using entropy engine
@app.route("/api/entropy", methods=["POST"])
def analyze_entropy():
    try:
        data = request.get_json()

        if not data or "file_path" not in data:
            return jsonify({
                "error": "file_path is required"
            }), 400

        file_path = data["file_path"]

        result = analyze_file(file_path)

        return jsonify(result)

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


# Get latest entropy analysis result
@app.route("/api/entropy-status", methods=["GET"])
def get_entropy_status():
    try:

        # No analysis has happened yet
        if not ENTROPY_STATUS_PATH.exists():
            return jsonify({
                "status": "WAITING",
                "entropy": None,
                "file": None,
                "message": "No file analyzed yet"
            })

        # Read latest analysis
        with open(
            ENTROPY_STATUS_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            entropy_data = json.load(file)

        return jsonify(entropy_data)

    except Exception as error:
        return jsonify({
            "status": "ERROR",
            "error": str(error)
        }), 500


# Temporary endpoint to create test security alert
@app.route("/api/test-alert", methods=["POST"])
def create_test_alert():
    insert_sample_alert()

    return jsonify({
        "message": "Test alert created successfully"
    })


if __name__ == "__main__":
    print("RansomTrap Dashboard Backend starting...")
    print("Entropy Status API: ACTIVE")
    app.run(debug=True, port=5000)