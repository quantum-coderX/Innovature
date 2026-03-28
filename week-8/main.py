from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import hmac
from datetime import datetime, timezone
from database import db
from config import Config
from models import User, OTP, utc_now
from auth import mail, require_role, require_2fa_verified, require_2fa_and_role, validate_email_format
from auth import (
    create_user, authenticate_user, create_otp_for_user, send_otp_email,
    verify_otp, create_jwt_token, get_current_user, update_last_login,
    log_login_attempt, cleanup_expired_otps
)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
mail.init_app(app)

# ==================== Error Handlers ====================

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'message': 'Unauthorized access'}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({'message': 'Forbidden'}), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

# ==================== Health Check ====================

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'API is running',
        'message': 'Two-Factor Authentication API with Email OTP',
        'timestamp': utc_now().isoformat()
    }), 200

# ==================== Auth Routes ====================

def _process_login(username, password, required_role=None):
    """Authenticate user, enforce optional role, and trigger OTP/token flow."""
    user, auth_message = authenticate_user(username, password)

    if not user:
        return jsonify({'message': auth_message}), 401

    if required_role and user.role != required_role:
        return jsonify({'message': f'Access denied. {required_role.capitalize()} credentials required'}), 403

    # If 2FA is enabled, send OTP
    if user.two_fa_enabled:
        otp = create_otp_for_user(user.id)
        success, otp_message = send_otp_email(user, otp.otp_code)

        if not success:
            return jsonify({'message': otp_message}), 500

        return jsonify({
            'message': 'OTP sent successfully to your email',
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'two_fa_required': True,
            'otp_expiry_minutes': 5
        }), 200

    # If 2FA is not enabled, create token immediately
    access_token = create_jwt_token(user.id)
    update_last_login(user.id)
    log_login_attempt(user.id, success=True)

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Username, email, and password are required'}), 400
    
    username = data.get('username').strip()
    email = data.get('email').strip()
    password = data.get('password')
    requested_role = data.get('role', 'user').strip().lower() if data.get('role') else 'user'

    if requested_role != 'user':
        return jsonify({'message': 'Public registration only allows the user role'}), 403
    
    # Validate email format
    is_valid_email, email_result = validate_email_format(email)
    if not is_valid_email:
        return jsonify({'message': f'Invalid email format: {email_result}'}), 400
    
    email = email_result  # Use normalized email
    
    # Validate password length
    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long'}), 400
    
    # Create user
    user, message = create_user(username, email, password, 'user')
    
    if not user:
        return jsonify({'message': message}), 400
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 201

@app.route('/api/auth/bootstrap/admin', methods=['POST'])
def bootstrap_admin():
    """Create the first admin account using bootstrap key."""
    if not app.config.get('ENABLE_ADMIN_BOOTSTRAP', False):
        return jsonify({'message': 'Admin bootstrap is disabled'}), 403

    provided_key = request.headers.get('X-ADMIN-BOOTSTRAP-KEY', '')
    configured_key = app.config.get('ADMIN_BOOTSTRAP_KEY', '')

    if not configured_key or not hmac.compare_digest(provided_key, configured_key):
        return jsonify({'message': 'Invalid bootstrap key'}), 401

    if User.query.filter_by(role='admin').first():
        return jsonify({'message': 'Admin account already exists'}), 409

    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Username, email, and password are required'}), 400

    username = data.get('username').strip()
    email = data.get('email').strip()
    password = data.get('password')

    is_valid_email, email_result = validate_email_format(email)
    if not is_valid_email:
        return jsonify({'message': f'Invalid email format: {email_result}'}), 400

    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long'}), 400

    user, message = create_user(username, email_result, password, 'admin')
    if not user:
        return jsonify({'message': message}), 400

    return jsonify({
        'message': 'Admin bootstrap completed successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user and send OTP"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400
    
    username = data.get('username').strip()
    password = data.get('password')

    return _process_login(username, password)

@app.route('/api/auth/admin/login', methods=['POST'])
def admin_login():
    """Authenticate admin and send OTP"""
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400

    username = data.get('username').strip()
    password = data.get('password')

    return _process_login(username, password, required_role='admin')

@app.route('/api/auth/verify-otp', methods=['POST'])
def verify_two_fa():
    """Verify OTP and grant access"""
    data = request.get_json()
    
    if not data or not data.get('user_id') or not data.get('otp_code'):
        return jsonify({'message': 'User ID and OTP code are required'}), 400
    
    user_id = data.get('user_id')
    otp_code = data.get('otp_code').strip()
    
    # Verify OTP
    success, message = verify_otp(user_id, otp_code)
    
    if not success:
        return jsonify({'message': message}), 401
    
    # Create JWT token
    user = db.session.get(User, user_id)
    access_token = create_jwt_token(user.id)
    update_last_login(user.id)
    log_login_attempt(user.id, success=True)
    
    return jsonify({
        'message': 'OTP verified successfully',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200

@app.route('/api/auth/resend-otp', methods=['POST'])
def resend_otp():
    """Resend OTP to user's email"""
    data = request.get_json()
    
    if not data or not data.get('user_id'):
        return jsonify({'message': 'User ID is required'}), 400
    
    user_id = data.get('user_id')
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Create new OTP
    otp = create_otp_for_user(user.id)
    success, message = send_otp_email(user, otp.otp_code)
    
    if not success:
        return jsonify({'message': message}), 500
    
    return jsonify({
        'message': 'OTP resent successfully',
        'otp_expiry_minutes': 5
    }), 200

# ==================== User Routes ====================

@app.route('/api/users/profile', methods=['GET'])
@require_2fa_verified
def get_profile():
    """Get current user profile"""
    user = get_current_user()
    
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
            'two_fa_enabled': user.two_fa_enabled,
            'two_fa_verified': user.two_fa_verified,
            'is_email_verified': user.is_email_verified,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'created_at': user.created_at.isoformat()
        }
    }), 200

@app.route('/api/users/profile', methods=['PUT'])
@require_2fa_verified
def update_profile():
    """Update user profile"""
    data = request.get_json()
    user = get_current_user()
    
    if data.get('email'):
        # Validate email format
        is_valid_email, email_result = validate_email_format(data.get('email'))
        if not is_valid_email:
            return jsonify({'message': f'Invalid email format: {email_result}'}), 400
        
        email = email_result  # Use normalized email
        
        # Check if email is already taken
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({'message': 'Email already in use'}), 400
        
        user.email = email
        user.is_email_verified = False  # Require re-verification
    
    if data.get('username'):
        # Check if username is already taken
        existing_user = User.query.filter_by(username=data.get('username')).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({'message': 'Username already in use'}), 400
        
        user.username = data.get('username')
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200

@app.route('/api/users', methods=['GET'])
@require_role('admin')
def list_users():
    """List all users (Admin only)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = User.query.paginate(page=page, per_page=per_page)
    users = pagination.items
    
    return jsonify({
        'users': [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'role': u.role,
            'is_active': u.is_active,
            'created_at': u.created_at.isoformat()
        } for u in users],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
@require_role('admin')
def get_user(user_id):
    """Get user details (Admin only)"""
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
            'two_fa_enabled': user.two_fa_enabled,
            'failed_login_attempts': user.failed_login_attempts,
            'is_account_locked': user.is_account_locked(),
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None
        }
    }), 200

@app.route('/api/users/<int:user_id>/lock', methods=['POST'])
@require_role('admin')
def lock_user(user_id):
    """Lock user account (Admin only)"""
    current_user = get_current_user()
    
    # Prevent admin from locking their own account
    if current_user.id == user_id:
        return jsonify({'message': 'Cannot lock your own account'}), 400
    
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'User account locked successfully'}), 200

@app.route('/api/users/<int:user_id>/unlock', methods=['POST'])
@require_role('admin')
def unlock_user(user_id):
    """Unlock user account (Admin only)"""
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user.is_active = True
    user.reset_failed_attempts()
    db.session.commit()
    
    return jsonify({'message': 'User account unlocked successfully'}), 200

@app.route('/api/users/<int:user_id>/role', methods=['PUT'])
@require_role('admin')
def update_user_role(user_id):
    """Update user role (Admin only)"""
    current_user = get_current_user()
    
    # Prevent admin from changing their own role
    if current_user.id == user_id:
        return jsonify({'message': 'Cannot change your own role'}), 400
    
    data = request.get_json()
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not data.get('role'):
        return jsonify({'message': 'Role is required'}), 400
    
    valid_roles = ['admin', 'user', 'moderator']
    if data.get('role') not in valid_roles:
        return jsonify({'message': f'Invalid role. Valid roles: {", ".join(valid_roles)}'}), 400
    
    # Prevent removing the last admin
    if user.role == 'admin' and data.get('role') != 'admin':
        admin_count = User.query.filter_by(role='admin').count()
        if admin_count <= 1:
            return jsonify({'message': 'Cannot remove the last admin account'}), 400
    
    user.role = data.get('role')
    db.session.commit()
    
    return jsonify({
        'message': 'User role updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role
        }
    }), 200

# ==================== Admin Dashboard ====================

@app.route('/api/admin/dashboard', methods=['GET'])
@require_role('admin')
def admin_dashboard():
    """Admin dashboard with statistics"""
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    locked_accounts = User.query.filter(User.locked_until.isnot(None)).count()
    two_fa_enabled = User.query.filter_by(two_fa_enabled=True).count()
    
    # User distribution by role
    admin_count = User.query.filter_by(role='admin').count()
    user_count = User.query.filter_by(role='user').count()
    moderator_count = User.query.filter_by(role='moderator').count()
    
    return jsonify({
        'statistics': {
            'total_users': total_users,
            'active_users': active_users,
            'locked_accounts': locked_accounts,
            'two_fa_enabled': two_fa_enabled,
            'role_distribution': {
                'admin': admin_count,
                'user': user_count,
                'moderator': moderator_count
            }
        }
    }), 200

# ==================== Data Initialization ====================

def initialize_roles():
    """Initialize default roles"""
    from models import Role
    
    roles_data = [
        {
            'name': 'admin',
            'description': 'Administrator with full access',
            'permissions': {
                'users.view': True,
                'users.create': True,
                'users.edit': True,
                'users.delete': True,
                'users.lock': True,
                'reports.view': True
            }
        },
        {
            'name': 'user',
            'description': 'Regular user with basic access',
            'permissions': {
                'profile.view': True,
                'profile.edit': True,
                'notes.view': True,
                'notes.create': True
            }
        },
        {
            'name': 'moderator',
            'description': 'Moderator with user management capabilities',
            'permissions': {
                'users.view': True,
                'users.edit': True,
                'reports.view': True,
                'reports.moderate': True
            }
        }
    ]
    
    for role_data in roles_data:
        if not Role.query.filter_by(name=role_data['name']).first():
            role = Role(**role_data)
            db.session.add(role)
    
    db.session.commit()

# ==================== Application Context ====================

with app.app_context():
    db.create_all()
    initialize_roles()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
