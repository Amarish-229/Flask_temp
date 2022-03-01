from distutils.command.config import config
import os
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from src.database import db
from src.blueprints.authentication import auth
from src.blueprints.filesuplode import handle_files
from src.config.swagger import template, swagger_config
from flasgger import Swagger


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # CORS(app)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            UPLOAD_FOLDER=os.path.join(os.path.dirname(__file__), "../uploads"),

            SWAGGER={
                'title': "Print API",
                'uiversion': 3
            }
        )
    else:
        app.config.from_mapping(test_config)

    JWTManager(app)
    Swagger(app, config=swagger_config, template=template)
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(auth)
    app.register_blueprint(handle_files)

    return app