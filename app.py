from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'your-database-host',     # Replace with your database host URL
    'user': 'your-database-user',     # Replace with your database username
    'password': 'your-database-password',  # Replace with your database password
    'database': 'vehicle_tracking_db' # Replace with your database name
}

# Home route to render HTML dashboard
@app.route('/')
def index():
    return render_template('dashboard.html')

# Endpoint to receive location data from the Android app
@app.route('/location', methods=['POST'])
def location():
    data = request.json
    driver_id = data['driver_id']
    name = data['name']
    mobile = data['mobile']
    latitude = data['latitude']
    longitude = data['longitude']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO driver_location (driver_id, name, mobile, latitude, longitude, timestamp) VALUES (%s, %s, %s, %s, %s, %s)",
            (driver_id, name, mobile, latitude, longitude, timestamp)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Location saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
