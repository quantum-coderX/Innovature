from database import db
from datetime import datetime, timedelta, timezone
import os

def utc_now():
    """Get current UTC time as timezone-aware datetime"""
    return datetime.now(timezone.utc)

def ensure_aware(dt):
    """Convert naive datetime to aware UTC datetime"""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt

class User(db.Model):
    """User model with role-based access control"""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Role-based access control
    role = db.Column(db.String(20), nullable=False, default='user')  # admin, user, moderator
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_email_verified = db.Column(db.Boolean, nullable=False, default=False)
    
    # 2FA settings
    two_fa_enabled = db.Column(db.Boolean, nullable=False, default=True)
    two_fa_verified = db.Column(db.Boolean, nullable=False, default=False)
    
    # Account lockout
    failed_login_attempts = db.Column(db.Integer, nullable=False, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)  # Timestamp when account is unlocked
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    otps = db.relationship('OTP', backref='user', lazy=True, cascade='all, delete-orphan')
    login_attempts = db.relationship('LoginAttempt', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def is_account_locked(self):
        """Check if account is currently locked"""
        if self.locked_until:
            locked_until = ensure_aware(self.locked_until)
            if utc_now() < locked_until:
                return True
        return False
    
    def reset_failed_attempts(self):
        """Reset failed login attempts and unlock account"""
        self.failed_login_attempts = 0
        self.locked_until = None
    
    def increment_failed_attempts(self, max_attempts=5, lockout_duration_minutes=30):
        """Increment failed login attempts and lock account if exceeded"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= max_attempts:
            self.locked_until = utc_now() + timedelta(minutes=lockout_duration_minutes)


class OTP(db.Model):
    """One-Time Password model for 2FA"""
    __tablename__ = 'otp'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    otp_code = db.Column(db.String(10), nullable=False)  # 6-digit OTP
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime, nullable=False)  # OTP expiry time
    attempts = db.Column(db.Integer, nullable=False, default=0)  # Track verification attempts
    
    def __repr__(self):
        return f'<OTP {self.user_id}>'
    
    def is_expired(self):
        """Check if OTP has expired"""
        expires_at = ensure_aware(self.expires_at)
        return utc_now() > expires_at
    
    def is_valid(self):
        """Check if OTP is valid (not expired and not verified)"""
        return not self.is_expired() and not self.is_verified
    
    @classmethod
    def cleanup_expired_otps(cls):
        """Delete all expired OTPs from database"""
        cls.query.filter(cls.expires_at < utc_now()).delete()
        db.session.commit()


class LoginAttempt(db.Model):
    """Track login attempts for security logging"""
    __tablename__ = 'login_attempt'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 or IPv6
    success = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    reason = db.Column(db.String(255), nullable=True)  # Failure reason
    
    def __repr__(self):
        return f'<LoginAttempt {self.user_id} - {self.success}>'


class Role(db.Model):
    """Role model for RBAC"""
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # admin, user, moderator
    description = db.Column(db.String(255), nullable=True)
    permissions = db.Column(db.JSON, nullable=False, default={})  # JSON object with permissions
    
    def __repr__(self):
        return f'<Role {self.name}>'
