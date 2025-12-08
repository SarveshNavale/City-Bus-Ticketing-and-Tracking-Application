from flask import Flask, render_template, send_from_directory, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#SAR1807",
    database="RotaryClub_Database"
)

@app.route('/')
def home():
    return render_template("homepage.html")


@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/dino')
def dino():
    return render_template("dino-rush.html")

@app.route('/static/games/dino/<path:filename>')
def serve_dino_files(filename):
    return send_from_directory('static/games/dino', filename)

# ================== LOCATION UPDATE ROUTE ==================

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.get_json()

    user_id = data["user_id"]
    lat = data["latitude"]
    lon = data["longitude"]

    cursor = db.cursor()
    cursor.execute(
        "UPDATE cust_info SET latitude=%s, longitude=%s, last_seen=%s WHERE id=%s",
        (lat, lon, datetime.now(), user_id)
    )
    db.commit()
    cursor.close()

    return jsonify({"status": "success"})

# ================== GET LOCATION ROUTE ==================

@app.route('/get_location/<int:user_id>')
def get_location(user_id):
    cursor = db.cursor()
    cursor.execute("SELECT latitude, longitude FROM cust_info WHERE id=%s", (user_id,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        return jsonify({
            "latitude": float(row[0]),
            "longitude": float(row[1])
        })

    return jsonify({"error": "User not found"}), 404

# ================== RUN SERVER ==================

if __name__ == '__main__':      
    app.run(host="0.0.0.0", port=5000, debug=True)
