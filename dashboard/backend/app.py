from flask import Flask, jsonify
from flask_cors import CORS

from services.database import initialize_database, get_connection

app = Flask(__name__)
CORS(app)

# Create database tables when backend starts
initialize_database()


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    })


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



if __name__ == "__main__":
    print("RansomTrap Dashboard Backend starting...")
    app.run(debug=True, port=5000)



    
    