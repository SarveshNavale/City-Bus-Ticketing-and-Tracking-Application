from flask import Flask, render_template, request, redirect, url_for, send_file
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
    
    return render_template("homepage.html") # replace name of page here tht you are currently editing

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
