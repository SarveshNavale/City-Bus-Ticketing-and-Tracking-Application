from flask import Flask, render_template, send_from_directory
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#SAR1807",
    database="RotaryClub_Database"
)

@app.route('/')
def home():
    return render_template("play.html")

@app.route('/dino')
def dino():
    return render_template("dino-rush.html")

@app.route('/static/games/dino/<path:filename>')
def serve_dino_files(filename):
    return send_from_directory('static/games/dino', filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
