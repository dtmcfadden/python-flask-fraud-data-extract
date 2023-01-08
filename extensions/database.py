from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder

db = SQLAlchemy(session_options={'autocommit': True})
seeder = FlaskSeeder()


def init_app(app):
    db.init_app(app)
    seeder.init_app(app, db)
    migrate = Migrate(app, db)
