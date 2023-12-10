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
                    name TEXT NOT NULL,
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

cursor.execute('''CREATE TABLE IF NOT EXISTS main_preview (
                    id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL,
                    associates TEXT NOT NULL,
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
    cursor.execute('SELECT user_type FROM preview WHERE email = ? and token = ?', (email,token,))
    rows = cursor.fetchall()

    for row in rows:
        db_user_type = row[0]

        if db_user_type == "Owner":
            return True

    conn.commit()
    return False


def add_associate_in_main_preview(email,token):
    cursor.execute('SELECT associates FROM main_preview WHERE token = ?',(token,))
    current_associates = cursor.fetchone()
    current_associates = current_associates[0]

    cursor.execute('SELECT name FROM users WHERE email = ?',(email,))
    user_name = cursor.fetchone()
    user_name = user_name[0]

    new_associate = {'email':email,'name':user_name}

    new_associates = []
    if current_associates:
        current_associates = json.loads(current_associates)
        for i in current_associates:
            new_associates.append(i)
    else:
        pass

    new_associates.append(new_associate)

    new_associates = json.dumps(new_associates)

    cursor.execute('UPDATE main_preview SET associates = ? WHERE token = ?',(new_associates,token))

    return True


@associate_bp.route('/add', methods=['POST'])
def add_associate():
    data = request.json
    token = data.get('token')
    email = data.get('email')
    user = data.get('user')
    timestamp = datetime.datetime.now()
    new_user_type = "Associate"

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
                        add_associate_in_main_preview(email,token)
                        cursor.execute('INSERT INTO preview (email, user_type, maindata, mediaName, docName, language, creationTime, modifyTime, token, willGenerate, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',(email,new_user_type,row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],timestamp))
                        conn.commit()
                        return jsonify({'message': 'Associate added successfully'})
                else:
                    return jsonify({'message': 'Token not found in the "preview" table'})
            return jsonify({'message': 'You Cannot add an Associate Because You are not the Creator of this file'})
    else:
        return jsonify({'message': "User doesn't exist"})


@associate_bp.route('/fetch', methods=['POST','GET'])
def fetch_associate():
    # try:
    data = request.json
    email = data.get('email')
    token = data.get('token')

    fetched_user_type = check_user_type(email,token)
    if fetched_user_type:
        cursor.execute('SELECT associates FROM main_preview WHERE email = ? and token = ?', (email,token,))
        associates = cursor.fetchone()

        if associates is None or associates[0] is None:
            associates_response = {
                'associates': [],
                'Status': True
            }
        else:
            associates = json.loads(associates[0])
            associates_response = {
                'associates': associates,
                'Status': True
            }
        return jsonify(associates_response)
    else:
        associates_response = {
            'associates': '',
            'Status': False
        }
        return jsonify(associates_response)

    conn.commit()
# except:
    #     return jsonify('There was a Error Try Contacting our Developer allenkiakshay8322@gmail.com')