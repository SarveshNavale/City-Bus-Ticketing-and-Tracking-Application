from flask import Flask, render_template, send_from_directory, request, jsonify, redirect, session

from dotenv import load_dotenv
from groq import Groq
import json
import requests

from qr_utils import generate_pass_qr,  extract_pass_number_from_qr, generate_ticket_qr

import random
import string
import os
import mysql.connector
from datetime import datetime, date, time, timedelta
import time  # This is the time module for sleep()
import threading
from math import radians, sin, cos, sqrt, atan2

load_dotenv()

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",

        password="#SAR1807",

        database="RotaryClub_Database"
    )
 
 
# ---------- normal routes ----------
@app.route('/')
def home():
    return render_template("registration.html")

@app.route('/robo')
def robo():
    return render_template("robo.html")



@app.route('/view_c')
def view_c():
    return render_template("complaints.html")

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template("tc_login.html")

@app.route('/admin_dashboard_actual')
def admin_dashboard_actual():
    return render_template(admin_dashboard.html)

@app.route('/select')
def select():
    return render_template("select.html")

@app.route('/play')
def play():
    return render_template("play.html")

@app.route('/home')
def backtohome():
    return render_template("homepage.html")

@app.route('/admin_login')
def admin():
    return render_template("admin_login.html")

@app.route('/backtohome')
def backtohomee():
    return render_template("homepage.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/routestime')
def routestime():
    return render_template("Timetable.html")

@app.route('/dino')
def dino():
    return render_template("dino-rush.html")

@app.route('/notification')
def notification():
    return render_template("notification.html")

@app.route('/static/games/dino/<path:filename>')
def serve_dino_files(filename):
    return send_from_directory('static/games/dino', filename)

@app.route('/tc_login')
def tc_login():
    return render_template("tc_login.html")

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/customer_helpline')
def customer_helpline():
    return render_template('customer_helpline.html')

@app.route('/terms_conditions')
def terms_conditions():
    return render_template('terms_conditions.html')


@app.route('/devs_corner')
def devs_corner():
    return render_template('devs_corner.html')




         #buy pass

@app.route('/buy_pass')
def buy_pass_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
    current_login = cursor.fetchone()

    cursor.close()
    db.close()

    if not current_login:
        return redirect('/')

    return render_template("buyPass.html")
def generate_unique_pass_number(cursor):
    import random
    import string

    while True:
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        pass_number = f"PS{random_chars}"

        cursor.execute(
            "SELECT id FROM passes_info WHERE pass_number = %s",
            (pass_number,)
        )

        if not cursor.fetchone():
            return pass_number
        
@app.route('/purchase_pass', methods=['POST'])
def purchase_pass():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        # Get logged in user
        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()

        if not current_login:
            return jsonify({'success': False, 'error': 'No user logged in'})

        mobile_no = current_login['mobile_no']

        # Get user name
        cursor.execute(
            "SELECT cust_name FROM cust_info WHERE cust_number = %s",
            (mobile_no,)
        )
        user = cursor.fetchone()

        if not user:
            return jsonify({'success': False, 'error': 'User not found'})

        # Get request data
        data = request.json or {}

        quantity = int(data.get('quantity', 1))
        amount_per_pass = float(data.get('amount_per_pass', 30.00))
        service_fee = float(data.get('service_fee', 0.50))

        #  Only limit per purchase (max 5)
        if quantity > 5:
            return jsonify({
                'success': False,
                'error': 'Maximum 5 passes allowed at a time'
            })

        current_date = datetime.now().date()
        current_time = datetime.now().time()

        passes_created = []

        for i in range(quantity):

            pass_number = generate_unique_pass_number(cursor)

            cursor.execute("""
                INSERT INTO passes_info
                (pass_holder, pass_number, amount_paid, mobile_no, issue_date, issue_time)
                VALUES (%s,%s,%s,%s,%s,%s)
            """,(
                user['cust_name'],
                pass_number,
                amount_per_pass,
                mobile_no,
                current_date,
                current_time
            ))

            passes_created.append(pass_number)

        db.commit()
   
        cursor.close()
        db.close()

        return jsonify({
            'success': True,
            'message': f'{quantity} pass purchased successfully',
            'pass_numbers': passes_created
        })

    except Exception as e:
        print("Pass purchase error:", e)
        return jsonify({
            'success': False,
            'error': str(e)
        })
        
@app.route('/view_pass')
def view_pass():

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()

        if not current_login:
            return redirect('/')

        mobile_no = current_login['mobile_no']

        cursor.execute(
            "SELECT cust_name FROM cust_info WHERE cust_number = %s",
            (mobile_no,)
        )
        user = cursor.fetchone()

        # latest purchase time
        cursor.execute("""
        SELECT issue_time
        FROM passes_info
        WHERE mobile_no = %s
        ORDER BY id DESC
        LIMIT 1
        """,(mobile_no,))

        latest = cursor.fetchone()

        if not latest:
            return render_template(
                "view_pass.html",
                holder_name=user['cust_name'],
                total_tickets=0,
                amount_paid=0,
                no_pass=True
            )

        latest_time = latest['issue_time']

        # fetch only latest purchase passes
        cursor.execute("""
        SELECT *
        FROM passes_info
        WHERE mobile_no = %s
        AND issue_time = %s
        """,(mobile_no,latest_time))

        passes = cursor.fetchall()

        cursor.close()
        db.close()

        total_tickets = len(passes)
        amount_paid = total_tickets * 30.50

        return render_template(
            "view_pass.html",
            passes=passes,
            holder_name=user['cust_name'],
            total_tickets=total_tickets,
            amount_paid=amount_paid,
            actual_user=True
        )

    except Exception as e:
        print("View pass error:", e)
        return "Error loading pass"
    
@app.route('/generate_pass_qr/<pass_number>')
def generate_pass_qr_route(pass_number):
    """Generate QR code for a specific pass"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT pass_number, pass_holder, mobile_no, amount_paid, issue_date, issue_time 
            FROM passes_info 
            WHERE pass_number = %s
        """, (pass_number,))
        
        pass_data = cursor.fetchone()
        cursor.close()
        db.close()
        
        if not pass_data:
            return jsonify({'success': False, 'error': 'Pass not found'})
        
        pass_data['amount_paid'] = float(pass_data['amount_paid'])
        pass_data['issue_date'] = str(pass_data['issue_date'])
        pass_data['issue_time'] = str(pass_data['issue_time'])
        
        qr_image = generate_pass_qr(pass_data)
        
        return jsonify({
            'success': True,
            'qr_image': qr_image,
            'pass_data': pass_data
        })
        
    except Exception as e:
        print(f"QR generation error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/verify_pass', methods=['POST'])
def verify_pass():
    """Verify a pass number (existing) or QR code data"""
    try:
        data = request.get_json()
        pass_number = data.get('pass_number', '').strip().upper()
        
        if not pass_number:
            return jsonify({'success': False, 'error': 'Pass number required'})
        
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM passes_info 
            WHERE pass_number = %s
        """, (pass_number,))
        
        pass_data = cursor.fetchone()
        cursor.close()
        db.close()
        
        if pass_data:
            pass_data['issue_date'] = str(pass_data['issue_date'])
            pass_data['issue_time'] = str(pass_data['issue_time'])
            pass_data['amount_paid'] = float(pass_data['amount_paid'])
            
            return jsonify({
                'success': True,
                'found': True,
                'pass': pass_data
            })
        else:
            return jsonify({
                'success': True,
                'found': False
            })
            
    except Exception as e:
        print(f"Verify pass error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/verify_pass_qr', methods=['POST'])
def verify_pass_qr():
    """Verify pass from QR code scan data"""
    try:
        data = request.get_json()
        qr_data = data.get('qr_data', '')
        
        try:
            qr_json = json.loads(qr_data)
            pass_number = qr_json.get('pn')
        except:
            pass_number = qr_data
        
        if not pass_number:
            return jsonify({'success': False, 'error': 'Invalid QR code'})
        
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM passes_info 
            WHERE pass_number = %s
        """, (pass_number,))
        
        pass_data = cursor.fetchone()
        cursor.close()
        db.close()
        
        if pass_data:
            pass_data['issue_date'] = str(pass_data['issue_date'])
            pass_data['issue_time'] = str(pass_data['issue_time'])
            pass_data['amount_paid'] = float(pass_data['amount_paid'])
            
            return jsonify({
                'success': True,
                'found': True,
                'pass': pass_data
            })
        else:
            return jsonify({
                'success': True,
                'found': False
            })
            
    except Exception as e:
        print(f"QR verify error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    
@app.route('/faqs')
def faqs():
    return render_template("FAQs.html")


@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.get_json()
    user_id = data["user_id"]
    lat = data["latitude"]
    lon = data["longitude"]

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE cust_info SET latitude=%s, longitude=%s, last_seen=%s WHERE id=%s",
        (lat, lon, datetime.now(), user_id)
    )
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"status": "success"})


@app.route('/get_location/<int:user_id>')
def get_location(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT latitude, longitude FROM cust_info WHERE id=%s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    db.close()

    if row and row[0] is not None:
        return jsonify({
            "latitude": float(row[0]),
            "longitude": float(row[1])
        })

    return jsonify({"error": "User not found"}), 404


@app.route('/get_buses')
def get_buses():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, bus_no, no_plate, route, latitude, longitude FROM bus_info")
    buses = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({"buses": buses})  


@app.route('/update_bus_location', methods=['POST'])
def update_bus_location():
    data = request.get_json()
    bus_id = data.get("bus_id")
    lat = data.get("latitude")
    lon = data.get("longitude")

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE bus_info SET latitude=%s, longitude=%s, last_seen=%s WHERE id=%s",
        (lat, lon, datetime.now(), bus_id)
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"status": "ok"})


# ── Registration ──────────────────────────────────────────────────────────────
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        name = data.get('name', '').strip()
        mobile = data.get('mobile', '').strip()
        age = data.get('age', '')
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        print(f"Registration attempt - Name: {name}, Mobile: {mobile}")

        if not all([name, mobile, age, email, password]):
            return jsonify({'success': False, 'error': 'All fields are required'})

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM cust_info WHERE cust_number = %s OR cust_email = %s",
                       (mobile, email))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            db.close()
            return jsonify({'success': False, 'error': 'User already exists with this mobile or email'})

        cursor.execute("""
            INSERT INTO cust_info (cust_name, cust_number, cust_age, cust_email, password) 
            VALUES (%s, %s, %s, %s, %s)
        """, (name, mobile, age, email, password))

        try:
            cursor.execute("SHOW TABLES LIKE 'current_login'")
            if not cursor.fetchone():
                cursor.execute("CREATE TABLE current_login (mobile_no VARCHAR(15) NOT NULL)")

            cursor.execute("DELETE FROM current_login")
            cursor.execute("INSERT INTO current_login (mobile_no) VALUES (%s)", (mobile,))
        except Exception as e:
            print(f"Warning: Could not update current_login: {e}")

        db.commit()
        cursor.close()
        db.close()

        print(f"User registered: {name}, Mobile: {mobile}")

        return jsonify({
            'success': True,
            'message': 'Registration successful!',
            'redirect': '/home'
        })

    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({
            'success': False,
            'error': f'Registration failed: {str(e)}'
        })


# ── Login ─────────────────────────────────────────────────────────────────────
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print("LOGIN START ==========")
        print(f"Login data: {data}")

        identifier = data.get('identifier', '').strip()
        password = data.get('password', '').strip()
        method = data.get('method', 'mobile')

        if not identifier or not password:
            return jsonify({'success': False, 'error': 'Mobile/Email and password required'})

        db = get_db()
        cursor = db.cursor(dictionary=True)

        if method == 'mobile':
            cursor.execute("SELECT * FROM cust_info WHERE cust_number = %s", (identifier,))
        else:
            cursor.execute("SELECT * FROM cust_info WHERE cust_email = %s", (identifier,))

        user = cursor.fetchone()

        if user:
            print(f"User found: {user.get('cust_name')}")

            if user.get('password') == password:
                print("Password correct")

                cursor.execute("DELETE FROM current_login")
                cursor.execute("INSERT INTO current_login (mobile_no) VALUES (%s)", (user['cust_number'],))
                db.commit()

                cursor.close()
                db.close()

                print("Login successful")
                return jsonify({
                    'success': True,
                    'message': 'Login successful!',
                    'redirect': '/home'
                })
            else:
                cursor.close()
                db.close()
                return jsonify({'success': False, 'error': 'Wrong password'})
        else:
            cursor.close()
            db.close()
            return jsonify({'success': False, 'error': 'User not found'})

    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/get_current_user')
def get_current_user():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
            current_login = cursor.fetchone()
            column_name = 'mobile_no'
        except:
            cursor.execute("SELECT mobo_no FROM current_login LIMIT 1")
            current_login = cursor.fetchone()
            column_name = 'mobo_no'

        if not current_login:
            cursor.close()
            db.close()
            return jsonify({
                'success': False,
                'error': 'No user logged in',
                'logged_in': False
            })

        mobile_in_login = current_login['mobile_no']

        cursor.execute("SELECT * FROM cust_info WHERE cust_number = %s", (mobile_in_login,))
        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:
            return jsonify({
                'success': True,
                'logged_in': True,
                'user': {
                    'name': user['cust_name'],
                    'mobile': user['cust_number'],
                    'age': user['cust_age'],
                    'email': user['cust_email']
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': f'User not found in cust_info',
                'logged_in': False
            })

    except Exception as e:
        print(f"get_current_user error: {e}")
        return jsonify({'success': False, 'error': str(e), 'logged_in': False})


@app.route('/clear_login', methods=['POST'])
def clear_login():
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(*) as count FROM current_login")
        count = cursor.fetchone()[0]

        if count > 0:
            cursor.execute("DELETE FROM current_login")
            db.commit()
            cursor.close()
            db.close()
            return jsonify({'success': True, 'cleared': True})
        else:
            cursor.close()
            db.close()
            return jsonify({'success': True, 'cleared': False})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/test_direct_db')
def test_direct_db():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM current_login")
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return f"<h1>Direct DB Test</h1><p>Rows in current_login: {len(result)}</p><pre>{result}</pre><p>Time: {datetime.now()}</p>"
    except Exception as e:
        return f"Error: {str(e)}"


# ── Haversine ─────────────────────────────────────────────────────────────────
def haversine_distance(lat1, lon1, lat2, lon2):
    try:
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)

        lat1, lon1, lat2, lon2 = radians(lat1), radians(lon1), radians(lat2), radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        R = 6371
        return R * c

    except Exception as e:
        print(f"Distance calculation error: {e}")
        return float('inf')

#Notification background service
def check_bus_proximity():
    db = None
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()

        if not current_login:
            print("No user logged in")
            return

        mobile_no = current_login['mobile_no']
        print(f"\n{'='*50}")
        print(f"Checking proximity for user: {mobile_no}")

        cursor.execute("""
            SELECT cust_number, latitude, longitude 
            FROM cust_info 
            WHERE cust_number = %s 
            AND latitude IS NOT NULL 
            AND longitude IS NOT NULL
        """, (mobile_no,))

        user = cursor.fetchone()

        if not user:
            print(f"User {mobile_no} has no location data")
            return
        
        print(f"User location: {user['latitude']}, {user['longitude']}")

        cursor.execute("""
            SELECT final_dest FROM tickets_info 
            WHERE mobile_no = %s 
            ORDER BY issue_date DESC, issue_time DESC 
            LIMIT 1
        """, (mobile_no,))
        
        ticket = cursor.fetchone()
        
        if not ticket:
            print(f"User {mobile_no} has no recent tickets")
            return
            
        final_destination = ticket['final_dest']
        print(f"User's destination: {final_destination}")
        
        route_number = None
        
        cursor.execute("""
            SELECT track_no FROM stops_info 
            WHERE stop_name LIKE %s 
            LIMIT 1
        """, (f'%{final_destination}%',))
        
        stop = cursor.fetchone()
        
        if stop:
            route_number = stop['track_no']
            print(f"Route number for destination: {route_number}")
        else:
            print(f"Destination '{final_destination}' not found in stops_info")
            return
       
        now = datetime.now()
        current_date = now.date()
        current_time = now.time()
        
        cursor.execute("""
            SELECT COUNT(*) as total FROM bus_info 
            WHERE route = %s
        """, (route_number,))
        total_route_buses = cursor.fetchone()['total']
        print(f"Total buses on route {route_number}: {total_route_buses}")
        
        cursor.execute("""
            SELECT COUNT(*) as recent FROM bus_info 
            WHERE route = %s
            AND last_seen >= NOW() - INTERVAL 30 MINUTE
        """, (route_number,))
        recent_route_buses = cursor.fetchone()['recent']
        print(f"Buses on route {route_number} with recent location: {recent_route_buses}")
        
        cursor.execute("""
            SELECT bus_no, no_plate, latitude, longitude, last_seen 
            FROM bus_info 
            WHERE route = %s
            AND latitude IS NOT NULL 
            AND longitude IS NOT NULL
            AND last_seen >= NOW() - INTERVAL 30 MINUTE
        """, (route_number,))

        buses = cursor.fetchall()
        print(f"Found {len(buses)} active buses on route {route_number}")

        notifications_added = 0

        for bus in buses:
            distance = haversine_distance(
                user['latitude'], user['longitude'],
                bus['latitude'], bus['longitude']
            )

            print(f"Bus {bus['bus_no']} ({bus['no_plate']}) (Route {route_number}) is {distance:.2f}KM away")

            if distance <= 1.0:
                # to avoid duplicates
                cursor.execute("""
                    SELECT id FROM notification_info 
                    WHERE user_mobile = %s
                    AND notif_heading LIKE %s
                    AND notif_heading LIKE %s
                    AND notif_date = CURDATE()
                    AND notif_time >= NOW() - INTERVAL 30 MINUTE
                """, (mobile_no, f'%Bus {bus["bus_no"]}%', f'%{final_destination}%'))

                if not cursor.fetchone():
                    heading = f"Bus {bus['bus_no']} ({bus['no_plate']}) to {final_destination} nearby!"
                    description = f"Bus {bus['bus_no']} ({bus['no_plate']}) heading to {final_destination} is within {distance:.2f}KM of your location at {current_time.strftime('%I:%M %p')}."

                    cursor.execute("""
                        INSERT INTO notification_info 
                        (notif_date, notif_time, notif_heading, notif_description, user_mobile, notification_type, is_read)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (current_date, current_time, heading, description, mobile_no, 'bus_proximity', False))

                    db.commit()
                    notifications_added += 1
                    print(f"✅ NOTIFICATION ADDED: Bus {bus['bus_no']} ({bus['no_plate']})")

        if notifications_added > 0:
            print(f"Added {notifications_added} new notifications")
        else:
            print("No new notifications added")
            
        print(f"{'='*50}\n")

    except Exception as e:
        print(f"Error in check_bus_proximity: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if db:
            db.close()


def notification_worker():
    while True:
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking bus proximity...")
            with app.app_context():
                check_bus_proximity()
            time.sleep(30)
        except Exception as e:
            print(f"Worker error: {e}")
            time.sleep(60)


def start_notification_service():
    worker_thread = threading.Thread(target=notification_worker, daemon=True)
    worker_thread.start()
    print("=" * 50)
    print("🔔 NOTIFICATION SERVICE STARTED")
    print("=" * 50)


@app.route('/force_check_notifications')
def force_check_notifications():
    try:
        check_bus_proximity()
        return jsonify({'success': True, 'message': 'Notification check triggered'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/notifications')
def show_notifications():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()

        if not current_login:
            return redirect('/')

        mobile_no = current_login['mobile_no']
        print(f"Fetching notifications for user: {mobile_no}")

        cursor.execute("""
            UPDATE notification_info 
            SET is_read = TRUE 
            WHERE user_mobile = %s AND (is_read = FALSE OR is_read IS NULL)
        """, (mobile_no,))
        db.commit()
        print(f"Marked notifications as read for user {mobile_no}")

        cursor.execute("""
            SELECT * FROM notification_info 
            WHERE user_mobile = %s
            ORDER BY notif_date DESC, notif_time DESC
            LIMIT 50
        """, (mobile_no,))

        notifications = cursor.fetchall()
        print(f"Found {len(notifications)} notifications for user {mobile_no}")

        cursor.close()
        db.close()

        return render_template("simple_notifications.html", notifications=notifications)

    except Exception as e:
        print(f"Notification error: {e}")
        import traceback
        traceback.print_exc()
        return render_template("simple_notifications.html", notifications=[])

@app.route('/check_new_notifications')
def check_new_notifications():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()

        if not current_login:
            return jsonify({'success': False, 'new_notifications': False, 'count': 0})

        # Check for unread notifications (is_read = FALSE or NULL)
        cursor.execute("""
            SELECT COUNT(*) as new_count 
            FROM notification_info 
            WHERE user_mobile = %s
            AND (is_read = FALSE OR is_read IS NULL)
        """, (current_login['mobile_no'],))

        result = cursor.fetchone()
        cursor.close()
        db.close()

        has_new = result['new_count'] > 0
        print(f"User {current_login['mobile_no']} has {result['new_count']} unread notifications")

        return jsonify({
            'success': True,
            'new_notifications': has_new,
            'count': result['new_count']
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/update_user_location_from_map', methods=['POST'])
def update_user_location_from_map():
    try:
        data = request.get_json()
        lat = data.get('latitude')
        lon = data.get('longitude')

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()

        if current_login:
            mobile_no = current_login[0]
            cursor.execute("""
                UPDATE cust_info 
                SET latitude = %s, longitude = %s, last_seen = NOW()
                WHERE cust_number = %s
            """, (lat, lon, mobile_no))
            db.commit()

        cursor.close()
        db.close()

        return jsonify({'success': True})

    except Exception as e:
        print(f"Location update error: {e}")
        return jsonify({'success': False, 'error': str(e)})


# --------------- REAL TIME TRACKED DRIVER (from driver_location table) ---------------
@app.route('/get_driver_locations')
def get_driver_locations():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    # cursor.execute("SELECT driver_id, driver_name, latitude, longitude, no_plate FROM driver_location")  # uncomment after ALTER TABLE ADD COLUMN no_plate
    cursor.execute("SELECT driver_id, driver_name, latitude, longitude FROM driver_location")
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(rows)

@app.route('/test_add_notification')
def test_add_notification():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()

        if not current_login:
            return jsonify({'success': False, 'error': 'No user logged in'})

        now = datetime.now()

        cursor.execute("""
            INSERT INTO notification_info 
            (notif_date, notif_time, notif_heading, notif_description, user_mobile, notification_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (now.date(), now.time(),
              '🔔 Test Notification',
              'This is a test notification to verify the display works',
              current_login['mobile_no'], 'test'))

        db.commit()
        cursor.close()
        db.close()

        return jsonify({'success': True, 'message': 'Test notification added'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# ── Stops ─────────────────────────────────────────────────────────────────────
@app.route('/search_stops')
def search_stops():
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify({"success": False, "stops": []})

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT stop_name FROM stops_info WHERE stop_name LIKE %s LIMIT 10",
        ('%' + query + '%',)
    )
    results = cursor.fetchall()
    cursor.close()
    db.close()

    stops = [row[0] for row in results]
    return jsonify({"success": True, "stops": stops})


@app.route('/choose_destination')
def choose_destination():
    destination = request.args.get('destination')
    if not destination:
        return redirect('/home')
    return render_template("Afterchoosingdestinationpage.html", destination=destination)


@app.route('/buy_ticket')
def buy_ticket():
    destination = request.args.get('dest')
    tickets_count = int(request.args.get('count', 1))

    if tickets_count > 5:
        tickets_count = 5

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
    current = cursor.fetchone()

    if not current:
        return redirect('/')

    mobile_no = current['mobile_no']

    cursor.execute("SELECT * FROM cust_info WHERE cust_number=%s", (mobile_no,))
    user = cursor.fetchone()

    if not user:
        return redirect('/home')

    cursor.execute("SELECT * FROM stops_info ORDER BY id")
    stops = cursor.fetchall()

    from_index = 0
    to_index = 0

    for i, stop in enumerate(stops):
        if stop['stop_name'] == destination:
            to_index = i

    stops_travelled = abs(to_index - from_index)
    price_per_ticket = stops_travelled * 2.5
    total_price = price_per_ticket * tickets_count

    cursor.close()
    db.close()

    return render_template(
        "confirm_ticket.html",
        from_stop=stops[from_index]['stop_name'],
        to_stop=destination,
        stops_travelled=stops_travelled,
        tickets_count=tickets_count,
        total_price=total_price
    )


@app.route('/pay_ticket', methods=['POST'])
def pay_ticket():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
    current = cursor.fetchone()

    if not current:
        return jsonify({"success": False})

    mobile_no = current['mobile_no']

    cursor.execute("SELECT id FROM cust_info WHERE cust_number=%s", (mobile_no,))
    user = cursor.fetchone()
    cust_id = user['id']

    data = request.get_json()
    from_stop = data['from_stop']
    to_stop = data['to_stop']
    stops_travelled = data['stops_travelled']
    tickets_count = data['tickets_count']
    total_price = data['total_price']

    ticket_number = "TC" + mobile_no

    cursor.execute("""
        INSERT INTO ticket_info 
        (ticket_number, cust_id, from_stop, to_stop, stops_travelled, tickets_count, amount_paid, issue_datetime)
        VALUES (%s,%s,%s,%s,%s,%s,%s,NOW())
    """, (ticket_number, cust_id, from_stop, to_stop, stops_travelled, tickets_count, total_price))

    db.commit()
    cursor.close()
    db.close()

    return jsonify({
        "success": True,
        "message": "Payment Successful",
        "ticket_number": ticket_number
    })


@app.route('/complaints')
def complaint():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM complaint")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("Complaint page.html", complaint=data)

@app.route('/save_ticket', methods=['POST'])
def save_ticket():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()

        if not current_login:
            return jsonify({'success': False, 'error': 'No user logged in'})

        mobile_no = current_login['mobile_no']

        cursor.execute("SELECT cust_name FROM cust_info WHERE cust_number = %s", (mobile_no,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'success': False, 'error': 'User not found'})

        data = request.get_json()
        start_dest = data.get('start_dest', 'Current Location')
        final_dest = data.get('final_dest')
        no_of_tickets = int(data.get('no_of_tickets', 1))
        amount_paid = float(data.get('amount_paid', 0))

        if not final_dest:
            return jsonify({'success': False, 'error': 'Destination is required'})

        current_datetime = datetime.now()
        timestamp = int(current_datetime.timestamp())
        ticket_number = f"TC{mobile_no}_{timestamp}"

        cursor.execute("""
            INSERT INTO tickets_info 
            (start_dest, final_dest, no_of_tickets, ticket_holder, mobile_no, ticket_number, amount_paid, issue_date, issue_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            start_dest,
            final_dest,
            no_of_tickets,
            user['cust_name'],
            mobile_no,
            ticket_number,
            amount_paid,
            current_datetime.date(),
            current_datetime.time()
        ))

        db.commit()
        
        ticket_id = cursor.lastrowid
        
        ticket_data = {
            'ticket_number': ticket_number,
            'ticket_holder': user['cust_name'],
            'mobile_no': mobile_no,
            'amount_paid': amount_paid,
            'start_dest': start_dest,
            'final_dest': final_dest,
            'issue_date': str(current_datetime.date()),
            'issue_time': str(current_datetime.time())
        }
        
        qr_image = generate_ticket_qr(ticket_data)
        
        try:
            cursor.execute("""
                UPDATE tickets_info SET qr_code = %s WHERE id = %s
            """, (qr_image, ticket_id))
            db.commit()
        except Exception as qr_error:
            print(f"Could not store QR code: {qr_error}")
        
        cursor.close()
        db.close()

        print(f"Ticket saved: {ticket_number} | {start_dest} -> {final_dest} | {user['cust_name']}")

        return jsonify({
            'success': True,
            'ticket_number': ticket_number,
            'message': 'Ticket saved successfully'
        })

    except Exception as e:
        print(f"Save ticket error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/generate_ticket_qr/<ticket_number>')
def generate_ticket_qr_route(ticket_number):
    """Generate QR code for a specific ticket"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT ticket_number, ticket_holder, mobile_no, amount_paid, start_dest, final_dest, issue_date, issue_time 
            FROM tickets_info 
            WHERE ticket_number = %s
        """, (ticket_number,))
        
        ticket_data = cursor.fetchone()
        cursor.close()
        db.close()
        
        if not ticket_data:
            return jsonify({'success': False, 'error': 'Ticket not found'})
        
        ticket_data['amount_paid'] = float(ticket_data['amount_paid'])
        ticket_data['issue_date'] = str(ticket_data['issue_date'])
        ticket_data['issue_time'] = str(ticket_data['issue_time'])
        
        qr_image = generate_ticket_qr(ticket_data)
        
        return jsonify({
            'success': True,
            'qr_image': qr_image,
            'ticket_data': ticket_data
        })
        
    except Exception as e:
        print(f"Ticket QR generation error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    
@app.route('/verify_ticket', methods=['POST'])
def verify_ticket():
    """Verify a ticket number"""
    try:
        data = request.get_json()
        ticket_number = data.get('ticket_number', '').strip()
        
        if not ticket_number:
            return jsonify({'success': False, 'error': 'Ticket number required'})
        
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM tickets_info 
            WHERE ticket_number = %s
        """, (ticket_number,))
        
        ticket_data = cursor.fetchone()
        cursor.close()
        db.close()
        
        if ticket_data:
            ticket_data['issue_date'] = str(ticket_data['issue_date'])
            ticket_data['issue_time'] = str(ticket_data['issue_time'])
            ticket_data['amount_paid'] = float(ticket_data['amount_paid'])
            
            return jsonify({
                'success': True,
                'found': True,
                'ticket': ticket_data
            })
        else:
            return jsonify({
                'success': True,
                'found': False
            })
            
    except Exception as e:
        print(f"Verify ticket error: {e}")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/verify_ticket_qr', methods=['POST'])
def verify_ticket_qr():
    """Verify ticket from QR code scan data"""
    try:
        data = request.get_json()
        qr_data = data.get('qr_data', '')
        
        try:
            qr_json = json.loads(qr_data)
            ticket_number = qr_json.get('tn') or qr_json.get('ticket_number')
        except:
            ticket_number = qr_data
        
        if not ticket_number:
            return jsonify({'success': False, 'error': 'Invalid QR code'})
        
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM tickets_info 
            WHERE ticket_number = %s
        """, (ticket_number,))
        
        ticket_data = cursor.fetchone()
        cursor.close()
        db.close()
        
        if ticket_data:
            ticket_data['issue_date'] = str(ticket_data['issue_date'])
            ticket_data['issue_time'] = str(ticket_data['issue_time'])
            ticket_data['amount_paid'] = float(ticket_data['amount_paid'])
            
            return jsonify({
                'success': True,
                'found': True,
                'ticket': ticket_data
            })
        else:
            return jsonify({
                'success': True,
                'found': False
            })
            
    except Exception as e:
        print(f"Ticket QR verify error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    
@app.route('/admin_login', methods=['POST'])
def admin_login():
    username = request.form.get('admin_id')
    password = request.form.get('password')

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admin_info WHERE admin_username=%s", (username,))
    admin = cursor.fetchone()
    cursor.close()
    db.close()

    if admin and admin['admin_password'] == password:
        return redirect('/select')
    else:
        return "Invalid admin login ❌"


@app.route('/admin_login', methods=['GET'])
def admin_login_page():
    return render_template("admin_login.html")

@app.route('/view_ticket')
def view_ticket():
    return render_template("view_ticket.html")

@app.route('/get_all_tickets')
def get_all_tickets():
    """API: Returns ALL tickets of the currently logged-in user from tickets_info"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()

        if not current_login:
            cursor.close()
            db.close()
            return jsonify({'success': False, 'error': 'No user logged in'})

        mobile_no = current_login['mobile_no']

        cursor.execute("""
            SELECT * FROM tickets_info
            WHERE mobile_no = %s
            ORDER BY issue_date DESC, issue_time DESC
        """, (mobile_no,))
        tickets = cursor.fetchall()

        cursor.close()
        db.close()

        serialized = []
        for t in tickets:
            serialized.append({
                'id':            t['id'],
                'start_dest':    t['start_dest'],
                'final_dest':    t['final_dest'],
                'no_of_tickets': t['no_of_tickets'],
                'ticket_holder': t['ticket_holder'],
                'mobile_no':     t['mobile_no'],
                'ticket_number': t['ticket_number'],
                'amount_paid':   float(t['amount_paid']),
                'issue_date':    str(t['issue_date']),
                'issue_time':    str(t['issue_time']),
            })

        return jsonify({'success': True, 'tickets': serialized})

    except Exception as e:
        print(f"get_all_tickets error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})


# ─────────────────────────────────────────────────────────────────────────────
# GET USER LOCATION — reads lat/lon from cust_info for logged-in user
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/get_user_location')
def get_user_location():
    """API: Returns lat/lon of the currently logged-in user from cust_info"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()

        if not current_login:
            cursor.close()
            db.close()
            return jsonify({'success': False, 'error': 'No user logged in'})

        mobile_no = current_login['mobile_no']

        cursor.execute("""
            SELECT latitude, longitude
            FROM cust_info
            WHERE cust_number = %s
            LIMIT 1
        """, (mobile_no,))
        user = cursor.fetchone()

        cursor.close()
        db.close()

        if not user or user['latitude'] is None:
            return jsonify({'success': False, 'error': 'No location data for this user'})

        return jsonify({
            'success':   True,
            'latitude':  float(user['latitude']),
            'longitude': float(user['longitude']),
        })

    except Exception as e:
        print(f"get_user_location error: {e}")
        return jsonify({'success': False, 'error': str(e)})


# ─────────────────────────────────────────────────────────────────────────────
# GET STOP COORDS — returns lat/lon of a stop by name
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/get_stop_coords')
def get_stop_coords():
    """API: Returns lat/lon of a stop by name"""
    stop_name = request.args.get('stop_name', '').strip()

    if not stop_name:
        return jsonify({'success': False, 'error': 'stop_name is required'})

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT latitude, longitude
            FROM stops_info
            WHERE stop_name = %s
            LIMIT 1
        """, (stop_name,))

        stop = cursor.fetchone()
        cursor.close()
        db.close()

        if not stop:
            return jsonify({'success': False, 'error': f'Stop "{stop_name}" not found'})

        return jsonify({
            'success':   True,
            'latitude':  float(stop['latitude']),
            'longitude': float(stop['longitude']),
        })

    except Exception as e:
        print(f"get_stop_coords error: {e}")
        return jsonify({'success': False, 'error': str(e)})


# ─────────────────────────────────────────────────────────────────────────────
# DELETE TICKET BY ID — deletes a specific ticket only if it belongs to current user
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
def delete_ticket(ticket_id):
    """
    API: Deletes a SPECIFIC ticket by its id — only if it belongs to the
    currently logged-in user. Called by JS after the 1-minute arrival
    proximity timer fires on view_ticket.html.
    """
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()

        if not current_login:
            cursor.close()
            db.close()
            return jsonify({'success': False, 'error': 'No user logged in'})

        mobile_no = current_login['mobile_no']

        # Verify the ticket belongs to this user
        cursor.execute("""
            SELECT id FROM tickets_info
            WHERE id = %s AND mobile_no = %s
        """, (ticket_id, mobile_no))
        ticket = cursor.fetchone()

        if not ticket:
            cursor.close()
            db.close()
            return jsonify({'success': False, 'error': 'Ticket not found or does not belong to this user'})

        # Delete only that specific row
        cursor.execute(
            "DELETE FROM tickets_info WHERE id = %s AND mobile_no = %s",
            (ticket_id, mobile_no)
        )
        db.commit()

        print(f"✅ Ticket id={ticket_id} deleted for user {mobile_no} after arrival timeout")

        cursor.close()
        db.close()

        return jsonify({'success': True, 'deleted_ticket_id': ticket_id})

    except Exception as e:
        print(f"delete_ticket error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})


# ─────────────────────────────────────────────────────────────────────────────
# SHUTDOWN CLEANUP
# ─────────────────────────────────────────────────────────────────────────────
import atexit

def cleanup_on_shutdown():
    try:
        print("\n" + "=" * 50)
        print("SERVER SHUTTING DOWN - Clearing current_login table")
        db = get_db()
        cursor = db.cursor()
        cursor.execute("TRUNCATE TABLE current_login")
        db.commit()
        cursor.close()
        db.close()
        print("current_login table truncated successfully")
        print("=" * 50)
    except Exception as e:
        print(f"Error truncating current_login: {e}")

atexit.register(cleanup_on_shutdown)

# ─────────────────────────────────────────────────────────────────────────────
# START
# ─────────────────────────────────────────────────────────────────────────────
start_notification_service()

# GROQ_API_KEY = os.getenv('GROQ_API_KEY')
# if not GROQ_API_KEY:
#  raise ValueError("GROQ_API_KEY not found in .env file")


# groq_client = Groq(api_key=GROQ_API_KEY)



def get_database_context():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    context = ""
    
    try:     
        cursor.execute("SELECT bus_no, no_plate, route FROM bus_info")
        buses = cursor.fetchall()
        if buses:
            context += "\nBUSES:\n"
            route_names = {1: "Kokan", 2: "Highway", 3: "Nachane", 4: "Railway"}
            for b in buses:
                route = route_names.get(b['route'], 'Unknown')
                context += f"- Bus {b['bus_no']} ({b['no_plate']}) - Route: {route}\n"
        
        cursor.execute("SELECT stop_name, track_no FROM stops_info")
        stops = cursor.fetchall()
        if stops:
            context += "\nSTOPS:\n"
            for s in stops:
                context += f"- {s['stop_name']} (Track {s['track_no']})\n"
        
        cursor.execute("SELECT notif_heading, notif_date FROM notification_info ORDER BY notif_date DESC LIMIT 3")
        notifs = cursor.fetchall()
        if notifs:
            context += "\nRECENT NOTIFICATIONS:\n"
            for n in notifs:
                context += f"- {n['notif_heading']} ({n['notif_date']})\n"
    
    except Exception as e:
        print(f"DB context error: {e}")
    
    cursor.close()
    db.close()
    return context

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        db_context = get_database_context()
        
        system_prompt = f"""You are Tikko Robo, assistant for Rotary Club transport system.
        
Current database information:
{db_context}

IMPORTANT RULES:
- If users ask about bus timings or schedules, tell them: "Bus timetables are available in the Timetable section. You'll also get notified when your bus is nearby!"

Answer questions using this data. Be helpful and friendly."""

        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        response = completion.choices[0].message.content
        return jsonify({"response": response})
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({"response": f"Error: {str(e)}"})




#to store complaints 



@app.route("/add_complaint", methods=["POST"])
def add_complaint():

    data = request.get_json()
    text = data.get("complaint")

    conn = get_db()
    cursor = conn.cursor()

    now = datetime.now()

    cursor.execute("""
        INSERT INTO complaint (comp_text, comp_time, comp_date)
        VALUES (%s, %s, %s)
    """, (text, now.strftime("%H:%M:%S"), now.strftime("%Y-%m-%d")))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"success": True})


@app.route("/get_complaints")
def get_complaints():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM complaint")
    complaints = cursor.fetchall()

    # 🔥 Convert time and date to string
    for c in complaints:
        if c["comp_time"]:
            c["comp_time"] = str(c["comp_time"])
        if c["comp_date"]:
            c["comp_date"] = str(c["comp_date"])

    cursor.close()
    conn.close()

    return jsonify(complaints)


@app.route("/delete_complaint/<int:id>", methods=["DELETE"])
def delete_complaint(id):
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM complaint WHERE id = %s", (id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:
        print("Delete Error:", e)
        return jsonify({"success": False})




















def fetch_location():

    while True:

        try:

            response = requests.get("https://drivertracker-a4290-default-rtdb.firebaseio.com/location.json")

            data = response.json()

            lat = data["latitude"]
            lon = data["longitude"]

            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="#SAR1807",
                database="RotaryClub_Database"
            )

            cursor = db.cursor()

            sql = "UPDATE driver_location SET latitude=%s, longitude=%s WHERE driver_id=1"
            cursor.execute(sql,(lat,lon))

            db.commit()

            cursor.close()
            db.close()

        except Exception as e:
            print(e)

        time.sleep(5)

thread = threading.Thread(target=fetch_location)
thread.daemon = True
thread.start()






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


@app.route("/tourist")
def tourist():
    return render_template("tourist.html")
#task completed