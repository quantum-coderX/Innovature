import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_required_env(key, description=""):
    """Get required environment variable, raise error if missing"""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Missing required environment variable: {key}. {description}")
    return value

def get_optional_env(key, default=""):
    """Get optional environment variable with default"""
    return os.getenv(key, default)

class Config:
    """Base configuration - requires environment variables"""
    
    # Database - REQUIRED
    SQLALCHEMY_DATABASE_URI = get_required_env(
        'DATABASE_URL',
        'Set DATABASE_URL in .env file'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT - REQUIRED (must be kept secret)
    JWT_SECRET_KEY = get_required_env(
        'JWT_SECRET_KEY',
        'Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"'
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Email Configuration - Optional for testing, required for production
    MAIL_SERVER = get_optional_env('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(get_optional_env('MAIL_PORT', '587'))
    MAIL_USE_TLS = get_optional_env('MAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
    MAIL_USERNAME = get_optional_env('MAIL_USERNAME', 'test@example.com')
    MAIL_PASSWORD = get_optional_env('MAIL_PASSWORD', 'test-password')
    MAIL_DEFAULT_SENDER = get_optional_env('MAIL_DEFAULT_SENDER', 'noreply@test.local')
    
    # OTP Settings
    OTP_EXPIRY_MINUTES = int(os.getenv('OTP_EXPIRY_MINUTES', 5))
    OTP_LENGTH = int(os.getenv('OTP_LENGTH', 6))
    
    # Account Lockout Settings
    MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', 5))
    LOCKOUT_DURATION_MINUTES = int(os.getenv('LOCKOUT_DURATION_MINUTES', 30))
    
    # 2FA Settings
    TWO_FA_REQUIRED = os.getenv('TWO_FA_REQUIRED', 'True').lower() in ('true', '1', 'yes')
    ENABLE_EMAIL_OTP = os.getenv('ENABLE_EMAIL_OTP', 'True').lower() in ('true', '1', 'yes')
    ENABLE_TOTP = os.getenv('ENABLE_TOTP', 'False').lower() in ('true', '1', 'yes')

    # Admin bootstrap settings
    ENABLE_ADMIN_BOOTSTRAP = os.getenv('ENABLE_ADMIN_BOOTSTRAP', 'False').lower() in ('true', '1', 'yes')
    ADMIN_BOOTSTRAP_KEY = get_optional_env('ADMIN_BOOTSTRAP_KEY', '')
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    ENABLE_ADMIN_BOOTSTRAP = True
    ADMIN_BOOTSTRAP_KEY = 'test-bootstrap-key'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
