from flask import Flask, render_template, jsonify, send_from_directory
from pymongo import MongoClient
import os
from datetime import datetime

app = Flask(__name__)

# ──────────────────────────────────────────
#  MONGODB CONNECTION
# ──────────────────────────────────────────
try:
    # Using the standard URI to avoid DNS issues on the Raspberry Pi
    MONGO_URI = "mongodb+srv://technogrowth:techno123@technogrowth06.2gabrww.mongodb.net/Technogrowth?retryWrites=true&w=majority"
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client['Technogrowth']
    collection = db['sensor_logs']
    # Test connection
    client.admin.command('ping')
    print("Website Backend: Connected to MongoDB Atlas.")
except Exception as e:
    print(f"Website Backend Error: {e}")
    collection = None

# ──────────────────────────────────────────
#  DATA FETCHING FUNCTIONS
# ──────────────────────────────────────────

def get_latest_sensor_data():
    if collection is None:
        return None
    try:
        # Fetch the single newest document based on the timestamp
        latest = collection.find().sort("timestamp", -1).limit(1)
        data_list = list(latest)
        return data_list[0] if data_list else None
    except Exception as e:
        print(f"Fetch Error: {e}")
        return None

# ──────────────────────────────────────────
#  ROUTES
# ──────────────────────────────────────────

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/sensors')
def api_sensors():
    data = get_latest_sensor_data()
    
    if data:
        # Map MongoDB keys to the format your frontend expects
        return jsonify({
            "timestamp":     data.get("timestamp").strftime("%Y-%m-%d %H:%M:%S") if isinstance(data.get("timestamp"), datetime) else data.get("timestamp"),
            "temperature":   data.get("temp", 0),
            "humidity":      data.get("hum", 0),
            "soil_moisture": data.get("moisture_avg", 0),
            "moisture_1":    data.get("moisture_1", 0),
            "moisture_2":    data.get("moisture_2", 0),
            "npk": {
                "nitrogen":   data.get("nitrogen", 0),
                "phosphorus": data.get("phosphorus", 0),
                "potassium":  data.get("potassium", 0),
                "status": "NORMAL"
            },
            "image_url": f"/growth_photos/{data.get('image', 'latest_cabbage.jpg')}"
        })
    else:
        return jsonify({"error": "No sensor data found"}), 404

# Route to serve photos from the Thonny directory
@app.route('/growth_photos/<filename>')
def serve_photo(filename):
    photo_path = '/home/technogrowth06/growth_photos'
    return send_from_directory(photo_path, filename)

# Mock routes for remaining dashboard elements
@app.route('/api/growth')
def api_growth():
    return jsonify({
        "day": 27, "harvest_day": 30, "days_left": 3,
        "stage": "Late Vegetative", "health": "Healthy"
    })

@app.route('/api/status')
def api_status():
    status = "online" if collection else "offline"
    return jsonify({"status": status, "version": "2.0.1"})

# ──────────────────────────────────────────
#  RUN
# ──────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 50)
    print("  TechnoGrowth Backend Launching...")
    print("  URL: http://0.0.0.0:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
