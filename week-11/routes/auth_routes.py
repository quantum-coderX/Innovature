import re
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from database import db
from models import User
from serializers import serialize_user, error_response, success_response
from auth import (
    ROLE_BUYER,
    parse_role_code,
    hash_password,
    verify_password,
    jwt_required_active_user,
    get_current_user,
)


auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}

    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not name or len(name) < 2 or len(name) > 120:
        return error_response('Name must be between 2 and 120 characters')
    if not email or not validate_email(email):
        return error_response('Valid email is required')
    if len(password) < 8:
        return error_response('Password must be at least 8 characters')
    if User.query.filter_by(email=email).first():
        return error_response('User with this email already exists')

    role = parse_role_code(data.get('role'), default=ROLE_BUYER)
    if role is None:
        return error_response('role must be 1/seller or 2/buyer')

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role=role,
        phone=(data.get('phone') or '').strip() or None,
        address=(data.get('address') or '').strip() or None,
        is_active=True,
    )
    db.session.add(user)
    db.session.commit()

    return success_response(serialize_user(user), 'Registration successful', 201)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not email or not password:
        return error_response('Email and password are required')

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(user.password_hash, password):
        return error_response('Invalid credentials')
    if not user.is_active:
        return error_response('Account is inactive')

    token = create_access_token(identity=str(user.id), additional_claims={'role_code': user.role})
    return success_response({'access_token': token, 'user': serialize_user(user)}, 'Login successful')


@auth_bp.route('/me', methods=['GET'])
@jwt_required_active_user
def me():
    user = get_current_user()
    return success_response(serialize_user(user))


@auth_bp.route('/validate', methods=['GET'])
@jwt_required_active_user
def validate_token():
    user = get_current_user()
    return success_response({'valid': True, 'user_id': user.id, 'role_code': user.role})
