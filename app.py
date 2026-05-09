#  TechnoGrowth · Flask Backend (app.py)
#  Matches the front-end design by Lyka Jane Hidalgo
# ══════════════════════════════════════════════════════

from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# --- HELPER FUNCTION TO READ REAL DATA ---
def get_latest_sensor_data():
    """Reads the JSON file created by the hardware script."""
    try:
        # Assumes sensor_data.json is in the same folder as app.py
        with open("sensor_data.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback if the hardware script hasn't created the file yet
        return {
            "temp": 0.0, "hum": 0.0, "moisture": 0.0,
            "n": 0, "p": 0, "k": 0, "timestamp": "Waiting..."
        }

# ──────────────────────────────────────────
#  REAL SENSOR FUNCTIONS
# ──────────────────────────────────────────

def read_temperature():
    data = get_latest_sensor_data()
    return data.get("temp", 0.0)

def read_humidity():
    data = get_latest_sensor_data()
    return data.get("hum", 0.0)

def read_soil_moisture():
    data = get_latest_sensor_data()
    return data.get("moisture", 0.0)

def read_npk():
    data = get_latest_sensor_data()
    return {
        "nitrogen": data.get("n", 0),
        "phosphorus": data.get("p", 0),
        "potassium": data.get("k", 0),
        "status": "NORMAL"
    }

# ──────────────────────────────────────────
#  MOCK DATA (KEEPING FOR UI DESIGN)
# ──────────────────────────────────────────

def get_growth_data():
    return {
        "day":          27,
        "harvest_day":  30,
        "days_left":    3,
        "stage":        "Late Vegetative",
        "health":       "Healthy",
        "growth_score": 88,
        "leaf_count":   12,
        "size_cm":      35,
        "growth_rate":  1.3,
    }

def get_device_status():
    return {
        "irrigation_pump": {"status": "OFF", "last_run": "2 hours ago", "total_today": "3.5 hrs"},
        "exhaust_fan":     {"status": "OFF", "last_run": "3 hours ago", "total_today": "1.2 hrs"},
        "humidifier":      {"status": "OFF", "last_run": "Never",       "total_today": "0 hrs"},
        "auto_mode":       True
    }

def get_alerts():
    return [
        {"type": "info",    "title": "Growth Milestone",           "desc": "Your Chinese cabbage has reached 12 leaves!",             "time": "5 hours ago"},
        {"type": "success", "title": "Optimal Conditions Achieved","desc": "All environmental parameters are within ideal ranges.",    "time": "1 day ago"},
    ]

# ──────────────────────────────────────────
#  ROUTES
# ──────────────────────────────────────────

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/sensors')
def api_sensors():
    # We use the timestamp from the hardware file to know exactly when sensors were last read
    data = get_latest_sensor_data()
    return jsonify({
        "timestamp":     data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "temperature":   read_temperature(),
        "humidity":      read_humidity(),
        "soil_moisture": read_soil_moisture(),
        "npk":           read_npk(),
    })

@app.route('/api/growth')
def api_growth():
    return jsonify(get_growth_data())

@app.route('/api/devices')
def api_devices():
    return jsonify(get_device_status())

@app.route('/api/alerts')
def api_alerts():
    return jsonify(get_alerts())

@app.route('/api/status')
def api_status():
    return jsonify({"status": "online", "version": "2.0.0"})

# ──────────────────────────────────────────
#  RUN
# ──────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 50)
    print("  TechnoGrowth · Chinese Cabbage Monitor")
    print("  http://127.0.0.1:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
