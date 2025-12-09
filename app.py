from flask import Flask, render_template, send_from_directory
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="flaskuser",
    password="shreyash45",
    database="RotaryClub_Database"
)

@app.route('/')
def home():
    return render_template("buyPass.html")

@app.route('/dino')
def dino():
    return render_template("dino-rush.html")

@app.route('/static/games/dino/<path:filename>')
def serve_dino_files(filename):
    return send_from_directory('static/games/dino', filename)
  
@app.route('/view_ticket')
def view_ticket():
    return render_template("view_ticket.html",
        from_stop="Maruti Mandir",
        to_stop="Hathkhamba",
        total_tickets=5,
        holder_name="Shreyash Khot",
        ticket_number="TC8011192222",
        amount_paid=28.20,
        issue_datetime="11/11/2011 | 2:17 AM"
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
