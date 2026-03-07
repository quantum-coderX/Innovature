import re
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from database import db
from models import User, Note
from auth import authenticate_user, create_user, get_current_user
from crud import get_notes, create_note, get_note, update_note, delete_note
from config import Config

def error(msg, code):
    return jsonify({'error': msg}), code

def note_dict(note):
    return {
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.isoformat()
    }

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

@app.route('/')
def health_check():
    return jsonify({'status': 'API is running', 'message': 'User Notes API with JWT auth'}), 200

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return error('Bad request', 400)

    username = data.get('username', '').strip().lower()
    password = data.get('password', '')

    if not username or not password:
        return error('Bad request', 400)
    if len(username) < 3 or len(username) > 50:
        return error('Bad request', 400)
    if not re.match(r'^[a-z0-9_]+$', username):
        return error('Bad request', 400)
    if len(password) < 8:
        return error('Bad request', 400)
    if not any(c.isupper() for c in password):
        return error('Bad request', 400)
    if not any(c.islower() for c in password):
        return error('Bad request', 400)
    if not any(c.isdigit() for c in password):
        return error('Bad request', 400)

    try:
        user = create_user(username, password)
        return jsonify({'user_id': user.id}), 201
    except Exception:
        return error('Registration failed', 500)

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return error('Bad request', 400)
    username = data.get('username', '').strip().lower()
    password = data.get('password', '')

    user = authenticate_user(username, password)
    if user:
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'access_token': access_token}), 200
    return error('Invalid credentials', 401)

@app.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    return '', 204

@app.route('/notes', methods=['GET'])
@jwt_required()
def read_notes():
    user = get_current_user()
    try:
        notes = get_notes(user.id)
        return jsonify([note_dict(n) for n in notes]), 200
    except Exception:
        return error('Internal server error', 500)

@app.route('/notes', methods=['POST'])
@jwt_required()
def create_user_note():
    user = get_current_user()
    data = request.get_json()
    if not data:
        return error('Bad request', 400)
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    if not title or not content:
        return error('Bad request', 400)
    if len(title) > 200 or len(content) > 10000:
        return error('Bad request', 400)
    try:
        note = create_note(title, content, user.id)
        return jsonify(note_dict(note)), 201
    except Exception:
        return error('Internal server error', 500)

@app.route('/notes/<int:note_id>', methods=['GET'])
@jwt_required()
def read_note(note_id):
    user = get_current_user()
    note = get_note(note_id, user.id)
    if not note:
        return error('Not found', 404)
    return jsonify(note_dict(note)), 200

@app.route('/notes/<int:note_id>', methods=['PATCH'])
@jwt_required()
def update_user_note(note_id):
    user = get_current_user()
    data = request.get_json()
    if not data:
        return error('Bad request', 400)
    title = data.get('title')
    if title is not None:
        title = title.strip()
        if len(title) > 200:
            return error('Bad request', 400)
    content = data.get('content')
    if content is not None:
        content = content.strip()
        if len(content) > 10000:
            return error('Bad request', 400)
    try:
        note = update_note(note_id, title, content, user.id)
        if not note:
            return error('Not found', 404)
        return jsonify(note_dict(note)), 200
    except Exception:
        return error('Internal server error', 500)

@app.route('/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_user_note(note_id):
    user = get_current_user()
    try:
        if not delete_note(note_id, user.id):
            return error('Not found', 404)
        return '', 204
    except Exception:
        return error('Internal server error', 500)

if __name__ == '__main__':
    app.run(debug=True)