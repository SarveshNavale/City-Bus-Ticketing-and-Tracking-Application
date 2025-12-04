from flask import Flask, render_template, request, redirect, url_for, send_file
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hrishi@123",
    database="RotaryClub_Database"
)

@app.route('/')
def home():
    
    return render_template("registration.html") # replace name of page here tht you are currently editing

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
