from flask import Blueprint, request, jsonify

import hashlib,json
import sqlite3
import datetime

associate_bp = Blueprint('Associate', __name__)

# Connect to SQLite database
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Create user table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT,
                    datetime TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS preview (
                    id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL,
                    user_type TEXT NOT NULL,
                    maindata TEXT NOT NULL,
                    mediaName TEXT NOT NULL,
                    docName TEXT NOT NULL,
                    language TEXT NOT NULL,
                    creationTime TEXT NOT NULL,
                    modifyTime TEXT NOT NULL,
                    token TEXT NOT NULL,
                    willGenerate TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )''')

conn.commit()


def check_associate(email, token):
    cursor.execute('SELECT token FROM preview WHERE email = ?', (email,))
    result = [row[0] for row in cursor.fetchall()]

    for db_token in result:
        if db_token == token:
            return True

    return False


def check_user_type(email, token):
    cursor.execute('SELECT user_type, token FROM preview WHERE email = ?', (email,))
    rows = cursor.fetchall()

    for row in rows:
        db_user_type = row[0]
        db_token = row[1]

        if db_token == token and db_user_type == "Owner":
            return True

    return False


@associate_bp.route('/add', methods=['POST'])
def add_associate():
    data = request.json
    token = data.get('token')
    email = data.get('email')
    user = data.get('user')
    timestamp = datetime.datetime.now()
    new_user_type = "Associate"

    print(user)

    cursor.execute('SELECT email FROM users WHERE email = ?', (email,))
    result_user = cursor.fetchone()

    if result_user:
        user_associated = check_associate(email,token)
        if user_associated == True:
            return jsonify({'message':'User Already Associated'})
        else:
            fetched_user_type = check_user_type(user,token)
            if fetched_user_type == True:
                cursor.execute('SELECT * FROM preview WHERE token = ?', (token,))
                result_tokens = cursor.fetchall()

                if result_tokens:
                    for row in result_tokens:
                        cursor.execute('INSERT INTO preview (email, user_type, maindata, mediaName, docName, language, creationTime, modifyTime, token, willGenerate, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',(email,new_user_type,row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],timestamp))
                        conn.commit()
                        return jsonify({'message': 'Associate added successfully'})
                else:
                    return jsonify({'message': 'Token not found in the "preview" table'})
            return jsonify({'message': 'You Cannot add an Associate Because You are not the Creator of this file'})
    else:
        return jsonify({'message': "User doesn't exist"})
