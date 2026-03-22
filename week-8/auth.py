from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_mail import Mail, Message
from email_validator import validate_email, EmailNotValidError
from functools import wraps
from datetime import datetime, timedelta, timezone
import random
import string
from database import db
from models import User, OTP, LoginAttempt, utc_now, ensure_aware
from config import Config

# Initialize Mail
mail = Mail()

# ==================== Email Validation ====================

def validate_email_format(email):
    """Validate email format using email-validator library"""
    try:
        # Normalize and validate the email
        valid = validate_email(email, check_deliverability=False)
        return True, valid.email
    except EmailNotValidError as e:
        return False, str(e)

# ==================== Password Management ====================

def hash_password(password):
    """Hash password using PBKDF2 with SHA256"""
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

def check_password(password, hashed):
    """Verify password against hash"""
    return check_password_hash(hashed, password)

# ==================== User Management ====================

def create_user(username, email, password, role='user'):
    """Create a new user with hashed password"""
    # Validate email format first
    is_valid, result = validate_email_format(email)
    if not is_valid:
        return None, f"Invalid email format: {result}"
    
    # Use the normalized email
    email = result
    
    if User.query.filter_by(username=username).first():
        return None, "Username already exists"
    
    if User.query.filter_by(email=email).first():
        return None, "Email already exists"
    
    hashed_password = hash_password(password)
    user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        role=role
    )
    db.session.add(user)
    db.session.commit()
    
    return user, "User created successfully"

def get_user_by_username(username):
    """Retrieve user by username"""
    return User.query.filter_by(username=username).first()

def get_user_by_email(email):
    """Retrieve user by email"""
    return User.query.filter_by(email=email).first()

def get_user_by_id(user_id):
    """Retrieve user by ID"""
    return db.session.get(User, user_id)

# ==================== OTP Generation & Verification ====================

def generate_otp(length=6):
    """Generate a random numeric OTP"""
    return ''.join(random.choices(string.digits, k=length))

def create_otp_for_user(user_id, expiry_minutes=5):
    """Create and save OTP for user"""
    OTP.query.filter_by(user_id=user_id, is_verified=False).delete()
    
    otp_code = generate_otp(Config.OTP_LENGTH)
    otp = OTP(
        user_id=user_id,
        otp_code=otp_code,
        expires_at=utc_now() + timedelta(minutes=expiry_minutes)
    )
    db.session.add(otp)
    db.session.commit()
    
    return otp

def send_otp_email(user, otp_code):
    """Send OTP via email"""
    try:
        subject = "Your One-Time Password (OTP) for Two-Factor Authentication"
        body = f"""
Hello {user.username},

Your One-Time Password (OTP) is: {otp_code}

This OTP will expire in 5 minutes.
If you did not request this OTP, please ignore this email.

Do not share your OTP with anyone.

Best regards,
2FA Authentication System
        """
        
        msg = Message(
            subject=subject,
            recipients=[user.email],
            body=body
        )
        
        mail.send(msg)
        return True, "OTP sent successfully"
    except Exception as e:
        return False, f"Failed to send OTP: {str(e)}"

def verify_otp(user_id, otp_code, max_attempts=3):
    """Verify OTP code and mark as verified if correct"""
    otp = OTP.query.filter_by(user_id=user_id, is_verified=False).order_by(OTP.created_at.desc()).first()
    
    if not otp:
        return False, "No OTP request found. Please request a new OTP."
    
    if otp.is_expired():
        return False, "OTP has expired. Please request a new OTP."
    
    otp.attempts += 1
    
    if otp.attempts > max_attempts:
        db.session.commit()
        return False, "Maximum OTP verification attempts exceeded. Please request a new OTP."
    
    if otp.otp_code != otp_code:
        db.session.commit()
        return False, "Invalid OTP. Please try again."
    
    # OTP is valid
    otp.is_verified = True
    user = db.session.get(User, user_id)
    user.two_fa_verified = True
    user.is_email_verified = True
    db.session.commit()
    
    return True, "OTP verified successfully"

def cleanup_expired_otps():
    """Remove expired OTPs from database"""
    OTP.cleanup_expired_otps()

# ==================== Authentication ====================

def authenticate_user(username, password):
    """Authenticate user with username and password"""
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return None, "Invalid username or password"
    
    # Check if account is locked
    if user.is_account_locked():
        locked_until = ensure_aware(user.locked_until)
        remaining_time = (locked_until - utc_now()).total_seconds() / 60
        return None, f"Account locked. Try again in {int(remaining_time)} minutes."
    
    # Check password
    if not check_password(password, user.password_hash):
        user.increment_failed_attempts(
            max_attempts=Config.MAX_LOGIN_ATTEMPTS,
            lockout_duration_minutes=Config.LOCKOUT_DURATION_MINUTES
        )
        db.session.commit()
        
        # Log failed attempt
        log_login_attempt(user.id, success=False, reason="Invalid password")
        
        if user.is_account_locked():
            return None, f"Account locked after {Config.MAX_LOGIN_ATTEMPTS} failed attempts. Try again in {Config.LOCKOUT_DURATION_MINUTES} minutes."
        
        return None, "Invalid username or password"
    
    # Reset failed attempts on successful password verification
    user.reset_failed_attempts()
    db.session.commit()
    
    return user, "Authentication successful"

def log_login_attempt(user_id, success=True, reason=None, ip_address=None):
    """Log login attempt for security auditing"""
    attempt = LoginAttempt(
        user_id=user_id,
        success=success,
        reason=reason,
        ip_address=ip_address
    )
    db.session.add(attempt)
    db.session.commit()

def create_jwt_token(user_id):
    """Create JWT access token"""
    user = db.session.get(User, user_id)
    if not user:
        return None
    
    additional_claims = {
        'username': user.username,
        'email': user.email,
        'role': user.role
    }
    
    access_token = create_access_token(
        identity=str(user_id),  # Convert to string for JWT compatibility
        additional_claims=additional_claims
    )
    
    return access_token

def get_current_user():
    """Get current authenticated user from JWT token"""
    user_id = get_jwt_identity()
    return db.session.get(User, int(user_id))

# ==================== Role-Based Access Control (RBAC) ====================

def require_role(*roles):
    """Decorator to enforce role-based access control"""
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = get_current_user()
            
            if not user:
                return {'message': 'User not found'}, 404
            
            if not user.is_active:
                return {'message': 'User account is inactive'}, 403
            
            if user.role not in roles:
                return {'message': f'Access denied. Required role(s): {", ".join(roles)}'}, 403
            
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator

def require_2fa_verified(fn):
    """Decorator to ensure 2FA is verified before access"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = get_current_user()
        
        if not user:
            return {'message': 'User not found'}, 404
        
        if not user.two_fa_verified:
            return {'message': '2FA verification required. Please verify your OTP.'}, 403
        
        return fn(*args, **kwargs)
    
    return wrapper

def require_2fa_and_role(*roles):
    """Decorator to enforce both 2FA verification and role-based access"""
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = get_current_user()
            
            if not user:
                return {'message': 'User not found'}, 404
            
            if not user.is_active:
                return {'message': 'User account is inactive'}, 403
            
            if not user.two_fa_verified:
                return {'message': '2FA verification required'}, 403
            
            if user.role not in roles:
                return {'message': f'Access denied. Required role(s): {", ".join(roles)}'}, 403
            
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator

# ==================== Utility Functions ====================

def update_last_login(user_id):
    """Update user's last login timestamp"""
    user = db.session.get(User, user_id)
    if user:
        user.last_login = utc_now()
        db.session.commit()

def verify_user_email(user_id):
    """Mark user email as verified"""
    user = db.session.get(User, user_id)
    if user:
        user.is_email_verified = True
        db.session.commit()
        return True
    return False
