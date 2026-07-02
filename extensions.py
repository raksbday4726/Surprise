from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instantiate SQLAlchemy database and Flask-Migrate globally
db = SQLAlchemy()
migrate = Migrate()
