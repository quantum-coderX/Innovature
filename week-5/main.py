from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from database import db
from models import User, Note
from auth import authenticate_user, create_user, get_current_user
from crud import get_notes, create_note, get_note, update_note, delete_note
from config import Config
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()
    logging.info("Database tables created/verified")

@app.route('/')
def health_check():
    logging.info("Health check requested")
    return jsonify({'status': 'API is running', 'message': 'User Notes API with JWT auth'}), 200

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        logging.warning("Invalid JSON in register request")
        return jsonify({'message': 'Invalid JSON'}), 400
    
    username = data.get('username', '').strip().lower()
    password = data.get('password', '')
    
    if not username or not password:
        logging.warning("Missing username or password in register")
        return jsonify({'message': 'Username and password required'}), 400
    if len(username) < 3 or len(username) > 50:
        logging.warning(f"Invalid username length: {len(username)}")
        return jsonify({'message': 'Username must be 3-50 characters'}), 400
    import re
    if not re.match(r'^[a-z0-9_]+$', username):
        logging.warning(f"Invalid username format: {username}")
        return jsonify({'message': 'Username can only contain letters, numbers, and underscores'}), 400
    if len(password) < 8:
        logging.warning(f"Password too short for user: {username}")
        return jsonify({'message': 'Password must be at least 8 characters long'}), 400
    if not any(c.isupper() for c in password):
        logging.warning(f"Password missing uppercase for user: {username}")
        return jsonify({'message': 'Password must contain at least one uppercase letter'}), 400
    if not any(c.islower() for c in password):
        logging.warning(f"Password missing lowercase for user: {username}")
        return jsonify({'message': 'Password must contain at least one lowercase letter'}), 400
    if not any(c.isdigit() for c in password):
        logging.warning(f"Password missing digit for user: {username}")
        return jsonify({'message': 'Password must contain at least one number'}), 400
    
    try:
        user = create_user(username, password)
        logging.info(f"User registered successfully: {username} (ID: {user.id})")
        return jsonify({'message': 'User created', 'user_id': user.id}), 201
    except Exception as e:
        logging.error(f"Registration failed for {username}: {str(e)}")
        if 'unique constraint' in str(e).lower() or 'duplicate' in str(e).lower():
            return jsonify({'message': 'Username already exists'}), 409
        return jsonify({'message': 'Registration failed'}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        logging.warning("Invalid JSON in login request")
        return jsonify({'message': 'Invalid JSON'}), 400
    username = data.get('username', '').strip().lower()
    password = data.get('password', '')
    
    user = authenticate_user(username, password)
    if user:
        access_token = create_access_token(identity=str(user.id))
        logging.info(f"User logged in: {username} (ID: {user.id})")
        return jsonify(access_token=access_token), 200
    logging.warning(f"Failed login attempt for: {username}")
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    user = get_current_user()
    logging.info(f"User logged out: ID {user.id}")
    # Logout is handled client-side by discarding the token
    return jsonify({'message': 'Logged out'}), 200

@app.route('/notes', methods=['GET'])
@jwt_required()
def read_notes():
    user = get_current_user()
    try:
        notes = get_notes(user.id)
        logging.info(f"User {user.id} retrieved {len(notes)} notes")
        return jsonify([{
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at.isoformat()
        } for note in notes]), 200
    except Exception as e:
        logging.error(f"Failed to retrieve notes for user {user.id}: {str(e)}")
        return jsonify({'message': 'Failed to retrieve notes'}), 500

@app.route('/notes', methods=['POST'])
@jwt_required()
def create_user_note():
    user = get_current_user()
    data = request.get_json()
    if not data:
        logging.warning(f"Invalid JSON in create note for user {user.id}")
        return jsonify({'message': 'Invalid JSON'}), 400
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    if not title and 'subject' in data:
        logging.warning(f"User {user.id} sent 'subject' instead of 'title': {data.get('subject')}")
        return jsonify({'message': 'Use "title" instead of "subject" for the note title'}), 400
    
    if not title or not content:
        logging.warning(f"Missing title or content in create note for user {user.id}. Received: title='{title}', content='{content[:50]}...'")
        return jsonify({'message': 'Title and content required'}), 400
    if len(title) > 200:
        logging.warning(f"Title too long for user {user.id}: {len(title)} chars")
        return jsonify({'message': 'Title must be 200 characters or less'}), 400
    if len(content) > 10000:
        logging.warning(f"Content too long for user {user.id}: {len(content)} chars")
        return jsonify({'message': 'Content must be 10,000 characters or less'}), 400
    
    try:
        note = create_note(title, content, user.id)
        logging.info(f"User {user.id} created note {note.id}: {title}")
        return jsonify({
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at.isoformat()
        }), 201
    except Exception as e:
        logging.error(f"Failed to create note for user {user.id}: {str(e)}")
        return jsonify({'message': 'Failed to create note'}), 500

@app.route('/notes/<int:note_id>', methods=['GET'])
@jwt_required()
def read_note(note_id):
    user = get_current_user()
    try:
        note = get_note(note_id, user.id)
        if not note:
            logging.warning(f"Note {note_id} not found for user {user.id}")
            return jsonify({'message': 'Note not found'}), 404
        logging.info(f"User {user.id} retrieved note {note_id}")
        return jsonify({
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at.isoformat()
        }), 200
    except Exception as e:
        logging.error(f"Failed to retrieve note {note_id} for user {user.id}: {str(e)}")
        return jsonify({'message': 'Failed to retrieve note'}), 500

@app.route('/notes/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_user_note(note_id):
    user = get_current_user()
    data = request.get_json()
    if not data:
        logging.warning(f"Invalid JSON in update note {note_id} for user {user.id}")
        return jsonify({'message': 'Invalid JSON'}), 400
    title = data.get('title')
    if title is not None:
        title = title.strip()
        if len(title) > 200:
            logging.warning(f"Title too long in update for user {user.id}: {len(title)} chars")
            return jsonify({'message': 'Title must be 200 characters or less'}), 400
    
    content = data.get('content')
    if content is not None:
        content = content.strip()
        if len(content) > 10000:
            logging.warning(f"Content too long in update for user {user.id}: {len(content)} chars")
            return jsonify({'message': 'Content must be 10,000 characters or less'}), 400
    
    try:
        note = update_note(note_id, title, content, user.id)
        if not note:
            logging.warning(f"Note {note_id} not found for update by user {user.id}")
            return jsonify({'message': 'Note not found'}), 404
        logging.info(f"User {user.id} updated note {note_id}")
        return jsonify({
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at.isoformat()
        }), 200
    except Exception as e:
        logging.error(f"Failed to update note {note_id} for user {user.id}: {str(e)}")
        return jsonify({'message': 'Failed to update note'}), 500

@app.route('/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_user_note(note_id):
    user = get_current_user()
    try:
        note = delete_note(note_id, user.id)
        if not note:
            logging.warning(f"Note {note_id} not found for delete by user {user.id}")
            return jsonify({'message': 'Note not found'}), 404
        logging.info(f"User {user.id} deleted note {note_id}")
        return jsonify({'message': 'Note deleted'}), 200
    except Exception as e:
        logging.error(f"Failed to delete note {note_id} for user {user.id}: {str(e)}")
        return jsonify({'message': 'Failed to delete note'}), 500

if __name__ == '__main__':
    logging.info("Starting User Notes API server")
    app.run(debug=True)