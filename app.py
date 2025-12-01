from flask import Flask, render_template, request, redirect, url_for, send_file
import mysql.connector
app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#SAR1807",
    database="RotaryClub_Database"
)