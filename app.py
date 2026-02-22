from flask import Flask, render_template, send_from_directory, request, jsonify, redirect
import mysql.connector
from datetime import datetime, date, time, timedelta
import time  # This is the time module for sleep()
import threading
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="hrishi@123",
        database="RotaryClub_Database"
    )

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#shreyash45",
        database="RotaryClub_Database"
    )
# ---------- normal routes sagle hite taka! ----------
@app.route('/')
def home():
    return render_template("registration.html")

@app.route('/robo')
def robo():
    return render_template("robo.html")

@app.route('/play')
def play():
    return render_template("play.html")

@app.route('/home')
def backtohome():
    return render_template("homepage.html")

@app.route('/backtohome')
def backtohomee():
    return render_template("homepage.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/dino')
def dino():
    return render_template("dino-rush.html")

@app.route('/notification')
def notification():
    return render_template("notification.html")

@app.route('/admin_login')
def admin():
    return render_template("admin_login.html")


@app.route('/static/games/dino/<path:filename>')
def serve_dino_files(filename):
    return send_from_directory('static/games/dino', filename)
  
@app.route('/view_ticket')
def view_ticket():
    return render_template(
        "view_ticket.html",
        from_stop="Maruti Mandir",
        to_stop="Hathkhamba",
        total_tickets=5,
        holder_name="Shreyash Khot",
        ticket_number="TC8011192222",
        amount_paid=28.20,
        issue_datetime="11/11/2011 | 2:17 AM"
    )

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

@app.route('/purchase_pass', methods=['POST'])
def purchase_pass():
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
            return jsonify({'success': False, 'error': 'User not found in database'})
        
        data = request.get_json()
        quantity = int(data.get('quantity', 1))
        amount_per_pass = float(data.get('amount_per_pass', 30.00))
        service_fee = float(data.get('service_fee', 0.50))
        payment_method = data.get('payment_method', 'gpay')
        
        total_amount = (quantity * amount_per_pass) + (quantity * service_fee)
        
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        current_time = current_datetime.time()
        
        timestamp = int(current_datetime.timestamp())
        
        passes_created = []
        for i in range(quantity):
            pass_number = f"PS{mobile_no}_{timestamp}_{i+1}"
            
            cursor.execute("""
                INSERT INTO passes_info 
                (pass_holder, pass_number, amount_paid, mobile_no, issue_date, issue_time)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                user['cust_name'],
                pass_number,
                amount_per_pass,
                mobile_no,
                current_date,
                current_time
            ))
            
            passes_created.append(pass_number)
        
        db.commit()
        
        placeholders = ','.join(['%s'] * len(passes_created))
        cursor.execute(f"""
            SELECT * FROM passes_info 
            WHERE pass_number IN ({placeholders})
            ORDER BY id DESC
        """, tuple(passes_created))
        
        passes = cursor.fetchall()
        
        serialized_passes = []
        for pass_item in passes:
            if isinstance(pass_item.get('issue_time'), type(datetime.now().time())):
                issue_time_str = str(pass_item['issue_time'])
            else:
                issue_time_str = str(pass_item.get('issue_time', ''))
            
            if isinstance(pass_item.get('issue_date'), type(datetime.now().date())):
                issue_date_str = str(pass_item['issue_date'])
            else:
                issue_date_str = str(pass_item.get('issue_date', ''))
            
            serialized_passes.append({
                'id': pass_item['id'],
                'pass_holder': pass_item['pass_holder'],
                'pass_number': pass_item['pass_number'],
                'amount_paid': float(pass_item['amount_paid']),
                'mobile_no': pass_item['mobile_no'],
                'issue_date': issue_date_str,
                'issue_time': issue_time_str
            })
        
        cursor.close()
        db.close()
        
        return jsonify({
            'success': True,
            'message': f'Successfully purchased {quantity} pass(es)',
            'passes': serialized_passes,  
            'details': {
                'pass_holder': user['cust_name'],
                'mobile_no': mobile_no,
                'total_amount': total_amount,
                'pass_numbers': passes_created,
                'purchase_time': current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
        
    except Exception as e:
        print(f"Pass purchase error: {e}")
        import traceback
        traceback.print_exc() 
        return jsonify({
            'success': False,
            'error': f'Pass purchase failed: {str(e)}'
        })
@app.route('/view_pass')
def view_pass():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()
        
        if not current_login:
            cursor.close()
            db.close()
            return render_template(
                "view_pass.html",
                total_tickets=5,
                holder_name="Shreyash Khot",
                pass_number="PS8011192222",
                amount_paid=500,
                issue_datetime="11/11/2011 | 2:17 AM",
                actual_user=False
            )
        
        mobile_no = current_login['mobile_no']
        
        cursor.execute("""
            SELECT * FROM passes_info 
            WHERE mobile_no = %s 
            ORDER BY issue_date DESC, issue_time DESC 
            LIMIT 1
        """, (mobile_no,))
        
        pass_data = cursor.fetchone()
        
        cursor.execute("SELECT cust_name FROM cust_info WHERE cust_number = %s", (mobile_no,))
        user = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if pass_data and user:
            issue_date = pass_data['issue_date']
            issue_time = pass_data['issue_time']
            issue_datetime = f"{issue_date} | {issue_time}"
            
            return render_template(
                "view_pass.html",
                total_tickets=1, 
                holder_name=user['cust_name'],
                pass_number=pass_data['pass_number'],
                amount_paid=pass_data['amount_paid'],
                issue_datetime=issue_datetime,
                actual_user=True,
                mobile_no=mobile_no,
                pass_id=pass_data['id']
            )
        else:
            return render_template(
                "view_pass.html",
                total_tickets=0,
                holder_name=user['cust_name'] if user else "User",
                pass_number="No active pass",
                amount_paid=0,
                issue_datetime="N/A",
                actual_user=True,
                mobile_no=mobile_no,
                no_pass=True
            )
            
    except Exception as e:
        print(f"View pass error: {e}")
        return render_template(
            "view_pass.html",
            total_tickets=5,
            holder_name="Shreyash Khot",
            pass_number="PS8011192222",
            amount_paid=500,
            issue_datetime="11/11/2011 | 2:17 AM",
            actual_user=False,
            error=str(e)
        )
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
    return jsonify(buses)

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
      
 #admin_login data

import bcrypt
from flask import Flask, render_template, request, jsonify, redirect
import mysql.connector

@app.route('/admin_login', methods=['POST'])
def admin_login():

    username = request.form.get('admin_id')
    password = request.form.get('password')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM admin_info WHERE admin_username=%s",
        (username,)
    )
    admin = cursor.fetchone()

    cursor.close()
    db.close()

    if admin and bcrypt.checkpw(password.encode(), admin['admin_password'].encode()):
        return redirect('/admin_dashboard')
    else:
        return "Invalid admin login ❌"
    
@app.route('/admin_login', methods=['GET'])
def admin_login_page():
    return render_template("admin_login.html")
 
@app.route('/admin_dashboard')
def admin_dashboard():
    return "<h1>Welcome Admin ✅</h1>"




#registration data

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
        
        print(f"User registered: {name}, Mobile (cust_number): {mobile}")
        print(f"Stored in current_login: {mobile}")
        
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
    
    
# login function 
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
            print(f"   DB Password: {user.get('password')}")
            print(f"   Input Password: {password}")
            
            if user.get('password') == password:
                print("Password correct")
                
                cursor.execute("DELETE FROM current_login")
                cursor.execute("INSERT INTO current_login (mobile_no) VALUES (%s)", (user['cust_number'],))
                db.commit()
                
                cursor.execute("SELECT * FROM current_login")
                stored = cursor.fetchone()
                print(f"Stored in current_login: {stored}")
                
                cursor.close()
                db.close()
                
                print("Login successful, redirecting to /home")
                print("LOGIN END ==========")
                
                return jsonify({
                    'success': True,
                    'message': 'Login successful!',
                    'redirect': '/home'
                })
            else:
                cursor.close()
                db.close()
                print("Wrong password")
                return jsonify({'success': False, 'error': 'Wrong password'})
        else:
            cursor.close()
            db.close()
            print("User not found")
            return jsonify({'success': False, 'error': 'User not found'})
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    
@app.route('/get_current_user')
def get_current_user():
    try:
        print("=" * 50)
        print("DEBUG: Getting current logged in user...")

        db = get_db()
        cursor = db.cursor(dictionary=True)
    
        print("Checking current_login table structure...")
        
        # First try with mobile_no, if fails try mobo_no
        try:
            cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
            current_login = cursor.fetchone()
            column_name = 'mobile_no'
        except:
            cursor.execute("SELECT mobo_no FROM current_login LIMIT 1")
            current_login = cursor.fetchone()
            column_name = 'mobo_no'
            
        print(f"Column used: {column_name}, Result: {current_login}")
        
        if not current_login:
            print("DEBUG: current_login table is EMPTY")
            # ... rest of your code
        
        if not current_login:
            print("DEBUG: current_login table is EMPTY")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"Available tables: {tables}")
            
            cursor.close()
            db.close()
            return jsonify({
                'success': False, 
                'error': 'No user logged in - current_login is empty',
                'debug': {'tables': tables},
                'logged_in': False
            })
        
        mobile_in_login = current_login['mobile_no']
        print(f"DEBUG: Mobile found in current_login: {mobile_in_login}")
        
        print(f"Searching cust_info for cust_number = {mobile_in_login}")
        cursor.execute("SHOW COLUMNS FROM cust_info")
        columns = cursor.fetchall()
        print(f"cust_info columns: {[col['Field'] for col in columns]}")
        
        cursor.execute("SELECT * FROM cust_info WHERE cust_number = %s", (mobile_in_login,))
        user = cursor.fetchone()
        
        if user:
            print(f"DEBUG: User FOUND in cust_info: {user}")
            print(f"   Name: {user.get('cust_name')}")
            print(f"   Mobile: {user.get('cust_number')}")
            print(f"   Age: {user.get('cust_age')}")
            print(f"   Email: {user.get('cust_email')}")
        else:
            print(f"DEBUG: User NOT FOUND in cust_info for mobile: {mobile_in_login}")

            cursor.execute("SELECT cust_number, cust_name FROM cust_info")
            all_users = cursor.fetchall()
            print(f"All users in cust_info: {all_users}")
        
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
                },
                'debug': {
                    'mobile_in_login': mobile_in_login,
                    'user_found': True
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': f'User with mobile {mobile_in_login} not found in cust_info',
                'logged_in': False,
                'debug': {
                    'mobile_in_login': mobile_in_login,
                    'user_found': False
                }
            })
            
    except Exception as e:
        print(f"DEBUG: Error in get_current_user: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'logged_in': False,
            'debug': {'exception': str(e)}
        })

@app.route('/clear_login', methods=['POST'])
def clear_login():
    """Clear login only if someone is actually logged in"""
    try:
        print("=" * 50)
        print("CLEAR_LOGIN CALLED!")
        print(f"Time: {datetime.now()}")
        print(f"Request method: {request.method}")
        print(f"Request headers: {dict(request.headers)}")
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM current_login")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"Clearing login (user was logged in)...")
            cursor.execute("DELETE FROM current_login")
            db.commit()
            cursor.close()
            db.close()
            return jsonify({'success': True, 'cleared': True})
        else:
            print("No one logged in, nothing to clear")
            cursor.close()
            db.close()
            return jsonify({'success': True, 'cleared': False})
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    
@app.route('/test_direct_db')
def test_direct_db():
    """Direct database test"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Direct query
        cursor.execute("SELECT * FROM current_login")
        result = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return f"""
        <h1>Direct DB Test</h1>
        <p>Rows in current_login: {len(result)}</p>
        <pre>{result}</pre>
        <p>Time: {datetime.now()}</p>
        """
    except Exception as e:
        return f"Error: {str(e)}"
    
# Haversine formula to calculate distance between two coordinates
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in kilometers"""
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

def check_bus_proximity():
    """Check if any bus is within 1KM of any user and add to notification_info"""
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
        print(f"Checking proximity for user: {mobile_no}")
        
        # Get current user's location
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
        
        # Get all buses with location (updated in last 5 minutes)
        cursor.execute("""
            SELECT bus_no, latitude, longitude 
            FROM bus_info 
            WHERE latitude IS NOT NULL 
            AND longitude IS NOT NULL
            AND last_seen >= NOW() - INTERVAL 5 MINUTE
        """)
        
        buses = cursor.fetchall()
        print(f"Found {len(buses)} active buses")
        
        now = datetime.now()
        current_date = now.date()
        current_time = now.time()
        
        notifications_added = 0
        
        for bus in buses:
            distance = haversine_distance(
                user['latitude'], user['longitude'],
                bus['latitude'], bus['longitude']
            )
            
            print(f"Bus {bus['bus_no']} is {distance:.2f}KM away")
            
            if distance <= 1.0:
                cursor.execute("""
                    SELECT id FROM notification_info 
                    WHERE notif_heading LIKE %s
                    AND user_mobile = %s
                    AND notif_time >= NOW() - INTERVAL 2 MINUTE
                """, (f'%Bus {bus["bus_no"]}%', mobile_no))
                
                if not cursor.fetchone():
                    heading = f"Bus {bus['bus_no']} nearby!"
                    description = f"Bus {bus['bus_no']} is within {distance:.2f}KM of your location at {current_time.strftime('%I:%M %p')}."
                    
                    cursor.execute("""
                        INSERT INTO notification_info 
                        (notif_date, notif_time, notif_heading, notif_description, user_mobile, notification_type)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (current_date, current_time, heading, description, mobile_no, 'bus_proximity'))
                    
                    db.commit()
                    notifications_added += 1
                    print(f"✅ NEW Notification: Bus {bus['bus_no']} is {distance:.2f}KM away at {current_time.strftime('%H:%M:%S')}")
                else:
                    print(f"⏳ Recent notification exists for Bus {bus['bus_no']} (skipping)")
        
        if notifications_added > 0:
            print(f"Added {notifications_added} new notifications")
        else:
            print("No new notifications added")
                    
    except Exception as e:
        print(f"Error in check_bus_proximity: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if db:
            db.close()

def notification_worker():
    """Background worker to check for notifications periodically"""
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
    """Start the notification background service"""
    worker_thread = threading.Thread(target=notification_worker, daemon=True)
    worker_thread.start()
    print("=" * 50)
    print("🔔 NOTIFICATION SERVICE STARTED")
    print("=" * 50)

@app.route('/force_check_notifications')
def force_check_notifications():
    """Manually trigger notification check"""
    try:
        check_bus_proximity()
        return jsonify({'success': True, 'message': 'Notification check triggered'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/notifications')
def show_notifications():
    """Display data from notification_info to notifications page"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()
        
        if not current_login:
            return redirect('/')
        
        mobile_no = current_login['mobile_no']
        
        cursor.execute("""
            SELECT * FROM notification_info 
            WHERE user_mobile = %s
            ORDER BY notif_date DESC, notif_time DESC
            LIMIT 50
        """, (mobile_no,))
        
        notifications = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return render_template("simple_notifications.html", notifications=notifications)
        
    except Exception as e:
        print(f"Notification error: {e}")
        return render_template("simple_notifications.html", notifications=[])
    
@app.route('/check_new_notifications')
def check_new_notifications():
    """Check if new notifications arrived for current user"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()
        
        if not current_login:
            return jsonify({'success': False, 'new_notifications': False, 'count': 0})
        
        cursor.execute("""
            SELECT COUNT(*) as new_count 
            FROM notification_info 
            WHERE user_mobile = %s
            AND notif_time >= NOW() - INTERVAL 5 MINUTE
        """, (current_login['mobile_no'],))
        
        result = cursor.fetchone()
        cursor.close()
        db.close()
        
        return jsonify({
            'success': True,
            'new_notifications': result['new_count'] > 0,
            'count': result['new_count']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/update_user_location_from_map', methods=['POST'])
def update_user_location_from_map():
    """Update user location from map page"""
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
            print(f"📍 Location updated for user {mobile_no}: {lat}, {lon}")
        
        cursor.close()
        db.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Location update error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/test_add_notification')
def test_add_notification():
    """Add a test notification manually"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Get current logged in user
        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()
        
        if not current_login:
            return jsonify({'success': False, 'error': 'No user logged in'})
        
        now = datetime.now()
        current_date = now.date()
        current_time = now.time()
        
        cursor.execute("""
            INSERT INTO notification_info 
            (notif_date, notif_time, notif_heading, notif_description, user_mobile, notification_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (current_date, current_time, 
              '🔔 Test Notification', 
              'This is a test notification to verify the display works',
              current_login['mobile_no'], 'test'))
        
        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({'success': True, 'message': 'Test notification added'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

import atexit

def cleanup_on_shutdown():
    """Clear current_login when server stops"""
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

start_notification_service()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
