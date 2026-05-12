from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# ──────────────────────────────────────────
#  MONGODB CONNECTION
#  Ensure this matches your Thonny connection string!
# ──────────────────────────────────────────
try:
    # Use the 'Technogrowth' database name we fixed earlier
    MONGO_URI = "mongodb+srv://jadedahan1008:techno123@technogrowth06.2gabrww.mongodb.net/Technogrowth?retryWrites=true&w=majority"
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client['Technogrowth']
    collection = db['sensor_logs']
    print("Website Backend: Connected to MongoDB Atlas.")
except Exception as e:
    print(f"Website Backend Error: {e}")
    collection = None

# ──────────────────────────────────────────
#  REAL-TIME DATA FETCHING
# ──────────────────────────────────────────

def get_latest_sensor_data():
    if collection is None:
        return None
    try:
        # Fetch the single newest document based on the timestamp
        latest = collection.find().sort("timestamp", -1).limit(1)
        return list(latest)[0]
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
        # Convert MongoDB document to the format your frontend expects
        return jsonify({
            "timestamp":     data.get("timestamp"),
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
            "image": data.get("image", "latest_cabbage.jpg")
        })
    else:
        return jsonify({"error": "No data found in database"}), 404

# Keep your other mock routes (api_growth, api_devices, etc.) below this
