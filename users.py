from flask import Blueprint, request, jsonify

import hashlib
import sqlite3
import datetime

user_bp = Blueprint('User', __name__)

# Connect to SQLite database
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Create user table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    password TEXT,
                    datetime TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS user_login_activity (
                    id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL,
                    login_status TEXT NOT NULL,
                    datetime TEXT NOT NULL
                )''')

conn.commit()


@user_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    print(data)
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    date_time = datetime.datetime.now()

    if not email or not password:
        return jsonify({'message': 'Incomplete data'}), 400

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({'message': 'Email already in use'}), 400

    cursor.execute('INSERT INTO users (email, name, password, datetime) VALUES (?, ?, ?, ?)', (email, name, hashed_password, date_time))
    conn.commit()

    return jsonify({'message': 'Signup successful'})


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    date_time = datetime.datetime.now()

    if not email or not password:
        return jsonify({'message': 'Incomplete data'}), 400

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?',
                   (email, hashed_password))

    user = cursor.fetchone()

    if user:
        login_status = "Success"
        cursor.execute('INSERT INTO user_login_activity (email, login_status, datetime) VALUES (?, ?, ?)', (email, login_status, date_time))
        conn.commit()
        return jsonify({'message': 'Login successful','success': True, 'user':user[2]})
    else:
        login_status = "Fail"
        cursor.execute(
            'INSERT INTO user_login_activity (email, login_status, datetime) VALUES (?, ?, ?)',
            (email, login_status, date_time))
        conn.commit()
        return jsonify({'message': 'Login failed', 'success': False})