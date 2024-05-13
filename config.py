import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///myapp.db')  # Fallback to SQLite if no env var
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads/'  # Folder where uploaded files will be stored
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload limit to prevent large uploads

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Outputs the SQL that SQLAlchemy generates to the console, helpful for debugging

class ProductionConfig(Config):
    DEBUG = False
    # Ensure the production database URI is configured through environment variables only
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'  # Use an in-memory database for tests
    WTF_CSRF_ENABLED = False  # Disable CSRF tokens in the form for easier testing
