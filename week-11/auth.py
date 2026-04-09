from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User


ROLE_SELLER = 1
ROLE_BUYER = 2
ROLE_LABELS = {
    ROLE_SELLER: 'seller',
    ROLE_BUYER: 'buyer',
}


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    if not password_hash:
        return False
    return check_password_hash(password_hash, password)


def get_current_user():
    identity = get_jwt_identity()
    if identity is None:
        return None
    try:
        return db.session.get(User, int(identity))
    except (TypeError, ValueError):
        return None


def parse_role_code(value, default=None):
    """Convert input role (code or label) to numeric code."""
    if value is None:
        return default

    if isinstance(value, int):
        return value if value in ROLE_LABELS else None

    text = str(value).strip().lower()
    if text.isdigit():
        code = int(text)
        return code if code in ROLE_LABELS else None

    if text == 'seller':
        return ROLE_SELLER
    if text == 'buyer':
        return ROLE_BUYER

    return None


def jwt_required_active_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = get_current_user()
        if not user or not user.is_active:
            return jsonify({'error': 'Unauthorized'}), 401
        return fn(*args, **kwargs)

    return wrapper


def seller_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = get_current_user()
        if not user or not user.is_active:
            return jsonify({'error': 'Unauthorized'}), 401
        if user.role != ROLE_SELLER:
            return jsonify({'error': 'Forbidden: seller access required'}), 403
        return fn(*args, **kwargs)

    return wrapper
