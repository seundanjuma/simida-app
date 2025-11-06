from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
STATUS_FILE = "doctor_status.json"


def read_status():
    """Read doctor statuses from file."""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}


def write_status(data):
    """Write doctor statuses to file."""
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/get_status", methods=["GET"])
def get_status():
    """Return all doctor statuses."""
    return jsonify(read_status())


@app.route("/update_status", methods=["POST"])
def update_status():
    """Update one doctor's status."""
    data = request.json
    doctor = data.get("doctor")
    status = data.get("status")

    if not doctor or not status:
        return jsonify({"error": "doctor and status required"}), 400

    current = read_status()
    current[doctor] = status
    write_status(current)
    return jsonify({"success": True})


if __name__ == "__main__":
    # Run the Flask server
    app.run(host="0.0.0.0", port=5000)
