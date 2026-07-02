import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key_12345')
    
    # MySQL Database configuration
    DB_USER = os.environ.get('MYSQL_USER', 'root')
    DB_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    DB_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    DB_PORT = os.environ.get('MYSQL_PORT', '3306')
    DB_NAME = os.environ.get('MYSQL_DATABASE', 'birthday_universe')
    
    # Escape the password to handle special characters in the connection string
    escaped_password = urllib.parse.quote_plus(DB_PASSWORD) if DB_PASSWORD else ''
    
    # Connection string for SQLAlchemy using PyMySQL driver
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{escaped_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database connection pool settings (for performance and auto-reconnects)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_recycle': 280,
        'pool_pre_ping': True
    }
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.environ.get('UPLOAD_FOLDER', 'uploads'))
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
