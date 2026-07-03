from flask import Flask, send_from_directory
from flask_cors import CORS
import os



from app.extensions import db, migrate
from app.logging_config import configure_logging



def create_app(config_class=None):

    """Flask application factory (keeps external behavior identical)."""
    app = Flask(
        __name__,
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
        static_url_path=''
    )
    configure_logging()
    if config_class is None:
        # Use config factory (selects DevelopmentConfig/ProductionConfig/TestingConfig)
        from app.config_factory import get_config_from_env
        config_class = get_config_from_env()

    app.config.from_object(config_class)

    # Ensure FLASK_ENV controls debug (no auto debug in prod)
    app.debug = bool(getattr(config_class, 'DEBUG', False))


    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Auto-create tables if they don't exist (safe – create_all is a no-op for
    # tables that are already present in the database).
    # Models must be imported so SQLAlchemy's metadata knows about them.
    import app.models.wishes  # noqa: F401
    import app.models.uploads  # noqa: F401

    with app.app_context():
        try:
            db.create_all()
        except Exception:
            # Don't crash on DB init issues; API routes will return JSON errors.
            pass


    from app.routes.wishes import wishes_bp
    from app.routes.health import health_bp

    app.register_blueprint(wishes_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_frontend(path):
        ignored_extensions = {'.py', '.pyc', '.env', '.example', '.git', '.gitignore', '.txt'}
        _, ext = os.path.splitext(path)
        if ext in ignored_extensions or path == 'config':
            return "Access Denied", 403

        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return "Not Found", 404

    return app

