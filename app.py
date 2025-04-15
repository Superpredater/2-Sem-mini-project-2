from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
CORS(app)

# Database config (SQLite file)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ims_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Basic validation
    if not username or not email or not password:
        return jsonify({'message': 'All fields are required.'}), 400

    if len(password) < 6:
        return jsonify({'message': 'Password must be at least 6 characters.'}), 400

    # Check if email or username already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered.'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already taken.'}), 400

    # Hash password
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create new user
    new_user = User(username=username, email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User registered!',
        'user': {
            'id': new_user.id,
            'username': username,
            'email': email
        }
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password):
        return jsonify({'message': 'Invalid email or password.'}), 401

    return jsonify({
        'message': 'Login successful!',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
