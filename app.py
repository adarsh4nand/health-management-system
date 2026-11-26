from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure key

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'health_wellness'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get today's habits for the user
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT habit_name, habit_type, quantity 
        FROM habits 
        WHERE user_id = %s AND DATE(created_at) = CURDATE()
    """, (session['user_id'],))
    
    habits = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', habits=habits)

@app.route('/habits')
def habits():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get today's habits for the user
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT habit_name, habit_type, quantity, created_at 
        FROM habits 
        WHERE user_id = %s AND DATE(created_at) = CURDATE()
        ORDER BY created_at DESC
    """, (session['user_id'],))
    
    habits = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('habits.html', habits=habits)

@app.route('/health_tips')
def health_tips():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('health_tips.html')

@app.route('/add_habit', methods=['POST'])
def add_habit():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    habit_name = request.form['habit_name']
    habit_type = request.form['habit_type']
    quantity = int(request.form['quantity'])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO habits (user_id, habit_name, habit_type, quantity, created_at)
            VALUES (%s, %s, %s, %s, NOW())
        """, (session['user_id'], habit_name, habit_type, quantity))
        
        conn.commit()
        flash('Habit added successfully!', 'success')
    except Exception as e:
        print(f"Error: {e}")
        flash('Error adding habit', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('habits'))

# Add login and registration routes if not already present
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user and user['password'] == password:  # In production, use proper password hashing
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
            
        cursor.close()
        conn.close()
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO users (username, password, created_at)
                VALUES (%s, %s, NOW())
            """, (username, password))
            
            conn.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error: {e}")
            flash('Username already exists', 'error')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
