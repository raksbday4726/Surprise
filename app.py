import os
from flask import Flask, send_from_directory
from flask_cors import CORS
# Legacy imports kept for compatibility with the existing app.py implementation.
from config import Config
from extensions import db, migrate


# NOTE: legacy create_app kept below for compatibility; Phase 1 refactor introduces app/__init__.py
# but we preserve this implementation to avoid any risk of behavior change.
def create_app(config_class=Config):

    # Initialize Flask app, setting static_folder to root ('.') to serve files in-place
    app = Flask(__name__, static_folder='.', static_url_path='')
    app.config.from_object(config_class)

    # Initialize extensions (CORS, DB, and Migrations)
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Automatically create database tables if they do not exist
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            # Don't crash the app on DB init issues; API routes will return JSON errors.
            pass


    # Register modular Blueprints
    from routes.wishes import wishes_bp
    from api.health import health_bp

    app.register_blueprint(wishes_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')



    # Serve index.html at the root URL
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    # Catch-all route to serve story.html, wish.html, and other static assets
    @app.route('/<path:path>')
    def serve_frontend(path):
        # Prevent accessing python/env files via static route
        ignored_extensions = {'.py', '.pyc', '.env', '.example', '.git', '.gitignore', '.txt'}
        _, ext = os.path.splitext(path)
        if ext in ignored_extensions or path == 'config':
            return "Access Denied", 403

        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return "Not Found", 404

    return app

# Compatibility entrypoint (keep behavior aligned with the refactored app factory)
if __name__ == '__main__':
    # Prefer the package app factory so /api/* blueprints are registered consistently.
    from run import app as flask_app
    flask_app.run(host='127.0.0.1', port=5000, debug=True)



