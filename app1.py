from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app1 = Flask(__name__)
CORS(app1)  # Allow cross-origin if your frontend runs separately

# --- Create database and table ---
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

init_db()

# --- Registration Route ---
@app1.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])

    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                  (username, email, password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully', 'user': {'username': username, 'email': email}})
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Email already exists'}), 400

# --- Login Route ---
@app1.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[3], password):
        return jsonify({'message': 'Login successful', 'user': {'username': user[1], 'email': user[2]}})
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

if __name__ == '__main__':
    app1.run(debug=True)
