from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='h7V4kCJ9ySec4tOQjoik2A',
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, 'water_quality.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY='dfc77058462ab931095114bb89816729'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    from webapp import models, routes
    app.register_blueprint(routes.bp)

    @app.cli.command('init-db')
    def init_db_command():
        db.create_all()
        print('Initialised the database.')

    return app
