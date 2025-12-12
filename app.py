from flask import Flask, render_template, send_from_directory, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="hrishi@123",
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

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/map')
def map():
    return render_template("map.html")




@app.route('/dino')
def dino():
    return render_template("dino-rush.html")

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
@app.route('/view_pass')
def view_pass():
    return render_template(
        "view_pass.html",
        total_tickets=5,
        holder_name="Shreyash Khot",
        pass_number="PS8011192222",
        amount_paid=500,
        issue_datetime="11/11/2011 | 2:17 AM"
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

# ---------- NEW: return all buses (id, bus_no, no_plate, route, lat, lon) ----------
@app.route('/get_buses')
def get_buses():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, bus_no, no_plate, route, latitude, longitude FROM bus_info")
    buses = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(buses)

# ---------- NEW: update a bus location (called by client every 5s) ----------
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
        print("Login attempt:", data)
        
        identifier = data.get('identifier', '').strip()
        password = data.get('password', '').strip()
        method = data.get('method', 'mobile')
        
        if not identifier or not password:
            return jsonify({'success': False, 'error': 'Mobile/Email and password required'})
        
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        if method == 'mobile':
            cursor.execute("SELECT * FROM cust_info WHERE cust_number = %s", (identifier,))
            print(f"Searching by cust_number: {identifier}")
        else:
            cursor.execute("SELECT * FROM cust_info WHERE cust_email = %s", (identifier,))
            print(f"Searching by cust_email: {identifier}")
        
        user = cursor.fetchone()
        
        if user:
            print(f"User found: {user.get('cust_name', 'Unknown')}")
            print(f"   Mobile (cust_number): {user.get('cust_number')}")
            print(f"   Password in DB: {user.get('password', 'Not set')}")
            
            db_password = user.get('password')
            if not db_password:
                print("User has no password set in database")
                cursor.close()
                db.close()
                return jsonify({'success': False, 'error': 'Password not set for this user'})

            if db_password == password:
                print(f"Password correct for {user['cust_name']}")
                
                try:
                    cursor.execute("SHOW TABLES LIKE 'current_login'")
                    table_exists = cursor.fetchone()
                    if not table_exists:
                        print("current_login table doesn't exist")
                        cursor.execute("CREATE TABLE current_login (mobile_no VARCHAR(15) NOT NULL)")
                        print("Created current_login table")
                    
                    cursor.execute("DELETE FROM current_login")
                    
                    mobile_to_store = user['cust_number']
                    cursor.execute("INSERT INTO current_login (mobile_no) VALUES (%s)", (mobile_to_store,))
                    
                    db.commit()
                    print(f"Mobile stored in current_login: {mobile_to_store}")
                    
                    cursor.close()
                    db.close()
                    
                    return jsonify({
                        'success': True,
                        'message': 'Login successful!',
                        'redirect': '/home'
                    })
                    
                except Exception as db_error:
                    print(f"Database error during login storage: {db_error}")
                    cursor.close()
                    db.close()
                    return jsonify({'success': False, 'error': f'Database error: {str(db_error)}'})
                
            else:
                cursor.close()
                db.close()
                print(f"Password mismatch. DB: {db_password}, Input: {password}")
                return jsonify({'success': False, 'error': 'Wrong password'})
        else:
            cursor.close()
            db.close()
            print("User not found")
            return jsonify({'success': False, 'error': 'User not found'})
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    
# retrieve current logged in user
@app.route('/get_current_user')
def get_current_user():
    try:
        print("=" * 50)
        print("DEBUG: Getting current logged in user...")

        db = get_db()
        cursor = db.cursor(dictionary=True)
    
        print("Checking current_login table...")
        cursor.execute("SELECT * FROM current_login")
        all_logins = cursor.fetchall()
        print(f"All rows in current_login: {all_logins}")
        
        cursor.execute("SELECT mobile_no FROM current_login LIMIT 1")
        current_login = cursor.fetchone()
        print(f"First row in current_login: {current_login}")
        
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

if __name__ == "__main__":
    # you can set debug=False if you want debug disabled,
    # but leaving debug=True is fine while developing
    app.run(host="0.0.0.0", port=5000, debug=True)