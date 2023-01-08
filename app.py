import os
from dotenv import load_dotenv
from flask import Flask
from extensions import database, commands
from blueprints.main.views import main
from blueprints.fraud.views import fraud
# from blueprints.seeder.views import seeder


# blueprint import


def create_app():
    load_dotenv()

    app = Flask(__name__)
    # setup with the configuration provided by the user / environment
    app.config.from_object(os.getenv('APP_SETTINGS'))

    # setup all our dependencies
    database.init_app(app)
    commands.init_app(app)

    # register blueprint
    app.register_blueprint(main)
    app.register_blueprint(fraud, url_prefix='/fraud')
    # app.register_blueprint(seeder)

    # with app.app_context():
    #     commands.create_db()

    return app


if __name__ == "__main__":
    create_app().run()
