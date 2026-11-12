from flask import Flask, render_template, request, jsonify, session, redirect, url_for, make_response
import sqlite3
from datetime import date, timedelta
import csv
import io
import os
from ml_tips import get_personalized_tip

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_super_secret_key_123')

# --- SQLITE DATABASE SETUP ---
DB_NAME = 'health_awareness.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name like a dictionary
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS daily_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            log_date DATE NOT NULL,
            water_glasses INTEGER DEFAULT 0,
            sleep_hours REAL DEFAULT 0,
            exercise_mins INTEGER DEFAULT 0,
            mood_rating INTEGER DEFAULT 5,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    try:
        conn.execute("INSERT INTO users (username, password) VALUES ('student1', 'pass123')")
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # User already exists
    conn.close()

# Initialize database on startup
init_db()

# --- DUMMY DATA FOR AWARENESS & RESOURCES ---
HEALTH_RESOURCES = [
    {"name": "National Mental Health Helpline", "type": "Helpline", "contact": "9152987821", "icon": "📞"},
    {"name": "Local Community Yoga Center", "type": "Physical Activity", "contact": "Open 6 AM - 8 AM", "icon": "🧘"},
    {"name": "Govt. Free Health Camp", "type": "Preventive Care", "contact": "Every 1st Sunday", "icon": "🏥"},
    {"name": "Clean Water Initiative", "type": "Hydration", "contact": "District Office", "icon": "💧"}
]

HEALTH_MYTHS = [
    {"myth": "Drinking cold water causes colds.", "fact": "Colds are caused by viruses, not by the temperature of the water you drink."},
    {"myth": "You need to drink exactly 8 glasses of water a day.", "fact": "Water needs vary by weight, activity level, and climate. Our app calculates your exact need!"},
    {"myth": "Cracking your knuckles causes arthritis.", "fact": "Studies show no link between knuckle cracking and osteoarthritis."},
    {"myth": "You lose most of your body heat through your head.", "fact": "You lose heat from any uncovered part of your body. Cover your hands and feet too!"}
]

# --- ROUTES ---

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        return redirect(url_for('dashboard'))
    return "Invalid Credentials! <a href='/'>Go Back</a>"

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    user_id = session['user_id']
    today = date.today()

    water = 0
    sleep = 0
    exercise = 0
    weight = 0
    water_goal_glasses = 8 

    if request.method == 'POST':
        water = int(request.form.get('water', 0))
        sleep = float(request.form.get('sleep', 0))
        exercise = int(request.form.get('exercise', 0))
        weight = request.form.get('weight', 0)
        
        # AI Wellness Score Calculation (1-10)
        water_score = min(3, (water / 8) * 3)
        sleep_score = min(4, (sleep / 8) * 4)
        exercise_score = min(3, (exercise / 30) * 3)
        wellness_score = round(water_score + sleep_score + exercise_score)

        try:
            if float(weight) > 0:
                water_goal_glasses = round((float(weight) * 0.033) / 0.25)
            else:
                water_goal_glasses = 8
        except ValueError:
            water_goal_glasses = 8

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO daily_logs (user_id, log_date, water_glasses, sleep_hours, exercise_mins, mood_rating)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, today, water, sleep, exercise, wellness_score))
        conn.commit()
        conn.close()

    tip, videos = get_personalized_tip(water, sleep, exercise)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch Historical Data
    cursor.execute("""
        SELECT last_updated, water_glasses, sleep_hours, exercise_mins, mood_rating 
        FROM daily_logs WHERE user_id = ? ORDER BY last_updated DESC
    """, (user_id,))
    history_data = cursor.fetchall()

    # Calculate Streak
    cursor.execute("""
        SELECT DISTINCT log_date FROM daily_logs WHERE user_id = ? ORDER BY log_date DESC
    """, (user_id,))
    unique_dates = [row['log_date'] for row in cursor.fetchall()]
    
    streak = 0
    if unique_dates:
        latest_log_date = unique_dates[0]
        if latest_log_date == str(today):
            streak = 1
            for i in range(1, len(unique_dates)):
                # Simple streak logic for demo
                streak += 1 

    # Fetch Community Stats
    cursor.execute("SELECT COUNT(DISTINCT user_id) as total_users, ROUND(AVG(water_glasses), 1) as avg_water, ROUND(AVG(sleep_hours), 1) as avg_sleep FROM daily_logs")
    community_stats = cursor.fetchone()
    conn.close()

    return render_template('dashboard.html', 
                           username=session['username'], 
                           tip=tip, 
                           videos=videos, 
                           history=history_data,
                           streak=streak,
                           community=community_stats,
                           water_goal=water_goal_glasses)

@app.route('/api/habit_data')
def habit_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT log_date, water_glasses, sleep_hours, exercise_mins 
        FROM daily_logs WHERE user_id = ? ORDER BY log_date DESC LIMIT 7
    """, (user_id,))
    data = cursor.fetchall()
    conn.close()

    dates = [str(row['log_date']) for row in data][::-1]
    water = [row['water_glasses'] for row in data][::-1]
    sleep = [row['sleep_hours'] for row in data][::-1]

    return jsonify({'dates': dates, 'water': water, 'sleep': sleep})

@app.route('/export_data')
def export_data():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT last_updated, water_glasses, sleep_hours, exercise_mins, mood_rating FROM daily_logs WHERE user_id = ? ORDER BY last_updated DESC", (session['user_id'],))
    data = cursor.fetchall()
    conn.close()

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Date & Time', 'Water (Glasses)', 'Sleep (Hours)', 'Exercise (Mins)', 'AI Wellness Score (1-10)'])
    for row in data:
        cw.writerow([row['last_updated'], row['water_glasses'], row['sleep_hours'], row['exercise_mins'], row['mood_rating']])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename={session['username']}_health_data.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/resources')
def resources():
    if 'user_id' not in session: return redirect(url_for('home'))
    return render_template('resources.html', resources=HEALTH_RESOURCES, username=session['username'])

@app.route('/awareness')
def awareness():
    if 'user_id' not in session: return redirect(url_for('home'))
    return render_template('awareness.html', myths=HEALTH_MYTHS, username=session['username'])

@app.route('/subscribe', methods=['POST'])
def subscribe():
    if 'user_id' not in session: return redirect(url_for('home'))
    email = request.form.get('email')
    print(f"[SYSTEM] Reminder subscribed for {email}!") 
    return render_template('dashboard.html', 
                           username=session['username'], 
                           tip="✅ Success! You will now receive daily wellness reminders.", 
                           videos=[], history=[], streak=0, community=None, water_goal=8)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

# --- THIS IS THE CRUCIAL PART THAT STARTS THE SERVER ---
if __name__ == '__main__':
    print("Starting HealthTrack Server...")
    app.run(debug=True, port=5000)