import os
import urllib.parse

from dotenv import load_dotenv

load_dotenv()


def _get_env(name: str, default: str | None = None) -> str | None:
    val = os.environ.get(name)
    if val is None or val == "":
        return default
    return val


def _require_env(name: str) -> str:
    value = _get_env(name)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


class BaseConfig:
    # Debug controlled by environment; keep safe defaults.
    DEBUG = False

    # SECRET_KEY
    # - In development: allow fallback for local use.
    # - In production: require it via Render env vars.
    SECRET_KEY = _get_env('SECRET_KEY', 'dev_secret_key_12345')

    # MySQL Database configuration
    # - In development: require via env once actually starting DB-backed endpoints.
    # - In production: require these values.
    DB_USER = _get_env('MYSQL_USER', 'root')
    DB_PASSWORD = _get_env('MYSQL_PASSWORD', '')
    DB_HOST = _get_env('MYSQL_HOST', 'localhost')
    DB_PORT = _get_env('MYSQL_PORT', '3306')
    DB_NAME = _get_env('MYSQL_DATABASE', 'birthday_universe')

    @classmethod
    def validate_or_raise(cls) -> None:
        if cls is ProductionConfig:
            _require_env('SECRET_KEY')
            _require_env('MYSQL_USER')
            _require_env('MYSQL_PASSWORD')
            _require_env('MYSQL_HOST')
            _require_env('MYSQL_PORT')
            _require_env('MYSQL_DATABASE')

        if not cls.DB_NAME:
            raise RuntimeError('Missing MYSQL_DATABASE')



# Build DB URI after class creation using the configured values.
# (Still compatible with SQLAlchemy.)

# Escape the password to handle special characters in the connection string
escaped_password = urllib.parse.quote_plus(BaseConfig.DB_PASSWORD) if BaseConfig.DB_PASSWORD else ''

BaseConfig.SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{BaseConfig.DB_USER}:{escaped_password}@{BaseConfig.DB_HOST}:{BaseConfig.DB_PORT}/{BaseConfig.DB_NAME}"
)
BaseConfig.SQLALCHEMY_TRACK_MODIFICATIONS = False




BaseConfig.SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'max_overflow': 20,
    'pool_recycle': 280,
    'pool_pre_ping': True
}

BaseConfig.UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
BaseConfig.MAX_CONTENT_LENGTH = int(
    os.environ.get('MAX_CONTENT_LENGTH', str(5 * 1024 * 1024))
)
BaseConfig.ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

BaseConfig.JSON_SORT_KEYS = False



class DevelopmentConfig(BaseConfig):
    # Debug controlled by environment
    DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'


class TestingConfig(BaseConfig):
    DEBUG = False


class ProductionConfig(BaseConfig):
    DEBUG = False


def get_config_class():
    env = os.environ.get('FLASK_ENV', 'development').lower()
    if env == 'production':
        return ProductionConfig
    if env == 'testing':
        return TestingConfig
    return DevelopmentConfig


