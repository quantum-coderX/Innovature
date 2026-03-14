import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-dev-key')

    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError('DATABASE_URL environment variable is not set')
    if SECRET_KEY == 'dev-secret-key' or JWT_SECRET_KEY == 'jwt-dev-key':
        import warnings
        warnings.warn('Using default secret keys — set SECRET_KEY and JWT_SECRET_KEY env vars in production', stacklevel=2)