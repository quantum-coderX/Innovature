from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import db
from models import User

def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

def check_password(password, hashed):
    return check_password_hash(hashed, password)

def create_user(username, password):
    hashed = hash_password(password)
    user = User(username=username, password_hash=hashed)
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password(password, user.password_hash):
        return user
    return None

def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)