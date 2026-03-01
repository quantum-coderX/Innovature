from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from database import db
from models import User, Note
from auth import authenticate_user, create_user, get_current_user
from crud import get_notes, create_note, get_note, update_note, delete_note
from config import Config

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
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400
    user = create_user(username, password)
    return jsonify({'message': 'User created', 'user_id': user.id}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = authenticate_user(username, password)
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    # Logout is handled client-side by discarding the token
    return jsonify({'message': 'Logged out'}), 200

@app.route('/notes', methods=['GET'])
@jwt_required()
def read_notes():
    user = get_current_user()
    notes = get_notes(user.id)
    return jsonify([{
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.isoformat()
    } for note in notes]), 200

@app.route('/notes', methods=['POST'])
@jwt_required()
def create_user_note():
    user = get_current_user()
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    if not title or not content:
        return jsonify({'message': 'Title and content required'}), 400
    note = create_note(title, content, user.id)
    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.isoformat()
    }), 201

@app.route('/notes/<int:note_id>', methods=['GET'])
@jwt_required()
def read_note(note_id):
    user = get_current_user()
    note = get_note(note_id, user.id)
    if not note:
        return jsonify({'message': 'Note not found'}), 404
    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.isoformat()
    }), 200

@app.route('/notes/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_user_note(note_id):
    user = get_current_user()
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    note = update_note(note_id, title, content, user.id)
    if not note:
        return jsonify({'message': 'Note not found'}), 404
    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.isoformat()
    }), 200

@app.route('/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_user_note(note_id):
    user = get_current_user()
    note = delete_note(note_id, user.id)
    if not note:
        return jsonify({'message': 'Note not found'}), 404
    return jsonify({'message': 'Note deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)