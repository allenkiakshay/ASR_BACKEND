from flask import Blueprint, request, jsonify

import hashlib,json
import sqlite3
import datetime

preview_bp = Blueprint('Preview', __name__)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS preview (
                    id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL,
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
@preview_bp.route('/adddata', methods=['POST'])
def adddata():
    data = request.json
    email = str(data.get('email')['user'])
    mediaName = str(data.get('mediaName'))
    docName = str(data.get('docName'))
    language = str(data.get('language'))
    creationTime = str(data.get('creationTime'))
    modifyTime = str(data.get('modifyTime'))
    token = str(data.get('token'))
    willGenerate = str(data.get('willGenerate'))
    timestamp = datetime.datetime.now()

    cursor.execute('INSERT INTO preview (email, maindata, mediaName, docName, language, creationTime, modifyTime, token, willGenerate, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (email, json.dumps(data), mediaName, docName, language, creationTime, modifyTime, token, willGenerate, timestamp))
    conn.commit()

    cursor.execute('SELECT maindata FROM preview WHERE email = ?', (email,))
    rows = cursor.fetchall()

    data_list = [row[0] for row in rows]

    rectified_list = []

    for item in data_list:
        try:
            rectified_item = json.loads(item)
            rectified_list.append(rectified_item)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {str(e)}")

    return jsonify(rectified_list)

@preview_bp.route('/fetchdata', methods=['POST','GET'])
def fetchdata():
    try:
        data = request.get_json()
        email = data.get('user')

        cursor.execute('SELECT maindata FROM preview WHERE email = ?', (email,))
        rows = cursor.fetchall()

        data_list = [row[0] for row in rows]

        rectified_list = []

        for item in data_list:
            try:
                rectified_item = json.loads(item)
                rectified_list.append(rectified_item)
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {str(e)}")

        return jsonify(rectified_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500