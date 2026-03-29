import os
from datetime import timedelta

class Config:
    """Application configuration"""
    
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://ecommerce_user:ecommerce_password@localhost:5432/ecommerce_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Log SQL queries
    
    # JSON
    JSON_SORT_KEYS = False
    
    # Pagination
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 10
    MAX_PER_PAGE = 100
    
    # Query parameters
    PRODUCT_SEARCH_MIN_LENGTH = 2
    PRICE_FILTER_PRECISION = 2

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "week9-change-this-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


# Export the config
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
