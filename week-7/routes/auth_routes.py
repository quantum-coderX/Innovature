import re
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from auth import authenticate_user, create_user


auth_bp = Blueprint('auth', __name__)


def error(msg, code):
    return jsonify({'error': msg}), code


@auth_bp.route('/auth/register', methods=['POST'])
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


@auth_bp.route('/auth/login', methods=['POST'])
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


@auth_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    return '', 204
