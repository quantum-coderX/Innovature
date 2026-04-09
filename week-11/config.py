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
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "week10-change-this-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    # ────────────────────────────────────────────────────────────
    # Image / Upload Settings  (Week 10)
    # ────────────────────────────────────────────────────────────
    # Root folder where uploaded images are stored on disk.
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "static/uploads/products")
    # Root folder where auto-generated thumbnails are stored.
    THUMBNAIL_FOLDER = os.getenv("THUMBNAIL_FOLDER", "static/uploads/thumbnails")
    # Allowed MIME types (checked against actual file content, not extension).
    ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
    # Allowed file extensions (secondary guard).
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
    # Maximum file size per upload in bytes (5 MB).
    MAX_IMAGE_SIZE_BYTES = int(os.getenv("MAX_IMAGE_SIZE_BYTES", 5 * 1024 * 1024))
    # Maximum number of images stored per product.
    MAX_IMAGES_PER_PRODUCT = int(os.getenv("MAX_IMAGES_PER_PRODUCT", 5))
    # Thumbnail dimensions (width, height) in pixels.
    THUMBNAIL_SIZE = (300, 300)


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
